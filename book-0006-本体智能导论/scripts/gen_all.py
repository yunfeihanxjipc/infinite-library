# -*- coding: utf-8 -*-
"""《本体智能导论》(book-0006) 配图脚本。

运行：python scripts/gen_all.py
输出：figures/图X-Y.png （文件名严格匹配正文「图 X-Y」引用）
风格：学术概念图，统一配色，中文字体。
"""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, Circle,
                                Ellipse, Polygon, Rectangle, Wedge)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

# 统一配色
BLUE = "#2C5F8A"
LIGHT = "#E8F0F7"
GREEN = "#2E7D5B"
LGREEN = "#E6F2EA"
AMBER = "#B07D2B"
LAMBER = "#F8EFDD"
RED = "#A33B3B"
LRED = "#F6E3E3"
GRAY = "#5A5A5A"
LGRAY = "#ECECEC"
DARK = "#1A3350"
GOLD = "#C9A227"


# -------------------- 通用辅助函数 --------------------

def save(fig, name):
    """保存并关闭图像。"""
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("已生成:", name)


def new_canvas(title, xlim=(0, 12), ylim=(0, 7), figsize=(8, 5)):
    """创建统一画布并绘制标题。"""
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.text(sum(xlim) / 2, ylim[1] - 0.15, title,
            ha="center", va="top", fontsize=14, weight="bold", color=DARK)
    return fig, ax


def box(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=10, tc=DARK, lw=1.4, bold=False):
    """圆角方框。"""
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=lw, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, weight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, color=BLUE, rad=0, lw=1.5, ms=13, ls="-"):
    """带箭头连线。"""
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=ms,
        linewidth=lw, color=color, linestyle=ls,
        connectionstyle="arc3,rad=%s" % rad))


def line(ax, x1, y1, x2, y2, color=GRAY, lw=1.3, ls="-", rad=0):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-", linewidth=lw,
        color=color, linestyle=ls,
        connectionstyle="arc3,rad=%s" % rad))


def circle_node(ax, x, y, text, r=0.5, fc=LIGHT, ec=BLUE, fs=9, tc=DARK):
    ax.add_patch(Circle((x, y), r, linewidth=1.4, edgecolor=ec, facecolor=fc))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc)


def ellipse_node(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=9, tc=DARK):
    ax.add_patch(Ellipse((x, y), w, h, linewidth=1.4, edgecolor=ec, facecolor=fc))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc)


def caption(ax, x, y, text, fs=9, color=GRAY):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color)


def flow(name, title, steps, colors=None, fs=9, figsize=(8, 5), note=None):
    """横向流程/流水线图。steps 为字符串列表。"""
    n = len(steps)
    fig, ax = new_canvas(title, (0, 12), (0, 7), figsize)
    gap = 11.2 / n
    w = min(1.9, gap - 0.18)
    xs = [0.4 + i * gap for i in range(n)]
    if colors is None:
        colors = [LIGHT] * n
    for i, (s, x) in enumerate(zip(steps, xs)):
        box(ax, x, 3.0, w, 1.1, s, fc=colors[i], fs=fs, bold=True)
        if i < n - 1:
            arrow(ax, x + w + 0.02, 3.55, xs[i + 1] - 0.04, 3.55)
    if note:
        caption(ax, 6, 1.6, note)
    save(fig, name)


def ladder(name, title, levels, note=None):
    """语义之梯/层级图：levels 为 (标签, 说明) 列表，自底向上。"""
    fig, ax = new_canvas(title, (0, 12), (0, 7))
    n = len(levels)
    h = 0.8
    gap = 0.25
    total = n * h + (n - 1) * gap
    y0 = (6.3 - total) / 2
    palette = [LIGHT, LGREEN, LAMBER, LRED, LGRAY, "#EFEAF7"]
    edge = [BLUE, GREEN, AMBER, RED, GRAY, "#7A5A9A"]
    for i, (label, desc) in enumerate(levels):
        y = y0 + i * (h + gap)
        box(ax, 2.5, y, 7.0, h, "%s　%s" % (label, desc),
            fc=palette[i % len(palette)], ec=edge[i % len(edge)], fs=10.5)
        if i > 0:
            arrow(ax, 6.0, y - gap, 6.0, y + 0.02, color=GRAY, rad=0, lw=1.1, ms=9)
    if note:
        caption(ax, 6, 0.5, note)
    save(fig, name)


def radar(name, title, labels, values, colors=None):
    """雷达图。values 为 0-1 之间的数值。"""
    n = len(labels)
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111, polar=True)
    angles = [i * 2 * math.pi / n for i in range(n)]
    angles_closed = angles + [angles[0]]
    vals = values + [values[0]]
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=10, color=DARK)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels([])
    ax.set_ylim(0, 1.05)
    ax.plot(angles_closed, vals, color=BLUE, lw=2)
    ax.fill(angles_closed, vals, color=LIGHT, alpha=0.9)
    for a, v in zip(angles, values):
        ax.plot(a, v, "o", color=AMBER, ms=6)
    ax.set_title(title, fontsize=14, weight="bold", color=DARK, pad=16)
    save(fig, name)


def layer_stack(name, title, layers, note=None):
    """纵向分层架构图：layers 为 (标题, 子项) 列表，自顶向下。"""
    fig, ax = new_canvas(title, (0, 12), (0, 7))
    n = len(layers)
    h = 0.85
    gap = 0.18
    total = n * h + (n - 1) * gap
    y0 = (6.2 - total) / 2
    palette = [LIGHT, LGREEN, LAMBER, LRED, "#EFEAF7", LGRAY]
    edge = [BLUE, GREEN, AMBER, RED, "#7A5A9A", GRAY]
    for i, (label, sub) in enumerate(layers):
        y = y0 + (n - 1 - i) * (h + gap)
        box(ax, 1.5, y, 9.0, h, "%s　｜　%s" % (label, sub),
            fc=palette[i % len(palette)], ec=edge[i % len(edge)], fs=10.5)
    if note:
        caption(ax, 6, 0.4, note)
    save(fig, name)


# -------------------- 各图绘制 --------------------

def fig_1_1():
    """本体智能四层结构与语义之梯"""
    fig, ax = new_canvas("本体智能四层结构与语义之梯", (0, 12), (0, 7))
    levels = [("数据层", "记号与事实（句法）"),
              ("结构层", "三元组与模式（RDF/OWL）"),
              ("语义层", "概念、关系与推理（描述逻辑）"),
              ("智能层", "知识驱动的理解与决策")]
    ladder_data = levels
    palette = [LIGHT, LGREEN, LAMBER, LRED]
    edge = [BLUE, GREEN, AMBER, RED]
    h = 0.95; gap = 0.3; total = 4 * h + 3 * gap; y0 = (6.2 - total) / 2
    for i, (label, desc) in enumerate(ladder_data):
        y = y0 + i * (h + gap)
        box(ax, 2.0, y, 8.0, h, "%s　%s" % (label, desc),
            fc=palette[i], ec=edge[i], fs=11, bold=True)
        ax.plot([1.0, 1.6], [y + h / 2, y + h / 2], color=edge[i], lw=2)
        if i > 0:
            arrow(ax, 6.0, y - gap, 6.0, y + 0.03, color=GRAY, ms=9)
    ax.text(0.75, y0 + total / 2, "语\n义\n之\n梯", ha="center", va="center",
            fontsize=12, color=DARK, weight="bold", linespacing=1.5)
    caption(ax, 6, 0.4, "自下而上：从记号到意义；本体规范概念，推理揭示隐含结论")
    save(fig, "图1-1.png")


def fig_2_1():
    fig, ax = new_canvas("范畴、实体与属性的层次", (0, 12), (0, 7))
    box(ax, 4.5, 5.2, 3.0, 0.9, "范畴（Concept）", fc=LIGHT, ec=BLUE, fs=11, bold=True)
    for x, c in [(2.0, "实体 a"), (6.0, "实体 b"), (10.0, "实体 c")]:
        box(ax, x - 0.9, 3.2, 1.8, 0.8, c, fc=LGREEN, ec=GREEN, fs=10)
        arrow(ax, 6.0, 5.2, x, 4.0, color=GRAY)
    for x, p in [(2.0, "属性 P"), (6.0, "属性 Q"), (10.0, "属性 R")]:
        box(ax, x - 0.9, 1.3, 1.8, 0.8, p, fc=LAMBER, ec=AMBER, fs=10)
        arrow(ax, x, 3.2, x, 2.1, color=AMBER)
    caption(ax, 6, 0.4, "范畴为根、实体为叶、属性连边；划分条件见式（2-1）")
    save(fig, "图2-1.png")


def fig_3_1():
    fig, ax = new_canvas("一阶逻辑的模型论结构", (0, 12), (0, 7))
    ellipse_node(ax, 3.0, 4.5, 3.6, 1.3, "论域 D（个体集合）", fc=LIGHT, ec=BLUE)
    ellipse_node(ax, 9.0, 4.5, 3.6, 1.3, "解释函数 I", fc=LGREEN, ec=GREEN)
    box(ax, 4.5, 1.6, 3.0, 1.0, "公式集 Γ", fc=LAMBER, ec=AMBER, fs=11)
    box(ax, 8.5, 1.6, 3.0, 1.0, "满足关系 |= ", fc=LRED, ec=RED, fs=11)
    arrow(ax, 3.0, 3.85, 3.0, 2.6, color=GRAY)
    arrow(ax, 9.0, 3.85, 9.0, 2.6, color=GRAY)
    arrow(ax, 7.5, 2.1, 8.5, 2.1, color=RED)
    line(ax, 4.8, 4.5, 7.2, 4.5, color=BLUE, lw=1.8)
    caption(ax, 6, 0.5, "Γ |= φ 当且仅当所有满足 Γ 的解释 I 都满足 φ")
    save(fig, "图3-1.png")


def fig_4_1():
    fig, ax = new_canvas("ALC 概念构造算子与集合语义", (0, 12), (0, 7))
    items = [("交 (and)", "C∩D"), ("并 (or)", "C∪D"), ("非 (not)", "Δ\\C"),
             ("存在限制", "存在 R 后继"), ("全称限制", "所有 R 后继")]
    xs = [1.4, 3.6, 5.8, 8.0, 10.2]
    for i, ((op, sem), x) in enumerate(zip(items, xs)):
        box(ax, x - 0.85, 3.2, 1.7, 1.0, op, fc=LIGHT if i % 2 == 0 else LGREEN,
            ec=BLUE if i % 2 == 0 else GREEN, fs=10.5, bold=True)
        caption(ax, x, 2.6, sem, fs=9)
    caption(ax, 6, 1.4, "每个概念对应论域的一个子集；构造算子按集合运算解释（式 4-1）")
    save(fig, "图4-1.png")


def fig_5_1():
    """RDF 三元组图模型"""
    fig, ax = new_canvas("RDF 三元组图模型", (0, 12), (0, 7))
    nodes = {"阿司匹林": (2.5, 4.6), "药物": (6.0, 5.4), "治疗": (6.0, 2.6), "头痛": (9.8, 4.6)}
    for t, (x, y) in nodes.items():
        circle_node(ax, x, y, t, r=0.75, fc=LIGHT if t in ("阿司匹林", "头痛") else LGREEN,
                    ec=BLUE if t in ("阿司匹林", "头痛") else GREEN, fs=9.5)
    # 谓词边
    arrow(ax, 3.1, 4.6, 5.4, 5.2)
    caption(ax, 4.3, 5.15, "type", fs=9, color=GRAY)
    arrow(ax, 3.1, 4.2, 5.4, 3.0)
    caption(ax, 4.2, 3.2, "治疗", fs=9, color=GRAY)
    arrow(ax, 6.7, 2.9, 9.1, 4.3)
    caption(ax, 7.9, 3.1, "domain", fs=9, color=GRAY)
    caption(ax, 6, 0.6, "(主语, 谓词, 客体) 构成有向标记图；RDFS 蕴涵扩张补出隐含边")
    save(fig, "图5-1.png")


def fig_6_1():
    """OWL 子语言层级与 DL 对应"""
    fig, ax = new_canvas("OWL 子语言层级与 DL 对应", (0, 12), (0, 7))
    layers = [("OWL Full", "表达力最强，不可判定"),
              ("OWL DL", "可判定，对应描述逻辑 SROIQ(D)"),
              ("OWL Lite", "最弱，对应 SHIF(D) 子集")]
    colors = [LRED, LIGHT, LGREEN]
    edges = [RED, BLUE, GREEN]
    for i, ((label, sub), c, e) in enumerate(zip(layers, colors, edges)):
        w = 6.5 - i * 0.9
        x = (12 - w) / 2
        y = 4.6 - i * 1.5
        box(ax, x, y, w, 1.0, "%s　｜　%s" % (label, sub), fc=c, ec=e, fs=10.5)
    caption(ax, 6, 0.5, "自内而外表达力递增；DL 保证推理可判定，是工程常用子集")
    save(fig, "图6-1.png")


def fig_7_1():
    """SPARQL 图模式匹配示意"""
    fig, ax = new_canvas("SPARQL 图模式匹配示意", (0, 12), (0, 7))
    box(ax, 0.5, 4.2, 4.5, 1.6, "查询模式\n(?x, type, 药物)\n(?x, 治疗, ?y)",
        fc=LAMBER, ec=AMBER, fs=10)
    box(ax, 7.0, 4.2, 4.5, 1.6, "RDF 图 G\n三元组集合（事实）",
        fc=LIGHT, ec=BLUE, fs=10)
    arrow(ax, 5.0, 5.0, 7.0, 5.0, color=GRAY, lw=2)
    caption(ax, 6.0, 5.3, "匹配", fs=9)
    box(ax, 3.5, 1.6, 5.0, 1.2, "变量绑定 Ω\n?x→阿司匹林，?y→头痛",
        fc=LGREEN, ec=GREEN, fs=10.5)
    arrow(ax, 9.25, 4.2, 6.0, 2.8, color=GREEN)
    caption(ax, 6, 0.5, "基本图模式匹配：在 G 中寻找满足所有三元组的变量赋值")
    save(fig, "图7-1.png")


def fig_8_1():
    fig, ax = new_canvas("规则、约束与描述逻辑的结合", (0, 12), (0, 7))
    boxes = [(0.5, "SWRL 规则\n(规则层)"), (4.5, "SHACL 约束\n(验证层)"), (8.5, "DL 推理\n(本体层)")]
    for x, t in boxes:
        box(ax, x, 3.4, 3.0, 1.3, t, fc=LIGHT, ec=BLUE, fs=10.5)
    arrow(ax, 3.5, 4.05, 4.5, 4.05, color=GRAY)
    arrow(ax, 7.5, 4.05, 8.5, 4.05, color=GRAY)
    box(ax, 3.5, 1.2, 5.0, 1.1, "统一知识库（演绎 + 校验）", fc=LGREEN, ec=GREEN, fs=11, bold=True)
    arrow(ax, 2.0, 3.4, 5.0, 2.3, color=GREEN)
    arrow(ax, 10.0, 3.4, 7.0, 2.3, color=GREEN)
    caption(ax, 6, 0.4, "规则补演绎、约束保质量、DL 提供可判定的语义基础")
    save(fig, "图8-1.png")


def fig_9_1():
    flow("图9-1.png", "描述逻辑推理机体系",
         ["OWL 本体", "翻译为 DL", "Tableau 展开", "一致性检测", "分类/蕴含"],
         colors=[LIGHT, LIGHT, LGREEN, LAMBER, LGREEN], fs=9,
         note="推理机把描述逻辑知识库化为范式并判定可满足性，输出分类与蕴含结论")
    # 上面 flow 用 (0,12)x(0,7)，但流程在 y=3；重写以加说明已足够


def fig_10_1():
    flow("图10-1.png", "信息抽取流程",
         ["文本", "NER 实体", "RE 关系", "事件抽取", "归一化", "三元组"],
         colors=[LIGHT, LGREEN, LGREEN, LAMBER, LAMBER, LGREEN], fs=9,
         note="从非结构化文本逐级抽取实体、关系与事件，归一化为知识图谱三元组")


def fig_11_1():
    """知识图谱构建流水线（生命周期闭环）"""
    fig, ax = new_canvas("知识图谱构建流水线", (0, 12), (0, 7))
    steps = ["知识获取", "知识抽取", "知识融合", "知识加工", "质量评估", "更新维护"]
    xs = [0.4 + i * 1.92 for i in range(6)]
    for i, (s, x) in enumerate(zip(steps, xs)):
        box(ax, x, 3.2, 1.6, 1.0, s, fc=[LIGHT, LGREEN, LAMBER, LIGHT, LGREEN, LAMBER][i],
            ec=[BLUE, GREEN, AMBER, BLUE, GREEN, AMBER][i], fs=9, bold=True)
        if i < 5:
            arrow(ax, x + 1.62, 3.7, xs[i + 1] - 0.04, 3.7, ms=10)
    # 本体驱动反馈闭环
    box(ax, 4.5, 1.2, 3.0, 0.9, "本体驱动与反馈", fc=LRED, ec=RED, fs=10)
    arrow(ax, 2.0, 3.2, 5.0, 2.1, color=RED, rad=0.15, ms=10)
    arrow(ax, 10.0, 3.2, 7.0, 2.1, color=RED, rad=-0.15, ms=10)
    caption(ax, 6, 0.45, "六阶段生命周期；本体规范模式并驱动迭代闭环")
    save(fig, "图11-1.png")


def fig_12_1():
    """实体对齐与知识融合"""
    fig, ax = new_canvas("实体对齐与知识融合", (0, 12), (0, 7))
    box(ax, 1.2, 3.4, 3.6, 1.8, "图谱 G1\n阿司匹林 / Aspirin", fc=LIGHT, ec=BLUE, fs=10)
    box(ax, 7.2, 3.4, 3.6, 1.8, "图谱 G2\n乙酰水杨酸", fc=LIGHT, ec=BLUE, fs=10)
    for y in [4.6, 4.0]:
        line(ax, 4.8, y, 7.2, y, color=GRAY, lw=1.3, ls="--")
    caption(ax, 6.0, 4.9, "相似度计算", fs=9)
    box(ax, 4.5, 1.3, 3.0, 1.0, "融合后实体（去重）", fc=LGREEN, ec=GREEN, fs=10.5, bold=True)
    arrow(ax, 3.0, 3.4, 5.0, 2.3, color=GREEN)
    arrow(ax, 9.0, 3.4, 7.0, 2.3, color=GREEN)
    caption(ax, 6, 0.45, "对齐建立等量关系，融合消解同名异义与异名同义")
    save(fig, "图12-1.png")


def fig_13_1():
    radar("图13-1.png", "知识图谱质量维度",
          ["完整性", "正确性", "一致性", "新鲜度"], [0.85, 0.78, 0.9, 0.65])


def fig_14_1():
    """大规模图谱存储与分区"""
    fig, ax = new_canvas("大规模图谱存储与分区", (0, 12), (0, 7))
    box(ax, 0.5, 4.0, 4.0, 1.3, "三元组 (s, p, o)", fc=LIGHT, ec=BLUE, fs=11, bold=True)
    for i, idx in enumerate(["SPO", "POS", "OSP"]):
        box(ax, 5.3 + i * 2.2, 4.0, 2.0, 1.3, "%s 索引" % idx, fc=LGREEN, ec=GREEN, fs=10)
        arrow(ax, 4.5, 4.65, 5.3 + i * 2.2, 4.65, color=GRAY, ms=9)
    box(ax, 0.5, 1.6, 4.0, 1.2, "字典编码\nID 化存储", fc=LAMBER, ec=AMBER, fs=10)
    box(ax, 5.3, 1.6, 6.2, 1.2, "图分区（按连通分量 / 哈希）　→　分布式查询",
        fc=LRED, ec=RED, fs=10)
    arrow(ax, 2.5, 4.0, 2.5, 2.8, color=GRAY)
    caption(ax, 6, 0.4, "多索引加速不同查询模式；字典编码压缩存储，分区支持水平扩展")
    save(fig, "图14-1.png")


def fig_15_1():
    """前向链与后向链推理"""
    fig, ax = new_canvas("前向链与后向链推理", (0, 12), (0, 7))
    box(ax, 0.6, 4.6, 3.0, 1.0, "事实 + 规则", fc=LIGHT, ec=BLUE, fs=10)
    box(ax, 4.6, 4.6, 3.0, 1.0, "前向链\n事实驱动", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 8.6, 4.6, 3.0, 1.0, "新事实（不动点）", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 3.6, 5.1, 4.6, 5.1)
    arrow(ax, 7.6, 5.1, 8.6, 5.1)
    box(ax, 0.6, 2.0, 3.0, 1.0, "目标假设", fc=LIGHT, ec=BLUE, fs=10)
    box(ax, 4.6, 2.0, 3.0, 1.0, "后向链\n目标驱动", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 8.6, 2.0, 3.0, 1.0, "子目标回溯", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 3.6, 2.5, 4.6, 2.5)
    arrow(ax, 7.6, 2.5, 8.6, 2.5)
    caption(ax, 6, 0.6, "前向链从事实推出所有结论；后向链从目标反推所需证据")
    save(fig, "图15-1.png")


def fig_16_1():
    """知识图谱嵌入与链路预测"""
    fig, ax = new_canvas("知识图谱嵌入与链路预测", (0, 12), (0, 7))
    # 向量平移示意
    ax.arrow(2.0, 3.2, 3.0, 1.4, width=0.04, head_width=0.28,
             head_length=0.35, fc=BLUE, ec=BLUE, length_includes_head=True)
    ax.arrow(5.2, 4.7, 2.8, -1.6, width=0.04, head_width=0.28,
             head_length=0.35, fc=GREEN, ec=GREEN, length_includes_head=True)
    circle_node(ax, 1.8, 3.1, "头 h", r=0.55, fc=LIGHT, ec=BLUE)
    circle_node(ax, 5.2, 4.7, "h+r", r=0.55, fc=LGREEN, ec=GREEN)
    circle_node(ax, 8.2, 3.0, "尾 t", r=0.55, fc=LAMBER, ec=AMBER)
    caption(ax, 3.5, 4.9, "关系 r 为平移向量", fs=9, color=GRAY)
    caption(ax, 7.0, 4.1, "打分 ‖h+r−t‖", fs=9, color=GRAY)
    box(ax, 8.6, 5.2, 2.8, 1.0, "链路预测\n补全缺失三元组", fc=LRED, ec=RED, fs=9.5)
    caption(ax, 6, 0.6, "TransE：头实体加关系向量应接近尾实体，分数低者更可能成立")
    save(fig, "图16-1.png")


def fig_17_1():
    flow("图17-1.png", "规则学习流程",
         ["正例/负例", "背景知识", "ILP 搜索", "规则集", "验证评估"],
         colors=[LIGHT, LIGHT, LGREEN, LAMBER, LGREEN], fs=9.5,
         note="归纳逻辑编程从样例与背景知识中搜索覆盖正例、排除负例的规则")


def fig_18_1():
    """时序与概率知识推理"""
    fig, ax = new_canvas("时序与概率知识推理", (0, 12), (0, 7))
    ax.annotate("", xy=(11.3, 3.6), xytext=(0.7, 3.6),
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.6))
    caption(ax, 11.0, 3.0, "时间 τ", fs=9)
    intervals = [(1.5, 4.5, 2.2, "(h,r,t)@t1", LIGHT, BLUE),
                 (4.9, 8.5, 4.6, "(h,r,t)@t2", LGREEN, GREEN),
                 (8.9, 11.0, 3.0, "(h,r,t)@t3", LAMBER, AMBER)]
    for x1, x2, y, label, fc, ec in intervals:
        ax.plot([x1, x2], [y, y], color=ec, lw=6, solid_capstyle="round", alpha=0.7)
        caption(ax, (x1 + x2) / 2, y + 0.5, label, fs=8.5, color=DARK)
        caption(ax, (x1 + x2) / 2, y - 0.5, "P∈[0,1]", fs=8, color=GRAY)
    caption(ax, 6, 0.6, "事实带时间区间与概率标注；推理同时处理时序演化与不确定性")
    save(fig, "图18-1.png")


def fig_19_1():
    """常识知识表示：默认规则与非单调修正"""
    fig, ax = new_canvas("常识知识表示", (0, 12), (0, 7))
    box(ax, 0.6, 4.0, 3.4, 1.2, "默认规则\n鸟通常能飞", fc=LIGHT, ec=BLUE, fs=10)
    box(ax, 4.8, 4.0, 3.0, 1.2, "已知：企鹅是鸟", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 8.8, 4.0, 2.6, 1.2, "例外：企鹅不会飞", fc=LAMBER, ec=AMBER, fs=9.5)
    arrow(ax, 4.0, 4.6, 4.8, 4.6)
    arrow(ax, 7.8, 4.6, 8.8, 4.6)
    box(ax, 4.0, 1.3, 4.0, 1.1, "非单调修正：撤回「会飞」", fc=LRED, ec=RED, fs=10.5, bold=True)
    arrow(ax, 10.0, 4.0, 6.0, 2.4, color=RED, rad=0.1)
    caption(ax, 6, 0.4, "默认推理在新证据出现时可撤回结论，区别于经典单调逻辑")
    save(fig, "图19-1.png")


def fig_20_1():
    flow("图20-1.png", "本体工程开发流程",
         ["需求分析", "概念化", "形式化", "实现", "评估", "维护"],
         colors=[LIGHT, LGREEN, LIGHT, LGREEN, LAMBER, LRED], fs=9.5,
         note="六阶段开发方法；能力问题在评估阶段反馈，驱动本体迭代演进")


def fig_21_1():
    """本体设计模式与模块化"""
    fig, ax = new_canvas("本体设计模式与模块化", (0, 12), (0, 7))
    box(ax, 4.0, 5.2, 4.0, 0.9, "顶层本体（通用概念）", fc=LIGHT, ec=BLUE, fs=10.5)
    box(ax, 1.2, 3.5, 3.6, 0.9, "领域本体（医学）", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 7.2, 3.5, 3.6, 0.9, "领域本体（法律）", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 4.0, 1.5, 4.0, 0.9, "应用本体（复用模块）", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 5.0, 5.2, 3.0, 4.4, color=GRAY)
    arrow(ax, 7.0, 5.2, 9.0, 4.4, color=GRAY)
    arrow(ax, 3.0, 3.5, 5.0, 2.4, color=GRAY)
    arrow(ax, 9.0, 3.5, 7.0, 2.4, color=GRAY)
    caption(ax, 6, 0.4, "顶层—领域—应用三层结构；设计模式封装可复用的建模经验")
    save(fig, "图21-1.png")


def fig_22_1():
    flow("图22-1.png", "本体匹配流水线",
         ["输入本体 A/B", "预处理", "相似度计算", "映射发现", "一致性校验"],
         colors=[LIGHT, LIGHT, LGREEN, LAMBER, LGREEN], fs=9.5,
         note="按名称、结构、语义多层次计算相似度，发现并校验概念间映射")


def fig_22_2():
    """嵌入对齐的向量空间"""
    fig, ax = new_canvas("嵌入对齐的向量空间", (0, 12), (0, 7))
    # 两个分布簇
    import numpy as np
    np.random.seed(1)
    for cx, color, ec, label in [(3.0, LIGHT, BLUE, "本体 A"), (9.0, LGREEN, GREEN, "本体 B")]:
        xs = cx + np.random.randn(30) * 0.7
        ys = 3.5 + np.random.randn(30) * 0.6
        ax.scatter(xs, ys, s=28, color=color, edgecolor=ec, alpha=0.85, zorder=2)
        caption(ax, cx, 5.6, label, fs=10, color=ec)
    for i in range(4):
        y = 2.6 + i * 0.6
        arrow(ax, 3.8, y, 8.2, y, color=AMBER, rad=0.05, lw=1.2, ms=10)
    caption(ax, 6, 1.2, "对齐变换将两空间映射到同一向量空间", fs=9, color=GRAY)
    caption(ax, 6, 0.5, "对应实体在共享空间中彼此靠近，实现自动对齐")
    save(fig, "图22-2.png")


def fig_23_1():
    flow("图23-1.png", "本体变更传播流程",
         ["需求变更", "影响分析", "版本传播", "一致性检查", "发布新版本"],
         colors=[LIGHT, LAMBER, LGREEN, LRED, LGREEN], fs=9.5,
         note="变更沿依赖边传播，检查下游模块一致性后受控发布")


def fig_24_1():
    """神经—符号三分法"""
    fig, ax = new_canvas("神经—符号三分法", (0, 12), (0, 7))
    items = [("符号主义", "规则与逻辑\n可解释、可推理", LIGHT, BLUE),
             ("连接主义", "神经网络\n感知与泛化", LGREEN, GREEN),
             ("融合主义", "神经+符号\n互补协同", LAMBER, AMBER)]
    for i, (t, d, fc, ec) in enumerate(items):
        x = 0.6 + i * 4.0
        box(ax, x, 3.0, 3.4, 1.8, "%s\n%s" % (t, d), fc=fc, ec=ec, fs=10)
    caption(ax, 6, 1.2, "符号擅显式推理，神经擅隐式的感知与学习，融合取长补短")
    save(fig, "图24-1.png")


def fig_25_1():
    flow("图25-1.png", "可微前向链推理",
         ["事实（向量）", "可微规则", "软匹配", "迭代传播", "预测结果"],
         colors=[LIGHT, LGREEN, LGREEN, LAMBER, LGREEN], fs=9.5,
         note="规则以连续参数表示，前向链在向量空间可微，支持端到端学习")


def fig_26_1():
    """消息传递与规则对应"""
    fig, ax = new_canvas("消息传递与规则对应", (0, 12), (0, 7))
    for x, t in [(2.0, "实体 u"), (6.0, "关系 r"), (10.0, "实体 v")]:
        circle_node(ax, x, 4.5, t, r=0.7, fc=LIGHT, ec=BLUE, fs=10)
    arrow(ax, 2.7, 4.5, 5.3, 4.5)
    arrow(ax, 6.7, 4.5, 9.3, 4.5)
    caption(ax, 4.0, 5.2, "消息 m", fs=9, color=GRAY)
    caption(ax, 8.0, 5.2, "聚合", fs=9, color=GRAY)
    box(ax, 3.0, 1.6, 6.0, 1.0, "一轮消息传递 ≈ 一条逻辑规则的软应用",
        fc=LGREEN, ec=GREEN, fs=10.5)
    caption(ax, 6, 0.4, "图神经网络的消息传递可视为可微的规则推理")
    save(fig, "图26-1.png")


def fig_27_1():
    """知识正则示意"""
    fig, ax = new_canvas("知识正则示意", (0, 12), (0, 7))
    box(ax, 0.6, 3.4, 3.4, 1.2, "数据拟合损失\nL_data", fc=LIGHT, ec=BLUE, fs=10.5)
    box(ax, 4.5, 3.4, 3.0, 1.2, "+", fc=LGRAY, ec=GRAY, fs=14)
    box(ax, 7.8, 3.4, 3.6, 1.2, "知识正则\nL_KG", fc=LGREEN, ec=GREEN, fs=10.5)
    box(ax, 3.0, 1.3, 6.0, 1.1, "约束嵌入满足本体公理与逻辑关系", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 9.6, 3.4, 6.0, 2.4, color=GREEN, rad=0.1)
    caption(ax, 6, 0.4, "把符号知识作为正则项注入神经模型，兼顾数据与知识")
    save(fig, "图27-1.png")


def fig_28_1():
    radar("图28-1.png", "三类方法能力雷达图",
          ["表达力", "可解释", "可学习", "可判定", "数据效率"],
          [0.9, 0.85, 0.35, 0.8, 0.4])


def fig_29_1():
    """参数化知识示意"""
    fig, ax = new_canvas("参数化知识示意", (0, 12), (0, 7))
    box(ax, 0.6, 3.4, 3.4, 1.4, "知识三元组\n(h, r, t)", fc=LIGHT, ec=BLUE, fs=10.5)
    arrow(ax, 4.0, 4.1, 5.2, 4.1)
    box(ax, 5.2, 3.4, 3.6, 1.4, "神经网络权重\n（参数化）", fc=LGREEN, ec=GREEN, fs=10.5)
    arrow(ax, 8.8, 4.1, 10.0, 4.1)
    box(ax, 10.0, 3.4, 1.6, 1.4, "隐式\n知识", fc=LAMBER, ec=AMBER, fs=9.5)
    caption(ax, 6, 1.6, "知识从显式符号转为分布式参数，可被学习与微调")
    save(fig, "图29-1.png")


def fig_29_2():
    """知识编辑定位"""
    fig, ax = new_canvas("知识编辑定位", (0, 12), (0, 7))
    box(ax, 0.6, 4.6, 3.4, 1.0, "待更新事实", fc=LIGHT, ec=BLUE, fs=10.5)
    box(ax, 4.6, 4.6, 3.0, 1.0, "定位关键参数", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 8.4, 4.6, 3.0, 1.0, "局部修改权重", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 4.0, 5.1, 4.6, 5.1)
    arrow(ax, 7.6, 5.1, 8.4, 5.1)
    box(ax, 3.0, 2.0, 6.0, 1.0, "验证：更新目标知识、不影响其他知识", fc=LRED, ec=RED, fs=10)
    arrow(ax, 9.9, 4.6, 6.0, 3.0, color=RED, rad=0.1)
    caption(ax, 6, 0.5, "定位并编辑模型中承载特定知识的参数，实现精准知识更新")
    save(fig, "图29-2.png")


def fig_30_1():
    """RAG 架构"""
    fig, ax = new_canvas("RAG 架构", (0, 12), (0, 7))
    box(ax, 0.4, 4.0, 2.6, 1.2, "用户问题", fc=LIGHT, ec=BLUE, fs=10.5)
    box(ax, 3.6, 4.0, 2.8, 1.2, "向量检索\n知识库", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 7.2, 4.0, 2.6, 1.2, "增强提示\n(上下文)", fc=LAMBER, ec=AMBER, fs=10)
    box(ax, 10.2, 4.0, 1.6, 1.2, "LLM\n生成", fc=LRED, ec=RED, fs=9.5)
    arrow(ax, 3.0, 4.6, 3.6, 4.6)
    arrow(ax, 6.4, 4.6, 7.2, 4.6)
    arrow(ax, 9.8, 4.6, 10.2, 4.6)
    box(ax, 3.6, 1.6, 6.4, 1.0, "外部知识库（文档→向量索引）", fc=LGRAY, ec=GRAY, fs=10)
    arrow(ax, 5.0, 4.0, 5.0, 2.6, color=GRAY)
    caption(ax, 6, 0.4, "先检索相关知识，再连同问题送入大模型生成，缓解幻觉")
    save(fig, "图30-1.png")


def fig_31_1():
    """校准曲线"""
    fig, ax = plt.subplots(figsize=(8, 5))
    import numpy as np
    conf = np.linspace(0, 1, 20)
    acc = 0.5 * conf + 0.5 * conf ** 2  # 未校准：S 形偏离对角线
    ax.plot([0, 1], [0, 1], "--", color=GRAY, lw=1.5, label="理想校准")
    ax.plot(conf, acc, "o-", color=BLUE, lw=2, label="模型（示意）")
    ax.fill_between(conf, acc, conf, color=LIGHT, alpha=0.6)
    ax.set_xlabel("预测置信度", fontsize=11)
    ax.set_ylabel("实际正确率", fontsize=11)
    ax.set_title("校准曲线", fontsize=14, weight="bold", color=DARK)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, ls=":", alpha=0.4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    save(fig, "图31-1.png")


def fig_32_1():
    """LLM 生成知识图谱流水线"""
    fig, ax = new_canvas("LLM 生成知识图谱流水线", (0, 12), (0, 7))
    steps = ["语料输入", "LLM 抽取", "实体关系", "模式对齐", "融合入库"]
    xs = [0.6 + i * 2.35 for i in range(5)]
    for i, (s, x) in enumerate(zip(steps, xs)):
        box(ax, x, 3.4, 1.9, 1.1, s, fc=[LIGHT, LGREEN, LGREEN, LAMBER, LGREEN][i],
            ec=[BLUE, GREEN, GREEN, AMBER, GREEN][i], fs=9.5, bold=True)
        if i < 4:
            arrow(ax, x + 1.92, 3.95, xs[i + 1] - 0.04, 3.95, ms=10)
    caption(ax, 6, 1.8, "大模型承担开放抽取，本体模式约束输出结构", fs=9)
    caption(ax, 6, 1.2, "抽取结果经对齐与融合后入库，形成可用知识图谱", fs=9)
    save(fig, "图32-1.png")


def fig_33_1():
    """双向增强循环"""
    fig, ax = new_canvas("双向增强循环", (0, 12), (0, 7))
    box(ax, 3.8, 4.4, 4.4, 1.1, "大语言模型 LLM", fc=LIGHT, ec=BLUE, fs=11, bold=True)
    box(ax, 3.8, 1.6, 4.4, 1.1, "知识图谱 KG", fc=LGREEN, ec=GREEN, fs=11, bold=True)
    arrow(ax, 6.0, 4.4, 6.0, 2.7, color=GREEN, lw=2)
    arrow(ax, 8.4, 2.1, 8.4, 4.0, color=BLUE, lw=2, rad=0.0)
    caption(ax, 9.2, 3.3, "KG → LLM\n注入知识", fs=9, color=GREEN)
    caption(ax, 3.0, 3.4, "LLM → KG\n抽取/补全", fs=9, color=BLUE)
    caption(ax, 6, 0.5, "图谱为语言模型提供可验证知识，语言模型助图谱构建与补全")
    save(fig, "图33-1.png")


def fig_34_1():
    """语义搜索架构"""
    fig, ax = new_canvas("语义搜索架构", (0, 12), (0, 7))
    box(ax, 0.4, 3.6, 2.6, 1.2, "自然语言查询", fc=LIGHT, ec=BLUE, fs=10)
    box(ax, 3.6, 3.6, 2.8, 1.2, "语义解析\n(意图/实体)", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 7.0, 3.6, 2.4, 1.2, "本体推理\n扩展", fc=LAMBER, ec=AMBER, fs=10)
    box(ax, 10.0, 3.6, 1.8, 1.2, "结果\n排序", fc=LRED, ec=RED, fs=9.5)
    arrow(ax, 3.0, 4.2, 3.6, 4.2)
    arrow(ax, 6.4, 4.2, 7.0, 4.2)
    arrow(ax, 9.4, 4.2, 10.0, 4.2)
    box(ax, 3.6, 1.4, 5.8, 1.0, "知识图谱 + 向量索引", fc=LGRAY, ec=GRAY, fs=10)
    arrow(ax, 8.2, 3.6, 6.5, 2.4, color=GRAY)
    caption(ax, 6, 0.4, "超越关键词匹配：理解查询语义并借助本体推理召回相关结果")
    save(fig, "图34-1.png")


def fig_35_1():
    """疾病—药物知识图谱"""
    fig, ax = new_canvas("疾病—药物知识图谱", (0, 12), (0, 7))
    nodes = {"疾病 A": (6.0, 5.3), "药物 X": (2.8, 3.2), "药物 Y": (9.2, 3.2),
             "症状 S": (2.8, 1.6), "靶点 T": (9.2, 1.6)}
    for t, (x, y) in nodes.items():
        circle_node(ax, x, y, t, r=0.85,
                    fc=LIGHT if t.startswith("疾病") else (LGREEN if t.startswith("药物") else LAMBER),
                    ec=BLUE if t.startswith("疾病") else (GREEN if t.startswith("药物") else AMBER), fs=9.5)
    edges = [("疾病 A", "药物 X", "治疗"), ("疾病 A", "药物 Y", "治疗"),
             ("药物 X", "症状 S", "缓解"), ("药物 Y", "靶点 T", "作用于")]
    pos = nodes
    for a, b, lab in edges:
        ax.annotate("", xy=pos[b], xytext=pos[a],
                    arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4))
        mx = (pos[a][0] + pos[b][0]) / 2
        my = (pos[a][1] + pos[b][1]) / 2
        caption(ax, mx, my + 0.2, lab, fs=8, color=GRAY)
    caption(ax, 6, 0.35, "以疾病为中心连接药物、症状与靶点，支撑用药与推理")
    save(fig, "图35-1.png")


def fig_36_1():
    """企业知识图谱架构"""
    layer_stack("图36-1.png", "企业知识图谱架构",
                [("应用层", "智能问答 / 风险管控 / 决策支持"),
                 ("推理层", "规则推理 / 图算法 / 链路预测"),
                 ("知识层", "企业本体 + 实体、关系、事件"),
                 ("数据层", "业务库 / 文档 / 日志 / 外部数据")],
                note="自底向上汇聚多源数据，经本体组织后支撑上层业务应用")


def fig_37_1():
    """法律政务知识图谱"""
    fig, ax = new_canvas("法律政务知识图谱", (0, 12), (0, 7))
    center = (6.0, 3.8)
    circle_node(ax, *center, "法律知识图谱", r=1.1, fc=LIGHT, ec=BLUE, fs=10)
    satellites = [(2.4, 5.0, "法条"), (9.6, 5.0, "案例"),
                  (2.4, 2.4, "主体"), (9.6, 2.4, "事项"), (6.0, 1.0, "时间")]
    for x, y, t in satellites:
        circle_node(ax, x, y, t, r=0.7, fc=LGREEN if t not in ("时间",) else LAMBER,
                    ec=GREEN if t not in ("时间",) else AMBER, fs=9.5)
        arrow(ax, center[0] + (x - center[0]) * 0.22,
              center[1] + (y - center[1]) * 0.22,
              center[0] + (x - center[0]) * 0.75,
              center[1] + (y - center[1]) * 0.75, color=GRAY, ms=9)
    caption(ax, 6, 0.25, "以法条、案例、主体、事项与时间多维关联，支持法律检索与辅助裁判")
    save(fig, "图37-1.png")


def fig_38_1():
    """本体系统工程化工具链"""
    fig, ax = new_canvas("本体系统工程化工具链", (0, 12), (0, 7))
    steps = ["建模 (Protégé)", "存储 (三元组库)", "推理 (推理机)",
             "查询 (SPARQL)", "可视化", "版本管理"]
    xs = [0.4 + i * 1.95 for i in range(6)]
    for i, (s, x) in enumerate(zip(steps, xs)):
        box(ax, x, 3.2, 1.65, 1.1, s, fc=[LIGHT, LGREEN, LIGHT, LGREEN, LAMBER, LRED][i],
            ec=[BLUE, GREEN, BLUE, GREEN, AMBER, RED][i], fs=8.5, bold=True)
        if i < 5:
            arrow(ax, x + 1.67, 3.75, xs[i + 1] - 0.04, 3.75, ms=9)
    caption(ax, 6, 1.8, "覆盖建模、存储、推理、查询、可视化与版本管理的完整工具生态", fs=9)
    save(fig, "图38-1.png")


def fig_39_1():
    """本体与世界模型接口"""
    fig, ax = new_canvas("本体与世界模型接口", (0, 12), (0, 7))
    box(ax, 0.6, 3.2, 3.4, 1.6, "符号世界\n本体 / 概念 / 规则", fc=LIGHT, ec=BLUE, fs=10.5)
    box(ax, 8.0, 3.2, 3.4, 1.6, "神经世界\n感知 / 向量 / 预测", fc=LGREEN, ec=GREEN, fs=10.5)
    box(ax, 4.6, 3.2, 2.8, 1.6, "接口层\n接地 / 对齐\n/ 映射", fc=LAMBER, ec=AMBER, fs=9.5)
    arrow(ax, 4.0, 4.0, 4.6, 4.0)
    arrow(ax, 7.4, 4.0, 8.0, 4.0)
    caption(ax, 6, 1.6, "本体提供可解释的结构，世界模型提供对环境的预测能力")
    caption(ax, 6, 1.1, "接口把符号接地到感知，把预测抽象为概念", fs=9)
    save(fig, "图39-1.png")


def fig_40_1():
    """语义之梯的裂缝"""
    fig, ax = new_canvas("语义之梯的裂缝", (0, 12), (0, 7))
    levels = [("符号层", "形式规则清晰"), ("向量层", "分布式表示"),
              ("感知层", "信号与模式"), ("物理层", "世界与身体")]
    palette = [LIGHT, LGREEN, LAMBER, LRED]
    edge = [BLUE, GREEN, AMBER, RED]
    h = 1.0; gap = 0.25; total = 4 * h + 3 * gap; y0 = (6.2 - total) / 2
    for i, (label, desc) in enumerate(levels):
        y = y0 + i * (h + gap)
        box(ax, 2.5, y, 7.0, h, "%s　%s" % (label, desc),
            fc=palette[i], ec=edge[i], fs=10.5)
        if i > 0:
            # 裂缝：锯齿形箭头
            arrow(ax, 6.0, y - gap, 6.0, y + 0.03, color=RED, rad=0, ms=8, lw=1.2)
            caption(ax, 6.4, y - gap / 2, "裂缝", fs=8, color=RED)
    caption(ax, 6, 0.4, "符号与亚符号之间仍存在语义接地与可解释性的鸿沟")
    save(fig, "图40-1.png")


def fig_41_1():
    """全书四层结构与语义之梯总览"""
    fig, ax = new_canvas("全书四层结构与语义之梯总览", (0, 12), (0, 7))
    layers = [("基础篇", "逻辑、描述逻辑、RDF/OWL"),
              ("推理篇", "推理机、规则、概率与时序"),
              ("工程篇", "知识图谱构建、存储、质量"),
              ("智能篇", "神经符号融合、LLM+KG、世界模型")]
    palette = [LIGHT, LGREEN, LAMBER, LRED]
    edge = [BLUE, GREEN, AMBER, RED]
    h = 1.0; gap = 0.25; total = 4 * h + 3 * gap; y0 = (6.3 - total) / 2
    for i, (label, desc) in enumerate(layers):
        y = y0 + i * (h + gap)
        box(ax, 2.0, y, 8.0, h, "%s　｜　%s" % (label, desc),
            fc=palette[i], ec=edge[i], fs=10.5, bold=True)
        if i > 0:
            arrow(ax, 6.0, y - gap, 6.0, y + 0.03, color=GRAY, ms=9)
    caption(ax, 6, 0.4, "四层递进呼应语义之梯：从形式基础走向知识驱动的智能")
    save(fig, "图41-1.png")


# -------------------- 主流程 --------------------

def main():
    fig_funcs = [
        fig_1_1, fig_2_1, fig_3_1, fig_4_1, fig_5_1, fig_6_1, fig_7_1, fig_8_1,
        fig_9_1, fig_10_1, fig_11_1, fig_12_1, fig_13_1, fig_14_1, fig_15_1,
        fig_16_1, fig_17_1, fig_18_1, fig_19_1, fig_20_1, fig_21_1, fig_22_1,
        fig_22_2, fig_23_1, fig_24_1, fig_25_1, fig_26_1, fig_27_1, fig_28_1,
        fig_29_1, fig_29_2, fig_30_1, fig_31_1, fig_32_1, fig_33_1, fig_34_1,
        fig_35_1, fig_36_1, fig_37_1, fig_38_1, fig_39_1, fig_40_1, fig_41_1,
    ]
    for fn in fig_funcs:
        fn()
    print("配图生成完成，共 %d 张。" % len(fig_funcs))


if __name__ == "__main__":
    main()
