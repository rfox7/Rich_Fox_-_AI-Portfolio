"""SQL allow-list: every statement the agent sends is checked here first.

This is the first line of defense. The second is the database itself:
agent_user has no permission to DROP, ALTER or DELETE outside staging, so
even a statement that slipped past this check would be refused by Azure SQL.

Rules
-----
1. One statement per call, no comments (comments can hide extra SQL).
2. Allowed verbs: SELECT, WITH (read-only), INSERT, UPDATE, DELETE, MERGE.
3. Blocked keywords anywhere: DROP, TRUNCATE, ALTER, GRANT, EXEC, etc.
4. Writes only go to the staging, dw or agent schemas.
5. DELETE only in staging.
6. UPDATE outside staging needs a WHERE clause.
7. MERGE into dw can't include a DELETE branch.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

WRITE_SCHEMAS = {"staging", "dw", "agent"}

BLOCKED = re.compile(
    r"\b(DROP|TRUNCATE|ALTER|GRANT|REVOKE|DENY|EXEC|EXECUTE|SHUTDOWN|BACKUP|RESTORE|"
    r"RECONFIGURE|OPENROWSET|OPENQUERY|BULK|ATTACH|DETACH|PRAGMA|xp_\w+|sp_\w+|"
    r"CREATE\s+(LOGIN|USER|DATABASE|ROLE|PROCEDURE|FUNCTION|TRIGGER))\b",
    re.IGNORECASE,
)
ALLOWED_VERBS = {"SELECT", "WITH", "INSERT", "UPDATE", "DELETE", "MERGE"}
WRITE_VERBS = {"INSERT", "UPDATE", "DELETE", "MERGE"}


class SafetyViolation(Exception):
    """Raised when the agent tries something outside its boundaries."""


@dataclass
class GuardResult:
    allowed: bool
    reason: str
    verb: str = ""
    target: str = ""


def _strip_literals(sql: str) -> str:
    """Blank out quoted text so a value like 'DROP ME' doesn't trigger a block."""
    return re.sub(r"'(?:[^']|'')*'", "''", sql)


def _target_of(verb: str, sql: str) -> str:
    patterns = {
        "INSERT": r"^\s*INSERT\s+(?:INTO\s+)?([\w\.\[\]\"]+)",
        "UPDATE": r"^\s*UPDATE\s+([\w\.\[\]\"]+)",
        "DELETE": r"^\s*DELETE\s+(?:FROM\s+)?([\w\.\[\]\"]+)",
        "MERGE": r"^\s*MERGE\s+(?:INTO\s+)?([\w\.\[\]\"]+)",
    }
    m = re.search(patterns[verb], sql, re.IGNORECASE)
    return re.sub(r"[\[\]\"]", "", m.group(1)).lower() if m else ""


def check_sql(sql: str) -> GuardResult:
    if not sql or not sql.strip():
        return GuardResult(False, "Empty SQL statement")

    clean = _strip_literals(sql).strip()

    if "--" in clean or "/*" in clean:
        return GuardResult(False, "Comments are not allowed in agent SQL")
    if ";" in clean.rstrip(";"):
        return GuardResult(False, "Only one statement per call is allowed")

    blocked = BLOCKED.search(clean)
    if blocked:
        return GuardResult(False, f"Blocked keyword: {blocked.group(0).upper()}")

    verb = clean.split(None, 1)[0].upper()
    if verb not in ALLOWED_VERBS:
        return GuardResult(False, f"Statement type '{verb}' is not on the allow-list", verb)

    if verb in ("SELECT", "WITH"):
        if verb == "WITH" and re.search(r"\b(INSERT|UPDATE|DELETE|MERGE)\b", clean, re.IGNORECASE):
            return GuardResult(False, "Write statements can't start with a CTE", verb)
        return GuardResult(True, "Read-only query", verb)

    target = _target_of(verb, clean)
    schema = target.split(".", 1)[0] if "." in target else ""
    if schema not in WRITE_SCHEMAS:
        return GuardResult(False, f"Writes must target staging, dw or agent (got '{target or '?'}')", verb, target)

    if verb == "DELETE" and schema != "staging":
        return GuardResult(False, "DELETE is only allowed in the staging schema", verb, target)

    if verb == "UPDATE" and schema != "staging" and not re.search(r"\bWHERE\b", clean, re.IGNORECASE):
        return GuardResult(False, "UPDATE outside staging needs a WHERE clause", verb, target)

    if verb == "MERGE" and schema == "dw" and re.search(r"\bTHEN\s+DELETE\b", clean, re.IGNORECASE):
        return GuardResult(False, "MERGE into dw can't delete rows", verb, target)

    return GuardResult(True, f"{verb} on {target} allowed", verb, target)


def enforce(sql: str) -> GuardResult:
    """Like check_sql, but raises SafetyViolation when the statement is refused."""
    result = check_sql(sql)
    if not result.allowed:
        raise SafetyViolation(result.reason)
    return result
