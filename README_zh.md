[English](README.md) · [中文](README_zh.md)

# A-writer-should-do

给智能体用的写作技能：读一本书的全文，编译出另一套技能，用来按这本书里核实过的写法起草、改写和检查新文章。

[![Stars](https://img.shields.io/github/stars/masterball-w/A-writer-should-do?style=flat-square&logo=github)](https://github.com/masterball-w/A-writer-should-do/stargazers)
[![Tag](https://img.shields.io/github/v/tag/masterball-w/A-writer-should-do?style=flat-square&label=tag)](https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Child skills](https://img.shields.io/badge/child%20skills-7-blueviolet?style=flat-square)

本仓库是一组 `SKILL.md` 说明，供会加载技能目录的宿主使用（Cursor、Claude Code，或其他读取 `SKILL.md` 的宿主）。它不是模型，不是 Python 库，也不是一个可以单独运行的文风转换程序。仓库里的 Python 只负责把 EPUB、MOBI、AZW3 转成纯文本。

当前 git 标签是 [`v2.1.0`](https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0)，指向 `main`。母技能和仓库里的七个子技能使用的文件名并不相同。见[仓库里的两套布局](#仓库里的两套布局)。

## 这是什么

母技能是 [`SKILL.md`](SKILL.md)（`name: a-writer-should-do`），里面是蒸馏步骤。把一本书的全文交给智能体，它按文本功能取样，只保留有证据的模式，写出子目录 `write-like-{作者或作品}/`，并把报告 `{书名}_声纹蒸馏报告.md` 放在当前工作目录。

子技能才是用来写新文章的。仓库里的七个目录是已经做好的子技能。每个子技能都写明：只依据单本书，不覆盖该作者的其他作品。

母技能自己写下的规则：

- 一本书只代表这部作品、这个时期和这种文体。同一种机制至少出现在三部跨时期作品里，才可以暂且叫做作者的稳定指纹。
- 一条核心指纹至少要有三处跨章节证据，和至少一处反例。出现次数只说明值得调查，不能代替功能判断。
- 新文章不得搬用原句、专名、人物、情节、独创比喻或真实经历。
- 「冷峻」「轻盈」这一类词不能当作写作指令。它们只在架构、取材和句子行为已经写进初稿之后，用来验收。

## 功能

母技能实际规定的内容：

- **提取清洗之后的六步**：判定作品边界；建立分层样本库并登记元数据；提取四层指纹；用证据和反例核验；把指纹编译成操作卡；用三段 800–1500 字的短样做回归（日常低冲突、关系或制度高压、回忆/议论/说明密集）。
- **四层分开提取。** 架构（一个单元从什么状态进入、离开）、内容（选什么材料、详略如何）、语言（按叙述、对话、回忆、议论分别计量）、气韵（删掉标志词之后综合质感是否还在）。气韵层只做验收，不单独生成。
- **操作卡**只用一种格式：输入、步骤、可观察的输出、通过/失败条件、返工、证据编号、不适用的场景。低频现象留在报告里，不写进生成规则。
- **子技能里的四级。** A 级是动笔前加载的全局约束；B 级是每个场景选 3–5 张操作卡；C 级是当前文本功能对应的语言剖面；D 级是成稿后的校验，包括常见的 AI 失败。D 级负面样本不进入写初稿的上下文。
- **共用的四张表：** 人物利益表、场景操作卡、段落运行卡、对话行动表。对话行动表用来分析原作里已经有的连续引号对白。原作若默认转述，这张表不是生成步骤。
- **文件放哪里。** 报告留在当前工作目录。子技能写到你指定的目录；没指定就先问。成稿保存为当前目录下的 `{标题}.md`；重名时追加序号，不静默覆盖。

仓库里已有的子技能（这是较早的布局，也是磁盘上的文件）：

- 主文件 `SKILL.md`：Literary DNA Summary、风格总纲、加载顺序、最多五条 Common Failure Modes（错误 / 原因 / 修正）、校验清单、只作结构参照的种子文本库、边界说明。
- 六个维度文件，按顺序加载：精神模型、母题与世界观、叙事结构、语言节奏、表达技法与留白，最后是编辑校验。
- 维度 1–5 的规则标记：✅ 遵循、❌ 避免、💡 可选技法、🤖 该维度的 AI 特征规避。有的规则会写上来自原书的次数。子文件没有规定每一条 ✅ 都必须达到同一个次数。三处证据加一处反例是母技能的规则。
- 在同一个子技能里，A1–A13 那张表只在维度 6（`06-generation-editor.md`）：句式 A1–A13、用词 B1–B8、结构 C1–C6、质感 D1–D5，然后是真实性检查、编辑三问（删什么、哪里停、哪里留白）、人写技术 E1–E8、叙事逻辑自检、反模仿伦理。维度 1–5 仍有各自的 🤖 条目。这是给智能体逐条核对的清单，不是分类器。

电子书提取是母技能和脚本都写明的步骤：

| 脚本 | 输入 | 依赖 | 代码里的行为 |
|---|---|---|---|
| `scripts/extract_epub.py` | `.epub` | Python 标准库 | 读 `META-INF/container.xml`，按 OPF spine 顺序抽取，去掉非正文标记 |
| `scripts/extract_mobi.py` | `.mobi` | `pip install mobi`，或 Calibre 的 `ebook-convert` | 先用 `mobi` 包，失败再用 Calibre。Calibre 路径是先转成 EPUB，再调用 EPUB 脚本 |
| `scripts/extract_azw3.py` | `.azw3` | Calibre 的 `ebook-convert`，或 `pip install mobi` | 先 Calibre，再退回 MOBI 脚本 |
| `scripts/_text_clean.py` | 无（不是命令行工具） | 标准库 | 共用的 HTML 转纯文本，以及 `h1`–`h6` 标题索引 |

每个提取脚本写出两个 UTF-8 文件：

- `{文件名}_fulltext.txt` — 正文
- `{文件名}_toc.txt` — 每行一条：`序号<TAB>缩进标题<TAB>该条在正文中的字符偏移`

EPUB 的目录来源依次是 NCX navMap、名为 `nav.xhtml` / `nav.html` / `toc.xhtml` 的 EPUB 3 nav 文档，两者都没有时用 `h1`–`h6`。找不到文件、没有 OPF，或抽不出正文时，脚本以错误退出。带 DRM 的文件不会被解开；MOBI 和 AZW3 脚本会提示先自行去除 DRM，然后停止。本仓库不提供去除 DRM 的步骤。

## 仓库里的两套布局

新的蒸馏按母技能 [`SKILL.md`](SKILL.md) 执行。它要求生成：

```text
write-like-{作者或作品}/
├── SKILL.md
├── 01-world-and-material.md
├── 02-character-and-information.md
├── 03-architecture-and-scene.md
├── 04-voice-and-syntax.md
├── 05-expression-and-space.md
└── 06-generation-and-validation.md
```

分析过程中还要求把样本元数据放进 `_meta/`（JSON 或 CSV）。仓库里没有 `_meta/` 示例。

下面七个子技能是更早做成的。它们的文件是 `01-author-spirit.md`、`02-theme-worldview.md`、`03-narrative-mechanism.md`、`04-language-rhythm.md`、`05-expression-and-space.md`、`06-generation-editor.md`。使用这些子技能时加载这些文件。不要把它们改成母技能模板里的文件名；仓库里没有一张对照表。

| 子目录 | 该技能写明的书 | 技能自己写明的范围 |
|---|---|---|
| `write-like-pha` | 《人生拒绝清单》，pha 著，程俐 译 | 示弱、否定式命题。语言规则包含译者的影响。 |
| `write-like-zhouguoping` | 《人生哲思录》 | 格言加随感。不包括他的学术著作。 |
| `write-like-yuhua` | 《我们生活在巨大的差距里》 | 这本散文集。不是他的小说。 |
| `write-like-yuhua-novel` | 《活着》 | 这部长篇。技能写明小说任务用本目录，不用 `write-like-yuhua`。 |
| `write-like-liuzhenyun` | 《一日三秋》 | 这本书的讲述口气。不是他的其他小说。 |
| `write-like-lijieren` | 《死水微澜》 | 这本书。不是大河三部曲的后两部。 |
| `write-like-moyan` | 《蛙》 | 莫言后期：转述、书信框架、判决悬置。技能写明不包括《红高粱》《生死疲劳》那种密度。 |

[v2.1.0 的 Release 说明](https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0) 和旧版 README 写过一套四类文体规则（虚构、非虚构论述、散文随笔、实用），并说它贯穿分析、提取、生成、校验。这些章节不在 `SKILL.md` 里，也不在子技能文件里。本 README 不把它们当作当前行为。

## 安装

需要 Git。只有提取电子书时才需要 Python 3.8+。安装技能就是把目录复制到宿主的技能路径。母技能的 `name` 是 `a-writer-should-do`；在 Cursor 里目录名应与它一致。

```bash
git clone https://github.com/masterball-w/A-writer-should-do.git

# Cursor 用户级。项目内则放到 .cursor/skills/
mkdir -p ~/.cursor/skills
cp -r A-writer-should-do ~/.cursor/skills/a-writer-should-do

# Claude Code 用户级。项目内则放到 .claude/skills/
mkdir -p ~/.claude/skills
cp -r A-writer-should-do ~/.claude/skills/a-writer-should-do
```

只用现成的子技能写作、不做蒸馏时，单独复制那个目录：

```bash
cp -r A-writer-should-do/write-like-zhouguoping ~/.cursor/skills/
```

可选的提取依赖：

```bash
pip install mobi          # MOBI，以及 AZW3 的回退路径
# Calibre 提供 ebook-convert：AZW3 优先使用，MOBI 在 mobi 包不可用时使用
```

仓库没有 `requirements.txt`，也没有可安装的包。

## 使用

### 1. 准备纯文本

`.txt` 和 `.md` 可以直接交给技能。电子书的提取脚本会在 `-o` 指向的目录不存在时自动创建它。

```bash
python3 scripts/extract_epub.py "$HOME/books/book.epub" -o "$HOME/books/out"
python3 scripts/extract_mobi.py "$HOME/books/book.mobi" -o "$HOME/books/out"
python3 scripts/extract_azw3.py "$HOME/books/book.azw3" -o "$HOME/books/out"
```

不写 `-o` 时，输出到输入文件所在目录。成功时脚本会打印两个输出路径、正文字符数和目录条数。

### 2. 用母技能蒸馏

在对话里指出提取结果，并说明子技能保存到哪里：

```text
用 a-writer-should-do 处理 ~/books/out/书名_fulltext.txt。
目录用 ~/books/out/书名_toc.txt。
生成的 write-like-* 保存到 ~/.cursor/skills/。
```

宿主若支持按名字调用，也可以用 `/a-writer-should-do`。没有写保存位置时，技能要求先确认再写目录。报告写到当前工作目录。

按这套步骤新生成的子技能，使用[两套布局](#仓库里的两套布局)里的新文件名，不是现有七个子技能的文件名。

### 3. 用子技能写作

```text
用 write-like-zhouguoping 写一篇约 1500 字的随笔，
题目是：机器能写字的时代，人还在做什么。
```

已入库的子技能要求：先读 Literary DNA Summary，再按维度 1–5 写初稿，然后执行维度 6 的全部校验。成稿以 `{文章标题}.md` 保存到当前工作目录。母技能另外规定：同名文件追加序号，不覆盖。

这些目录也写了更小的任务：改写一段，或按校验清单和失败案例检查一篇已有的稿子。

## 示例

下图只用了仓库里已经有的文字。它对应已入库的周国平子技能（旧的六文件布局），不是当前母技能模板的一次实时运行。

<p><img src="docs/images/demo.png" alt="一本书、周国平子技能，以及一篇新的短文" width="100%"></p>

图的来源是 [`docs/src/demo.html`](docs/src/demo.html)。

**子技能 Literary DNA Summary**，摘自 [`write-like-zhouguoping/SKILL.md`](write-like-zhouguoping/SKILL.md)：

> 核心表达机制：格言短段（单句成段）与密实随感段交错；辩证翻转代替线性论证；「我」字入场再推及「我们」；抽象判断必须落回一个具象物。
>
> 生成时最需避免：俯视说教、总结升华式结尾、给出彻底解决方案、华丽辞藻与精致形容词。

**用这个子技能写的文章：** [`write-like-zhouguoping/灵魂还有事可做_AI时代人生哲思.md`](write-like-zhouguoping/灵魂还有事可做_AI时代人生哲思.md)（节选）。文件头写明它由 `write-like-zhouguoping` 写出。

> 有一回深夜，我试着让一台机器替我写一段文字。它写得很快，字句也通顺，我读完却一点也不动心。我想起从前自己写东西，为一句话想半天，删了又写，写了又删，心里倒是高兴的。
>
> 我是可以被替代的。
>
> 机器越来越像人，人越来越像机器，这两件事貌似相反，实则相通。如今人人都向机器要答案，渐渐就懒得向自己提问题了。

单句成段，以及「貌似相反，实则相通」这种翻转，就是上面摘要里点名的两种做法。这篇是仓库里的新文章，不是原书。

## 项目结构

```text
A-writer-should-do/
├── SKILL.md                 # 母技能（当前蒸馏规程）
├── README.md                # 英文说明
├── README_zh.md             # 本文件
├── LICENSE                  # MIT 许可证，版权人 masterball-w，2026
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .github/ISSUE_TEMPLATE/  # Bug 报告与功能请求
├── docs/
│   ├── images/demo.png
│   └── src/demo.html
├── scripts/
│   ├── extract_epub.py
│   ├── extract_mobi.py
│   ├── extract_azw3.py
│   └── _text_clean.py
├── write-like-pha/          # 1 个主文件 + 6 个维度文件
├── write-like-zhouguoping/  # 同上，另有一篇示例文章
├── write-like-yuhua/
├── write-like-yuhua-novel/
├── write-like-liuzhenyun/
├── write-like-lijieren/
└── write-like-moyan/
```

每个子目录都是主文件加上 `01` 到 `06`。没有测试，也没有 `requirements.txt`。许可证是 MIT，见下文。

## 已知限制

下面是当前代码里的缺口，不是已经承诺的行为：

- 母技能模板和七个子技能的文件名、章节组织和规则格式都不一样。
- 母技能第 3 步要求用脚本、按同一文本功能统计句长分位数、短句（≤15 字）占比、长句（≥50 字）占比、用词和标点，并且不准凭经验编造数字。`scripts/` 里只有电子书提取脚本。
- `extract_mobi.py` 走 `mobi` 包解包时，不把 NCX 链接映射到字符偏移，而是把第 *i* 条目录到第 *i* 个 HTML 文件的起点。EPUB 3 的 nav 解析把每条目录的层级都记成 0。
- 子技能的种子文本库引用了原书段落，并要求仿结构、不仿原句。母技能禁止把原句写进子技能。两套说法都在仓库里。
- 这里没有自动的「AI 文本检测器」。维度 6 是智能体逐条核对的清单。

## 参与贡献

Bug 和功能请求使用 [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) 里的模板。欢迎修提取脚本、按所引原书校正一条规则，或把母技能模板和子技能收成同一套布局。提交大的技能目录之前请先读 [`CONTRIBUTING.md`](CONTRIBUTING.md)：不要提交整本仍受版权保护的书，也不要加入去除 DRM 的步骤。

## 许可证

本项目以 [MIT 许可证](LICENSE) 发布。Copyright (c) 2026 masterball-w。

MIT 许可覆盖本仓库中的技能文件、脚本和文档。子技能里引用的图书段落仍归原书版权所有。MIT 不重新许可这些引文。

## 维护者的其他项目

- [supplement-checker](https://github.com/masterball-w/supplement-checker) — 另一个智能体技能：拍一张保健品照片，再查成分研究、各地注册和价格。它不属于本仓库。
