"""Checks the LLM connection:  py check_llm.py"""
import logging

from src import config
from src.agent import llm

logging.basicConfig(level=logging.ERROR)


def mask(key: str) -> str:
    return f"{key[:10]}...{key[-4:]} ({len(key)} chars)" if key else "(not set)"


print(f"LLM_PROVIDER setting : {config.LLM_PROVIDER or '(blank = auto)'}")
print(f"ANTHROPIC_API_KEY    : {mask(config.ANTHROPIC_API_KEY)}")
print(f"OPENAI_API_KEY       : {mask(config.OPENAI_API_KEY)}")
print(f"Provider chosen      : {llm._provider() or 'none (no key found in .env)'}")
provider, client = llm._client()
if client is None:
    print(f"Result               : no LLM client. {llm.last_error or 'Check the key and LLM_PROVIDER in .env.'}")
else:
    print(f"Model                : {llm.model_name()}")
    reply = llm.chat("You are a connection test.", "Reply with the single word OK.", max_tokens=10)
    print(f"Result               : {'connected, reply = ' + repr(reply) if reply else 'call failed -> ' + llm.last_error}")

if client is not None:
    # Same call the agent makes when it reads a request (see src/agent/reasoning.py)
    from src.agent import reasoning
    sample = "Hey, can you take a look at the sales stuff that came in, but don't actually put it in the warehouse yet"
    llm.last_error = ""
    task = reasoning.parse_request(sample)
    print(f"Agent's reading      : intent={task.intent}, dry_run={task.dry_run}, {task.notes}")
    llm.last_error = ""
    note = llm.chat("You review a data pipeline run. In 2-3 plain sentences, say what went wrong, what worked, "
                    "and what to try next time.", '{"status":"checked","rows_rejected":23}', max_tokens=150)
    print(f"Reflection call      : {'ok, ' + repr(note[:80]) + '...' if note else 'failed -> ' + (llm.last_error or 'empty reply')}")
