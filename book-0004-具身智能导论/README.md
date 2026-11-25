# 《具身智能导论》 · Introduction to Embodied Intelligence

一部系统论述「具身智能」的中文学术专著：智能体通过身体与物理世界交互、在感知—认知—行动闭环中涌现智能的理论、方法与工程体系。全书以「感知—认知—行动闭环」为理论基础、以「策略学习」为核心、以「感知—理解—规划—执行」为脉络，把机器人学、控制论、计算机视觉、强化学习与基础模型中彼此隔离的具身方法放进同一张地图。

A Chinese-language academic monograph offering a systematic treatment of embodied intelligence — the theories, methods, and engineering practice by which agents develop intelligence through physical interaction, unified by the perception-cognition-action loop, centered on policy learning, and organized along the thread of *perception – understanding – planning – execution*.

---

## 关于本书 · About

《具身智能导论》面向具身智能、机器人学、强化学习、计算机视觉方向的研究生、科研人员与资深工程从业者。全书以感知—认知—行动闭环为理论基础、以策略学习为核心、以「感知—理解—规划—执行」为脉络，把两百余年间彼此隔离的方法与学科放进同一张地图：从控制论与行为主义机器人学，经概率机器人与 SLAM、模仿学习、强化学习，进入视觉—语言—动作模型（VLA）与具身基础模型。

全书提出并贯穿一套自建框架：具身智能的四层能力（感知、理解、规划、执行）与闭环原则，据此对每一个方法追问其处于闭环哪一环、隐含什么假设、突破了前一方法的什么限制、无法突破什么理论边界。共九篇四十一章，含一百余个编号公式、四十余幅配图、三百余条章末参考文献与附录 A–F；以桌面物体抓取与装配任务为贯穿案例，辅以移动导航、人形机器人、自动驾驶的专题案例。核心模型给出完整推导，重要论断标注文献，每一方法配算例并说明其适用边界。书稿源文件以开源方式发布。

---

## 规模 · At a Glance

| 项目 | 数量 |
|------|------|
| 篇 / 章 | 9 篇 / 41 章 |
| 编号公式 | 一百余 |
| 章末参考文献 | 三百余 |
| 配图 | 约 40 幅（脚本生成） |
| 附录 | A–F（6 个） |
| 全稿 | `具身智能导论-全稿.md`，由各章拼接生成 |

资料搜集截至 **2026 年 11 月**；前沿工作多为预印本，以「趋势性描述 + 原始出处」著录。算例数值除注明出处者外均为教学示意。

---

## 内容结构 · Contents

| 部分 | 内容 |
|------|------|
| 第一篇（1—4 章） | 具身认知、机器人学与控制理论基础 |
| 第二篇（5—9 章） | 感知与状态估计 |
| 第三篇（10—14 章） | 运动与控制 |
| 第四篇（15—18 章） | 模仿学习 |
| 第五篇（19—23 章） | 强化学习与操作 |
| 第六篇（24—28 章） | 视觉—语言—动作模型 |
| 第七篇（29—32 章） | 仿真与现实迁移 |
| 第八篇（33—36 章） | 评估、安全与工程 |
| 第九篇（37—41 章） | 具身通用智能与开放问题 |
| 附录 A–F | 数学工具包、环境与基准、工具链、符号、术语索引、算例复现 |

---

## 仓库结构 · Repository Layout

书稿内容（唯一真源）：`前置说明.md`、`chapters/NN-短名.md`（41 章）、`附录.md`、`figures/`、`具身智能导论-全稿.md`（拼接生成物）、`scripts/`（配图脚本）。撰写文档：`撰写规范.md`、`插图规划.md`。

重建全稿：

```bash
{ cat 前置说明.md; printf '\n\n---\n\n'; for f in chapters/*.md; do cat "$f"; printf '\n\n---\n\n'; done; cat 附录.md; } > 具身智能导论-全稿.md
```

---

## 如何引用 · Citation

> 韩云飞. 具身智能导论. 2026.

```bibtex
@book{han2026ei,
  author = {韩云飞}, title = {具身智能导论}, year = {2026}, note = {开源书稿}
}
```

---

## 许可 · License

书稿源文件采用 **CC BY-NC-SA 4.0** 开源，详见根目录 `LICENSE`。
