# Bilingual `english-content` Triad Design

## Goal

Optimize `english-content` for a creator who publishes separate English and Chinese versions of the same YouTube topic, while preserving all existing commands and council graph metadata.

## Compatibility Decision

Keep the existing Triad ID and members:

`english-content` = Krashen + Jobs + Rams

Do not rename it to `bilingual-content` and do not add a 32nd Triad. This preserves `--triad english-content`, the 31-Triad roster, persona frontmatter, and all existing integrations.

## Updated Meaning

The Triad should deliberate the complete two-edition workflow rather than assuming one English-only video:

- Krashen protects acquisition value and comprehensibility in the English edition.
- Jobs ensures each edition has a clear, audience-specific content promise rather than feeling like a mechanical translation.
- Rams keeps each edition clear, usable, and natural for its intended audience.

The editions are separate uploads of the same topic. The guidance should favor localization of script, examples, title, thumbnail, pacing, and promise instead of word-for-word translation.

## Canonical Copy

Update the rationale in `SKILL.md` and `README.md` to:

`Acquisition value + bilingual packaging + audience clarity`

Update the rationale in `README.zh-CN.md` to:

`习得价值 + 双语版本包装 + 观众清晰度`

Update the English example question to:

`How should I produce separate English and Chinese versions of the same YouTube topic so each feels native to its audience?`

Update the Chinese example question to:

`同一个 YouTube 选题应该如何分别制作英文版和中文版，才能让两类观众都觉得自然？`

## Coordinator Routing Guidance

Add the same routing guidance to `SKILL.codex.md` and `SKILL.gemini.md`, immediately after their Triads tables:

> Treat `english-content` as the route for requests about publishing separate English and Chinese editions of the same topic, including localized scripts, examples, titles, thumbnails, pacing, and content promises. Keep each edition natural for its audience instead of translating word for word.

`SKILL.md` already auto-selects from Triad domain keywords and rationales, so its updated rationale provides the matching signal without changing the execution sequence.

## Scope

Modify:

- `SKILL.md`
- `SKILL.codex.md`
- `SKILL.gemini.md`
- `README.md`
- `README.zh-CN.md`

Do not modify:

- persona files or frontmatter;
- Triad IDs, members, count, or ordering;
- profile membership;
- execution steps, voting, routing mechanics, or provider behavior;
- historical design and implementation records.

## Validation

- All five current coordinator/README surfaces retain the `english-content` ID.
- The three coordinator tables still map `english-content` to Krashen + Jobs + Rams.
- The README rationales and example questions match the canonical copy exactly.
- Codex and Gemini contain identical bilingual-version routing guidance.
- No `bilingual-content` ID is introduced.
- The exact council graph, bilingual README checks, installation dry-runs, and `git diff --check` continue to pass.
