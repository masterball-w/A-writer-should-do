# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions follow the git tags. `v2.1.0` is the latest tag on `main`. `2.2.0` below is the next release; it is not tagged until that release is published. There is no `v0.1.0`.

本文件记录仓库里确实存在的行为。`v2.1.0` 是 `main` 上最新的标签。下面的 `2.2.0` 是下一次发布，打标签之前还不是 git tag。没有 `v0.1.0`。

## [Unreleased]

### Added

- Added `write-like-changshi`, a three-file skill distilled from the Chinese translation of Thomas Paine's *Common Sense*: 25 samples, an import receipt, language/discourse profiles, and a validation file.

### Fixed

- `extract_epub.py` and `extract_mobi.py` create the `-o` output directory if it does not exist, instead of failing when they open the output file. `extract_azw3.py` gets the same behavior through them.

### Changed

- Parent `SKILL.md` is now a two-layer, three-file distillation spec covering language and discourse only. Architecture, content selection, the four shared tables, `_meta/`, the separate distillation report, and the three-sample regression are removed. Rule cards now need an action, two same-function evidence ids, and one recorded exception.
- Statistics are now diagnostic only: sentence length, paragraph share, and word-frequency numbers describe the source and are no longer generation quotas. Added a voice-feel summary, 3–5 breathing-point observations, a read-aloud pass, and a signature-word deletion check.
- Removed all story-layer rules from the template and the Mo Yan sample, including content instructions about death, moral judgment, and what to leave unwritten. Rules now cover phonology, morphology, syntax, punctuation, discourse linking, register, and rhetoric only. Every rule must pass a subject-swap test. The Mo Yan profile adds Chinese-specific morphology, syntax, and discourse layers.
- Added input-handling rules: strip front matter (TOC, prefaces, afterwords, appendices), decide whether the book is a story collection or a novel, take 4–5 stories from a collection, 2,000–4,000 character blocks per chapter for a novel with a TOC (capped at 8–12 chapters), and 6–10 spaced continuous blocks for a novel without a TOC. The profile now records an import receipt with coverage. Close-reading samples are continuous paragraph groups of 200–800 characters: short paragraphs stay intact, and paragraphs over 800 characters are cut at sentence boundaries; paragraph-level metrics must come from the import corpus or full text, not from merged samples.
- `write-like-moyan` migrated to the three-file layout (`SKILL.md`, `01-style-profile.md`, `02-validation.md`). The other six children are unchanged.
- Added a significance-screening step (3.5) to the parent skill: coverage, baseline, distinctiveness, and position filters; a ban on per-paragraph quotas; at least three negative fingerprints; and an audit of AI-common constructions such as "not X but Y", "first/second/finally", and "in conclusion". Low-frequency source patterns now go on the blacklist instead of becoming recommended syntax. Calibration now includes a metric comparison: any output metric more than twice the source frequency must be revised.
- `write-like-changshi` rebuilt against the new screening rules. "Not X but Y" drops from a per-paragraph frame to a full-text maximum of one (source: 4/585 sentences, 0.68%); paragraph-final rhetorical questions drop from a rule to a negative fingerprint (source: 3/143 paragraphs, 2.1%); punctuation ceilings added (semicolon/colon 3, dash 1.5, quotes 2 per 1,000 characters); measurement kept diagnostic.
- Added Step 6, an AI-tone check after style calibration, plus `references/ai-tone-check.md`. Suspicious features are first compared with the source profile; source-level usage within twice the source rate is exempt. Remaining hits use three layers (countable, semantic, human review) and six levels (A/B/C/F/X/H), with seven minimal-rewrite principles. `write-like-changshi/02-validation.md` now embeds a compact check table. The protocol paraphrases public findings from `larashero3-dotcom/lieflat-less-ai-tone` (CC BY-NC 4.0); no code is copied.
- `README.md` and `README_zh.md` now describe both layouts and mark `write-like-moyan` as the migrated example.

### 新增

- 新增 `write-like-changshi`：从托马斯·潘恩《常识》中译本蒸馏的三文件技能，含 25 个样本、导入回执、语言/话语剖面与校验文件。

### 修复

- `-o` 指向的目录不存在时，`extract_epub.py` 和 `extract_mobi.py` 会自动创建它，不再在打开输出文件时失败。`extract_azw3.py` 经由这两个脚本得到同样的行为。

### 变更

- 母技能 `SKILL.md` 简化为两层、三文件的蒸馏规程：只提取语言与叙述话语。架构、内容取舍、四张表、`_meta/`、独立蒸馏报告和三段回归测试均已移除。规则卡改为「动作 + 两处同功能证据 + 一处例外」。
- 统计值改为只作诊断：句长、段落占比和词频只描述原作，不再作为生成配额。新增语感总述、3–5 条呼吸点、朗读检查与删标志词检查。
- 母技能与莫言样板移除全部故事层规则，包括死亡怎么写、人物该不该被审判、什么该留白等内容指令。规则只覆盖语音、词法、句法、标点、篇章衔接、语域与修辞，并须通过换题材测试。莫言剖面补充了汉语词法、句法与篇章层。
- 新增导入处理：剥离目录、前言、后记、附录等附属部分；判断短篇集或长篇；短篇集取 4–5 篇；有目录的长篇每章取 2,000–4,000 字符连续块（章数过多时抽 8–12 章）；无目录的长篇跳跃抽 6–10 块并留间隔。剖面新增导入回执与覆盖率。细读样本改为 200–800 字的连续段落群：短段保留原样，超过 800 字的自然段按句边界截取；段落级指标必须用导入语料或全文统计，不能从合并样本反推。
- `write-like-moyan` 迁移到三文件布局（`SKILL.md`、`01-style-profile.md`、`02-validation.md`）。其余六个子技能未改动。
- 母技能新增显著性筛选步骤（3.5）：覆盖率、基线、区分度、位置四道筛；禁止「每段至少一个 X」类配额；至少 3 条负向指纹；审计「不是……而是……」「首先/其次/最后」「综上所述」等 AI 高发句式。原书低频的模式改为进黑名单，不再作为推荐句式。校准增加指标对照：成稿任一指标超过源频率 2 倍即返修。
- 按新筛法重建 `write-like-changshi`：「不是……而是……」从每段框架降为全文最多 1 次（源书 4/585 句，0.68%）；段末反问从规则改为负向指纹（源书 3/143 段，2.1%）；新增标点上限（分号/冒号 3、破折号 1.5、引号 2，每千字）；统计仍只作诊断。
- 母技能新增 Step 6「AI 味校验与最小改写」，并新增 `references/ai-tone-check.md`：可疑特征先对源书基线，源书本来就有且成稿未超 2 倍的不判 AI 味；其余按脚本可数、语义判读、人审三层检查，分 A/B/C/F/X/H 六级处置，改写遵守七条最小改动原则。`write-like-changshi/02-validation.md` 内嵌精简校验表。协议只转述 `larashero3-dotcom/lieflat-less-ai-tone` 的公开研究结论（CC BY-NC 4.0），不复制代码。
- `README.md` 与 `README_zh.md` 同步说明两套布局，并标明 `write-like-moyan` 为迁移样板。

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
