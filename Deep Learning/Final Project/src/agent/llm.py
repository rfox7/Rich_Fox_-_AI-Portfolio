"""Optional LLM client: Claude (Anthropic), OpenAI, or Azure OpenAI.

`chat()` returns None when no key is set or the call fails. Every caller has
a rule-based fallback, so the agent works fully offline; the LLM makes
request parsing and reflection notes smarter.

Which provider is used:
* LLM_PROVIDER in .env ("anthropic", "openai" or "azure"), or if that's blank,
* the first key found: ANTHROPIC_API_KEY, then Azure OpenAI, then OPENAI_API_KEY.
"""
from __future__ import annotations

import logging
import re
from functools import lru_cache

from src import config

log = logging.getLogger(__name__)
last_error: str = ""  # the most recent LLM problem, shown by the check below


def _provider() -> str | None:
    wanted = config.LLM_PROVIDER
    if wanted in ("anthropic", "openai", "azure"):
        return wanted
    if config.ANTHROPIC_API_KEY:
        return "anthropic"
    if config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_API_KEY:
        return "azure"
    if config.OPENAI_API_KEY:
        return "openai"
    return None


@lru_cache(maxsize=1)
def _client():
    provider = _provider()
    try:
        if provider == "anthropic" and config.ANTHROPIC_API_KEY:
            from anthropic import Anthropic
            return provider, Anthropic(api_key=config.ANTHROPIC_API_KEY)
        if provider == "azure" and config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_API_KEY:
            from openai import AzureOpenAI
            return provider, AzureOpenAI(azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
                                         api_key=config.AZURE_OPENAI_API_KEY,
                                         api_version=config.AZURE_OPENAI_API_VERSION)
        if provider == "openai" and config.OPENAI_API_KEY:
            from openai import OpenAI
            return provider, OpenAI(api_key=config.OPENAI_API_KEY)
    except ImportError as exc:
        global last_error
        last_error = f"package not installed: {exc} (run: py -m pip install -r requirements.txt)"
        log.info("LLM package not installed (%s); running without an LLM", exc)
    return None, None


def available() -> bool:
    return _client()[1] is not None


def model_name() -> str:
    provider, _ = _client()
    return config.ANTHROPIC_MODEL if provider == "anthropic" else config.LLM_MODEL


def name() -> str:
    """Short label for the reasoning trace, e.g. 'LLM (claude-haiku-5-5)'."""
    return f"LLM ({model_name()})" if available() else "rules"


def chat(system: str, user: str, max_tokens: int = 400, json_mode: bool = False) -> str | None:
    global last_error
    provider, client = _client()
    if client is None:
        return None
    try:
        if provider == "anthropic":
            if json_mode:
                system += " Reply with one JSON object only, no other text."
            # No temperature here: newer Anthropic SDKs and models don't accept it.
            resp = client.messages.create(
                model=config.ANTHROPIC_MODEL,
                max_tokens=max(max_tokens, 1024),  # room to think before answering; short replies cost the same
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", "text") == "text")
            if not text.strip():
                last_error = f"empty reply (stop_reason={getattr(resp, 'stop_reason', '?')})"
                return None
        else:
            kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
            resp = client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                max_tokens=max_tokens,
                temperature=0,
                **kwargs,
            )
            text = resp.choices[0].message.content or ""
        if json_mode:
            match = re.search(r"\{.*\}", text, re.DOTALL)  # tolerate ```json fences or extra words
            text = match.group(0) if match else text
        return text.strip() or None
    except Exception as exc:  # noqa: BLE001 - LLM trouble must never stop the pipeline
        last_error = f"{type(exc).__name__}: {exc}"
        log.warning("LLM call failed, using fallback: %s", exc)
        return None

