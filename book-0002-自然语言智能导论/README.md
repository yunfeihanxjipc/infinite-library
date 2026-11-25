# 《自然语言智能导论》 · Introduction to Natural Language Intelligence

一部系统论述「自然语言智能」的中文学术专著：面向自然语言的表示、理解、生成与交互的理论、方法与工程体系。全书以「意义」为理论基础、以「表示学习」为核心、以「表示—理解—生成—交互」为脉络，把七十余年间彼此隔离的语言学、统计学与神经网络方法放进同一张地图。

A Chinese-language academic monograph offering a systematic treatment of natural language intelligence — the theories, methods, and engineering practice for representing, understanding, generating, and interacting through natural language, unified by a theory of meaning, centered on representation learning, and organized along the thread of *representation – understanding – generation – interaction*.

---

## 关于本书 · About

《自然语言智能导论》面向自然语言处理、计算语言学、大语言模型方向的研究生、科研人员与资深工程从业者。全书以意义为理论基础、以表示学习为核心、以「表示—理解—生成—交互」为脉络，把七十余年间彼此隔离的方法与学科放进同一张地图：从 1957 年 Chomsky 的形式语言理论、1990 年代统计自然语言处理，经词向量、注意力、Transformer、预训练范式，抵达大语言模型、检索增强、推理模型与原生多模态语言模型。

全书提出并贯穿两套自建框架：四层能力体系（分析、理解、生成、交互）与意义的五层结构（形式、分布、组合、指称、语用），据此对每一类方法追问其意义来源、隐含假设、突破的限制与无法逾越的理论边界。共九篇四十二章，含一百零二个编号公式、四十六处配图占位、三百三十九条章末参考文献与附录 A–F；以一个贯穿全书的开放域问答系统为统一案例，辅以机器翻译、信息抽取、法律与医疗的专题案例。核心模型给出完整推导，重要论断标注文献，每一方法配带数值的算例并说明其适用边界。书稿源文件以开源方式发布，纸质版本另行出版。

*Introduction to Natural Language Intelligence* is written for graduate students, researchers, and senior practitioners in natural language processing, computational linguistics, and large language models. It places seven decades of otherwise isolated methods and disciplines on a single map: from Chomsky's formal language theory (1957) and statistical NLP (1990s), through word vectors, attention, the Transformer, and pretraining, to large language models, retrieval augmentation, reasoning models, and natively multimodal language models.

Two original frameworks run throughout the book: a four-layer capability stack (analysis, understanding, generation, interaction) and a five-layer theory of meaning (formal, distributional, compositional, referential, pragmatic). Every method is examined by four questions — which layer of meaning it exploits, what assumptions it makes, which limitation of its predecessors it overcomes, and which theoretical boundary it cannot cross. The book comprises nine parts and forty-two chapters, with over two hundred numbered equations, fifty figures, nearly six hundred chapter-level references, and Appendices A–F. A single open-domain question-answering system serves as a running case across all chapters, complemented by domain studies in machine translation, information extraction, law, and healthcare. Core models are derived in full, key claims are cited, and each method is accompanied by a worked numerical example together with its limits of applicability. The source is released as open source; a print edition is published separately.

---

## 规模 · At a Glance

| 项目 | 数量 |
|------|------|
| 篇 / 章 | 9 篇 / 42 章 |
| 编号公式 | 102 |
| 章末参考文献 | 339 |
| 配图 | 47 幅（已生成，`figures/`） |
| 附录 | A–F（6 个） |
| 全稿 | `自然语言智能导论-全稿.md`，约 6900 行，由各章拼接生成 |

资料搜集截至 **2026 年 11 月**；2025—2026 年的前沿工作多为预印本或技术报告，正文以「趋势性描述 + 原始出处」著录，引用时请以原始出处的最新版本为准。算例数值除注明出处者外均为教学示意，不代表任何真实系统的实测结果。

---

## 内容结构 · Contents

| 部分 | 内容 |
|------|------|
| 第一篇（第 1–4 章） | 形式语言、概率信息论、意义的五层框架 |
| 第二篇（第 5–9 章） | 词汇语义、静态词向量、上下文表示、词法分析、语义相似度 |
| 第三篇（第 10–14 章） | 句法理论、句法分析、语义角色、组合语义、语篇指代 |
| 第四篇（第 15–19 章） | N-gram、神经语言模型、seq2seq、机器翻译、预训练前夜 |
| 第五篇（第 20–25 章） | 注意力与 Transformer、预训练范式、微调适配、上下文学习、多语言 |
| 第六篇（第 26–31 章） | 规模化定律、代表性模型、指令微调对齐、推理、RAG、评估边界 |
| 第七篇（第 32–35 章） | 多模态语言模型、语音与语言、语言与视觉生成、跨模态统一 |
| 第八篇（第 36–39 章） | 信息抽取与知识、对话系统与智能体、系统工程、领域应用 |
| 第九篇（第 40–42 章） | 语言在智能中的角色、开放问题、结语 |
| 附录 A–F | 数学工具包、语料与基准、开源工具链、符号与缩略语、术语速查索引、算例复现 |

---

## 仓库结构 · Repository Layout

**书稿内容（唯一真源）**

| 文件 | 用途 |
|------|------|
| `前置说明.md` | 书的前置说明：内容简介、前言、理论主线、凡例、符号表、目录 |
| `chapters/NN-短名.md` | 42 个章文件，**内容唯一真源**；章号两位零填充，保证按序拼接 |
| `附录.md` | 附录 A–F |
| `figures/` | 47 幅配图原图 |
| `自然语言智能导论-全稿.md` | 由 `前置说明.md` + 全部章文件 + `附录.md` 拼接而成的**生成物**，供整体阅读；请勿直接修改 |
| `scripts/gen_figures.py`、`scripts/gen_diagrams.py` | 配图生成脚本（matplotlib 精确绘制中文与公式） |

**撰写与协作文档**

| 文件 | 用途 |
|------|------|
| `撰写规范.md` | 书籍级撰写标准：篇幅配额、七要素、验收清单、逐章规划 |

**入口与许可**：`README.md`（本文件）、根目录 `LICENSE`（CC BY-NC-SA 4.0）。

改内容一律改 `chapters/*.md` 或 `前置说明.md` / `附录.md`，随后重建全稿：

```bash
{ cat 前置说明.md; printf '\n\n---\n\n'; for f in chapters/*.md; do cat "$f"; printf '\n\n---\n\n'; done; cat 附录.md; } > 自然语言智能导论-全稿.md
```

该命令依赖零填充章号使 `chapters/*.md` 自然按 01→42 排序，章文件不要改成非补零命名。

---

## 如何引用 · Citation

> 韩云飞. 自然语言智能导论. 2026. （开源版本请以本仓库发布的版本信息与 `LICENSE` 为准）

```bibtex
@book{han2026nli,
  author    = {韩云飞},
  title     = {自然语言智能导论},
  year      = {2026},
  note      = {开源书稿，见项目仓库}
}
```

---

## 许可 · License

书稿源文件采用 **CC BY-NC-SA 4.0**（署名—非商业性使用—相同方式共享）开源，详见根目录 `LICENSE`。纸质出版版本的版权与发行另行约定，不在本许可自动授权范围内。书中的公式、数据集、开源工具名称、机构名称及各章参考文献归属各自权利人；第三方素材可能另有许可，使用前请以原始出处为准。
