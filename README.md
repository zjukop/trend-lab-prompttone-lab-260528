# PromptTone Lab

Minimal starter for **PromptTone Lab — Benchmark & Auto-Repair Prompt Framing**.

## What this does
- Runs a tiny tone benchmark (`authoritarian`, `neutral`, `empathetic`, `coaching`)
- Scores outputs with simple heuristics (completion, refusal, verbosity, contradiction)
- Supports a `patch` mode to soften harsh prompts

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
prompttone-lab run --task "Explain recursion in 2 sentences"
prompttone-lab patch --prompt "Do this now and don't fail"
```

## Test
```bash
pytest -q
```
