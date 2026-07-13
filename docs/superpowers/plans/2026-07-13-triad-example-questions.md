# Triad Example Questions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one concrete example question to every predefined Triad row in the English and Simplified Chinese READMEs.

**Architecture:** Extend the existing two 31-row Markdown tables from three to four columns without changing their IDs, members, rationales, order, or surrounding `<details>` structure. Validate the two tables with a dependency-free Python parser, then run the existing bilingual README and repository checks.

**Tech Stack:** Markdown, Python 3 standard library, Bash, Git

## Global Constraints

- Modify `README.md` and `README.zh-CN.md` only for the product change.
- Add `Example Question` to the English table and `问题样例` to the Chinese table.
- Preserve all 31 Triad IDs, member combinations, row order, and rationales.
- Use the exact approved questions from `docs/superpowers/specs/2026-07-13-triad-example-questions-design.md`.
- English examples end with `?`; Chinese examples end with `？`.
- Do not add repeated `/council` command prefixes to table cells.
- Do not change coordinator routing, personas, or the upstream repository.

---

### Task 1: Extend both predefined-Triad tables

**Files:**
- Modify: `README.md:185-222`
- Modify: `README.zh-CN.md:194-231`

**Interfaces:**
- Consumes: the existing ordered 31-row English and Chinese tables and the approved bilingual examples.
- Produces: two ordered 31-row, four-column tables with unique example questions.

- [ ] **Step 1: Run the failing table contract**

```bash
python3 - <<'PY'
from pathlib import Path

def parse(path, summary):
    text = Path(path).read_text()
    start = text.index(summary)
    table_start = text.index("\n|", start) + 1
    table_end = text.index("\n\n</details>", table_start)
    lines = [line for line in text[table_start:table_end].splitlines() if line.startswith("|")]
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines[2:]]
    return header, rows

english_header, english_rows = parse("README.md", "<summary><strong>Pre-defined Triads</strong>")
chinese_header, chinese_rows = parse("README.zh-CN.md", "<summary><strong>预定义 Triad</strong>")
assert english_header == ["Domain", "Triad", "Rationale", "Example Question"]
assert chinese_header == ["领域", "Triad", "组合逻辑", "问题样例"]
assert len(english_rows) == len(chinese_rows) == 31
assert all(len(row) == 4 for row in english_rows + chinese_rows)
assert [row[0] for row in english_rows] == [row[0] for row in chinese_rows]
assert len({row[3] for row in english_rows}) == 31
assert len({row[3] for row in chinese_rows}) == 31
assert all(row[3].endswith("?") for row in english_rows)
assert all(row[3].endswith("？") for row in chinese_rows)
PY
```

Expected: FAIL because both current tables have only three columns.

- [ ] **Step 2: Replace the English table with the approved four-column table**

Use `apply_patch` to preserve the surrounding `<details>` block and replace only the table with:

```markdown
| Domain | Triad | Rationale | Example Question |
|--------|-------|-----------|------------------|
| `architecture` | Aristotle + Ada + Feynman | Classify + formalize + simplicity-test | Should we split our monolith into microservices now? |
| `strategy` | Sun Tzu + Machiavelli + Aurelius | Terrain + incentives + moral grounding | How should we enter a market dominated by two larger competitors? |
| `ethics` | Aurelius + Socrates + Lao Tzu | Duty + questioning + natural order | Should we ship a persuasive feature that may encourage compulsive use? |
| `debugging` | Feynman + Socrates + Ada | Bottom-up + assumption testing + formal verification | Why does this service fail only under production load? |
| `innovation` | Ada + Lao Tzu + Aristotle | Abstraction + emergence + classification | How can we redesign online learning without copying existing course platforms? |
| `conflict` | Socrates + Machiavelli + Aurelius | Expose + predict + ground | How should two cofounders resolve a deadlock over product direction? |
| `complexity` | Lao Tzu + Aristotle + Ada | Emergence + categories + formalism | How can we simplify a workflow with too many interacting rules? |
| `risk` | Sun Tzu + Aurelius + Feynman | Threats + resilience + empirical verification | What could make this launch fail catastrophically, and how do we reduce the risk? |
| `shipping` | Torvalds + Musashi + Feynman | Pragmatism + timing + first-principles | Is this product ready to release this week, or should we delay? |
| `product` | Torvalds + Machiavelli + Watts | Ship it + incentives + reframing | Which feature should we build next to create the most user value? |
| `founder` | Musashi + Sun Tzu + Torvalds | Timing + terrain + engineering reality | Should I leave my job to work on this startup full-time? |
| `ai` | Karpathy + Sutskever + Ada | Empirical ML + scaling frontier + formal limits | Which model architecture should we test for this reasoning task? |
| `ai-product` | Karpathy + Torvalds + Machiavelli | ML capability + shipping pragmatism + incentives | How should we turn this AI prototype into a reliable paid product? |
| `ai-safety` | Sutskever + Aurelius + Socrates | Safety frontier + moral clarity + assumption destruction | What safeguards do we need before letting this agent take actions? |
| `decision` | Kahneman + Munger + Aurelius | Bias detection + inversion + moral clarity | Should we hire now or preserve runway for six more months? |
| `systems` | Meadows + Lao Tzu + Aristotle | Feedback loops + emergence + categories | Why does improving one team's metric make the overall system worse? |
| `uncertainty` | Taleb + Sun Tzu + Sutskever | Tail risk + terrain + scaling frontier | How should we plan when demand could be ten times higher or lower? |
| `design` | Rams + Torvalds + Watts | User clarity + maintainability + reframing | How can we make this onboarding flow clearer without adding more screens? |
| `economics` | Munger + Machiavelli + Sun Tzu | Models + incentives + competition | Will this freemium model create sustainable unit economics? |
| `bias` | Kahneman + Socrates + Watts | Cognitive bias + assumption destruction + frame audit | What assumptions are distorting our belief that users want this feature? |
| `creative` | Rubin + Leonardo + Rams | Artistic truth + invention + user clarity | How can I make this video concept more original without losing clarity? |
| `creator` | Rubin + Jobs + Watts | Authentic work + product direction + reframing | What should my YouTube channel stand for so viewers remember it? |
| `editing` | Rubin + Rams + Feynman | Essence + clarity + comprehension test | What should I cut from this video to make the core idea land? |
| `product-vision` | Jobs + Rams + Torvalds | Integrated experience + user need + feasibility | What should the complete user experience feel like three years from now? |
| `launch` | Jobs + Musashi + Machiavelli | Story + timing + incentives | How should we position and launch this product to earn early trust? |
| `creator-product` | Jobs + Rubin + Karpathy | Packaging + authenticity + AI capability | How can I turn my AI engineering content into a useful product? |
| `invention` | Leonardo + Ada + Feynman | Observation + formalization + empirical testing | How could we solve this problem with a mechanism that does not exist yet? |
| `prototype` | Leonardo + Torvalds + Karpathy | Sketch + build + empirical iteration | What is the smallest prototype that can test the riskiest assumption? |
| `language-learning` | Krashen + Kahneman + Feynman | Acquisition + learning bias + reality check | How can I improve my English listening without turning practice into memorization? |
| `learn-in-public` | Krashen + Leonardo + Rubin | Input + visible learning + authentic expression | How should I document my AI learning journey without pretending to be an expert? |
| `english-content` | Krashen + Jobs + Rams | Acquisition value + content promise + viewer clarity | How can I make English YouTube videos that learners understand and native viewers still enjoy? |
```

- [ ] **Step 3: Replace the Chinese table with the approved four-column table**

Use `apply_patch` to preserve the surrounding `<details>` block and replace only the table with:

```markdown
| 领域 | Triad | 组合逻辑 | 问题样例 |
|------|-------|----------|----------|
| `architecture` | Aristotle + Ada + Feynman | 分类 + 形式化 + 简洁性检验 | 我们现在应该把单体应用拆成微服务吗？ |
| `strategy` | Sun Tzu + Machiavelli + Aurelius | 局势 + 激励 + 道德根基 | 面对两个占主导地位的大型竞争对手，我们应该如何进入这个市场？ |
| `ethics` | Aurelius + Socrates + Lao Tzu | 责任 + 质疑 + 自然秩序 | 我们应该上线一个可能诱导用户沉迷的说服性功能吗？ |
| `debugging` | Feynman + Socrates + Ada | 自下而上 + 假设检验 + 形式验证 | 为什么这个服务只在生产负载下失败？ |
| `innovation` | Ada + Lao Tzu + Aristotle | 抽象 + 涌现 + 分类 | 不照搬现有课程平台，我们可以怎样重新设计在线学习？ |
| `conflict` | Socrates + Machiavelli + Aurelius | 揭示 + 预测 + 奠基 | 两位联合创始人应该如何化解产品方向上的僵局？ |
| `complexity` | Lao Tzu + Aristotle + Ada | 涌现 + 范畴 + 形式化 | 我们如何简化一个规则过多且相互影响的工作流？ |
| `risk` | Sun Tzu + Aurelius + Feynman | 威胁 + 韧性 + 经验验证 | 什么可能导致这次发布灾难性失败，我们该如何降低风险？ |
| `shipping` | Torvalds + Musashi + Feynman | 务实 + 时机 + 第一性原理 | 这个产品本周适合发布，还是应该延期？ |
| `product` | Torvalds + Machiavelli + Watts | 交付 + 激励 + 重构问题 | 下一步做哪个功能能创造最大的用户价值？ |
| `founder` | Musashi + Sun Tzu + Torvalds | 时机 + 局势 + 工程现实 | 我应该辞职全职投入这个创业项目吗？ |
| `ai` | Karpathy + Sutskever + Ada | 经验机器学习 + 规模化前沿 + 形式边界 | 针对这个推理任务，我们应该测试哪种模型架构？ |
| `ai-product` | Karpathy + Torvalds + Machiavelli | 机器学习能力 + 务实交付 + 激励 | 我们应该如何把这个 AI 原型变成可靠的付费产品？ |
| `ai-safety` | Sutskever + Aurelius + Socrates | 安全前沿 + 道德清醒 + 拆解假设 | 在允许这个智能体自主执行操作前，我们需要哪些安全措施？ |
| `decision` | Kahneman + Munger + Aurelius | 偏差识别 + 逆向思考 + 道德清醒 | 我们应该现在招聘，还是把现金跑道再延长六个月？ |
| `systems` | Meadows + Lao Tzu + Aristotle | 反馈回路 + 涌现 + 分类 | 为什么提升一个团队的指标反而让整个系统变差？ |
| `uncertainty` | Taleb + Sun Tzu + Sutskever | 尾部风险 + 局势 + 规模化前沿 | 当需求可能相差十倍时，我们应该如何制定计划？ |
| `design` | Rams + Torvalds + Watts | 用户清晰度 + 可维护性 + 重构问题 | 不增加页面的情况下，如何让这个新手引导流程更清晰？ |
| `economics` | Munger + Machiavelli + Sun Tzu | 思维模型 + 激励 + 竞争 | 这种免费增值模式能形成可持续的单位经济模型吗？ |
| `bias` | Kahneman + Socrates + Watts | 认知偏差 + 拆解假设 + 审视框架 | 哪些假设扭曲了我们对“用户需要这个功能”的判断？ |
| `creative` | Rubin + Leonardo + Rams | 艺术真实 + 发明 + 用户清晰度 | 如何让这个视频创意更具原创性，同时保持清晰？ |
| `creator` | Rubin + Jobs + Watts | 真实创作 + 产品方向 + 重构问题 | 我的 YouTube 频道应该代表什么，才能让观众记住？ |
| `editing` | Rubin + Rams + Feynman | 核心本质 + 清晰度 + 理解检验 | 为了让核心观点更有冲击力，这个视频应该删掉什么？ |
| `product-vision` | Jobs + Rams + Torvalds | 整合体验 + 用户需求 + 可行性 | 三年后，完整的用户体验应该给人什么感受？ |
| `launch` | Jobs + Musashi + Machiavelli | 叙事 + 时机 + 激励 | 我们应该如何定位并发布这款产品，才能尽早赢得信任？ |
| `creator-product` | Jobs + Rubin + Karpathy | 包装 + 真实表达 + AI 能力 | 如何把我的 AI 工程内容转化为真正有用的产品？ |
| `invention` | Leonardo + Ada + Feynman | 观察 + 形式化 + 经验检验 | 我们能否用一种尚不存在的机制解决这个问题？ |
| `prototype` | Leonardo + Torvalds + Karpathy | 描绘 + 构建 + 经验迭代 | 能验证最大风险假设的最小原型是什么？ |
| `language-learning` | Krashen + Kahneman + Feynman | 习得 + 学习偏差 + 现实检验 | 如何提升英语听力，又不把练习变成死记硬背？ |
| `learn-in-public` | Krashen + Leonardo + Rubin | 输入 + 公开学习 + 真实表达 | 我应该如何记录 AI 学习过程，同时不假装自己是专家？ |
| `english-content` | Krashen + Jobs + Rams | 习得价值 + 内容承诺 + 观众清晰度 | 如何制作学习者能听懂、母语观众也愿意看的英语 YouTube 视频？ |
```

- [ ] **Step 4: Run the table contract again**

Run the Python command from Step 1.

Expected: PASS with exit code `0` and no output.

- [ ] **Step 5: Verify the first three columns were not changed**

```bash
git diff --word-diff=porcelain -- README.md README.zh-CN.md
```

Expected: changes are limited to the two table headers/separators and the appended fourth cell in each of the 62 data rows.

- [ ] **Step 6: Run repository validation**

```bash
python3 .superpowers/sdd/final-fix-readme-check.py
./scripts/council-simulation-checklist.sh
git diff --check
```

Expected: bilingual README checks and the council checklist pass; `git diff --check` has no output. The optional `shellcheck` step may warn if unavailable.

- [ ] **Step 7: Commit the README change**

```bash
git add README.md README.zh-CN.md
git commit -m "docs: add triad example questions"
```

Expected: one product commit modifying exactly the two README files.

---

### Task 2: Publish and integrate the example-question tables

**Files:**
- Modify remotely: `jameskitfu/council-of-high-intelligence` branch `codex/add-creator-members`
- Modify remotely: `jameskitfu/council-of-high-intelligence` branch `main`

**Interfaces:**
- Consumes: the verified Task 1 commit plus the committed design and plan.
- Produces: a fork-internal Pull Request and a fast-forwarded fork `main`; upstream `origin` remains untouched.

- [ ] **Step 1: Push the feature branch**

```bash
git push fork codex/add-creator-members
```

Expected: the fork's feature branch advances to the Task 1 commit.

- [ ] **Step 2: Create a fork-internal draft Pull Request**

Create a PR in `jameskitfu/council-of-high-intelligence` from `codex/add-creator-members` to `main` titled:

```text
docs: add triad example questions
```

Describe the 31 bilingual examples, unchanged routing behavior, and validation results.

- [ ] **Step 3: Integrate in an isolated temporary worktree**

From the main repository root:

```bash
git fetch fork main
git worktree add -b codex/fork-main-integration .worktrees/fork-main-integration fork/main
git -C .worktrees/fork-main-integration merge --ff-only codex/add-creator-members
git -C .worktrees/fork-main-integration ./scripts/council-simulation-checklist.sh
```

Expected: fast-forward succeeds and the merged tree passes the checklist.

- [ ] **Step 4: Push and verify fork main**

```bash
git -C .worktrees/fork-main-integration push fork HEAD:main
git -C .worktrees/fork-main-integration fetch fork main
test "$(git -C .worktrees/fork-main-integration rev-parse HEAD)" = "$(git -C .worktrees/fork-main-integration rev-parse fork/main)"
```

Expected: fork `main` advances and local/remote SHAs match.

- [ ] **Step 5: Clean up the temporary integration worktree**

```bash
git worktree remove .worktrees/fork-main-integration
git worktree prune
git branch -d codex/fork-main-integration
```

Expected: only the temporary integration worktree/branch are removed; the feature worktree remains available.
