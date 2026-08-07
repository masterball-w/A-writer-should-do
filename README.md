<div align="center">

# 📖 A-writer-should-do

**书籍写作特征蒸馏** — 从单本图书文本中系统化提取作者的全维度写作特征，<br>生成可直接调用的写作指导 Skill，内置反AI特征检测机制

[![Stars](https://img.shields.io/github/stars/masterball-w/A-writer-should-do?style=flat-square&logo=github&color=yellow)](https://github.com/masterball-w/A-writer-should-do/stargazers)
[![Forks](https://img.shields.io/github/forks/masterball-w/A-writer-should-do?style=flat-square&logo=git&color=orange)](https://github.com/masterball-w/A-writer-should-do/forks)
[![Issues](https://img.shields.io/github/issues/masterball-w/A-writer-should-do?style=flat-square&color=red)](https://github.com/masterball-w/A-writer-should-do/issues)
[![Last Commit](https://img.shields.io/github/last-commit/masterball-w/A-writer-should-do?style=flat-square&logo=git&color=blue)
](https://github.com/masterball-w/A-writer-should-do/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/masterball-w/A-writer-should-do?style=flat-square&color=green)]()
[![Languages](https://img.shields.io/github/languages/count/masterball-w/A-writer-should-do?style=flat-square&color=lightgrey)]()

![Skill](https://img.shields.io/badge/Skill-Writing%20Style%20Distillation-orange?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-000000?style=flat-square&logo=markdown&logoColor=white)
![Anti-AI](https://img.shields.io/badge/Anti--AI-Built--in%20Detection-brightgreen?style=flat-square)
![Instances](https://img.shields.io/badge/Style%20Instances-5-blueviolet?style=flat-square)

</div>

---

## 📑 目录

- [概述](#-概述)
- [母子 Skill 界定](#️-母子-skill-界定)
- [子 Skill 实例一览](#-子-skill-实例一览)
- [工作流程](#-工作流程)
- [八维度输出结构](#-八维度输出结构)
- [反AI三层机制](#️-反ai三层机制)
- [快速开始](#-快速开始)
- [文件说明](#-文件说明)
- [适用文体](#-适用文体)
- [质量保障](#-质量保障)

---

## ✨ 概述

**A-writer-should-do** 是一个写作特征蒸馏 Skill（母 Skill），用于从单本图书的完整文本或章节文本中，分层级、系统化地提取作者的全维度写作特征，随后将所有特征转化为可执行的写作指导规则，最终输出一套派生写作指导 Skill 文件集（子 Skill）。

该 Skill 遵循「宏观→中观→微观→深层」的递进顺序，通过七大核心执行原则（由整体到局部、先分类再提取、频次验证、主动降噪、文本锚定、边界声明、反AI特征优先）保证特征提取的准确性与可复用性，排除文体格式、题材要求、时代语言、译者风格等外部干扰。

> 💡 与普通风格提取工具不同，本 Skill 内置**反AI特征检测机制**：在提取作者特征的同时，同步识别作者写作中天然对抗AI生成模式的特征（如不规则句长分布、非工整的论证结构、未经打磨的粗糙用词、碎片化段落节奏等），并将这些反AI特征优先转化为硬性写作规则与 AI 典型写法黑名单，确保生成的写作指导不仅形似原作者风格，还能规避AI典型写法。

## 🏗️ 母子 Skill 界定

本仓库包含两层 Skill，须明确区分：

| 层级 | 名称 | 角色 | 说明 |
|:---:|---|---|---|
| 🏭 母 Skill | `A-writer-should-do` | 特征蒸馏方法论 | 定义提取原则、流水线、维度细则、转换法则、模板与自检清单。本身不针对特定作者，是生成子 Skill 的"工厂"。输入书籍文本，输出一套派生写作指导文件集 |
| 📄 子 Skill | `write-like-{作者}` | 派生写作指导实例 | 由母 Skill 以单本书为输入蒸馏生成，针对该作者的风格提供可执行的写作规则与种子文本库，直接用于仿写 |

- **母 Skill 不可直接用于仿写**：它只负责"从书中提取特征并生成指导规则"，不包含任何具体作者的写作规则。
- **子 Skill 由母 Skill 生成**：每输入一本新书，母 Skill 即可生成一个对应的 `write-like-{作者}` 子 Skill，各子 Skill 相互独立、平行收录于本仓库。

## 🎨 子 Skill 实例一览

| # | 子 Skill | 蒸馏来源 | 风格定位 |
|:---:|---|---|---|
| 1 | `write-like-pha` | 《人生拒绝清单》（pha 著，程俐 译） | "废柴"自嘲式言说、否定式命题、人生减负哲学 |
| 2 | `write-like-zhouguoping` | 《周国平人生哲思录》 | 冲淡平和的哲理散文、灵魂叙事 |
| 3 | `write-like-yuhua` | 《我们生活在巨大的差距里》 | 余华散文杂文：冷静的社会观察、经验叙事 |
| 4 | `write-like-yuhua-novel` | 《活着》 | 余华小说：冷峻克制、民间口语、白描死亡、黑色幽默 |
| 5 | `write-like-liuzhenyun` | 《一日三秋》 | 刘震云：以笑话写哭、日常物丈量生死、链条对话、绕圈归因 |

> 📌 同一作者的不同文体可分别蒸馏、并存使用（如 `write-like-yuhua` 与 `write-like-yuhua-novel`）：散文任务用散文版，小说任务用小说版。

## 🔄 工作流程

```
输入书籍文本（epub / mobi / azw3 电子书文件需先经步骤0脚本提取）
    │
    ▼
步骤0  源文本准备（extract_epub / extract_mobi / extract_azw3 脚本 →
        {书名}_fulltext.txt 纯正文 + {书名}_toc.txt 索引式目录）
    │
    ▼
步骤1  前置判定与边界声明（文体类型 / 文本属性 / 评估范围）
    │
    ▼
步骤2  全局锚定（核心主题 / 风格调性 / 结构范式）
    │
    ▼
步骤3  中观拆解（章节逻辑 / 篇幅密度 / 线索锚点）
    │
    ▼
步骤4  抽样精读（开篇段 + 核心段 + 过渡段 + 结尾段）
    │
    ▼
步骤5  深层提炼（人格感 / 情绪基调）
    │
    ▼
步骤5.5  反AI特征识别与标注（节奏 / 结构 / 用词 / 句式 / 质感）
    │
    ▼
步骤6  交叉校验与内部报告（频次≥3 / 原文例证 / 降噪排除 / 反AI清单）
    │
    ▼
步骤7  特征转规则 → 生成派生写作指导 Skill 文件集
    │
    ▼
步骤8  写作产出落盘（按派生 Skill 生成的文章以 {文章标题}.md 保存到当前工作目录）
    │
    ▼
输出：write-like-{作者}/  （1个主调度文件 + 8个维度指导文件）
```

## 📐 八维度输出结构

派生 Skill 以文件集形式输出，主 `SKILL.md` 规定执行顺序，八个维度各为独立文件：

| 执行顺序 | 文件 | 维度 | 职责 |
|:---:|---|---|---|
| 1 | `01-style-personality.md` | 整体写作风格与人格底色 | 确立文风基调、叙事立场、情绪底色 |
| 2 | `02-structure-layout.md` | 写作框架与谋篇布局 | 规划结构范式、起承转合、详略排布 |
| 3 | `03-theme-material.md` | 主题取向与内容选择偏好 | 确定核心母题、素材选择、取舍倾向 |
| 4 | `04-rhythm-density.md` | 叙事/论证节奏与信息密度 | 控制篇幅粒度、信息释放节奏、留白度 |
| 5 | `05-logic-texture.md` | 行文逻辑与内容肌理 | 搭建推理/叙事逻辑、句段衔接 |
| 6 | `06-word-sentence.md` | 词句习惯与语言惯性 | 约束用词偏好、句式结构、语气惯性 |
| 7 | `07-rhetoric.md` | 修辞策略与表达技法 | 选择修辞类型、意象体系、感官调度 |
| 8 | `08-cognition-value.md` | 认知模式与价值底色 | 校验思维路径、价值立场、辩证程度 |

每个维度文件包含四类规则：

| 标记 | 规则类型 | 来源 |
|:---:|---|---|
| ✅ | 遵循（硬性规则） | 频次≥3处验证通过的核心特征 |
| ❌ | 避免（排除规则） | 降噪项 |
| 💡 | 可选（局部技法） | 频次不足3次 |
| 🤖 | AI特征规避（优先级最高） | 反AI特征清单 + AI典型写法黑名单 |

每条规则附注原文例证作为示范样本。

## 🛡️ 反AI三层机制

| 层级 | 机制 | 说明 |
|:---:|---|---|
| 1️⃣ | 反AI特征识别（步骤5.5） | 从节奏、结构、用词、句式、质感五个维度扫描作者文本中天然对抗AI模式的特征 |
| 2️⃣ | 🤖规避规则与AI写法黑名单（法则6-7） | 句式（A1-A11）、用词（B1-B8）、结构（C1-C6）、质感（D1-D5）四类黑名单全局强制收录，逐条校验 |
| 3️⃣ | 人写模拟技术 + 种子文本结构参照法（法则8-9） | E1-E8 八项人写特征注入技术；种子文本库作结构范式与语感基准，内容按规则全新生成，禁止改写原文 |

> 🔍 黑名单示例：**A11「短直简」速记式描写** — 禁止"照得人脸上发青""把东西攥在手里，攥得发白"这类无过程、无细节、无叙事功能的状态派发式描写。

## 🚀 快速开始

### 用母 Skill 蒸馏新书

1. 将 `A-writer-should-do` 目录放置于当前 IDE 的 Skill 目录下
2. 提供单本图书的完整文本或章节文本；若为 epub / mobi / azw3 电子书文件，先执行 `scripts/` 下对应提取脚本（见 SKILL.md「十二、脚本使用指南」），产出 `{书名}_fulltext.txt` 与 `{书名}_toc.txt`
3. Skill 自动按流水线执行特征提取、反AI扫描与校验
4. 最终在当前 IDE 的 Skill 目录下生成一套 `write-like-{作者}/` 写作指导文件

### 用子 Skill 指导仿写

1. 将任一子 Skill（如 `write-like-yuhua-novel`）放置于当前 IDE 的 Skill 目录下
2. 调用该 Skill，要求按对应作者风格写作或校验文本
3. 子 Skill 按八维度规则与种子文本库指导仿写，并通过🤖规则规避AI典型写法
4. 成稿按母 Skill「步骤8：写作产出落盘」规则，以 `{文章标题}.md` 保存到当前工作目录

## 📁 文件说明

```
A-writer-should-do/
├── SKILL.md              # 母 Skill 完整定义（执行原则 / 流水线 / 提取细则 / 转换法则 / 模板 / 自检清单）
├── README.md             # 本说明
├── scripts/              # 配套提取脚本（步骤0：电子书转纯文本）
│   ├── extract_epub.py   # EPUB 提取（纯标准库：正文 + 索引式 TOC）
│   ├── extract_mobi.py   # MOBI 提取（mobi 包解包，回退 calibre）
│   ├── extract_azw3.py   # AZW3 提取（calibre 转 epub，回退 mobi 包）
│   └── _text_clean.py    # 共用清洗模块：去除 style/script/head 等，只保留正文
├── write-like-pha/           # 子 Skill 实例1（基于《人生拒绝清单》蒸馏生成）
│   ├── SKILL.md              # 子 Skill 主调度文件（风格总纲 / 执行顺序 / 校验清单 / 种子文本库）
│   ├── 01-style-personality.md
│   ├── 02-structure-layout.md
│   ├── 03-theme-material.md
│   ├── 04-rhythm-density.md
│   ├── 05-logic-texture.md
│   ├── 06-word-sentence.md
│   ├── 07-rhetoric.md
│   └── 08-cognition-value.md
├── write-like-zhouguoping/   # 子 Skill 实例2（基于《周国平人生哲思录》蒸馏生成，同构8+1文件）
├── write-like-yuhua/         # 子 Skill 实例3（基于《我们生活在巨大的差距里》蒸馏生成，同构8+1文件）
├── write-like-yuhua-novel/   # 子 Skill 实例4（基于《活着》蒸馏生成，同构8+1文件）
└── write-like-liuzhenyun/    # 子 Skill 实例5（基于《一日三秋》蒸馏生成，同构8+1文件）
```

## 🎯 适用文体

小说、散文、杂文、社科论述、传记等各类文体的完整书籍文本或章节文本。纯文本（txt/md）可直接输入；EPUB / MOBI / AZW3 等电子书格式由 `scripts/` 下的提取脚本转为纯文本（去除 style 等非正文元素，只保留正文与索引式 TOC）后再进入流水线。针对不同文体，Skill 内置差异化权重指引，自动调整各维度的提取深度。

## ✅ 质量保障

- **两阶段输出**：先完成内部特征分析报告（校验用），再转化为派生 Skill
- **反AI三层机制**：反AI特征识别（步骤5.5）→ 🤖规避规则与AI写法黑名单（法则6-7）→ 人写模拟技术 + 种子文本结构参照法（法则8-9）
- **四组自检清单**：分析报告自检（9.1）、派生文件集自检（9.2）、反AI特征规避自检（9.3）、种子文本结构参照自检（9.4）
- **叙事逻辑自检**：写作产出后强制执行称谓辈分、对话因果、设定一致性、时间金额四项独立校验

---

<div align="center">

**📖 从一本书，蒸馏一种文风。**

如果这个项目对你有帮助，欢迎 ⭐ Star 支持一下

</div>
