# Triad Example Questions Design

## Goal

Make the 31 predefined Triads easier to understand by adding one concrete, realistic example question for every row in both READMEs.

## Scope

Modify only the predefined-Triad tables in `README.md` and `README.zh-CN.md`.

- Add a fourth column named `Example Question` in English.
- Add a fourth column named `问题样例` in Simplified Chinese.
- Preserve all 31 Triad IDs, member combinations, row order, and rationales.
- Do not change coordinator routing, persona metadata, or execution behavior.

## Content Rules

- Each row contains one concise, standalone question without a repeated `/council` command prefix.
- Questions must describe realistic decisions or problems that the named Triad is suited to deliberate.
- Examples must be distinct rather than minor rewrites of one another.
- English and Chinese questions must have equivalent intent, while Chinese should read naturally rather than word-for-word.
- English examples end with `?`; Chinese examples end with `？`.

## Approved Examples

| Triad ID | English Example Question | 中文问题样例 |
|---|---|---|
| `architecture` | Should we split our monolith into microservices now? | 我们现在应该把单体应用拆成微服务吗？ |
| `strategy` | How should we enter a market dominated by two larger competitors? | 面对两个占主导地位的大型竞争对手，我们应该如何进入这个市场？ |
| `ethics` | Should we ship a persuasive feature that may encourage compulsive use? | 我们应该上线一个可能诱导用户沉迷的说服性功能吗？ |
| `debugging` | Why does this service fail only under production load? | 为什么这个服务只在生产负载下失败？ |
| `innovation` | How can we redesign online learning without copying existing course platforms? | 不照搬现有课程平台，我们可以怎样重新设计在线学习？ |
| `conflict` | How should two cofounders resolve a deadlock over product direction? | 两位联合创始人应该如何化解产品方向上的僵局？ |
| `complexity` | How can we simplify a workflow with too many interacting rules? | 我们如何简化一个规则过多且相互影响的工作流？ |
| `risk` | What could make this launch fail catastrophically, and how do we reduce the risk? | 什么可能导致这次发布灾难性失败，我们该如何降低风险？ |
| `shipping` | Is this product ready to release this week, or should we delay? | 这个产品本周适合发布，还是应该延期？ |
| `product` | Which feature should we build next to create the most user value? | 下一步做哪个功能能创造最大的用户价值？ |
| `founder` | Should I leave my job to work on this startup full-time? | 我应该辞职全职投入这个创业项目吗？ |
| `ai` | Which model architecture should we test for this reasoning task? | 针对这个推理任务，我们应该测试哪种模型架构？ |
| `ai-product` | How should we turn this AI prototype into a reliable paid product? | 我们应该如何把这个 AI 原型变成可靠的付费产品？ |
| `ai-safety` | What safeguards do we need before letting this agent take actions? | 在允许这个智能体自主执行操作前，我们需要哪些安全措施？ |
| `decision` | Should we hire now or preserve runway for six more months? | 我们应该现在招聘，还是把现金跑道再延长六个月？ |
| `systems` | Why does improving one team's metric make the overall system worse? | 为什么提升一个团队的指标反而让整个系统变差？ |
| `uncertainty` | How should we plan when demand could be ten times higher or lower? | 当需求可能相差十倍时，我们应该如何制定计划？ |
| `design` | How can we make this onboarding flow clearer without adding more screens? | 不增加页面的情况下，如何让这个新手引导流程更清晰？ |
| `economics` | Will this freemium model create sustainable unit economics? | 这种免费增值模式能形成可持续的单位经济模型吗？ |
| `bias` | What assumptions are distorting our belief that users want this feature? | 哪些假设扭曲了我们对“用户需要这个功能”的判断？ |
| `creative` | How can I make this video concept more original without losing clarity? | 如何让这个视频创意更具原创性，同时保持清晰？ |
| `creator` | What should my YouTube channel stand for so viewers remember it? | 我的 YouTube 频道应该代表什么，才能让观众记住？ |
| `editing` | What should I cut from this video to make the core idea land? | 为了让核心观点更有冲击力，这个视频应该删掉什么？ |
| `product-vision` | What should the complete user experience feel like three years from now? | 三年后，完整的用户体验应该给人什么感受？ |
| `launch` | How should we position and launch this product to earn early trust? | 我们应该如何定位并发布这款产品，才能尽早赢得信任？ |
| `creator-product` | How can I turn my AI engineering content into a useful product? | 如何把我的 AI 工程内容转化为真正有用的产品？ |
| `invention` | How could we solve this problem with a mechanism that does not exist yet? | 我们能否用一种尚不存在的机制解决这个问题？ |
| `prototype` | What is the smallest prototype that can test the riskiest assumption? | 能验证最大风险假设的最小原型是什么？ |
| `language-learning` | How can I improve my English listening without turning practice into memorization? | 如何提升英语听力，又不把练习变成死记硬背？ |
| `learn-in-public` | How should I document my AI learning journey without pretending to be an expert? | 我应该如何记录 AI 学习过程，同时不假装自己是专家？ |
| `english-content` | How can I make English YouTube videos that learners understand and native viewers still enjoy? | 如何制作学习者能听懂、母语观众也愿意看的英语 YouTube 视频？ |

## Table Layout

The English header becomes:

```markdown
| Domain | Triad | Rationale | Example Question |
|--------|-------|-----------|------------------|
```

The Chinese header becomes:

```markdown
| 领域 | Triad | 组合逻辑 | 问题样例 |
|------|-------|----------|----------|
```

The tables remain inside their existing collapsed `<details>` sections. No command prefix is added to individual cells so the table stays as narrow as practical.

## Validation

- Each README contains exactly 31 predefined-Triad rows and four columns per row.
- The ordered Triad ID list is identical across English and Chinese.
- The member combinations and rationale text remain unchanged.
- Every example is non-empty, unique within its language, and ends with the correct question mark.
- Existing README structure, local links, council graph checks, and `git diff --check` continue to pass.
