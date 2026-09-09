# Council Reliability Implementation Plan

> **For agentic workers:** Implementation was authorized by the user's “开始吧” following the five-point review. Execute task-by-task in this fresh checkout on `codex/council-reliability`. Preserve the approved scope and validate before delivery.

**Goal:** Make Claude, Codex and Gemini apply the same routing, fallback and voting rules.

**Architecture:** Keep the existing persona/catalog data. Move execution rules into one installed protocol, with three small host adapters. Use Python standard-library helpers for deterministic route and tally decisions; the host remains responsible for model calls.

**Tech Stack:** Python 3.9+, unittest, Bash, Markdown, GitHub Actions.

**Spec:** The approved review in this task, items 1–3 plus their behavioral tests. No changes to member selection defaults, persona identities, 1.5× domain weighting, or round counts. No production installation, remote writes or model-provider charges.

## Global Constraints

- Reuse the existing 22-member catalog and profile/triad relationships.
- Keep simulated outputs out of independent voting; failed seats remain in the original denominator.
- A live host is not always Anthropic; CLI installation is not authentication or inference readiness.
- Impossible routing constraints must produce a bounded, explicit degraded result.
- Preserve all existing authorization boundaries and user files.

## Tasks

- [x] Add failing scenario tests in `tests/test_runtime.py`, `tests/test_detection.py`, and `tests/test_install.py`. Run with `python3 -m unittest discover -s tests -v` and retain failure evidence.
- [x] Implement `scripts/council_runtime.py`: `route` reads JSON members/providers/optional manual assignments and returns assignments plus exact conflicts and search status; `tally` reads a locked panel, options and observed responses and returns votes, exclusions, quorum and result. Both use JSON stdin or `--input FILE` and produce JSON stdout.
- [x] Make `scripts/detect-providers.sh --host claude|codex|gemini` report the actual host through `scripts/detect_providers.py`. Probe installation only by default; record authentication and inference as unknown. Test fake external CLIs, unavailable providers, quoted paths and timeouts without network calls.
- [x] Extract `protocol/core.md` and `protocol/runtime.md`; replace the three duplicated execution sequences with adapters. All modes use the same route, retry, host fallback, tally and Chairman policy. Test isolated consuming-agent scenarios and preserve their actual outputs.
- [x] Extend `install.sh` to install shared protocol, helpers and required defaults for each client. Verify real installations only into temporary directories, including dry-run and custom roots.
- [x] Update documentation/checklist/CI to execute behavior tests and parse detection JSON. Run existing catalog checks, installation checks, shell syntax/lint when available, and `git diff --check`.
- [x] Review the final diff and write `docs/reliability-validation.md` with checks, outcomes and limits. Leave changes local and reviewable.

## Hand-checked acceptance cases

1. Jobs/Rubin/Torvalds with two providers: complete assignment, one or more conflicts, explicit relaxed status; with three providers: zero conflicts.
2. A manual mapping remains fixed even when it violates separation; the violation is reported.
3. Three seats weighted 1.5/1/1: the 1.5 seat plus one ordinary supporter clears 7/3; two ordinary supporters alone do not.
4. A simulated supporter never supplies a vote; all simulated gives analysis-only; one valid live seat never yields consensus.
5. Abstention, malformed stance, missing response, duplicate execution and host fallback do not create invented independent support.
6. Each isolated client installation can read the shared protocol and run the helpers without relying on another client's directory.

## Validation evidence

Results are recorded in `docs/reliability-validation.md` after execution. Script tests prove mechanical decisions, while consuming-agent scenarios provide bounded evidence of protocol use; neither proves live integration with every provider.
