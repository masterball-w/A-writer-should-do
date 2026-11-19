[English](README.md) · [中文](README_zh.md)

# A-writer-should-do

给智能体用的写作技能：读一本书的全文，编译出另一套技能，用来按这本书里核实过的写法起草、改写和检查新文章。

[![Stars](https://img.shields.io/github/stars/masterball-w/A-writer-should-do?style=flat-square&logo=github)](https://github.com/masterball-w/A-writer-should-do/stargazers)
[![Tag](https://img.shields.io/github/v/tag/masterball-w/A-writer-should-do?style=flat-square&label=tag)](https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Child skills](https://img.shields.io/badge/child%20skills-8-blueviolet?style=flat-square)

本仓库是一组 `SKILL.md` 说明，供会加载技能目录的宿主使用（Cursor、Claude Code，或其他读取 `SKILL.md` 的宿主）。它不是模型，不是 Python 库，也不是一个可以单独运行的文风转换程序。仓库里的 Python 只负责把 EPUB、MOBI、AZW3 转成纯文本。

当前 git 标签是 [`v2.1.0`](https://github.com/masterball-w/A-writer-should-do/releases/tag/v2.1.0)，指向 `main`。母技能模板现在产出三个文件：`write-like-moyan` 与 `write-like-changshi` 已采用新模板，其余六个子技能仍是旧的六维度布局。见[仓库里的两套布局](#仓库里的两套布局)。

## 这是什么

母技能是 [`SKILL.md`](SKILL.md)（`name: a-writer-should-do`），里面是蒸馏步骤。把一本书的全文交给智能体，它按文本功能取样，只保留有证据的模式，写出三文件的子目录 `write-like-{作者或作品}/`。

子技能才是用来写新文章的。仓库里的八个目录是已经做好的子技能。每个子技能都写明：只依据单本书，不覆盖该作者的其他作品。

母技能自己写下的规则：

- 一本书只代表这部作品、这个时期和这种文体。同一种机制至少出现在三部跨时期作品里，才可以暂且叫做作者的稳定指纹。
- 一条规则至少要有两处同功能证据，并记录一处例外；只出现一次的现象进样本索引，不进规则。
- 新文章不得搬用原句、专名、人物、情节、独创比喻或真实经历。
- 「冷峻」「轻盈」这一类词不能当作写作指令。它们只在语言与叙述话语规则写进初稿之后，用来验收。

## 功能

母技能实际规定的内容：

- **七步蒸馏**（提取清洗之后）：判定作品边界；按功能取样；提取语言与叙述话语两层指纹；做显著性筛选与负向指纹；把规则卡分入三个文件；用 300–500 字短样校准，并做朗读、删标志词与指标对照；成稿后做 AI 味校验与最小改写。
- **导入处理。** 目录、扉页、版权页、前言、序言、后记、附录、注释等附属部分先剥离，只留正文。智能体判断是短篇集还是长篇：短篇集选 4–5 篇，每篇 2,000–4,000 字符；有目录的长篇按章取 2,000–4,000 字符连续块，章数过多时抽 8–12 章；无目录的长篇跳跃抽 6–10 块，块间留间隔。每块都是连续正文，不切成句子碎片。细读样本是 200–800 字的连续段落群，不是单段：短对话段保留原样，超过 800 字的自然段按句边界截取。
- **两层指纹，不再是四层。** 语言层记录语音与韵律、词法与词性、句法（话题-评论、意合、流水句）、标点语法、篇章衔接；叙述话语层记录人称与话语呈现、叙述者标记、情绪的语言手段、反讽的语域落差、比喻来源域、开头结尾句法。数字只描述原作，是诊断依据，不是写作配额。
- **显著性筛选。** 候选特征须过覆盖率、基线对照、区分度、位置验证四道筛：覆盖率低于 10% 段落或密度低于 1/1000 字的特征只能做可选备注或负向规则；源频率须达到同类文体基线的 2 倍。另写至少 3 条负向指纹（原书不做什么），并审计「不是……而是……」「首先/其次/最后」等 AI 高发句式，原书低频的一律进黑名单。
- **规则卡**只有一种格式：条件动作（「当……时，做……」）、源频率、生成上限、至少两处同功能证据编号、一处例外。禁止「每段至少一个 X」这类配额；硬约束只保留 3–5 条，按区分度排序。
- **AI 味校验。** 参考 `lieflat-less-ai-tone` 公开的两轮实测（629 篇对照 + 270 对同题同事实配对复测）。每个可疑特征先对源书基线：原书本来就这么写、且成稿未超源频率 2 倍的，不判 AI 味。其余按脚本可数、语义判读、人审三层检查，分 A/B/C/F/X/H 六级处置。改写遵守最小改动、信息守恒、不制造参差、结构不动、风格优先、引文不改、改后复测；X 级（正文问句、序数词小标题、「这意味着」、列表引出冒号、概括替代等）永不改。
- **不带故事层规则。** 架构、人物利益、场景状态转移、情节、母题、素材取舍，以及「死亡该怎么写」这类内容指令全部排除。每条规则必须通过换题材测试：换成无关题材后规则仍成立。
- **文件放哪里。** 子技能写到你指定的目录；没指定就先问。成稿保存为当前目录下的 `{标题}.md`；重名时追加序号，不静默覆盖。

其余六个子技能仍是较早的布局（`write-like-moyan` 与 `write-like-changshi` 已改为三文件）：

- 主文件 `SKILL.md`：Literary DNA Summary、风格总纲、加载顺序、最多五条 Common Failure Modes（错误 / 原因 / 修正）、校验清单、只作结构参照的种子文本库、边界说明。
- 六个维度文件，按顺序加载：精神模型、母题与世界观、叙事结构、语言节奏、表达技法与留白，最后是编辑校验。
- 维度 1–5 的规则标记：✅ 遵循、❌ 避免、💡 可选技法、🤖 该维度的 AI 特征规避。有的规则会写上来自原书的次数。子文件没有规定每一条 ✅ 都必须达到同一个次数。两处同功能证据加一处例外是母技能当前的规则。
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
├── SKILL.md            # 边界、总纲、硬约束、失败模式、加载顺序
├── 01-style-profile.md # 语言剖面、叙述话语、样本索引
└── 02-validation.md    # AI 黑名单、负面样本、验收清单
```

不再生成独立的 `{书名}_声纹蒸馏报告.md`，证据并入 `01-style-profile.md` 末尾的样本索引；也不再建 `_meta/` 目录。

`write-like-moyan` 与 `write-like-changshi` 是这套布局的样板。下面其余六个子技能是更早做成的。它们的文件是 `01-author-spirit.md`、`02-theme-worldview.md`、`03-narrative-mechanism.md`、`04-language-rhythm.md`、`05-expression-and-space.md`、`06-generation-editor.md`。使用这些子技能时加载这些文件；不要把它们改成新模板。

| 子目录 | 该技能写明的书 | 技能自己写明的范围 |
|---|---|---|
| `write-like-pha` | 《人生拒绝清单》，pha 著，程俐 译 | 示弱、否定式命题。语言规则包含译者的影响。 |
| `write-like-zhouguoping` | 《人生哲思录》 | 格言加随感。不包括他的学术著作。 |
| `write-like-yuhua` | 《我们生活在巨大的差距里》 | 这本散文集。不是他的小说。 |
| `write-like-yuhua-novel` | 《活着》 | 这部长篇。技能写明小说任务用本目录，不用 `write-like-yuhua`。 |
| `write-like-liuzhenyun` | 《一日三秋》 | 这本书的讲述口气。不是他的其他小说。 |
| `write-like-lijieren` | 《死水微澜》 | 这本书。不是大河三部曲的后两部。 |
| `write-like-changshi` | 《常识》，托马斯·潘恩 著，武建勋、申梦琪 译 | 中译本的论说语言。不是潘恩的英文原文。 |
| `write-like-moyan` | 《蛙》 | 莫言后期：转述、书信框架、判决悬置。已迁移到三文件模板。 |

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

宿主若支持按名字调用，也可以用 `/a-writer-should-do`。没有写保存位置时，技能要求先确认再写目录。

按这套步骤新生成的子技能，使用[两套布局](#仓库里的两套布局)里的三文件模板。

### 3. 用子技能写作

```text
用 write-like-zhouguoping 写一篇约 1500 字的随笔，
题目是：机器能写字的时代，人还在做什么。
```

六个旧子技能要求：先读 Literary DNA Summary，再按维度 1–5 写初稿，然后执行维度 6 的全部校验。`write-like-moyan` 与 `write-like-changshi` 改为：加载 `SKILL.md`，按段落功能取 `01-style-profile.md` 的剖面，成稿后用 `02-validation.md` 校验。成稿以 `{文章标题}.md` 保存到当前工作目录。母技能另外规定：同名文件追加序号，不覆盖。

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
├── references/
│   └── ai-tone-check.md     # Step 6 的 AI 味校验协议
├── write-like-pha/          # 1 个主文件 + 6 个维度文件
├── write-like-zhouguoping/  # 同上，另有一篇示例文章
├── write-like-yuhua/
├── write-like-yuhua-novel/
├── write-like-liuzhenyun/
├── write-like-lijieren/
├── write-like-changshi/     # 3 个文件：SKILL.md、剖面、校验
└── write-like-moyan/        # 3 个文件：SKILL.md、剖面、校验
```

六个子目录是主文件加上 `01` 到 `06`；`write-like-moyan` 与 `write-like-changshi` 是三文件模板。没有测试，也没有 `requirements.txt`。许可证是 MIT，见下文。

## 已知限制

下面是当前代码里的缺口，不是已经承诺的行为：

- 三文件模板目前由 `write-like-moyan` 和 `write-like-changshi` 使用；其余六个子技能仍是六维度布局与旧规则格式。
- 母技能第 3 步要求按同一文本功能统计句长分布、长短句占比、用词和标点，不得编造数字。`scripts/` 里只有电子书提取脚本。
- `extract_mobi.py` 走 `mobi` 包解包时，不把 NCX 链接映射到字符偏移，而是把第 *i* 条目录到第 *i* 个 HTML 文件的起点。EPUB 3 的 nav 解析把每条目录的层级都记成 0。
- 六个旧子技能的种子文本库引用了原书段落，并要求仿结构、不仿原句。母技能禁止把原句写进子技能。两套说法都在仓库里。
- 这里没有自动的「AI 文本检测器」。母技能 Step 6 与六个旧子技能的维度 6 都是智能体逐条核对的清单，不是分类器；检测结果只描述文本特征，不判断作者。

## 参与贡献

Bug 和功能请求使用 [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) 里的模板。欢迎修提取脚本、按所引原书校正一条规则，或把其余子技能迁移到三文件模板。提交大的技能目录之前请先读 [`CONTRIBUTING.md`](CONTRIBUTING.md)：不要提交整本仍受版权保护的书，也不要加入去除 DRM 的步骤。

## 许可证

本项目以 [MIT 许可证](LICENSE) 发布。Copyright (c) 2026 masterball-w。

MIT 许可覆盖本仓库中的技能文件、脚本和文档。子技能里引用的图书段落仍归原书版权所有。MIT 不重新许可这些引文。

## 维护者的其他项目

- [supplement-checker](https://github.com/masterball-w/supplement-checker) — 另一个智能体技能：拍一张保健品照片，再查成分研究、各地注册和价格。它不属于本仓库。
