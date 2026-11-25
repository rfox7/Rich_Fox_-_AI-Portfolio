"""LLM path, tested without a real API key by swapping in fake replies."""
from types import SimpleNamespace

from src.agent import llm, reasoning


def test_llm_reply_is_used(monkeypatch):
    monkeypatch.setattr(llm, "chat", lambda *a, **k: '{"intent":"load","file_pattern":"sales_*.csv","dry_run":true}')
    task = reasoning.parse_request("Have a look at the sales numbers that came in but hold off on loading")
    assert task.intent == "load" and task.dry_run is True and task.notes.startswith("parsed by")


def test_bad_llm_reply_falls_back_to_rules(monkeypatch):
    monkeypatch.setattr(llm, "chat", lambda *a, **k: "Sure! I think you want to load files.")
    task = reasoning.parse_request("Just check the sales files, don't load them")
    assert task.dry_run is True and task.notes == "parsed by rules"


def test_unsafe_file_pattern_from_llm_is_ignored(monkeypatch):
    monkeypatch.setattr(llm, "chat", lambda *a, **k: '{"intent":"load","file_pattern":"../../*.csv"}')
    assert reasoning.parse_request("load the sales files").file_pattern == "*.csv"


def test_claude_reply_parsing(monkeypatch):
    """chat() pulls the JSON out of a Claude reply even with extra words around it."""
    class FakeMessages:
        def create(self, **kwargs):
            assert kwargs["model"] and kwargs["system"].endswith("no other text.")
            return SimpleNamespace(content=[SimpleNamespace(text='Here you go:\n```json\n{"intent":"status"}\n```')])
    monkeypatch.setattr(llm, "_client", lambda: ("anthropic", SimpleNamespace(messages=FakeMessages())))
    assert llm.chat("system", "user", json_mode=True) == '{"intent":"status"}'
