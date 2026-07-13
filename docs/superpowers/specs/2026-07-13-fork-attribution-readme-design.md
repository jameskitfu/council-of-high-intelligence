# Fork Attribution README Design

## Goal

Make the fork relationship and authorship explicit without implying that the current maintainer created the upstream project.

## Scope

Update `README.md` and `README.zh-CN.md` only.

## Presentation

Add a visible attribution notice near the top of each README, immediately after the language selector and before the header image.

English meaning:

- This repository is a fork of `0xNyk/council-of-high-intelligence`.
- The original project was created by `@0xNyk`.
- This fork is extended and maintained by `@jameskitfu`.

Chinese meaning:

- 本仓库基于 `0xNyk/council-of-high-intelligence` fork 并扩展。
- 原项目由 `@0xNyk` 创建。
- 当前 fork 由 `@jameskitfu` 维护。

Use direct GitHub links for the upstream repository, original author, and current maintainer.

## Repository Links

Change all three Quickstart clone commands in each README from the upstream repository to:

`https://github.com/jameskitfu/council-of-high-intelligence.git`

Keep the existing upstream Release, Stars, and Star History links as historical provenance for the original project.

## Cleanup

Remove the stale `Support the Project` and `支持项目` table-of-contents entries because the corresponding donation sections were already removed.

## Validation

- Both READMEs contain the upstream repository link and both author handles.
- All six Quickstart clone commands point to the fork.
- No stale support-section table-of-contents entries remain.
- English and Chinese structure stays aligned.
- Local Markdown links resolve.
- The council simulation checklist and `git diff --check` pass.
