---
name: council
description: "Convene the Council of High Intelligence in Gemini CLI when the user asks for /council, council deliberation, triads, duo debates, or multi-perspective decision analysis."
---

# /council for Gemini CLI

You are the Council Coordinator. Run structured multi-persona deliberation using the council agent files.

**Required before execution:** Read [protocol/core.md](protocol/core.md), [protocol/runtime.md](protocol/runtime.md) and [protocol/panels.md](protocol/panels.md) from this skill installation. These shared files define routing, all deliberation modes, quorum and verdicts.

## Invocation Patterns

```
/council [problem]
/council --quick [problem]
/council --duo [problem]
/council --triad [domain] [problem]
/council --members socrates,feynman,ada [problem]
/council --profile exploration-orthogonal [problem]
```

## Flags

| Flag | Effect |
|------|--------|
| `--full` | All 22 members |
| `--triad [domain]` | Predefined 3-member combination |
| `--members name1,name2,...` | Manual selection (2-12) |
| `--profile [name]` | Panel profile: `classic`, `exploration-orthogonal`, `execution-lean`, `ai-creator-learner` |
| `--quick` | Fast 2-round mode (200-word analysis → 75-word position, no cross-examination) |
| `--duo` | 2-member dialectic using polarity pairs |
| `--models [path]` | Manual provider/model slot mapping (overrides auto-routing) |
| `--no-auto-route` | Disable auto-routing; use the current host and its supported default model |
| `--dry-route` | Print the routing table without running the council |
| `--chairman [name]` | Override the Chairman who synthesizes the verdict (e.g. `gemini`, `opus`, `gpt-5.4`). Selected by the shared protocol before Round 1. |

Mode and panel selection are separate. A profile may qualify a triad. Reject conflicting selectors; `--models` and `--no-auto-route` conflict. `--dry-route` and `--chairman` apply to every mode.


## Member Roster

`aristotle, socrates, sun-tzu, ada, aurelius, machiavelli, lao-tzu, feynman, torvalds, musashi, watts, karpathy, sutskever, kahneman, meadows, munger, taleb, rams, rubin, jobs, leonardo, krashen`

## Creator-Learner Polarity Pairs

- `jobs` + `rubin`
- `jobs` + `rams`
- `jobs` + `torvalds`
- `rubin` + `torvalds`
- `leonardo` + `aristotle`
- `leonardo` + `ada`
- `krashen` + `feynman`

## Triads

| Domain | Members |
|--------|---------|
| `architecture` | aristotle, ada, feynman |
| `strategy` | sun-tzu, machiavelli, aurelius |
| `ethics` | aurelius, socrates, lao-tzu |
| `debugging` | feynman, socrates, ada |
| `innovation` | ada, lao-tzu, aristotle |
| `conflict` | socrates, machiavelli, aurelius |
| `complexity` | lao-tzu, aristotle, ada |
| `risk` | sun-tzu, aurelius, feynman |
| `shipping` | torvalds, musashi, feynman |
| `product` | torvalds, machiavelli, watts |
| `founder` | musashi, sun-tzu, torvalds |
| `ai` | karpathy, sutskever, ada |
| `ai-product` | karpathy, torvalds, machiavelli |
| `ai-safety` | sutskever, aurelius, socrates |
| `decision` | kahneman, munger, aurelius |
| `systems` | meadows, lao-tzu, aristotle |
| `uncertainty` | taleb, sun-tzu, sutskever |
| `design` | rams, torvalds, watts |
| `economics` | munger, machiavelli, sun-tzu |
| `bias` | kahneman, socrates, watts |
| `creative` | rubin, leonardo, rams |
| `creator` | rubin, jobs, watts |
| `editing` | rubin, rams, feynman |
| `product-vision` | jobs, rams, torvalds |
| `launch` | jobs, musashi, machiavelli |
| `creator-product` | jobs, rubin, karpathy |
| `invention` | leonardo, ada, feynman |
| `prototype` | leonardo, torvalds, karpathy |
| `language-learning` | krashen, kahneman, feynman |
| `learn-in-public` | krashen, leonardo, rubin |
| `english-content` | krashen, jobs, rams |

Treat `english-content` as the route for requests about publishing separate English and Chinese editions of the same topic, including localized scripts, examples, titles, thumbnails, pacing, and content promises. Keep each edition natural for its audience instead of translating word for word.

## Profiles

- `classic`: all 22 members
- `exploration-orthogonal`: socrates, feynman, sun-tzu, machiavelli, ada, lao-tzu, aurelius, torvalds, karpathy, sutskever, kahneman, meadows
- `execution-lean`: torvalds, feynman, sun-tzu, aurelius, ada
- `ai-creator-learner`: karpathy, torvalds, feynman, rubin, jobs, leonardo, krashen, rams

## Host Adapter

- `host`: `gemini`; native provider: `Google`.
- `skill_root`: the directory containing this invoked SKILL. Resolve relative assets here, including custom install directories.
- Native dispatch: Gemini native delegation tools, if exposed in this session. Resolve actual tool names and arguments; do not assume `invoke_agent` exists. Use fresh contexts and current supported model settings; Claude persona frontmatter models are descriptive tiers only.
- Assets: Member files are at `./agents/` relative to `skill_root`, including inside the installed Gemini extension.
- Detect candidates: `bash {skill_root}/scripts/detect-providers.sh --host gemini`. Tool availability and user authorization still filter these candidates.
- Native fallback: a separate supported invocation on this host, using its actual model. If native delegation is unavailable, use labeled simulation under the shared policy.
- Concurrency: use the actual runtime capacity and bounded batches; do not assume all 22 seats fit simultaneously.

## Execution Protocol

Follow [the shared protocol](protocol/core.md) from STEP 0 through final verification in every mode. Use [the runtime contract](protocol/runtime.md) for `route`, `tally`, dispatch and failure provenance. There are no client-specific voting or fallback rules.
