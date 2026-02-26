---
name: token-cost
description: >-
  Analyze Claude Code session token usage and estimate costs.
  Use when the user asks: "how many tokens", "token cost", "cuántos tokens",
  "cuánto costó", "token usage", "session cost", "coste de la sesión",
  "tokens gastados", "tokens del proyecto", "total tokens", "/token-cost",
  or wants to know the token consumption or estimated USD cost of the current,
  a previous, or all sessions in the project.
---

# Token Cost Analyzer

Run the bundled script to show token usage and estimated cost for a session.

```bash
python3 <skill-dir>/scripts/token_cost.py [--session current|last|all|SESSION_ID] [--project PROJECT_PATH] [--detail]
```

- `--session current` (default): most recent session
- `--session last`: previous session (skipping current)
- `--session all`: aggregate all sessions in the project (with per-session breakdown table)
- `--session <UUID>`: specific session by ID
- `--project`: override project path (defaults to cwd)
- `--detail` / `-d`: show all user prompts per session (filters system noise)

## What it reports

- Per-model token breakdown (input, output, cache read, cache write)
- Total tokens and assistant turn count
- Session duration
- Estimated cost in USD (fetched live from `https://models.dev/api.json`)

## When invoked

1. Determine which session the user wants (`current`, `last`, or specific)
2. Run the script with appropriate flags
3. Present the output directly
