# 《世界模型导论》 · Introduction to World Models

一部系统论述「世界模型」的中文学术专著：智能体学习世界内部模型、并据此预测、干预与规划的理论、方法与工程体系。全书以「Next-State Prediction」为理论基础、以「潜在动力学」为核心、以「观测—状态—动力学—规划」为脉络，把控制论、认知科学、强化学习与生成模型中彼此隔离的世界建模思想放进同一张地图。

A Chinese-language academic monograph offering a systematic treatment of world models — the theories, methods, and engineering practice by which agents learn internal models of the world to predict, intervene, and plan, unified by next-state prediction, centered on latent dynamics, and organized along the thread of *observation – state – dynamics – planning*.

---

## 关于本书 · About

《世界模型导论》面向世界模型、强化学习、具身智能、生成模型方向的研究生、科研人员与资深工程从业者。全书以 Next-State Prediction 为理论基础、以潜在动力学为核心、以「观测—状态—动力学—规划」为脉络，把两百余年间彼此隔离的世界建模思想放进同一张地图：从卡尔曼滤波与最优控制，经 POMDP、预测编码与自由能原理、World Models、Dreamer、JEPA、视频生成世界模型，抵达交互世界模型、3D 世界生成与具身世界模型。

全书提出并贯穿一套自建框架：世界模型的七要素（状态表示、状态转移、观测生成、不确定性、动作条件化、奖励/目标、基于模型的规划），据此对每一个模型追问其具备哪几个要素、隐含什么假设、突破了前一模型的什么限制、无法突破什么理论边界。共九篇四十一章，含一百余个编号公式、四十余幅配图、三百余条章末参考文献与附录 A–F；以倒立摆与推箱子机器人等物理交互任务为贯穿案例，辅以自动驾驶、天气、游戏与机器人操作的专题案例。核心模型给出完整推导，重要论断标注文献，每一方法配算例并说明其适用边界。书稿源文件以开源方式发布，纸质版本另行出版。

---

## 规模 · At a Glance

| 项目 | 数量 |
|------|------|
| 篇 / 章 | 9 篇 / 41 章 |
| 编号公式 | 一百余 |
| 章末参考文献 | 三百余 |
| 配图 | 约 40 幅（`figures/`，由脚本生成） |
| 附录 | A–F（6 个） |
| 全稿 | `世界模型导论-全稿.md`，由各章拼接生成 |

资料搜集截至 **2026 年 11 月**；2025—2026 年的前沿工作多为预印本或技术报告，正文以「趋势性描述 + 原始出处」著录。算例数值除注明出处者外均为教学示意，不代表任何真实系统的实测结果。

---

## 内容结构 · Contents

| 部分 | 内容 |
|------|------|
| 第一篇（第 1–4 章） | 状态空间、预测编码与最优控制的理论基础 |
| 第二篇（第 5–8 章） | 经典世界模型：HMM、卡尔曼、POMDP、系统辨识 |
| 第三篇（第 9–13 章） | 深度世界模型：World Models、PlaNet、Dreamer、RSSM |
| 第四篇（第 14–18 章） | 生成式世界模型：视频生成、Sora 类、3D 生成 |
| 第五篇（第 19–22 章） | 预测编码与 JEPA 路线 |
| 第六篇（第 23–27 章） | 动作条件化与交互世界模型 |
| 第七篇（第 28–31 章） | 物理与 3D 世界模型 |
| 第八篇（第 32–35 章） | 评估、局限与训练挑战 |
| 第九篇（第 36–41 章） | 世界模型与通用智能、开放问题 |
| 附录 A–F | 数学工具包、环境与基准、开源工具链、符号、术语索引、算例复现 |

---

## 仓库结构 · Repository Layout

**书稿内容（唯一真源）**

| 文件 | 用途 |
|------|------|
| `前置说明.md` | 内容简介、前言、理论主线、凡例、符号表、目录 |
| `chapters/NN-短名.md` | 41 个章文件，内容唯一真源；章号两位零填充 |
| `附录.md` | 附录 A–F |
| `figures/` | 配图原图（脚本生成） |
| `世界模型导论-全稿.md` | 由前置说明 + 章文件 + 附录拼接而成，请勿直接修改 |
| `scripts/gen_figures.py`、`scripts/gen_diagrams.py` | 配图生成脚本 |

**撰写文档**：`撰写规范.md`、`插图规划.md`。

改内容一律改 `chapters/*.md` 或 `前置说明.md` / `附录.md`，随后重建全稿：

```bash
{ cat 前置说明.md; printf '\n\n---\n\n'; for f in chapters/*.md; do cat "$f"; printf '\n\n---\n\n'; done; cat 附录.md; } > 世界模型导论-全稿.md
```

---

## 如何引用 · Citation

> 韩云飞. 世界模型导论. 2026.

```bibtex
@book{han2026wm,
  author = {韩云飞},
  title  = {世界模型导论},
  year   = {2026},
  note   = {开源书稿，见项目仓库}
}
```

---

## 许可 · License

书稿源文件采用 **CC BY-NC-SA 4.0** 开源，详见根目录 `LICENSE`。纸质出版版本的版权与发行另行约定。
