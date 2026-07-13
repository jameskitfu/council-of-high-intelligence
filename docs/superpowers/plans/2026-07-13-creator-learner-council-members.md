# Creator-Learner Council Members Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand Council of High Intelligence from 18 to 22 members with Rick Rubin, Steve Jobs, Leonardo da Vinci, and Stephen Krashen, including complete three-platform routing and bilingual documentation.

**Architecture:** Each member remains an isolated persona file with structured frontmatter and the repository's standard eight-section prompt contract. Static coordinator tables in Claude, Codex, and Gemini expose the same 22-member roster, 11 new triads, polarity routing, and an eight-seat `ai-creator-learner` profile; the installer continues discovering persona files dynamically.

**Tech Stack:** Markdown persona protocols, YAML frontmatter, Bash validation and installation scripts

## Global Constraints

- Add exactly four members: `jobs`, `rubin`, `leonardo`, and `krashen`; do not add Naval Ravikant.
- The resulting roster contains exactly 22 `agents/council-*.md` files.
- Preserve the existing deliberation rounds, weighted voting, Chairman selection, provider detection, and fallback behavior.
- Keep `SKILL.md`, `SKILL.codex.md`, `SKILL.gemini.md`, `README.md`, and `README.zh-CN.md` semantically synchronized.
- Keep `exploration-orthogonal` and `execution-lean` unchanged; add only the new `ai-creator-learner` profile.
- `classic` and `--full` contain all 22 members; automatic default selection remains one three-member triad.
- Manual member selection accepts `2-12` members.
- Follow the agent section order and constraints in `CLAUDE.md`, including Grounding Protocol immediately after Identity and tailored Round 2 output instructions.
- All user-facing documentation must describe the new 22-member roster and warn that full mode is expensive.

---

### Task 1: Test-first persona expansion

**Files:**
- Create: `agents/council-jobs.md`
- Create: `agents/council-rubin.md`
- Create: `agents/council-leonardo.md`
- Create: `agents/council-krashen.md`
- Modify: `scripts/council-simulation-checklist.sh`

**Interfaces:**
- Consumes: the agent schema documented in `CLAUDE.md` and exemplified by `agents/council-rams.md`.
- Produces: four discoverable `council-*.md` personas with valid frontmatter, provider affinity, polarity pairs, triad identifiers, profile membership, and structured outputs.

- [ ] **Step 1: Extend the checklist before adding persona files**

Require `agent_count == 22`, explicitly require `jobs rubin leonardo krashen`, and validate their frontmatter-derived metadata through the existing generic structure, grounding-placement, and provider-affinity loops. Add platform integration assertions for all four names, the `ai-creator-learner` profile, and these triads: `creative`, `creator`, `editing`, `product-vision`, `launch`, `creator-product`, `invention`, `prototype`, `language-learning`, `learn-in-public`, `english-content`.

- [ ] **Step 2: Run the checklist and verify RED**

Run: `./scripts/council-simulation-checklist.sh`

Expected: FAIL because the repository still has 18 agents or because `agents/council-jobs.md` is missing.

- [ ] **Step 3: Create the four persona files**

Use the exact metadata and boundaries below:

| ID | Figure | Domain | Model | Polarity | Pairs | Triads | Profile | Affinity |
|---|---|---|---|---|---|---|---|---|
| `jobs` | Steve Jobs | Product taste & integrated experience | opus | Shape the whole experience around one clear promise | rubin, rams, torvalds | creator, product-vision, launch, creator-product, english-content | classic, ai-creator-learner | anthropic, openai |
| `rubin` | Rick Rubin | Creative direction & artistic truth | opus | Listen to what the work wants to become | jobs, torvalds | creative, creator, editing, creator-product, learn-in-public | classic, ai-creator-learner | anthropic, google |
| `leonardo` | Leonardo da Vinci | Observational synthesis & visual invention | opus | See it, sketch it, then understand it | aristotle, ada | creative, invention, prototype, learn-in-public | classic, ai-creator-learner | google, anthropic, openai |
| `krashen` | Stephen Krashen | Language acquisition & comprehensible input | sonnet | Acquire through meaningful input before forcing output | feynman | language-learning, learn-in-public, english-content | classic, ai-creator-learner | google, anthropic |

Each Analytical Method must contain five operational steps. Each Grounding Protocol must impose specific limits or evidence checks. Each `What You See` and `What You Tend to Miss` section stays within three sentences. Each Round 2 output uses `Disagree`, `Strengthened by`, `Position Update`, and `Evidence Label`; each standalone output ends with `Recommendation`, `Confidence`, and `What Would Change My Mind`.

- [ ] **Step 4: Run targeted structural checks**

Run:

```bash
for f in agents/council-{jobs,rubin,leonardo,krashen}.md; do
  grep -q '^## Grounding Protocol' "$f"
  grep -q '^## Analytical Method' "$f"
  grep -q '^## Output Format (Council Round 2)' "$f"
  grep -q '^## Output Format (Standalone)' "$f"
done
```

Expected: exit 0.

- [ ] **Step 5: Commit Task 1**

```bash
git add agents/council-{jobs,rubin,leonardo,krashen}.md scripts/council-simulation-checklist.sh
git commit -m "feat: add creator-learner council personas"
```

### Task 2: Integrate all three coordinator protocols

**Files:**
- Modify: `SKILL.md`
- Modify: `SKILL.codex.md`
- Modify: `SKILL.gemini.md`

**Interfaces:**
- Consumes: Task 1 member IDs and frontmatter contracts.
- Produces: platform-equivalent roster, panel selection, triad lookup, duo routing, and profile selection for all four members.

- [ ] **Step 1: Update roster counts and member tables**

Change all `18` full-roster references to `22`, change manual selection to `2-12`, fix `classic` from the stale `All 11 members` text to all 22, and add the four member rows or IDs to each platform file.

- [ ] **Step 2: Add polarity pairs and Duo keyword routing**

Add pairs for Jobs–Rubin, Jobs–Rams, Jobs–Torvalds, Rubin–Torvalds, Leonardo–Aristotle, Leonardo–Ada, and Krashen–Feynman. Add domain keyword routing for creative/creator/editing, product/brand/launch, invention/visual/prototype, and language/English/acquisition.

- [ ] **Step 3: Add 11 triads verbatim across platforms**

Use exactly the triads and membership defined in the design specification. Do not rename identifiers between platforms.

- [ ] **Step 4: Add the `ai-creator-learner` profile**

Use exactly: `karpathy, torvalds, feynman, rubin, jobs, leonardo, krashen, rams`.

- [ ] **Step 5: Run the checklist**

Run: `./scripts/council-simulation-checklist.sh`

Expected: platform integration checks and all existing protocol checks pass.

- [ ] **Step 6: Commit Task 2**

```bash
git add SKILL.md SKILL.codex.md SKILL.gemini.md
git commit -m "feat: integrate creator-learner council panels"
```

### Task 3: Synchronize bilingual documentation and project metadata

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: the final roster and panel identifiers from Task 2.
- Produces: equivalent English and Simplified Chinese user documentation plus contributor-facing architecture counts.

- [ ] **Step 1: Update English README**

Change all member-count references and badges from 18 to 22, add four member rows, add the new polarity pairs, 11 triads, `ai-creator-learner` profile, and an explicit note that `--full` invokes all 22 members and is the most expensive mode.

- [ ] **Step 2: Update Simplified Chinese README**

Mirror the English changes using natural Simplified Chinese while preserving all identifiers: Rick Rubin（里克·鲁宾）, Steve Jobs（史蒂夫·乔布斯）, Leonardo da Vinci（列奥纳多·达·芬奇）, Stephen Krashen（斯蒂芬·克拉申）.

- [ ] **Step 3: Update project metadata**

Add an Unreleased changelog entry describing the four members, 11 triads, and profile. Change `CLAUDE.md` architecture count from 18 to 22 and document that new agents must be wired into all three platform coordinators and both READMEs.

- [ ] **Step 4: Validate bilingual Markdown**

Run a Python assertion script that verifies balanced code fences and `<details>` tags, resolves local Markdown links, and checks that both READMEs contain all four member identifiers plus `ai-creator-learner`.

Expected: `Bilingual README checks passed`.

- [ ] **Step 5: Run full repository verification**

```bash
./scripts/council-simulation-checklist.sh
./install.sh --dry-run
./install.sh --dry-run --codex
./install.sh --dry-run --gemini
git diff --check
```

Expected: all commands exit 0; optional local-tool warnings are reported but do not fail.

- [ ] **Step 6: Commit Task 3**

```bash
git add README.md README.zh-CN.md CHANGELOG.md CLAUDE.md
git commit -m "docs: document 22-member creator-learner council"
```
