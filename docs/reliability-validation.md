# Council Reliability Validation

Date: 2026-09-09

The change was made on the isolated branch `codex/council-reliability`. It remains local; no installation into the user's home directories, provider calls, publication, commit or push was performed.

## Checks

| Check | Result |
|---|---|
| `python3 -m unittest discover -s tests -v` | 25 passed |
| `./scripts/council-simulation-checklist.sh` | passed |
| `shellcheck install.sh scripts/detect-providers.sh scripts/council-simulation-checklist.sh` | passed with isolated `shellcheck-py` 0.11.0.1 |
| `markdownlint --disable MD013 MD024 MD033 MD041 protocol/*.md` | passed |
| `python3 -m compileall -q scripts tests` | passed |
| `git diff --check` | passed |
| Temporary Claude/Codex/Gemini installations with paths containing spaces | passed; each received protocol, helpers and defaults |
| Dry-run installation | passed; target was not created |

## Behavior scenarios

`docs/evaluation-scenarios.json` contains three bounded consuming-agent scenarios and raw helper inputs/results:

- Two providers for the Jobs/Rubin/Torvalds triangle returns `relaxed` and the exact collocated pair; no model calls run under `--dry-route`.
- Two live ordinary seats supporting `ship` produce `split` at `2.0 / 3.5`; the simulated 1.5× Jobs seat is excluded from votes and remains in the denominator.
- A Gemini host with no native delegation or authorized external provider produces `analysis_only` and does not invent a Claude/OpenAI fallback.

The evaluator did not call real providers, spawn agents, or install into a live user configuration. These scenarios validate the protocol decisions and helper boundaries, not live compatibility with every CLI, model ID or host tool schema.

## Remaining limits

The route helper uses a bounded search and reports `search_limit` if its node budget is exhausted; that result is not a proof of optimality. Provider detection reports dispatch candidates and deliberately leaves authentication/inference readiness as `unknown` until an authorized call proves them. The model coordinator still needs the current host tool schema at runtime, as required by the shared adapter contract.
