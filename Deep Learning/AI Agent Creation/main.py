"""Command-line entry point.

    py main.py "Load this week's sales files and tell me what happened"
    py main.py "Just check the sales files, don't load them"
    py main.py "Show me the status of the last runs"
    py main.py                      (interactive mode, with thumbs up/down feedback)
"""
import logging
import sys

from src.agent import PipelineAgent


def interactive(agent: PipelineAgent) -> None:
    print("PipelinePilot - type a request, or 'quit'.")
    while True:
        try:
            text = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text.lower() in ("quit", "exit", "q"):
            break
        report = agent.run(text)
        print("\n" + report.message)
        if report.run_id:
            fb = input("Was this run good? [y/n/skip] ").strip().lower()
            if fb in ("y", "n"):
                print(agent.give_feedback(report.run_id, fb == "y"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    agent = PipelineAgent()
    if len(sys.argv) > 1:
        result = agent.run(" ".join(sys.argv[1:]))
        print("\n" + result.message)
    else:
        interactive(agent)
