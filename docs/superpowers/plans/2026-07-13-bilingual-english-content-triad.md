# Bilingual `english-content` Triad Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Broaden `english-content` to guide separate English and Chinese editions of the same YouTube topic without changing its ID, members, or execution behavior.

**Architecture:** Update the canonical rationale and bilingual README example, then add identical compact-coordinator routing guidance for Codex and Gemini. Protect compatibility with exact string assertions plus the existing dependency-free council graph checklist.

**Tech Stack:** Markdown, Python 3 standard library, Bash, Git

## Global Constraints

- Keep `english-content` as one of exactly 31 Triads.
- Keep its members exactly Krashen + Jobs + Rams.
- Do not introduce a `bilingual-content` Triad ID.
- Treat the English and Chinese editions as separate uploads of the same topic.
- Prefer localized scripts, examples, titles, thumbnails, pacing, and content promises over word-for-word translation.
- Do not modify persona frontmatter, profiles, voting, provider routing, or execution steps.
- Modify only `SKILL.md`, `SKILL.codex.md`, `SKILL.gemini.md`, `README.md`, and `README.zh-CN.md` for the product change.

---

### Task 1: Broaden `english-content` copy and routing guidance

**Files:**
- Modify: `SKILL.md:130`
- Modify: `SKILL.codex.md:82-84`
- Modify: `SKILL.gemini.md:82-84`
- Modify: `README.md:219`
- Modify: `README.zh-CN.md:228`

**Interfaces:**
- Consumes: the existing `english-content` Triad with Krashen, Jobs, and Rams.
- Produces: canonical bilingual-version wording across the main coordinator, compact coordinators, and bilingual READMEs.

- [ ] **Step 1: Run the failing bilingual-routing contract**

```bash
python3 - <<'PY'
from pathlib import Path

english_rationale = "Acquisition value + bilingual packaging + audience clarity"
chinese_rationale = "习得价值 + 双语版本包装 + 观众清晰度"
english_question = "How should I produce separate English and Chinese versions of the same YouTube topic so each feels native to its audience?"
chinese_question = "同一个 YouTube 选题应该如何分别制作英文版和中文版，才能让两类观众都觉得自然？"
routing = "Treat `english-content` as the route for requests about publishing separate English and Chinese editions of the same topic, including localized scripts, examples, titles, thumbnails, pacing, and content promises. Keep each edition natural for its audience instead of translating word for word."

skill = Path("SKILL.md").read_text()
readme = Path("README.md").read_text()
readme_zh = Path("README.zh-CN.md").read_text()
codex = Path("SKILL.codex.md").read_text()
gemini = Path("SKILL.gemini.md").read_text()

assert english_rationale in skill
assert english_rationale in readme
assert chinese_rationale in readme_zh
assert english_question in readme
assert chinese_question in readme_zh
assert codex.count(routing) == 1
assert gemini.count(routing) == 1
assert "`bilingual-content`" not in "\n".join((skill, readme, readme_zh, codex, gemini))
PY
```

Expected: FAIL because the current rationale and example describe an English-only video and neither compact coordinator contains the routing guidance.

- [ ] **Step 2: Update the canonical main-coordinator rationale**

Use `apply_patch` to change only the `english-content` rationale in `SKILL.md`:

```markdown
| `english-content` | Krashen + Jobs + Rams | Acquisition value + bilingual packaging + audience clarity |
```

- [ ] **Step 3: Add identical Codex and Gemini routing guidance**

Use `apply_patch` to insert this paragraph immediately after the Triads table and before `## Profiles` in both `SKILL.codex.md` and `SKILL.gemini.md`:

```markdown
Treat `english-content` as the route for requests about publishing separate English and Chinese editions of the same topic, including localized scripts, examples, titles, thumbnails, pacing, and content promises. Keep each edition natural for its audience instead of translating word for word.
```

- [ ] **Step 4: Update the English README row**

Use `apply_patch` to replace only the `english-content` row in `README.md` with:

```markdown
| `english-content` | Krashen + Jobs + Rams | Acquisition value + bilingual packaging + audience clarity | How should I produce separate English and Chinese versions of the same YouTube topic so each feels native to its audience? |
```

- [ ] **Step 5: Update the Simplified Chinese README row**

Use `apply_patch` to replace only the `english-content` row in `README.zh-CN.md` with:

```markdown
| `english-content` | Krashen + Jobs + Rams | 习得价值 + 双语版本包装 + 观众清晰度 | 同一个 YouTube 选题应该如何分别制作英文版和中文版，才能让两类观众都觉得自然？ |
```

- [ ] **Step 6: Run the bilingual-routing contract again**

Run the Python command from Step 1.

Expected: PASS with exit code `0` and no output.

- [ ] **Step 7: Verify compatibility and repository health**

```bash
./scripts/council-simulation-checklist.sh
git diff --check
git diff --stat
```

Expected: the exact 22-member/31-Triad graph and all installation dry-runs pass; `git diff --check` has no output; the product diff lists exactly the five scoped files.

- [ ] **Step 8: Commit the product change**

```bash
git add SKILL.md SKILL.codex.md SKILL.gemini.md README.md README.zh-CN.md
git commit -m "docs: broaden english-content for bilingual editions"
```

Expected: one product commit modifying exactly the five scoped files.

---

### Task 2: Publish and integrate the bilingual routing update

**Files:**
- Modify remotely: `jameskitfu/council-of-high-intelligence` branch `codex/optimize-bilingual-content`
- Modify remotely: `jameskitfu/council-of-high-intelligence` branch `main`

**Interfaces:**
- Consumes: the verified Task 1 commit plus the committed design and plan.
- Produces: a fork-internal Pull Request and a fast-forwarded fork `main`; no upstream repository remote is configured or modified.

- [ ] **Step 1: Push the feature branch**

```bash
git push -u origin codex/optimize-bilingual-content
```

Expected: the feature branch is created in `jameskitfu/council-of-high-intelligence`.

- [ ] **Step 2: Create a draft Pull Request**

Create a PR in `jameskitfu/council-of-high-intelligence` from `codex/optimize-bilingual-content` to `main` titled:

```text
docs: broaden english-content for bilingual editions
```

Describe the compatibility-preserving rationale update, separate English/Chinese edition workflow, compact-coordinator routing hints, and validation results.

- [ ] **Step 3: Integrate in a temporary external worktree**

From `/Users/fuhuan/Documents/aiagentmaster/council-of-high-intelligence`:

```bash
git fetch origin main
git worktree add -b codex/bilingual-content-integration /Users/fuhuan/Documents/aiagentmaster/.worktrees/council-bilingual-integration origin/main
git -C /Users/fuhuan/Documents/aiagentmaster/.worktrees/council-bilingual-integration merge --ff-only codex/optimize-bilingual-content
git -C /Users/fuhuan/Documents/aiagentmaster/.worktrees/council-bilingual-integration ./scripts/council-simulation-checklist.sh
```

Expected: the integration branch fast-forwards and the merged tree passes the checklist.

- [ ] **Step 4: Push and verify main**

```bash
git -C /Users/fuhuan/Documents/aiagentmaster/.worktrees/council-bilingual-integration push origin HEAD:main
git -C /Users/fuhuan/Documents/aiagentmaster/.worktrees/council-bilingual-integration fetch origin main
test "$(git -C /Users/fuhuan/Documents/aiagentmaster/.worktrees/council-bilingual-integration rev-parse HEAD)" = "$(git -C /Users/fuhuan/Documents/aiagentmaster/.worktrees/council-bilingual-integration rev-parse origin/main)"
```

Expected: fork `main` advances and local/remote SHAs match.

- [ ] **Step 5: Clean up only the temporary integration worktree**

```bash
git worktree remove /Users/fuhuan/Documents/aiagentmaster/.worktrees/council-bilingual-integration
git worktree prune
git branch -d codex/bilingual-content-integration
```

Expected: the temporary integration worktree and branch are removed; the feature worktree remains for review.
