"""Screens the user's request before the agent does anything.

Three outcomes:
* allowed    - a pipeline request the agent can handle
* blocked    - harmful or destructive (drop tables, wipe data, show passwords,
               prompt-injection attempts)
* out_of_scope - harmless but not something this agent does (it explains its
               limits instead of guessing)
"""
from __future__ import annotations

import re
from dataclasses import dataclass

MAX_REQUEST_CHARS = 1000

BLOCKED_PATTERNS = [
    (r"\b(drop|truncate|wipe|destroy|erase)\b", "destructive data operation"),
    (r"\bdelete\s+(all|everything|the\s+\w+\s+table|from\s+dw)\b", "destructive data operation"),
    (r"\b(password|credential|connection\s+string|api\s*key|secret)s?\b", "request for credentials"),
    (r"\b(ignore|disregard|forget)\b.{0,30}\b(instructions|rules|guardrails|safety)\b", "prompt injection attempt"),
    (r"\b(grant|revoke)\b.{0,20}\b(access|permission|admin)\b", "permission change"),
    (r"\b(shell|cmd|powershell|os\.system|subprocess)\b", "request to run system commands"),
]

IN_SCOPE_WORDS = re.compile(
    r"\b(load|import|ingest|process|run|check|validate|stage|merge|pipeline|files?|csv|sales|"
    r"data|status|report|summary|summarize|rejects?|last\s+run|history|what\s+happened)\b",
    re.IGNORECASE,
)

CAPABILITIES = (
    "I can load sales CSV files from the incoming folder into the warehouse, check and clean "
    "the data, and report what happened. I can also show the status of past runs. I can't "
    "delete or drop tables, change permissions, share credentials, or work outside the "
    "incoming data folder."
)


@dataclass
class ScreenResult:
    allowed: bool
    category: str  # allowed | blocked | out_of_scope
    reason: str


def screen_request(text: str) -> ScreenResult:
    if not text or not text.strip():
        return ScreenResult(False, "out_of_scope", "The request is empty. " + CAPABILITIES)
    if len(text) > MAX_REQUEST_CHARS:
        return ScreenResult(False, "blocked", f"Request is longer than {MAX_REQUEST_CHARS} characters.")

    for pattern, label in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return ScreenResult(False, "blocked", f"Refused: {label}. {CAPABILITIES}")

    if not IN_SCOPE_WORDS.search(text):
        return ScreenResult(False, "out_of_scope", "That's outside what I do. " + CAPABILITIES)

    return ScreenResult(True, "allowed", "OK")
