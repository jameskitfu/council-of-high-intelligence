# Fork Attribution README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clearly credit the upstream author, identify this repository as an extended fork, and make all Quickstart clone commands install the fork.

**Architecture:** Keep attribution and repository-selection changes confined to the two bilingual README files. Use equivalent English and Chinese notices near the title, preserve upstream historical badges, and validate exact links and counts with Python standard-library assertions before running the repository checklist.

**Tech Stack:** Markdown, Bash, Python 3 standard library, Git

## Global Constraints

- Update `README.md` and `README.zh-CN.md` only for the product change.
- Credit the original project and `@0xNyk` with direct GitHub links.
- Identify `@jameskitfu` as the maintainer of the extended fork.
- Change exactly three Quickstart clone commands in each README to `https://github.com/jameskitfu/council-of-high-intelligence.git`.
- Keep upstream Release, Stars, and Star History links unchanged.
- Remove the stale `Support the Project` and `支持项目` table-of-contents entries.
- Do not modify the upstream `0xNyk/council-of-high-intelligence` repository.

---

### Task 1: Add bilingual fork attribution and fork installation links

**Files:**
- Modify: `README.md:1-90`
- Modify: `README.zh-CN.md:1-96`

**Interfaces:**
- Consumes: the existing language selector, header image, table of contents, and three platform Quickstart blocks in each README.
- Produces: two structurally aligned README files with explicit upstream/current-maintainer attribution and six fork clone commands.

- [ ] **Step 1: Run the pre-change contract and verify it fails**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

fork_url = "https://github.com/jameskitfu/council-of-high-intelligence.git"
for path in (Path("README.md"), Path("README.zh-CN.md")):
    text = path.read_text()
    assert text.count(f"git clone {fork_url}") == 3, path
    assert "https://github.com/0xNyk/council-of-high-intelligence" in text, path
    assert "https://github.com/0xNyk" in text, path
    assert "https://github.com/jameskitfu" in text, path
assert "[Support the Project](#support-the-project)" not in Path("README.md").read_text()
assert "[支持项目](#支持项目)" not in Path("README.zh-CN.md").read_text()
PY
```

Expected: FAIL because neither README contains three fork clone commands or a `jameskitfu` attribution link.

- [ ] **Step 2: Add the English attribution notice**

Insert immediately after the language selector in `README.md`:

```markdown
> **Fork notice:** This repository is an extended fork of [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence), originally created by [@0xNyk](https://github.com/0xNyk) and maintained here by [@jameskitfu](https://github.com/jameskitfu).
```

Remove this stale table-of-contents entry:

```markdown
- [Support the Project](#support-the-project)
```

Replace all three English Quickstart clone commands with:

```bash
git clone https://github.com/jameskitfu/council-of-high-intelligence.git
```

- [ ] **Step 3: Add the Simplified Chinese attribution notice**

Insert immediately after the language selector in `README.zh-CN.md`:

```markdown
> **Fork 说明：** 本仓库基于 [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) fork 并扩展；原项目由 [@0xNyk](https://github.com/0xNyk) 创建，当前 fork 由 [@jameskitfu](https://github.com/jameskitfu) 维护。
```

Remove this stale table-of-contents entry:

```markdown
- [支持项目](#支持项目)
```

Replace all three Chinese Quickstart clone commands with:

```bash
git clone https://github.com/jameskitfu/council-of-high-intelligence.git
```

- [ ] **Step 4: Run the exact attribution and clone-link contract**

Run the Python command from Step 1 again.

Expected: PASS with exit code `0` and no output.

- [ ] **Step 5: Run bilingual Markdown and repository validation**

Run:

```bash
python3 .superpowers/sdd/final-fix-readme-check.py
./scripts/council-simulation-checklist.sh
git diff --check
```

Expected: `Bilingual README checks passed`, the council checklist completes successfully, and `git diff --check` produces no output. The optional `shellcheck` step may warn if the binary is not installed.

- [ ] **Step 6: Commit the product change**

```bash
git add README.md README.zh-CN.md
git commit -m "docs: credit upstream project and author"
```

Expected: one commit modifying exactly the two README files.

---

### Task 2: Publish and integrate the README attribution

**Files:**
- Modify remotely: `jameskitfu/council-of-high-intelligence` branch `codex/add-creator-members`
- Modify remotely: `jameskitfu/council-of-high-intelligence` branch `main`

**Interfaces:**
- Consumes: the verified Task 1 commit and the existing `fork` Git remote.
- Produces: a fork-internal Pull Request and a fast-forwarded fork `main`; upstream `origin` remains untouched.

- [ ] **Step 1: Push the feature branch to the fork**

```bash
git push fork codex/add-creator-members
```

Expected: the remote feature branch advances to the Task 1 commit.

- [ ] **Step 2: Create a fork-internal Pull Request**

Create a draft Pull Request in `jameskitfu/council-of-high-intelligence` from `codex/add-creator-members` to `main` titled:

```text
docs: credit upstream project and author
```

The body must summarize the attribution, fork clone links, stale table-of-contents cleanup, and validation commands.

- [ ] **Step 3: Fast-forward an isolated local integration branch**

```bash
git fetch fork main
git worktree add -b codex/fork-main-integration .worktrees/fork-main-integration fork/main
git -C .worktrees/fork-main-integration merge --ff-only codex/add-creator-members
```

Expected: the integration branch fast-forwards without conflicts.

- [ ] **Step 4: Validate and push fork main**

```bash
git -C .worktrees/fork-main-integration ./scripts/council-simulation-checklist.sh
git -C .worktrees/fork-main-integration push fork HEAD:main
git -C .worktrees/fork-main-integration fetch fork main
test "$(git -C .worktrees/fork-main-integration rev-parse HEAD)" = "$(git -C .worktrees/fork-main-integration rev-parse fork/main)"
```

Expected: checks pass, `fork/main` advances, and local/remote SHAs match.

- [ ] **Step 5: Clean up only the temporary integration worktree**

From the main repository root:

```bash
git worktree remove .worktrees/fork-main-integration
git worktree prune
git branch -d codex/fork-main-integration
```

Expected: the temporary integration worktree and branch are removed; the feature worktree remains available.
