from __future__ import annotations

import argparse
import json
import re
from time import perf_counter

TONES = {
    "authoritarian": "You must follow the instruction exactly.",
    "neutral": "Please complete the instruction clearly.",
    "empathetic": "Please help kindly and clearly; be supportive.",
    "coaching": "Guide step-by-step and encourage learning.",
}


def simulate_model(task: str, tone: str) -> str:
    # Deterministic local simulation for a runnable starter.
    prefix = {
        "authoritarian": "Answer:",
        "neutral": "Result:",
        "empathetic": "Happy to help:",
        "coaching": "Let's do it step by step:",
    }[tone]
    return f"{prefix} {task.strip()}"


def score_output(text: str) -> dict[str, float | int]:
    lower = text.lower()
    refusal = int(any(k in lower for k in ["cannot", "won't", "refuse"]))
    words = len(re.findall(r"\w+", text))
    completion = 1 if words >= 3 else 0
    contradiction = int("but" in lower and "however" in lower)
    return {
        "completion": completion,
        "refusal": refusal,
        "verbosity": words,
        "self_contradiction": contradiction,
    }


def run_benchmark(task: str) -> list[dict]:
    rows = []
    for tone in TONES:
        t0 = perf_counter()
        output = simulate_model(task, tone)
        latency_ms = int((perf_counter() - t0) * 1000)
        row = {"tone": tone, "output": output, "latency_ms": latency_ms, **score_output(output)}
        rows.append(row)
    return rows


def patch_prompt(prompt: str) -> str:
    softened = re.sub(r"\b(now|immediately|must|don't fail)\b", "", prompt, flags=re.IGNORECASE)
    softened = re.sub(r"\s+", " ", softened).strip(" .")
    return f"Please help with this kindly: {softened}."


def cli() -> None:
    parser = argparse.ArgumentParser(prog="prompttone-lab")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="run a tone benchmark")
    run_p.add_argument("--task", required=True)

    patch_p = sub.add_parser("patch", help="rewrite harsh prompt")
    patch_p.add_argument("--prompt", required=True)

    args = parser.parse_args()

    if args.cmd == "run":
        print(json.dumps(run_benchmark(args.task), indent=2))
    elif args.cmd == "patch":
        print(patch_prompt(args.prompt))


if __name__ == "__main__":
    cli()
