[English](README.md) · [中文](README_zh.md)

# A-writer-should-do

An agent skill that reads one book and compiles a second skill for drafting, rewriting, and checking new prose in that work's verified patterns.

[![Stars](https://img.shields.io/github/stars/masterball-w/A-writer-should-do?style=flat-square&logo=github)](https://github.com/masterball-w/A-writer-should-do/stargazers)
[![Tag](https://img.shields.io/github/v/tag/masterball-w/A-writer-should-do?style=flat-square&label=tag)](https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Child skills](https://img.shields.io/badge/child%20skills-8-blueviolet?style=flat-square)

This repository is a set of `SKILL.md` instructions for an agent host (Cursor, Claude Code, or another host that loads a skill folder). It is not a model, a Python library, or a program that restyles text by itself. The Python files only turn EPUB, MOBI, and AZW3 files into plain text.

The current git tag is [`v2.1.0`](https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0), and it points at `main`. The parent template now produces three files. `write-like-moyan` and `write-like-changshi` use it; the other six children still use the earlier six-dimension layout. See [Two layouts in this repository](#two-layouts-in-this-repository).

## What it is

The parent skill, [`SKILL.md`](SKILL.md) (`name: a-writer-should-do`), is the distillation procedure. You give the agent the full text of one book. It samples the book by function, keeps only patterns that have evidence, and writes a three-file child folder `write-like-{author-or-work}/`.

A child skill is what you load when you want new prose. The eight folders already in the repo are finished children. Each one says it was distilled from a single book, and each one says it does not cover that author's other books.

The parent skill's own rules:

- One book stands for that work, that period, and that genre. A stable author-level fingerprint needs the same mechanism in at least three works from different periods.
- A rule needs at least two pieces of same-function evidence and one recorded exception. A single instance goes into the sample index, not into a rule.
- Do not copy sentences, proper names, characters, plots, original metaphors, or real biographical episodes into new writing.
- Words such as "cold" or "light" are not instructions. They are checked only after the language and discourse rules have shaped the draft.

## Features

What the parent skill actually specifies:

- **Seven-step distillation**, after an extract-and-clean step: decide the work's boundary, sample by function, extract language and discourse fingerprints, screen for significance and write negative fingerprints, compile rule cards into three files, then calibrate with a 300–500 character sample, a read-aloud pass, a signature-word deletion check, and a metric comparison, and finally run an AI-tone check with minimal rewriting.
- **Input handling.** Front matter (TOC, title pages, copyright, prefaces, afterwords, appendices, notes) is stripped. The agent decides whether the book is a story collection or a novel: collections use 4–5 stories at 2,000–4,000 characters each; novels with a TOC take a 2,000–4,000 character block per chapter, capped at 8–12 chapters when the book runs long; novels without a TOC use 6–10 spaced continuous blocks. Every block is continuous prose, with gaps between blocks. Close-reading samples are continuous paragraph groups of 200–800 characters, not single paragraphs: short dialogue paragraphs stay as they are, and paragraphs over 800 characters are cut at sentence boundaries.
- **Two fingerprint layers, not four.** Language covers phonology and rhythm, morphology and word classes, sentence patterns (topic-comment, parataxis, clause chaining), punctuation grammar, and discourse linking. Discourse covers person and presentation, narrator markers, emotion handled through syntax, irony through register, metaphor domains, and opening/closing syntax. The numbers describe the source; they are diagnostic, not generation quotas.
- **Significance screening.** Candidates must pass four filters: coverage (at least 10% of paragraphs or 3 per 1,000 characters), baseline comparison, distinctiveness (at least twice the genre baseline), and position verification. Anything below the line becomes an optional note or a negative rule. The profile also records at least three negative fingerprints (what the source never does) and audits AI-common constructions such as "not X but Y" and "first/second/finally"; source-low patterns go on the blacklist.
- **Rule cards** use one format: a conditional action ("when X, do Y"), source frequency, a generation ceiling, at least two same-function evidence ids, and a recorded exception. Per-paragraph quotas are forbidden; only 3–5 hard rules survive, ranked by distinctiveness.
- **AI-tone check.** Based on the public two-round study behind `lieflat-less-ai-tone` (629 comparative texts plus 270 paired same-facts rewrites). Every suspicious feature is first checked against the source profile: if the book already uses it and the draft stays within twice the source rate, it is not treated as AI tone. Remaining hits pass three layers (countable, semantic, human review) and six levels (A/B/C/F/X/H). Rewrites follow minimal edit, information conservation, no manufactured unevenness, fixed structure, style reference first, no changes to quotations, and a re-test. X-level items such as body questions, ordinal subheads, "this means" restatement, list-introducing colons, and generalization are never changed.
- **No story-layer rules.** Architecture, character interests, scene state transitions, plots, motifs, material selection, and content instructions such as how to treat death are excluded. Every rule must pass a subject-swap test: replace the subject matter with something unrelated, and the rule must still hold.
- **Where files go.** The child skill goes to a directory you name; if you do not name one, the agent asks. A finished piece is saved as `{title}.md` in the working directory, and a name clash gets a numeric suffix instead of a silent overwrite.

What the six older children contain (`write-like-moyan` and `write-like-changshi` now use the three-file layout):

- A dispatcher `SKILL.md` with a Literary DNA Summary, a short style charter, the load order, up to five Common Failure Modes (`错误` / `原因` / `修正`), a checklist, a seed-text library used as structure reference, and a boundary note.
- Six dimension files, loaded in order: spirit, motifs, narrative mechanism, rhythm, technique and negative space, then a final edit.
- In dimensions 1–5, rules are marked ✅ (follow), ❌ (avoid), 💡 (optional technique), and 🤖 (AI-pattern avoidance for that dimension). A rule sometimes cites a count from the book. The child files do not define one numeric cutoff that every ✅ must meet. The two-instance-plus-one-exception rule is the parent skill's.
- Inside one child, the A1–A13 table lives only in dimension 6 (`06-generation-editor.md`): sentence patterns A1–A13, diction B1–B8, structure C1–C6, texture D1–D5, then a reality check, three edit questions (what to delete, where to pause, where to leave a gap), human-writing moves E1–E8, a narrative-logic pass, and an anti-imitation section. Dimensions 1–5 still have their own 🤖 lines. The list is a checklist for the agent, not a classifier.

Ebook extraction, which both the parent skill and the scripts implement:

| Script | Input | Dependencies | Behavior in code |
|---|---|---|---|
| `scripts/extract_epub.py` | `.epub` | Python standard library | Reads `META-INF/container.xml`, walks the OPF spine, strips non-body markup, writes plain text in spine order |
| `scripts/extract_mobi.py` | `.mobi` | `pip install mobi`, or Calibre's `ebook-convert` | Tries the `mobi` package first, then Calibre. The Calibre path converts to EPUB and reuses the EPUB script |
| `scripts/extract_azw3.py` | `.azw3` | Calibre's `ebook-convert`, or `pip install mobi` | Tries Calibre first, then the MOBI script |
| `scripts/_text_clean.py` | none (not a CLI) | standard library | Shared HTML-to-text cleaner and `h1`–`h6` heading index |

Each extractor writes two UTF-8 files next to each other:

- `{stem}_fulltext.txt` — body text
- `{stem}_toc.txt` — one entry per line: `index<TAB>indented title<TAB>character offset` into the full text

EPUB contents come from the NCX nav map, then an EPUB 3 `nav` document named `nav.xhtml`, `nav.html`, or `toc.xhtml`, then `h1`–`h6` headings if both are missing. The scripts exit with an error when the file is missing, the container has no OPF, or no body text is found. DRM-protected files are not unpacked; the MOBI and AZW3 scripts tell you to remove DRM yourself and then stop. This repository does not include DRM-removal steps.

## Two layouts in this repository

New distillations follow the parent [`SKILL.md`](SKILL.md). It tells the agent to create:

```text
write-like-{author-or-work}/
├── SKILL.md            # boundary, charter, hard constraints, failure modes, load order
├── 01-style-profile.md # language profile, discourse, sample index
└── 02-validation.md    # AI blacklist, negative samples, acceptance checklist
```

No separate distillation report is written; the evidence lives in the sample index at the end of `01-style-profile.md`. A `_meta/` sample directory is no longer used.

`write-like-moyan` and `write-like-changshi` are examples of this layout. The other six children below were built earlier. Their files are `01-author-spirit.md`, `02-theme-worldview.md`, `03-narrative-mechanism.md`, `04-language-rhythm.md`, `05-expression-and-space.md`, and `06-generation-editor.md`. Load those files when you use them; do not rename them to the new template.

| Child folder | Book named in that skill | Scope the skill itself states |
|---|---|---|
| `write-like-pha` | 《人生拒绝清单》, pha, translated by 程俐 | Self-deprecating, negative definitions. Language rules include the translator. |
| `write-like-zhouguoping` | 《人生哲思录》 | Aphorism plus informal essay. Not his academic books. |
| `write-like-yuhua` | 《我们生活在巨大的差距里》 | Yu Hua's essays in that collection. Not his novels. |
| `write-like-yuhua-novel` | 《活着》 | The novel. The skill says to use this folder, not `write-like-yuhua`, for fiction. |
| `write-like-liuzhenyun` | 《一日三秋》 | That novel's telling voice. Not his other novels. |
| `write-like-lijieren` | 《死水微澜》 | That novel. Not the later two books of the trilogy. |
| `write-like-changshi` | 《常识》, Thomas Paine, translated by 武建勋 and 申梦琪 | The Chinese translation's argumentative prose. Not Paine's English original. |
| `write-like-moyan` | 《蛙》 | Later Mo Yan: reported speech, a letter frame, suspended judgment. Migrated to the three-file template. |

The [v2.1.0 release notes](https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0) and the previous README describe a four-genre rule set (fiction, argumentative nonfiction, essay, practical writing) applied at analysis, extraction, generation, and checking. Those sections are not in `SKILL.md` or in the child files. This README does not treat them as current behavior.

## Install

Requires Git, and Python 3.8+ only when you extract an ebook. Installing a skill means copying a folder onto the agent's skill path. The parent's `name` field is `a-writer-should-do`; on Cursor the folder name should match.

```bash
git clone https://github.com/masterball-w/A-writer-should-do.git

# Cursor, user-wide. A project-local copy lives in .cursor/skills/ instead.
mkdir -p ~/.cursor/skills
cp -r A-writer-should-do ~/.cursor/skills/a-writer-should-do

# Claude Code, user-wide. A project-local copy lives in .claude/skills/ instead.
mkdir -p ~/.claude/skills
cp -r A-writer-should-do ~/.claude/skills/a-writer-should-do
```

To write with an existing child and not distill anything, copy that folder by itself:

```bash
cp -r A-writer-should-do/write-like-zhouguoping ~/.cursor/skills/
```

Optional extractors:

```bash
pip install mobi          # MOBI, and the AZW3 fallback
# Calibre provides ebook-convert, used by AZW3 first and by MOBI as a fallback
```

There is no `requirements.txt` and no installable package.

## Usage

### 1. Make plain text

`.txt` and `.md` can be passed through as they are. For an ebook, the scripts create the `-o` directory if it does not exist.

```bash
python3 scripts/extract_epub.py "$HOME/books/book.epub" -o "$HOME/books/out"
python3 scripts/extract_mobi.py "$HOME/books/book.mobi" -o "$HOME/books/out"
python3 scripts/extract_azw3.py "$HOME/books/book.azw3" -o "$HOME/books/out"
```

`-o` defaults to the input file's directory. On success the script prints the two output paths, the character count, and the number of TOC entries.

### 2. Distill with the parent skill

In the agent chat, point at the extracted text and say where the child skill should be saved:

```text
Use a-writer-should-do on ~/books/out/书名_fulltext.txt.
Use ~/books/out/书名_toc.txt as the table of contents.
Save the write-like-* folder to ~/.cursor/skills/.
```

You can also invoke it by name (`/a-writer-should-do` on hosts that work that way). If you leave the destination out, the skill says to ask before writing the folder.

A finished child from this procedure uses the three-file template in [Two layouts](#two-layouts-in-this-repository).

### 3. Write with a child skill

```text
Use write-like-zhouguoping to write an essay of about 1500 Chinese characters
on what a person still does in a time of machine-written text.
```

The six older children tell the agent to read the Literary DNA Summary first, draft with dimensions 1–5 in order, then run the whole of dimension 6. `write-like-moyan` and `write-like-changshi` instead load `SKILL.md`, take the matching profile from `01-style-profile.md`, and check with `02-validation.md`. The piece is saved as `{文章标题}.md` in the working directory. The parent skill adds: if that name exists, append a number, do not overwrite.

The same folders also describe narrower jobs: rewrite a passage, or check a draft against the checklist and the failure modes.

## Examples

The picture uses only text already stored in this repo. It is the shipped Zhou Guoping child (the older six-file layout), not a live run of the current parent template.

<p><img src="docs/images/demo.png" alt="One book, the Zhou Guoping child skill, and a short new essay" width="100%"></p>

Source of the picture: [`docs/src/demo.html`](docs/src/demo.html).

**Child skill, Literary DNA Summary** in [`write-like-zhouguoping/SKILL.md`](write-like-zhouguoping/SKILL.md) (abridged):

> Core mechanism: one-sentence aphorisms alternate with denser informal paragraphs; a claim is reversed instead of proved in a straight line; "I" enters before "we"; an abstract judgment has to land on a concrete thing.
>
> Do not: talk down to the reader, end with a moral, offer a complete plan, or use ornate adjectives.

**Piece written with that child:** [`write-like-zhouguoping/灵魂还有事可做_AI时代人生哲思.md`](write-like-zhouguoping/灵魂还有事可做_AI时代人生哲思.md) (abridged). The file header says it was written with `write-like-zhouguoping`.

> 有一回深夜，我试着让一台机器替我写一段文字。它写得很快，字句也通顺，我读完却一点也不动心。我想起从前自己写东西，为一句话想半天，删了又写，写了又删，心里倒是高兴的。
>
> 我是可以被替代的。
>
> 机器越来越像人，人越来越像机器，这两件事貌似相反，实则相通。如今人人都向机器要答案，渐渐就懒得向自己提问题了。

The single-sentence paragraph and the reversal ("貌似相反，实则相通") are the two moves named in that summary. The essay is new prose stored in the repo; it is not the source book.

## Project structure

```text
A-writer-should-do/
├── SKILL.md                 # Parent procedure (current distillation spec)
├── README.md                # This file
├── README_zh.md             # Chinese README
├── LICENSE                  # MIT License, copyright 2026 masterball-w
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .github/ISSUE_TEMPLATE/  # Bug report and feature request
├── docs/
│   ├── images/demo.png
│   └── src/demo.html
├── scripts/
│   ├── extract_epub.py
│   ├── extract_mobi.py
│   ├── extract_azw3.py
│   └── _text_clean.py
├── references/
│   └── ai-tone-check.md     # AI-tone protocol for Step 6
├── write-like-pha/          # 1 dispatcher + 6 dimension files
├── write-like-zhouguoping/  # same, plus one sample essay
├── write-like-yuhua/
├── write-like-yuhua-novel/
├── write-like-liuzhenyun/
├── write-like-lijieren/
├── write-like-changshi/     # 3 files: SKILL.md, profile, validation
└── write-like-moyan/        # 3 files: SKILL.md, profile, validation
```

Six child folders are the dispatcher plus `01` through `06`; `write-like-moyan` and `write-like-changshi` are the three-file template. There is no test suite and no `requirements.txt`. The license is MIT; see below.

## Limitations

These are gaps in the current tree, not planned behavior:

- The three-file template is used by `write-like-moyan` and `write-like-changshi`; the other six children still use the six-dimension layout and rule format.
- Step 3 of the parent skill requires sentence-length distributions, short- and long-sentence shares, vocabulary, and punctuation, measured on same-function samples and not invented. `scripts/` only contains the ebook extractors.
- `extract_mobi.py`, on the `mobi` package path, does not map NCX links to character offsets. It pairs TOC entry *i* with the start of HTML file *i*. The EPUB 3 nav parser records every entry at depth 0.
- The six older children's seed libraries quote passages from the source books and tell the agent to copy their structure, not their sentences. The parent skill forbids transferring original sentences into a child skill. Both statements are in the repo.
- Nothing here is an automated classifier of AI-written text. Step 6 of the parent skill and the older children's dimension 6 are checklists the agent applies by hand; the output describes text features, not the author.

## Contributing

Bug reports and feature requests use the templates in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/). Pull requests that fix an extractor, correct a rule against the book it cites, or migrate the remaining children to the three-file template are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before sending a large skill folder: do not commit a full copyrighted book, and do not add DRM-removal instructions.

## License

This project is released under the [MIT License](LICENSE). Copyright (c) 2026 masterball-w.

The MIT grant covers the skill files, scripts, and documentation in this repository. Passages quoted from books inside the child skills remain under those books' own copyright. MIT does not relicense those quotations.

## Maintainer's other project

- [supplement-checker](https://github.com/masterball-w/supplement-checker) — a separate agent skill: photograph a supplement, then check ingredient research, regional registration, and prices. It is not part of this repository.
