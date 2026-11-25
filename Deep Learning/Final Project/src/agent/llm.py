"""Optional LLM client (OpenAI or Azure OpenAI).

`chat()` returns None when no key is set or the call fails. Every caller has
a rule-based fallback, so the agent works fully offline; the LLM just makes
request parsing and reflection notes smarter.
"""
from __future__ import annotations

import logging
from functools import lru_cache

from src import config

log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _client():
    try:
        if config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_API_KEY:
            from openai import AzureOpenAI
            return AzureOpenAI(azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
                               api_key=config.AZURE_OPENAI_API_KEY,
                               api_version=config.AZURE_OPENAI_API_VERSION)
        if config.OPENAI_API_KEY:
            from openai import OpenAI
            return OpenAI(api_key=config.OPENAI_API_KEY)
    except ImportError:
        log.info("openai package not installed; running without an LLM")
    return None


def available() -> bool:
    return _client() is not None


def chat(system: str, user: str, max_tokens: int = 400, json_mode: bool = False) -> str | None:
    client = _client()
    if client is None:
        return None
    try:
        kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
        resp = client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=max_tokens,
            temperature=0,
            **kwargs,
        )
        return resp.choices[0].message.content
    except Exception as exc:  # noqa: BLE001 - LLM trouble must never stop the pipeline
        log.warning("LLM call failed, using fallback: %s", exc)
        return None
