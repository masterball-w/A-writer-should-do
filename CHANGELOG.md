# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions follow the git tags. `v2.1.0` is the latest tag on `main`. `2.2.0` below is the next release; it is not tagged until that release is published. There is no `v0.1.0`.

本文件记录仓库里确实存在的行为。`v2.1.0` 是 `main` 上最新的标签。下面的 `2.2.0` 是下一次发布，打标签之前还不是 git tag。没有 `v0.1.0`。

## [Unreleased]

### Fixed

- `extract_epub.py` and `extract_mobi.py` create the `-o` output directory if it does not exist, instead of failing when they open the output file. `extract_azw3.py` gets the same behavior through them.

### 修复

- `-o` 指向的目录不存在时，`extract_epub.py` 和 `extract_mobi.py` 会自动创建它，不再在打开输出文件时失败。`extract_azw3.py` 经由这两个脚本得到同样的行为。

## [2.2.0] - 2026-10-23

Documentation release. The parent skill, the seven child skills, and the extractor scripts are unchanged.

### Added

- `LICENSE`: MIT License. Copyright (c) 2026 masterball-w.
- `README_zh.md`, and an English rewrite of `README.md`. Each file links to the other at the top. Both describe the parent skill, the seven child folders, and the extractor scripts that are in the tree.
- `CONTRIBUTING.md` (English, with a Chinese summary).
- `CHANGELOG.md`.
- GitHub issue templates for bug reports and feature requests (`.github/ISSUE_TEMPLATE/`).

### Changed

- The README no longer describes a four-genre specialization system. That system is in the previous README and in the published GitHub release notes for `v2.1.0`. It is not in `SKILL.md` or the child skills.
- Documented that the parent template (`01-world-and-material.md` … `06-generation-and-validation.md`) and the shipped children (`01-author-spirit.md` … `06-generation-editor.md`) are different layouts.

### 新增与变更

文档发布。母技能、七个子技能和提取脚本的行为没有改动。

- 新增 `LICENSE`：MIT 许可证。Copyright (c) 2026 masterball-w。
- 用英文重写 `README.md`，并新增 `README_zh.md`。两份说明顶部互相链接，都只描述仓库里的母技能、七个子目录和提取脚本。
- 新增 `CONTRIBUTING.md`（英文，附中文摘要）、`CHANGELOG.md`，以及 Bug 报告和功能请求的 Issue 模板（`.github/ISSUE_TEMPLATE/`）。
- README 写明母技能模板（`01-world-and-material.md` 至 `06-generation-and-validation.md`）和已入库子技能（`01-author-spirit.md` 至 `06-generation-editor.md`）是两套布局。
- 不再把「四类文体特化」写成现有功能。该说法出现在旧 README 和已发布的 `v2.1.0` Release 说明里，不在 `SKILL.md` 或子技能文件里。

## [2.1.0] - 2026-10-12

First tagged snapshot of the repository: a parent agent skill, seven child writing skills, and ebook-to-text scripts. Tag: `v2.1.0`. The published GitHub release of this tag also claims a four-genre rule set; those rules are not in the tagged source. The notes below follow the files.

### Added

- Parent skill `SKILL.md` (`name: a-writer-should-do`): distill one book into a child skill.
  - Boundary: one book is that work, period, and genre. An author-level fingerprint needs the same mechanism in at least three works from different periods.
  - Evidence: at least three cross-chapter instances and one counterexample for a core fingerprint. Do not copy sentences, names, characters, plots, original metaphors, or real experiences.
  - Pipeline: extract and clean; set the boundary; build a stratified sample library with `_meta/` records; extract four layers (architecture, content, language, and qi-yun as a check only); verify; compile operation cards; regression-test three 800–1500 character samples.
  - Derived folder the parent asks for: `SKILL.md`, `01-world-and-material.md`, `02-character-and-information.md`, `03-architecture-and-scene.md`, `04-voice-and-syntax.md`, `05-expression-and-space.md`, `06-generation-and-validation.md`, plus `{书名}_声纹蒸馏报告.md` in the working directory.
  - Writing protocol for a derived skill, four shared tables, and output rules: ask for a destination if none was given; save a piece as `{title}.md` and add a numeric suffix on a name clash.
- Ebook extractors in `scripts/`:
  - `extract_epub.py` uses the Python standard library. Spine order, HTML cleaned to text, TOC from NCX, then EPUB 3 nav, then headings.
  - `extract_mobi.py` tries the `mobi` package, then Calibre's `ebook-convert`.
  - `extract_azw3.py` tries Calibre first, then the MOBI script.
  - `_text_clean.py` strips non-body markup. It is not a command.
  - Outputs: `{stem}_fulltext.txt` and `{stem}_toc.txt` (`index`, tab, indented title, tab, character offset). DRM files are refused.
- Seven child skills, each from one named book, on the earlier six-dimension layout (`01-author-spirit.md` through `06-generation-editor.md`):
  - `write-like-pha` — 《人生拒绝清单》
  - `write-like-zhouguoping` — 《人生哲思录》, plus the sample essay `灵魂还有事可做_AI时代人生哲思.md`
  - `write-like-yuhua` — 《我们生活在巨大的差距里》
  - `write-like-yuhua-novel` — 《活着》
  - `write-like-liuzhenyun` — 《一日三秋》
  - `write-like-lijieren` — 《死水微澜》
  - `write-like-moyan` — 《蛙》
- Each child dispatcher has a Literary DNA Summary, failure modes, a checklist, and a seed-text library marked as structure reference. Dimension 6 holds the only copy of the agent checklist A1–A13, B1–B8, C1–C6, D1–D5, edit questions, E1–E8, and the anti-imitation section.
- `docs/images/demo.png` and `docs/src/demo.html`, illustrating the Zhou Guoping child.

### Known in this tag

- The parent filenames and the seven child filenames are not the same, and no mapping file is included.
- The language layer tells the agent to run a measurement script. That script is not in `scripts/`.
- On the `mobi` unpack path, TOC offsets are paired by index with HTML files, not by NCX link. The EPUB 3 nav parser stores depth 0 for every entry.
- `-o` must already exist. There is no automated test and no `requirements.txt`.
- There is no `LICENSE` file.

### 本标签里有什么

仓库第一次打标签时的内容：一个母技能、七个子写作技能，以及电子书转纯文本的脚本。标签名 `v2.1.0`。GitHub 上这份 Release 还写了四类文体规则；这些规则不在该标签的源文件里。下面按文件记载。

- 母技能 `SKILL.md`：把一本书蒸馏成子技能。一本书只代表该作品、时期和文体；核心指纹要有三处跨章节证据和一处反例；禁止搬用原句、专名、人物、情节、独创比喻和真实经历。
- 流程：提取并清洗、判定边界、分层样本与 `_meta/`、四层指纹（架构、内容、语言、气韵只作验收）、核验、编译操作卡、三段 800–1500 字回归。
- 母技能要求的子目录文件名是 `01-world-and-material.md` 到 `06-generation-and-validation.md`。报告为工作目录下的 `{书名}_声纹蒸馏报告.md`。成稿为 `{标题}.md`，重名追加序号。
- `scripts/`：EPUB 只用标准库；MOBI 先 `mobi` 包再 Calibre；AZW3 先 Calibre 再 MOBI。输出纯文本和带字符偏移的目录。DRM 文件不提取。
- 七个子技能仍是旧的六维文件名（`01-author-spirit.md` 至 `06-generation-editor.md`），书目见上表。维度 6 有清单 A1–A13、B1–B8、C1–C6、D1–D5 和 E1–E8。`write-like-zhouguoping` 另有一篇示例文章。
- 同标签中的已知缺口：两套文件名未统一；语言层要求的统计脚本不在 `scripts/`；MOBI 解包路径的目录偏移按序号配对；EPUB 3 nav 的层级恒为 0；`-o` 目录必须事先存在；无测试、无 `requirements.txt`、无 `LICENSE`。

[2.2.0]: https://github.com/masterball-w/A-writer-should-do/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0
