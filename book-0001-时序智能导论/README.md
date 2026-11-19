# 《时序智能导论》 · Introduction to Time Series Intelligence

一部系统论述「时序智能」的中文学术专著：面向时间序列数据的分析、预测、建模与决策的理论、方法与工程体系。全书以「可预测性」为理论基础、以「动力学建模」为核心、以「预测—理解—决策」为脉络，把两百余年间彼此隔离的方法与学科放进同一张地图。

A Chinese-language academic monograph offering a systematic treatment of time series intelligence — the theories, methods, and engineering practice for analyzing, forecasting, modeling, and deciding over time-series data, unified by a theory of predictability, centered on dynamical modeling, and organized along the thread of *prediction – understanding – decision*.

---

## 关于本书 · About

《时序智能导论》面向时间序列、时序预测与时序智能方向的研究生、科研人员与资深工程从业者。全书以可预测性为理论基础、以动力学建模为核心、以「预测—理解—决策」为脉络，把两百余年间彼此隔离的方法与学科放进同一张地图：从 1927 年 Yule 的自回归、1970 年代 Box–Jenkins 方法学，经指数平滑、状态空间与卡尔曼滤波、GARCH，进入循环网络、卷积网络与 Transformer，抵达 2023 年以来的时序基础模型、大语言模型与时序世界模型。

全书提出并贯穿两套自建框架：四层能力体系（分析、预测、建模、决策）与五层可预测性（统计、信息论、动力学、因果、决策），据此对每一类方法追问其可预测性来源、隐含假设、突破的限制与无法逾越的理论边界。共九篇四十一章，含 216 个编号公式、50 幅配图、591 条章末参考文献与附录 A–F；以城市电网负荷为贯穿始终的统一案例，辅以金融、气象、交通、工业、医疗与零售专题案例。核心模型给出完整推导，重要论断标注文献，每一方法配带数值的算例并说明其适用边界。书稿源文件以开源方式发布，纸质版本另行出版。

*Introduction to Time Series Intelligence* is written for graduate students, researchers, and senior practitioners in time series analysis, forecasting, and time series intelligence. It places two centuries of otherwise isolated methods and disciplines on a single map: from Yule's autoregression (1927) and the Box–Jenkins methodology (1970s), through exponential smoothing, state-space models and Kalman filtering, GARCH, recurrent and convolutional networks and the Transformer, to the time-series foundation models, large language models, and time-series world models that have emerged since 2023.

Two original frameworks run throughout the book: a four-layer capability stack (analysis, forecasting, modeling, decision) and a five-layer theory of predictability (statistical, information-theoretic, dynamical, causal, decisional). Every method is examined by four questions — which layer of predictability it exploits, what assumptions it makes, which limitation of its predecessors it overcomes, and which theoretical boundary it cannot cross. The book comprises nine parts and forty-one chapters, with 216 numbered equations, 50 figures, 591 chapter-level references, and Appendices A–F. A single urban power-grid load series serves as a running case across all chapters, complemented by domain studies in finance, weather, transportation, industry, healthcare, and retail. Core models are derived in full, key claims are cited, and each method is accompanied by a worked numerical example together with its limits of applicability. The source is released as open source; a print edition is published separately.

---

## 规模 · At a Glance

| 项目 | 数量 |
|------|------|
| 篇 / 章 | 9 篇 / 41 章 |
| 编号公式 | 216 |
| 章末参考文献 | 591 |
| 配图 | 50 |
| 附录 | A–F（6 个） |
| 全稿 | `时序智能导论-全稿.md`，约 8200 行 |

资料搜集截至 **2026 年 11 月**；2025—2026 年的前沿工作多为预印本或技术报告，正文以「趋势性描述 + 原始出处」著录，引用时请以原始出处的最新版本为准。算例数值除注明出处者外均为教学示意，不代表任何真实系统的实测结果。

---

## 内容结构 · Contents

| 部分 | 内容 |
|------|------|
| 第一篇（第 1–4 章） | 随机过程、时频分析与可预测性理论 |
| 第二篇（第 5–10 章） | 预处理、特征、相似性、异常、变点与多元分析 |
| 第三篇（第 11–16 章） | 指数平滑、ARIMA、状态空间、层次调和、GARCH、贝叶斯结构时序 |
| 第四篇（第 17–25 章） | 机器学习、循环/卷积网络、Transformer、长序列与状态空间、图网络、概率生成、特殊时序 |
| 第五篇（第 26–29 章） | 时序基础模型范式、代表性模型、大语言模型与时序、能力边界 |
| 第六篇（第 30–32 章） | 世界模型、因果推断、从预测到决策 |
| 第七篇（第 33–37 章） | 控制论、动力系统、计量经济学、统计学、信号处理与信息论视角 |
| 第八篇（第 38–40 章） | 评估体系、典型应用、系统工程化 |
| 第九篇（第 41 章） | 未来展望与开放问题 |
| 附录 A–F | 数学工具包、数据集与基准、开源工具链、符号与缩略语、术语与速查索引、算例复现说明 |

---

## 仓库结构 · Repository Layout

**书稿内容（唯一真源）**

| 文件 | 用途 |
|------|------|
| `前置说明.md` | 书的前置说明：内容简介、前言、理论主线、凡例、符号表、目录 |
| `chapters/NN-短名.md` | 41 个章文件，**内容唯一真源**；章号两位零填充，保证按序拼接 |
| `附录.md` | 附录 A–F |
| `figures/图X-Y.png` | 50 幅配图原图 |
| `时序智能导论-全稿.md` | 由 `前置说明.md` + 全部章文件 + `附录.md` 拼接而成的**生成物**，供整体阅读；请勿直接修改 |
| `scripts/gen_figures.py`、`scripts/gen_diagrams.py` | 配图生成脚本（数据图、概念/架构图，matplotlib 精确绘制中文与公式） |

**撰写与协作文档**

| 文件 | 用途 |
|------|------|
| `撰写规范.md` | 书籍级撰写标准 v3：篇幅配额、七要素、验收清单、逐章规划 |
| `全书结构.md` | 结构重构规划：理论主线、目录 2.0、去重表、执行路线 |
| `插图规划.md` | 50 幅图的图号、类型、用途与生成提示词 |
| `CODEBUDDY.md` | 供协作工具阅读的项目说明与体例约定 |
| `CONTRIBUTING.md` | 贡献流程、体例约定、文献著录格式、贡献者名单 |
| `CHANGELOG.md` | 版本记录与待定事项 |
| `.gitignore` | 忽略系统与编辑器临时文件、脚本缓存、可再生中间产物 |

**入口与许可**：`README.md`（本文件）、`LICENSE`（CC BY-NC-SA 4.0）。

改内容一律改 `chapters/*.md` 或 `前置说明.md` / `附录.md`，随后重建全稿：

```bash
{ cat 前置说明.md; printf '\n\n---\n\n'; for f in chapters/*.md; do cat "$f"; printf '\n\n---\n\n'; done; cat 附录.md; } > 时序智能导论-全稿.md
```

该命令依赖零填充章号使 `chapters/*.md` 自然按 01→41 排序，章文件不要改成非补零命名。配图可分别用 `python scripts/gen_figures.py` 与 `python scripts/gen_diagrams.py` 重新生成（Python 3.14 + numpy + matplotlib 环境）。

---

## 算例复现 · Reproducing the Examples

各章带数值的算例、统一案例（城市电网负荷）与 ETT 等公开数据的使用约定，以及环境依赖、随机种子与数值容差，见**附录 F　算例复现说明**；数据集与工具链索引见附录 B、C。

---

## 如何引用 · Citation

> 韩云飞. 时序智能导论. 2026. （开源版本请以本仓库发布的版本信息与 `LICENSE` 为准）

```bibtex
@book{han2026tsi,
  author    = {韩云飞},
  title     = {时序智能导论},
  year      = {2026},
  note      = {开源书稿，见项目仓库}
}
```

---

## 参与贡献 · Contributing

欢迎勘误、文献更新、算例复现与译名建议。贡献流程、体例约定与文献著录格式见 [CONTRIBUTING.md](CONTRIBUTING.md)。本书不设固定致谢，对书稿有实质贡献者在**贡献者名单**中署名，随版本持续更新。

---

## 许可 · License

书稿源文件采用 **CC BY-NC-SA 4.0**（署名—非商业性使用—相同方式共享）开源，详见 [LICENSE](LICENSE)。纸质出版版本的版权与发行另行约定，不在本许可自动授权范围内。书中的公式、数据集、开源工具名称、机构名称及各章参考文献归属各自权利人；第三方素材可能另有许可，使用前请以原始出处为准。
