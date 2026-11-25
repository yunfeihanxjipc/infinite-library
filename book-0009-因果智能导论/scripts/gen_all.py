# -*- coding: utf-8 -*-
"""《因果智能导论》(book-0009) 配图脚本。
运行：python scripts/gen_all.py
作用：按正文引用的 51 个图号绘制学术风格概念图，输出到 figures/图X-Y.png。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Polygon
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

# 统一配色
BLUE = "#2C5F8A"
GREEN = "#2E7D5B"
AMBER = "#B07D2B"
RED = "#A33B3B"
LBLUE = "#E8F0F7"
LGREEN = "#E6F2EA"
LAMBER = "#F8EFDD"
LRED = "#F6E4E4"
GRAY = "#5A5A5A"
DARK = "#1A3350"
DASH = "#888888"


# ---------------- 通用辅助函数 ----------------
def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("已生成:", name)


def new(title, xlim=(0, 12), ylim=(0, 7)):
    """创建画布并写标题（学术风格）。"""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.text((xlim[0] + xlim[1]) / 2, ylim[1] - 0.18, title,
            ha="center", va="top", fontsize=13, weight="bold", color=DARK)
    return fig, ax


def box(ax, x, y, w, h, text, fc=LBLUE, ec=BLUE, fs=9.5, tc=DARK, lw=1.2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=lw, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc)


def node(ax, x, y, text, color=BLUE, r=0.42, fs=11, dashed=False, text_color="white"):
    ax.add_patch(Circle((x, y), r, facecolor="white" if dashed else color,
                        edgecolor=color, linewidth=1.6,
                        linestyle="--" if dashed else "-"))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=color if dashed else text_color, weight="bold")


def arrow(ax, x1, y1, x2, y2, color=BLUE, rad=0, lw=1.5, ms=13, dashed=False, ls="-"):
    ls_final = "--" if dashed else ls
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=ms,
        linewidth=lw, linestyle=ls_final, color=color,
        connectionstyle="arc3,rad=%s" % rad))


def edge(ax, p1, p2, color=BLUE, rad=0, lw=1.5, dashed=False, label=None, lp=None):
    """在两个节点中心之间画箭头，自动缩短到圆周。"""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dist = (dx * dx + dy * dy) ** 0.5
    r = 0.42
    if dist > 0:
        sx, sy = x1 + dx / dist * r, y1 + dy / dist * r
        ex, ey = x2 - dx / dist * r, y2 - dy / dist * r
    else:
        sx, sy, ex, ey = x1, y1, x2, y2
    arrow(ax, sx, sy, ex, ey, color=color, rad=rad, lw=lw, dashed=dashed)
    if label:
        lx, ly = lp if lp else ((x1 + x2) / 2, (y1 + y2) / 2)
        ax.text(lx, ly, label, ha="center", va="center", fontsize=9,
                color=color,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))


def note(ax, x, y, text, color=GRAY, fs=9.5, ha="center", bbox=True):
    kw = dict(ha=ha, va="center", fontsize=fs, color=color)
    if bbox:
        kw["bbox"] = dict(boxstyle="round,pad=0.25", fc="white", ec=color, alpha=0.9)
    ax.text(x, y, text, **kw)


def flow(ax, steps, y=3.0, h=0.9, w=None, colors=None, gap=0.15):
    """横向流程：steps 为字符串列表。"""
    if w is None:
        w = 11.2 / len(steps) - gap
    if colors is None:
        colors = [LBLUE] * len(steps)
    xs = [0.4 + i * (w + gap) for i in range(len(steps))]
    for s, x, c in zip(steps, xs, colors):
        ec = BLUE if c == LBLUE else (GREEN if c == LGREEN else AMBER)
        box(ax, x, y, w, h, s, fc=c, ec=ec, fs=9)
    for i in range(len(steps) - 1):
        arrow(ax, xs[i] + w + 0.01, y + h / 2, xs[i + 1] - 0.03, y + h / 2)
    return xs, w


def vflow(ax, steps, x=2.0, y0=5.5, dy=1.0, w=3.0, h=0.7, colors=None):
    """纵向流程。"""
    if colors is None:
        colors = [LBLUE] * len(steps)
    ys = [y0 - i * dy for i in range(len(steps))]
    for s, yy, c in zip(steps, ys, colors):
        ec = BLUE if c == LBLUE else (GREEN if c == LGREEN else AMBER)
        box(ax, x, yy - h / 2, w, h, s, fc=c, ec=ec, fs=9)
    for i in range(len(steps) - 1):
        arrow(ax, x + w / 2, ys[i] - h / 2 - 0.01, x + w / 2, ys[i + 1] + h / 2 + 0.01)
    return ys


def styled_ax(ax, xlabel, ylabel, title=None, grid=True):
    ax.set_xlabel(xlabel, fontsize=10, color=DARK)
    ax.set_ylabel(ylabel, fontsize=10, color=DARK)
    if title:
        ax.set_title(title, fontsize=11, color=DARK, weight="bold")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    if grid:
        ax.grid(True, ls=":", alpha=0.4)
    ax.tick_params(colors=GRAY, labelsize=9)


# ---------------- 各图绘制 ----------------
def fig_1_2():
    fig, ax = new("因果思想史时间轴", (0, 12), (0, 7))
    ax.plot([0.6, 11.4], [3.4, 3.4], color=GRAY, lw=1.5)
    events = [(1.1, "Hume\n1748"), (2.9, "Wright\n1921"), (4.3, "Rubin\n1974"),
              (5.6, "Granger\n1980"), (7.0, "Pearl\n1980/1995"),
              (8.6, "do-演算\n1995"), (10.2, "因果森林\n2011"), (11.2, "大模型\n2026")]
    for i, (x, t) in enumerate(events):
        c = [BLUE, GREEN, AMBER, RED][i % 4]
        node(ax, x, 3.4, "", color=c, r=0.12)
        ax.text(x, 4.0 if i % 2 == 0 else 2.8, t, ha="center", va="center",
                fontsize=8.5, color=DARK,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=c, alpha=0.9))
    stages = [("哲学", BLUE), ("统计", GREEN), ("图模型", AMBER), ("机器学习", RED), ("大模型", BLUE)]
    for i, (s, c) in enumerate(stages):
        x = 0.6 + i * 2.2
        box(ax, x, 5.6, 2.0, 0.6, s, fc="white", ec=c, fs=9.5, lw=1)
    note(ax, 6, 0.9, "主线：能力边界取决于对数据生成机制的结构性假设", fs=10)
    save(fig, "图1-2.png")


def ladder(ax, levels, right, title_center=6):
    """因果之梯台阶。levels: [(名称, 符号, 颜色)]；right: [(层,说明)]。"""
    for i, (name, sym, c) in enumerate(levels):
        y = 1.0 + i * 1.5
        w = 6.2 - i * 1.3
        box(ax, 0.8, y, w, 1.1, name + "\n" + sym, fc=c, ec=c, fs=10, tc="white")
        if i < len(levels) - 1:
            arrow(ax, 0.8 + w / 2, y + 1.12, 0.8 + w / 2, y + 1.46)
    for i, (a, b) in enumerate(right):
        y = 1.5 + i * 1.5
        ax.text(8.0, y, a, ha="left", va="center", fontsize=10, color=DARK, weight="bold")
        ax.text(8.0, y - 0.42, b, ha="left", va="center", fontsize=9, color=GRAY)


def fig_1_3():
    fig, ax = new("因果之梯：关联—干预—反事实", (0, 12), (0, 7))
    ladder(ax,
           [("Level 1 关联：看到什么", "P(Y | X)", BLUE),
            ("Level 2 干预：做了会怎样", "P(Y | do(X))", GREEN),
            ("Level 3 反事实：当初没做会怎样", "E[Y(x') | X,Y]", AMBER)],
           [("C1 / C2", "支撑 Level 1、2 建模"), ("C3", "对应 Level 2"),
            ("C4", "对应 Level 3")])
    save(fig, "图1-3.png")


def fig_1_4():
    fig, ax = new("统一案例：医疗治疗效应因果图", (0, 12), (0, 7))
    pos = {"S": (3, 5.2), "T": (6, 3.2), "Y": (9, 5.2), "U": (6, 1.2)}
    edge(ax, pos["S"], pos["T"], BLUE)
    edge(ax, pos["T"], pos["Y"], GREEN)
    edge(ax, pos["S"], pos["Y"], BLUE)
    edge(ax, pos["U"], pos["S"], GRAY, dashed=True)
    edge(ax, pos["U"], pos["Y"], GRAY, dashed=True)
    for k, (x, y) in pos.items():
        node(ax, x, y, k, GREEN if k == "U" else BLUE, dashed=(k == "U"))
    ax.text(4.3, 4.25, "后门路径 T ← S → Y", ha="center", fontsize=9, color=RED,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))
    note(ax, 6, 0.35, "S 病情   T 用药   Y 康复   U 生活习惯（潜在混杂）", fs=9)
    save(fig, "图1-4.png")


def fig_2_1():
    fig, ax = new("贝叶斯网络与条件独立", (0, 12), (0, 7))
    pos = {"S": (2.0, 3.5), "T": (4.5, 3.5), "Y": (7.0, 3.5)}
    edge(ax, pos["S"], pos["T"]); edge(ax, pos["T"], pos["Y"])
    for k, (x, y) in pos.items():
        node(ax, x, y, k)
    note(ax, 4.5, 5.3, "DAG：S → T → Y（含路径 S → Y 时省略直接边）", fs=9.5)
    lines = ["缺失的边对应一个条件独立断言：", "· T 与 Y 在给定 S 下独立（药物无效时）",
             "· 骨架 + v-结构 对应 条件独立集", "· d-分离判定全部条件独立"]
    for i, t in enumerate(lines):
        ax.text(8.2, 5.0 - i * 0.9, t, ha="left", va="center", fontsize=9.5,
                color=DARK if i == 0 else GRAY)
    save(fig, "图2-1.png")


def fig_2_2():
    fig, ax = new("d-分离的三种结构", (0, 12), (0, 7))
    graphs = [("链：A → B → C", ("A", "B", "C"), ("A", "B", "C"), "给定 B 阻断"),
              ("分叉：A ← B → C", ("A", "B", "C"), ("A", "B", "C"), "给定 B 阻断"),
              ("对撞：A → B ← C", ("A", "B", "C"), ("A", "B", "C"), "未给定 B 阻断；给定 B 连通")]
    for i, (ttl, names, _, desc) in enumerate(graphs):
        cx = 2.0 + i * 4.0
        pos = {names[0]: (cx - 1.2, 4.2), names[1]: (cx, 2.9), names[2]: (cx + 1.2, 4.2)}
        if i == 0:
            arrow(ax, cx - 0.8, 4.1, cx - 0.2, 3.1)
            arrow(ax, cx + 0.2, 3.1, cx + 0.8, 4.1)
        elif i == 1:
            arrow(ax, cx - 0.2, 3.1, cx - 0.8, 4.1)
            arrow(ax, cx + 0.2, 3.1, cx + 0.8, 4.1)
        else:
            arrow(ax, cx - 0.8, 4.1, cx - 0.2, 3.1)
            arrow(ax, cx + 0.8, 4.1, cx + 0.2, 3.1)
        for k, (x, y) in pos.items():
            node(ax, x, y, k, RED if k == "B" else BLUE, r=0.35, fs=10)
        ax.text(cx, 5.6, ttl, ha="center", fontsize=9.5, color=DARK)
        note(ax, cx, 1.4, desc, fs=8.5, bbox=False)
    save(fig, "图2-2.png")


def fig_3_1():
    fig, ax = new("干预前 / 后的图", (0, 12), (0, 7))
    # 左：原图
    p = {"S": (1.8, 4.8), "T": (3.8, 2.8), "Y": (5.8, 4.8)}
    edge(ax, p["S"], p["T"]); edge(ax, p["T"], p["Y"]); edge(ax, p["S"], p["Y"])
    for k, (x, y) in p.items():
        node(ax, x, y, k)
    ax.text(3.8, 6.0, "原图：S → T → Y，S → Y", ha="center", fontsize=9.5, color=DARK)
    # 右：do(T) 删除 S->T
    p2 = {"S": (7.2, 4.8), "T": (9.2, 2.8), "Y": (11.2, 4.8)}
    edge(ax, p2["T"], p2["Y"]); edge(ax, p2["S"], p2["Y"])
    for k, (x, y) in p2.items():
        node(ax, x, y, k, GREEN if k == "T" else BLUE)
    # 删除的入边用红色虚线 X
    ax.plot([7.5, 8.9], [4.6, 3.1], color=RED, lw=1.4, ls="--")
    ax.plot([7.6, 8.8], [3.0, 4.5], color=RED, lw=1.4, ls="--")
    ax.text(9.2, 6.0, "do(T=t)：删除 S → T", ha="center", fontsize=9.5, color=DARK)
    note(ax, 9.2, 1.1, "T 不再受 S 影响", fs=10, bbox=False)
    note(ax, 3.8, 1.1, "条件化不改变图结构", fs=10, bbox=False)
    save(fig, "图3-1.png")


def fig_3_2():
    fig, ax = new("后门准则与前门准则", (0, 12), (0, 7))
    # 左：后门被阻断
    p = {"X": (1.6, 4.6), "C": (3.6, 2.8), "Y": (5.6, 4.6), "Z": (3.6, 5.8)}
    edge(ax, p["X"], p["C"]); edge(ax, p["C"], p["Y"])
    edge(ax, p["X"], p["Y"], GREEN)
    edge(ax, p["Z"], p["C"], AMBER, dashed=True)
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN if k == "Y" else BLUE)
    ax.text(3.6, 6.5, "后门：X ← C → Y 被 Z 阻断", ha="center", fontsize=9.5, color=DARK)
    # 右：前门
    p2 = {"X": (7.2, 4.8), "M": (9.2, 4.8), "Y": (11.2, 4.8), "U": (9.2, 2.2)}
    edge(ax, p2["X"], p2["M"]); edge(ax, p2["M"], p2["Y"], GREEN)
    edge(ax, p2["X"], p2["Y"], BLUE, rad=0.35)
    edge(ax, p2["U"], p2["X"], GRAY, dashed=True)
    edge(ax, p2["U"], p2["Y"], GRAY, dashed=True)
    for k, (x, y) in p2.items():
        node(ax, x, y, k, GREEN if k == "M" else BLUE, dashed=(k == "U"))
    ax.text(9.2, 6.5, "前门：X → M → Y（U 未观测）", ha="center", fontsize=9.5, color=DARK)
    save(fig, "图3-2.png")


def fig_3_3():
    fig, ax = new("统一案例治疗效应因果图", (0, 12), (0, 7))
    p = {"S": (3, 5.2), "T": (6, 3.0), "Y": (9, 5.2)}
    edge(ax, p["S"], p["T"]); edge(ax, p["S"], p["Y"]); edge(ax, p["T"], p["Y"], GREEN)
    for k, (x, y) in p.items():
        node(ax, x, y, k)
    note(ax, 6, 6.2, "结构方程：S 外生；T = f_T(S, U_T)；Y = f_Y(T, S, U_Y)", fs=9.5)
    note(ax, 6, 1.0, "后门路径 T ← S → Y（需阻断以识别效应）", fs=10, color=RED)
    save(fig, "图3-3.png")


def fig_4_1():
    fig, ax = new("因果之梯：关联—干预—反事实", (0, 12), (0, 7))
    ladder(ax,
           [("Level 1 关联", "P(Y | X)", BLUE),
            ("Level 2 干预", "P(Y | do(X))", GREEN),
            ("Level 3 反事实", "E[Y(x') | X, Y]", AMBER)],
           [("观察分布", "关联所需信息"), ("因果图", "干预所需信息"),
            ("结构方程", "反事实所需信息")])
    save(fig, "图4-1.png")


def fig_4_2():
    fig, ax = new("辛普森悖论与层间不可约", (0, 12), (0, 7))
    ax1 = fig.add_axes([0.08, 0.15, 0.38, 0.62])
    ax2 = fig.add_axes([0.56, 0.15, 0.38, 0.62])
    rng = np.random.default_rng(1)
    for ax_, slope, title in [(ax1, None, "分组：甲科 / 乙科"), (ax2, -2.0, "合并：关联反转")]:
        for g, c, off in [(0, BLUE, 1.0), (1, GREEN, -1.0)]:
            x = rng.uniform(0, 4, 18)
            y = (0.6 * x + off) + rng.normal(0, 0.25, 18) if slope is None else (-2.0 * x + off) + rng.normal(0, 0.5, 18)
            ax_.scatter(x, y, color=c, alpha=0.75, s=22)
            if slope is None:
                xs = np.linspace(0, 4, 10)
                ax_.plot(xs, 0.6 * xs + off, color=c, lw=1.5)
        if slope is not None:
            xs = np.linspace(0, 4, 10)
            ax_.plot(xs, -2.0 * xs, color=RED, lw=2)
        styled_ax(ax_, "协变量", "结果 Y", title)
    fig.text(0.5, 0.92, "关联反转，干预调整揭示真实方向", ha="center", fontsize=11,
             color=RED, weight="bold", transform=fig.transFigure)
    save(fig, "图4-2.png")


def fig_5_1():
    fig, ax = new("马尔可夫等价类（v-结构）", (0, 12), (0, 7))
    items = [("X → Y", BLUE), ("Y → X", BLUE), ("X ← Z → Y", BLUE), ("X → Z ← Y（v-结构）", RED)]
    for i, (t, c) in enumerate(items):
        x = 0.5 + i * 3.0
        box(ax, x, 2.2, 2.7, 1.8, t, fc="white", ec=c, fs=9.5, lw=1.4)
        if i < 3:
            ax.text(x + 1.35, 1.5, "等价" if i < 2 else "可区分方向", ha="center",
                    fontsize=8.5, color=GRAY)
    note(ax, 6, 5.4, "同为骨架 X—Y：前三者无法区分方向；v-结构碰撞点唯一可辨识", fs=9.5)
    save(fig, "图5-1.png")


def fig_6_1():
    fig, ax = new("PC 算法两阶段流程", (0, 12), (0, 7))
    ax.text(3.2, 6.0, "阶段一：骨骼", ha="center", fontsize=11, color=DARK, weight="bold")
    ax.text(8.8, 6.0, "阶段二：定向", ha="center", fontsize=11, color=DARK, weight="bold")
    left = ["完全图", "按 ℓ 递增删边", "得骨骼 + sepset"]
    right = ["v-结构定向", "三条传播规则\n反复应用", "输出 CPDAG"]
    vflow(ax, left, x=1.2, y0=5.0, dy=1.5, w=3.8, h=0.85,
          colors=[LBLUE, LBLUE, LGREEN])
    vflow(ax, right, x=6.8, y0=5.0, dy=1.5, w=3.8, h=0.85,
          colors=[LAMBER, LAMBER, LGREEN])
    arrow(ax, 5.1, 3.5, 6.7, 3.5, color=GRAY)
    save(fig, "图6-1.png")


def fig_7_1():
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 10, 200)
    fwd = 2 + 6 * (1 - np.exp(-x / 2.5))
    bwd = fwd - 1.0 * (1 - np.exp(-(x - 6) / 1.2)) * (x > 6)
    ax.plot(x, fwd, color=BLUE, lw=2, label="前向加边")
    ax.plot(x[x > 6], bwd[x > 6], color=GREEN, lw=2, label="后向删边")
    ax.axvline(6, color=RED, ls="--", alpha=0.6)
    ax.plot(8.5, bwd[x > 6][-1], "o", color=AMBER, ms=9)
    ax.annotate("真等价类峰值", xy=(8.5, bwd[x > 6][-1]), xytext=(5.2, 5.0),
                arrowprops=dict(arrowstyle="->", color=GRAY), fontsize=9, color=DARK)
    styled_ax(ax, "等价类空间中的图（搜索步）", "评分", "GES 两阶段搜索")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    save(fig, "图7-1.png")


def fig_8_1():
    fig = plt.figure(figsize=(8, 5))
    ax1 = fig.add_axes([0.1, 0.56, 0.8, 0.34])
    ax2 = fig.add_axes([0.1, 0.12, 0.8, 0.34])
    rng = np.random.default_rng(2)
    res_f = rng.normal(0, 1, 400)
    ax1.hist(res_f, bins=22, color=BLUE, alpha=0.8)
    ax1.set_title("正向 X → Y：残差均匀、与 X 无关（检验通过）",
                  fontsize=9.5, color=GREEN)
    x = rng.uniform(0, 1, 120)
    res_r = res_f[:120] + 1.2 * x
    ax2.scatter(x, res_r, color=RED, s=18, alpha=0.75)
    ax2.set_title("反向 Y → X：残差对 X 呈依赖形态（检验失败）",
                  fontsize=9.5, color=RED)
    for ax_ in (ax1, ax2):
        ax_.set_xlabel("残差 / X", fontsize=9)
        ax_.grid(True, ls=":", alpha=0.35)
        ax_.tick_params(labelsize=8)
    fig.text(0.5, 0.97, "非高斯破解方向示意", ha="center", fontsize=12,
             color=DARK, weight="bold", transform=fig.transFigure)
    save(fig, "图8-1.png")


def fig_9_1():
    fig, ax = plt.subplots(figsize=(8, 5))
    t = np.arange(1, 21)
    r1 = 0.5 + 0.3 * np.sin(t / 2) + np.random.default_rng(3).normal(0, 0.08, 20)
    r2 = 0.2 + 0.12 * np.sin(t / 2) + np.random.default_rng(4).normal(0, 0.05, 20)
    ax.plot(t, r1, "o-", color=RED, lw=1.6, ms=4, label="仅用 Y 过去")
    ax.plot(t, r2, "o-", color=GREEN, lw=1.6, ms=4, label="加入 X 过去")
    ax.fill_between(t, r1, r2, color=AMBER, alpha=0.15)
    ax.annotate("残差显著减小 → F 检验判定 X → Y",
                xy=(12, (r1[11] + r2[11]) / 2), xytext=(3, 0.05),
                arrowprops=dict(arrowstyle="->", color=GRAY), fontsize=9, color=DARK)
    styled_ax(ax, "时间 t", "预测残差", "格兰杰因果的预测增量示意")
    ax.legend(frameon=False, fontsize=9)
    save(fig, "图9-1.png")


def fig_10_1():
    fig, ax = new("后门与前门准则图示", (0, 12), (0, 7))
    p = {"S": (1.6, 4.8), "T": (3.8, 2.8), "Y": (5.8, 4.8)}
    edge(ax, p["S"], p["T"]); edge(ax, p["T"], p["Y"], GREEN); edge(ax, p["S"], p["Y"])
    for k, (x, y) in p.items():
        node(ax, x, y, k)
    note(ax, 3.8, 1.2, "后门 T ← S → Y 被阻断", fs=9.5, color=RED)
    p2 = {"T": (7.2, 4.8), "M": (9.2, 4.8), "Y": (11.2, 4.8), "U": (9.2, 2.2)}
    edge(ax, p2["T"], p2["M"]); edge(ax, p2["M"], p2["Y"], GREEN)
    edge(ax, p2["U"], p2["T"], GRAY, dashed=True)
    edge(ax, p2["U"], p2["Y"], GRAY, dashed=True)
    for k, (x, y) in p2.items():
        node(ax, x, y, k, GREEN if k == "M" else BLUE, dashed=(k == "U"))
    note(ax, 9.2, 1.2, "前门 T → M → Y 绕过 U", fs=9.5, color=GREEN)
    save(fig, "图10-1.png")


def fig_11_1():
    fig, ax = new("RCT 与观察研究的因果图对比", (0, 12), (0, 7))
    # RCT
    p = {"R": (1.8, 4.8), "T": (4.0, 2.8), "Y": (6.0, 4.8), "S": (1.8, 2.2)}
    edge(ax, p["R"], p["T"], GREEN); edge(ax, p["T"], p["Y"], GREEN)
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN if k in ("R", "T", "Y") else GRAY)
    ax.text(4, 6.0, "RCT：R → T → Y", ha="center", fontsize=10, color=DARK)
    note(ax, 4, 1.0, "R 与 S 无连接，后门自动阻断", fs=9, bbox=False)
    # 观察
    p2 = {"S": (7.4, 4.8), "T": (9.4, 2.8), "Y": (11.4, 4.8)}
    edge(ax, p2["S"], p2["T"], RED); edge(ax, p2["T"], p2["Y"])
    edge(ax, p2["S"], p2["Y"], RED)
    for k, (x, y) in p2.items():
        node(ax, x, y, k, RED if k == "S" else BLUE)
    ax.text(9.4, 6.0, "观察：S → T → Y", ha="center", fontsize=10, color=DARK)
    note(ax, 9.4, 1.0, "后门开放，需调整 S", fs=9, bbox=False)
    save(fig, "图11-1.png")


def fig_12_1():
    fig, ax = plt.subplots(figsize=(8, 5))
    rng = np.random.default_rng(5)
    e_t = rng.beta(2, 2, 14)
    e_c = rng.beta(2, 2, 14)
    ax.scatter(e_t, np.ones(14) * 1, color=BLUE, s=55, label="处理组", zorder=3)
    ax.scatter(e_c, np.zeros(14), color=GREEN, s=55, label="对照组", zorder=3)
    for a, b in zip(np.sort(e_t), np.sort(e_c)):
        ax.plot([a, b], [1, 0], color=AMBER, alpha=0.5, lw=1)
    note(ax, 6, 5.35, "匹配后标准化均数差均 < 0.1", fs=9.5, color=GREEN)
    styled_ax(ax, "倾向得分 e", "组别", "倾向得分匹配示意")
    ax.set_yticks([0, 1]); ax.set_yticklabels(["对照", "处理"])
    ax.legend(frameon=False, fontsize=9)
    save(fig, "图12-1.png")


def fig_13_1():
    fig, ax = new("工具变量因果图", (0, 12), (0, 7))
    p = {"Z": (2.0, 4.8), "T": (5.0, 4.8), "Y": (9.0, 4.8), "U": (6.5, 2.0)}
    edge(ax, p["Z"], p["T"], GREEN)
    edge(ax, p["T"], p["Y"], GREEN)
    edge(ax, p["U"], p["T"], GRAY, dashed=True)
    edge(ax, p["U"], p["Y"], GRAY, dashed=True)
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN if k in ("Z", "T", "Y") else GRAY, dashed=(k == "U"))
    note(ax, 6.5, 6.0, "Z 与 U 无连接：T ← U → Y 混杂路径被绕过", fs=9.5, color=RED)
    save(fig, "图13-1.png")


def fig_14_1():
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(500, 720, 200)
    c = 600
    y_ctrl = 20000 + 12 * (x - c)
    y_treat = y_ctrl.copy()
    y_treat[x >= c] = 20000 + 12 * (x[x >= c] - c) + 1500
    ax.plot(x, y_ctrl, color=BLUE, lw=2, label="对照组")
    ax.plot(x[x < c], y_treat[x < c], color=RED, lw=2, label="处理组")
    ax.plot(x[x >= c], y_treat[x >= c], color=RED, lw=2)
    ax.plot(x, 20000 + 12 * (x - c), color=GRAY, ls="--", lw=1.5, label="反事实延长")
    ax.axvline(c, color=AMBER, ls=":", lw=1.5)
    ax.axvspan(c - 40, c + 40, color=AMBER, alpha=0.12)
    ax.annotate("跳跃约 1500 元", xy=(605, 20000 + 12 * 5 + 750),
                xytext=(630, 22500), arrowprops=dict(arrowstyle="->", color=GRAY),
                fontsize=9, color=DARK)
    styled_ax(ax, "运行变量分数 X（c = 600）", "收入 Y", "清晰断点回归示意")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    save(fig, "图14-1.png")


def fig_15_1():
    fig, ax = new("因果森林的异质效应分裂", (0, 12), (0, 7))
    box(ax, 4.6, 5.2, 2.8, 1.0, "根节点：按 X1 分裂", fc=LBLUE, ec=BLUE, fs=10)
    box(ax, 1.6, 2.6, 3.2, 1.0, "左叶：效应估计 0.2", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 7.2, 2.6, 3.2, 1.0, "右叶：效应估计 1.5", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 5.6, 5.2, 3.2, 3.6); arrow(ax, 6.4, 5.2, 8.8, 3.6)
    note(ax, 6, 1.2, "为效应差异而分裂；诚实估计需样本分割（训练 / 估计）", fs=9.5)
    save(fig, "图15-1.png")


def fig_16_1():
    fig, ax = new("反事实三步法", (0, 12), (0, 7))
    steps = [("溯因", "用事实 O=o\n推断 U 后验", LBLUE),
             ("行动", "do(X=x)\n改写结构方程", LGREEN),
             ("预测", "在 M_x 中\n重算 Y", LAMBER)]
    flow(ax, [a for a, _, _ in steps], y=4.0, h=1.2, w=2.6,
         colors=[c for _, _, c in steps], gap=0.9)
    for i, (a, b, _) in enumerate(steps):
        ax.text(2.0 + i * 3.4, 3.4, b, ha="center", va="top", fontsize=9, color=GRAY)
    note(ax, 6, 1.4, "Level 2 do：改变机制  |  Level 3 反事实：改写机制后重算", fs=10)
    save(fig, "图16-1.png")


def fig_17_1():
    fig, ax = new("中介路径分解", (0, 12), (0, 7))
    p = {"T": (2.0, 5.0), "M": (5.0, 5.0), "Y": (8.0, 5.0)}
    edge(ax, p["T"], p["M"], GREEN); edge(ax, p["M"], p["Y"], GREEN)
    edge(ax, p["T"], p["Y"], BLUE, rad=0.3, label="直接", lp=(5, 6.1))
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN if k == "M" else BLUE)
    box(ax, 1.0, 1.2, 4.4, 1.1, "NDE：T 改变，M 固定为 M_t'", fc=LBLUE, ec=BLUE, fs=9.5)
    box(ax, 6.4, 1.2, 4.4, 1.1, "NIE：T 固定，M 从 M_t' 换为 M_t", fc=LGREEN, ec=GREEN, fs=9.5)
    note(ax, 5.0, 3.4, "总效应 = 直接效应 + 间接效应（线性可加）", fs=9.5)
    save(fig, "图17-1.png")


def fig_18_1():
    fig, ax = new("反事实公平示意", (0, 12), (0, 7))
    p = {"A": (1.8, 5.0), "X": (5.0, 5.0), "Yhat": (9.0, 5.0), "U": (5.0, 2.2)}
    edge(ax, p["A"], p["Yhat"], RED, rad=-0.25, label="直接", lp=(6.5, 5.9))
    edge(ax, p["A"], p["X"], BLUE)
    edge(ax, p["X"], p["Yhat"], BLUE)
    edge(ax, p["U"], p["X"], GRAY, dashed=True)
    edge(ax, p["U"], p["Yhat"], GRAY, dashed=True)
    for k, (x, y) in p.items():
        node(ax, x, y, "Yhat" if k == "Yhat" else k, GREEN if k == "X" else BLUE,
             dashed=(k == "U"))
    note(ax, 6, 0.7, "反事实：把 A 从 a 改为 a' 后重算 Yhat（含经代理 X 的间接路径）", fs=9.5, color=RED)
    save(fig, "图18-1.png")


def fig_19_1():
    fig, ax = new("反事实评估的三层框架", (0, 12), (0, 7))
    layers = [("稳健性：敏感性 Γ 与界", LAMBER, AMBER, 1.0, 8.5),
              ("可观察含义：可检验约束", LGREEN, GREEN, 2.0, 6.5),
              ("结构合理性：假设论证", LBLUE, BLUE, 3.0, 4.5)]
    for t, fc, ec, y, w in layers:
        x = 6 - w / 2
        box(ax, x, y, w, 0.8, t, fc=fc, ec=ec, fs=10)
    ax.annotate("假设增强 → 结论收窄、稳健性提升", xy=(10.8, 2.5), xytext=(10.8, 5.5),
                ha="center", fontsize=9, color=GRAY,
                arrowprops=dict(arrowstyle="->", color=GRAY))
    note(ax, 6, 0.4, "光谱：点识别 → 部分识别 → 不可识别", fs=9.5)
    save(fig, "图19-1.png")


def fig_20_1():
    fig, ax = new("IRM 与虚假相关", (0, 12), (0, 7))
    envs = [("e1：X2 与 Y 正相关", BLUE, 1.5), ("e2：X2 与 Y 零相关", GREEN, 4.5),
            ("e3：X2 相关反转", RED, 7.5)]
    for t, c, x in envs:
        box(ax, x, 4.2, 2.8, 1.0, t, fc="white", ec=c, fs=9)
    box(ax, 10.2, 4.2, 1.6, 1.0, "IRM\n稳健", fc=LGREEN, ec=GREEN, fs=9)
    note(ax, 6, 6.0, "X1 → Y 稳定（因果）；X2 相关随环境变化（虚假）", fs=9.5)
    note(ax, 6, 2.6, "IRM 学到的表示 phi 只保留 X1，使权重 w 在两环境同时最优", fs=9.5, color=BLUE)
    note(ax, 6, 1.0, "测试环境 e3：ERM 崩塌，IRM 稳健", fs=9.5, color=RED)
    save(fig, "图20-1.png")


def fig_21_1():
    fig, ax = new("解耦表示与因果表示", (0, 12), (0, 7))
    # 左：解耦
    for k, (x, y) in {"Z1": (2.0, 5.0), "Z2": (2.0, 2.5), "X": (4.2, 3.75)}.items():
        node(ax, x, y, k, BLUE if k != "X" else GRAY, fs=10)
    ax.text(2.0, 6.0, "解耦表示", ha="center", fontsize=10, color=DARK, weight="bold")
    ax.text(2.0, 1.2, "Z1, Z2 独立但无方向", ha="center", fontsize=9, color=GRAY)
    # 右：因果表示
    p = {"Z1": (6.8, 5.0), "Z2": (9.0, 5.0), "X": (9.0, 2.5)}
    edge(ax, p["Z1"], p["Z2"], GREEN)
    edge(ax, p["Z2"], p["X"], BLUE)
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN if k == "Z2" else BLUE, fs=10)
    ax.annotate("do(Z1)", xy=(6.8, 4.5), xytext=(6.0, 2.0),
                arrowprops=dict(arrowstyle="->", color=RED), fontsize=9, color=RED)
    ax.text(9.0, 6.0, "因果表示", ha="center", fontsize=10, color=DARK, weight="bold")
    ax.text(9.0, 1.0, "Z1 → Z2，干预沿机制传导", ha="center", fontsize=9, color=GRAY)
    save(fig, "图21-1.png")


def fig_22_1():
    fig, ax = new("IRM 与 ERM 的表示对比", (0, 12), (0, 7))
    box(ax, 1.0, 2.4, 4.2, 1.6, "ERM：依赖虚假特征 S\n权重随环境翻转", fc=LRED, ec=RED, fs=10)
    box(ax, 6.8, 2.4, 4.2, 1.6, "IRM：锁定不变因果特征 C\n权重跨环境稳定", fc=LGREEN, ec=GREEN, fs=10)
    arrow(ax, 5.2, 3.2, 6.8, 3.2, color=GRAY)
    note(ax, 6, 5.4, "两环境下最优权重 w1*, w2*：ERM 差异大，IRM 一致", fs=9.5)
    save(fig, "图22-1.png")


def fig_22_2():
    fig, ax = plt.subplots(figsize=(8, 5))
    envs = ["e1", "e2", "e3"]
    r_erm = [0.22, 0.55, 0.48]
    r_irm = [0.25, 0.27, 0.29]
    x = np.arange(3); w = 0.35
    ax.bar(x - w / 2, r_erm, w, color=RED, label="ERM")
    ax.bar(x + w / 2, r_irm, w, color=GREEN, label="IRM")
    ax.axhline(np.mean(r_erm), color=RED, ls="--", alpha=0.5)
    ax.axhline(np.mean(r_irm), color=GREEN, ls="--", alpha=0.5)
    ax.annotate("最坏环境风险：IRM 更低", xy=(2, 0.3), xytext=(0.5, 0.62),
                arrowprops=dict(arrowstyle="->", color=GRAY), fontsize=9, color=DARK)
    styled_ax(ax, "环境", "风险", "多环境风险的 ERM 与稳健权衡")
    ax.set_xticks(x); ax.set_xticklabels(envs)
    ax.legend(frameon=False, fontsize=9)
    save(fig, "图22-2.png")


def fig_23_1():
    fig, ax = new("可辨识表示与不可辨识表示", (0, 12), (0, 7))
    box(ax, 0.8, 4.6, 2.0, 0.8, "机制 1", fc=LBLUE, ec=BLUE, fs=9)
    box(ax, 0.8, 2.8, 2.0, 0.8, "机制 2", fc=LGREEN, ec=GREEN, fs=9)
    arrow(ax, 2.8, 5.0, 4.8, 3.9); arrow(ax, 2.8, 3.2, 4.8, 3.9)
    node(ax, 5.6, 3.9, "潜变量", r=0.5, fs=9)
    arrow(ax, 6.1, 3.9, 7.6, 3.9)
    node(ax, 8.2, 3.9, "观测 X", color=GRAY, r=0.5, fs=9)
    ax.text(3.0, 6.0, "可辨识：机制假设 + 非高斯 / 多环境", ha="center", fontsize=9.5, color=DARK)
    ax.text(9.6, 2.0, "高斯情形：任意旋转等价\n→ 不可辨识", ha="center", fontsize=9.5, color=RED)
    save(fig, "图23-1.png")


def fig_23_2():
    fig, ax = new("因果表示统一理论图景", (0, 12), (0, 7))
    circ = [(4.0, 4.6, "可辨识性\n(第 23 章)", BLUE),
            (8.0, 4.6, "独立机制\n(第 8 章)", GREEN),
            (4.0, 2.0, "环境不变性\n(第 20 章)", AMBER),
            (8.0, 2.0, "干预语义\n(第 3 章)", RED)]
    for x, y, t, c in circ:
        ax.add_patch(Ellipse((x, y), 4.6, 2.2, facecolor="white", edgecolor=c, lw=1.3, alpha=0.9))
        ax.text(x, y + 0.6, t.split("\n")[0], ha="center", fontsize=9.5, color=c, weight="bold")
        ax.text(x, y - 0.15, t.split("\n")[1], ha="center", fontsize=8, color=GRAY)
    box(ax, 5.0, 3.0, 2.0, 0.9, "因果表示", fc="white", ec=DARK, fs=10, lw=1.8)
    save(fig, "图23-2.png")


def fig_24_1():
    fig, ax = new("虚假特征与对抗脆弱性", (0, 12), (0, 7))
    ax.set_aspect("auto")
    # 左：ERM 边界靠虚假特征
    ax.plot([0, 4], [1.5, 1.5], color=RED, lw=2)
    ax.scatter([1, 1.3, 0.8], [2.2, 2.5, 2.0], color=RED, s=40)
    ax.scatter([2.5, 2.8], [0.8, 0.5], color=BLUE, s=40)
    ax.annotate("扰动轻易跨越边界", xy=(2.2, 1.5), xytext=(0.3, 3.2),
                arrowprops=dict(arrowstyle="->", color=RED), fontsize=9, color=RED)
    ax.text(2.0, 6.0, "ERM：依赖虚假特征 S", ha="center", fontsize=10, color=DARK)
    # 右：因果模型
    ax.plot([8, 12], [2.0, 2.0], color=GREEN, lw=2)
    ax.scatter([9, 9.3], [2.8, 3.0], color=GREEN, s=40)
    ax.scatter([10.5, 10.8], [1.2, 1.0], color=GREEN, s=40)
    ax.annotate("扰动不跨越边界", xy=(9.6, 2.0), xytext=(8.3, 3.6),
                arrowprops=dict(arrowstyle="->", color=GREEN), fontsize=9, color=GREEN)
    ax.text(10.0, 6.0, "因果模型：只依赖 C", ha="center", fontsize=10, color=DARK)
    save(fig, "图24-1.png")


def fig_24_2():
    fig, ax = plt.subplots(figsize=(8, 5))
    it = np.arange(1, 21)
    pred = 0.9 * np.exp(-it / 4) + 0.1
    irm = 0.5 * (1 - np.exp(-it / 3)) * np.exp(-it / 18)
    cf = 0.35 * (1 - np.exp(-it / 5)) * np.exp(-it / 20)
    ax.plot(it, pred, color=BLUE, lw=2, label="预测损失")
    ax.plot(it, irm, color=GREEN, lw=2, label="IRM 惩罚")
    ax.plot(it, cf, color=AMBER, lw=2, label="反事实惩罚")
    ax.axvline(12, color=RED, ls="--", alpha=0.5)
    ax.annotate("因果模型稳态更稳健", xy=(14, 0.3), xytext=(9, 0.62),
                arrowprops=dict(arrowstyle="->", color=GRAY), fontsize=9, color=DARK)
    styled_ax(ax, "迭代次数", "损失", "因果正则化三项损失的作用")
    ax.legend(frameon=False, fontsize=9)
    save(fig, "图24-2.png")


def fig_25_1():
    fig, ax = new("三类漂移的因果图对照", (0, 12), (0, 7))
    items = [("协变量漂移：P(X) 变", LBLUE, "X → Y 机制不变"),
             ("标签漂移：P(Y|X) 变", LGREEN, "条件机制改变"),
             ("概念漂移：语义变", LAMBER, "变量含义改变")]
    for i, (t, fc, sub) in enumerate(items):
        x = 0.5 + i * 4.0
        box(ax, x, 4.2, 3.5, 1.0, t, fc=fc, ec=BLUE if i == 0 else (GREEN if i == 1 else AMBER), fs=9.5)
        p = {"X": (x + 0.9, 2.4), "Y": (x + 2.6, 2.4)}
        arrow(ax, p["X"][0] + 0.3, p["X"][1], p["Y"][0] - 0.3, p["Y"][1],
              color=GRAY, dashed=True, lw=2)
        node(ax, p["X"][0], p["X"][1], "X", r=0.35, fs=10)
        node(ax, p["Y"][0], p["Y"][1], "Y", r=0.35, fs=10)
        ax.text(x + 1.75, 1.1, sub, ha="center", fontsize=8.5, color=GRAY)
    note(ax, 6, 6.0, "虚线标出被改变的机制", fs=9.5, color=RED)
    save(fig, "图25-1.png")


def fig_25_2():
    fig, ax = new("因果领域适应流程", (0, 12), (0, 7))
    steps = ["因果图\n定位漂移", "判断\n可迁移", "目标域重估\n不可迁移部分", "部署"]
    xs, w = flow(ax, steps, y=3.3, h=1.2, w=2.3,
                 colors=[LBLUE, LGREEN, LAMBER, LGREEN], gap=0.55)
    labels = ["源域+目标域\n数据", "可迁移机制集", "校正后模型", "目标域策略"]
    for x, l in zip(xs, labels):
        ax.text(x + w / 2, 2.6, l, ha="center", va="top", fontsize=8.5, color=GRAY)
    save(fig, "图25-2.png")


def fig_26_1():
    fig, ax = new("因果 MDP 的结构因果图", (0, 12), (0, 7))
    # 左：因果 MDP 含 U
    p = {"U": (1.5, 5.2), "S": (1.5, 2.6), "A": (4.0, 4.0),
         "S'": (6.0, 5.2), "R": (6.0, 2.6)}
    edge(ax, p["U"], p["A"], GRAY, dashed=True)
    edge(ax, p["U"], p["S'"], GRAY, dashed=True)
    edge(ax, p["U"], p["R"], GRAY, dashed=True)
    edge(ax, p["S"], p["A"]); edge(ax, p["S"], p["S'"]); edge(ax, p["S"], p["R"])
    edge(ax, p["A"], p["S'"], GREEN); edge(ax, p["A"], p["R"], GREEN)
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN if k in ("A", "S'") else BLUE,
             dashed=(k == "U"), fs=10)
    ax.add_patch(FancyBboxPatch((0.9, 4.6), 1.2, 1.2, boxstyle="round,pad=0.1",
                                fill=False, edgecolor=GRAY, ls="--"))
    ax.text(3.75, 6.2, "因果 MDP：U 未观测混杂", ha="center", fontsize=9.5, color=DARK)
    # 右：经典 MDP
    q = {"S": (8.0, 4.2), "A": (10.0, 4.2), "S'": (11.4, 5.2), "R": (11.4, 3.0)}
    edge(ax, q["S"], q["A"], GREEN); edge(ax, q["A"], q["S'"], GREEN); edge(ax, q["A"], q["R"], GREEN)
    for k, (x, y) in q.items():
        node(ax, x, y, k, GREEN, fs=10)
    ax.text(9.8, 6.2, "经典 MDP：A → S', R（干净）", ha="center", fontsize=9.5, color=DARK)
    save(fig, "图26-1.png")


def fig_27_1():
    fig, ax = new("推荐系统的因果图与反馈回路", (0, 12), (0, 7))
    p = {"U": (1.8, 5.2), "I": (1.8, 2.8), "H": (4.0, 2.0),
         "A": (5.2, 4.4), "Y": (9.0, 4.4)}
    for k in ("U", "I", "H"):
        edge(ax, p[k], p["A"])
    for k in ("U", "I", "H", "A"):
        edge(ax, p[k], p["Y"], GREEN if k == "A" else BLUE)
    edge(ax, p["Y"], p["A"], RED, rad=-0.5, dashed=True, label="反馈", lp=(7.2, 3.3))
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN if k in ("A", "Y") else BLUE, fs=10)
    note(ax, 6, 1.0, "后门 A ← H → Y 需用 do 切断", fs=9.5, color=RED)
    save(fig, "图27-1.png")


def fig_28_1():
    fig, ax = new("LLM 因果推理的三种路径", (0, 12), (0, 7))
    items = [("纯 LLM\n直接输出", LBLUE, "Level 1", "低可信"),
             ("因果提示\nCoT / 图提示", LGREEN, "Level 2", "中可信"),
             ("LLM + 工具\n翻译层→do-引擎", LAMBER, "Level 2/3", "高可信")]
    for i, (t, fc, lvl, conf) in enumerate(items):
        x = 0.6 + i * 3.9
        box(ax, x, 3.2, 3.4, 1.6, t, fc=fc, ec=BLUE if i == 0 else (GREEN if i == 1 else AMBER), fs=9.5)
        note(ax, x + 1.7, 2.3, "触及 " + lvl, fs=9, bbox=False)
        note(ax, x + 1.7, 1.4, conf, fs=9, color=GRAY, bbox=False)
        if i < 2:
            arrow(ax, x + 3.45, 4.0, x + 3.85, 4.0, color=GRAY)
    note(ax, 6, 6.0, "可信度梯度：路径越依赖外部因果引擎，越触及高层之梯", fs=9.5)
    save(fig, "图28-1.png")


def fig_29_1():
    fig, ax = new("因果世界模型架构", (0, 12), (0, 7))
    box(ax, 0.6, 2.6, 1.8, 0.9, "观测 o_t", fc=LBLUE, ec=BLUE, fs=9.5)
    p = {"S¹": (4.0, 4.6), "S²": (4.0, 2.4)}
    edge(ax, (2.4, 3.05), p["S¹"]); edge(ax, (2.4, 3.05), p["S²"])
    edge(ax, p["S¹"], p["S²"], GREEN, label="Mi", lp=(4.0, 3.5))
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN, fs=10)
    box(ax, 7.0, 3.2, 2.0, 1.0, "因果图 G", fc=LGREEN, ec=GREEN, fs=10)
    arrow(ax, 4.5, 3.5, 7.0, 3.7)
    box(ax, 10.0, 4.4, 1.6, 0.8, "动作 A_t", fc=LAMBER, ec=AMBER, fs=9)
    arrow(ax, 10.0, 4.6, 8.9, 3.9, color=AMBER)
    note(ax, 6, 1.0, "对比：纯预测模型黑箱 s_t → s_{t+1}，无机制与干预语义", fs=9.5, color=RED)
    save(fig, "图29-1.png")


def fig_30_1():
    fig, ax = new("LLM 辅助的规模化因果发现流程", (0, 12), (0, 7))
    box(ax, 0.6, 3.6, 2.0, 1.0, "观测数据", fc=LBLUE, ec=BLUE, fs=9.5)
    box(ax, 3.0, 3.6, 2.2, 1.0, "NOTEARS 等\n候选图", fc=LBLUE, ec=BLUE, fs=9)
    box(ax, 0.6, 1.4, 2.0, 1.0, "文献", fc=LAMBER, ec=AMBER, fs=9.5)
    box(ax, 3.0, 1.4, 2.2, 1.0, "LLM 提取\n先验约束", fc=LAMBER, ec=AMBER, fs=9)
    box(ax, 6.0, 2.5, 2.2, 1.0, "融合模块\n数据+知识", fc=LGREEN, ec=GREEN, fs=9.5)
    box(ax, 9.2, 2.5, 2.4, 1.0, "输出图 +\nLLM 解释", fc=LGREEN, ec=GREEN, fs=9.5)
    for (a, b) in [((2.6, 4.1), (3.0, 4.1)), ((2.6, 1.9), (3.0, 1.9)),
                   ((5.2, 4.1), (6.0, 3.2)), ((5.2, 1.9), (6.0, 2.8)),
                   ((8.2, 3.0), (9.2, 3.0))]:
        arrow(ax, a[0], a[1], b[0], b[1])
    arrow(ax, 10.4, 2.5, 10.4, 1.1, color=GRAY, rad=0)
    note(ax, 6.5, 0.6, "专家验证回路（虚线反馈）", fs=9, color=GRAY, bbox=False)
    save(fig, "图30-1.png")


def fig_31_1():
    fig, ax = new("因果驱动的科学发现闭环", (0, 12), (0, 7))
    steps = ["数据", "规模化\n因果发现", "候选\n机制图", "LLM 语义\n文献整合", "实验设计\n(do)", "新数据\n回流"]
    n = len(steps)
    cx, cy, rx, ry = 6, 3.6, 4.6, 2.0
    pts = []
    for i in range(n):
        ang = np.pi / 2 - i * 2 * np.pi / n
        pts.append((cx + rx * np.cos(ang), cy + ry * np.sin(ang)))
    colors = [LBLUE, LGREEN, LAMBER, LBLUE, LGREEN, LAMBER]
    for (x, y), s, c in zip(pts, steps, colors):
        box(ax, x - 1.0, y - 0.5, 2.0, 1.0, s, fc=c, ec=BLUE, fs=8.5)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        arrow(ax, a[0], a[1], b[0], b[1], color=GRAY, rad=-0.05)
    note(ax, 6, 6.4, "三引擎：因果 · LLM · 发现", fs=9.5, color=DARK)
    save(fig, "图31-1.png")


def fig_32_1():
    fig, ax = new("因果评估的三层真值体系", (0, 12), (0, 7))
    layers = [("RCT 黄金标准：真实 ATE", LBLUE, BLUE, 4.6, 4.0),
              ("仿真 SEM：由方程给真值", LGREEN, GREEN, 3.0, 5.6),
              ("真值因果图：结构发现", LAMBER, AMBER, 1.4, 7.2)]
    for t, fc, ec, y, w in layers:
        box(ax, 1.0, y, w, 1.0, t, fc=fc, ec=ec, fs=10)
    methods = ["方法：RCT / 准实验", "方法：do / 反事实", "方法：结构学习"]
    for t, y in zip(methods, [4.9, 3.3, 1.7]):
        ax.text(9.2, y, t, ha="left", va="center", fontsize=9.5, color=GRAY)
    save(fig, "图32-1.png")


def fig_33_1():
    fig, ax = new("真实世界证据的因果分析流程", (0, 12), (0, 7))
    steps = ["电子病历\n理赔数据", "定义目标试验\n(七要素)", "时变暴露与混杂\n(g-formula/MSM)",
             "效应估计与\n敏感性分析", "与 RCT 证据\n三角互证"]
    flow(ax, steps, y=3.2, h=1.4, w=2.0,
         colors=[LBLUE, LBLUE, LGREEN, LGREEN, LAMBER], gap=0.35)
    note(ax, 6, 5.6, "各环节对应章节方法，层层递进形成可信证据链", fs=9.5)
    save(fig, "图33-1.png")


def fig_34_1():
    fig, ax = plt.subplots(figsize=(8, 5))
    t = np.array([0, 1, 2, 3, 4, 5])
    ctrl = np.array([20, 21, 22, 23, 24, 25.0])
    treat = np.array([20, 21, 22, 23.7, 25.0, 26.3])
    cf = np.array([20, 21, 22, 23, 24, 25.0])
    ax.plot(t, ctrl, "o-", color=BLUE, lw=2, label="对照组")
    ax.plot(t, treat, "o-", color=RED, lw=2, label="处理组")
    ax.plot(t, cf, "o--", color=GRAY, lw=1.5, label="对照组反事实延长")
    ax.axvline(2.5, color=AMBER, ls=":", lw=1.5)
    ax.fill_between([2.5, 5], [23, 23], [26.3, 26.3], color=GREEN, alpha=0.15)
    ax.annotate("DID 净效应 0.7", xy=(4, 24.7), xytext=(3.0, 20.5),
                arrowprops=dict(arrowstyle="->", color=GREEN), fontsize=9.5, color=GREEN)
    styled_ax(ax, "时间（政策前后）", "平均收入", "双重差分的平行趋势与政策效应")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    save(fig, "图34-1.png")


def fig_35_1():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(0, color=GRAY, lw=1)
    ax.axvline(0.5, color=GRAY, lw=1)
    quad = [(0.05, 0.6, "Sure things\n必转不可抬", LGREEN),
            (0.75, 0.6, "Persuadables\n应投放", LAMBER),
            (0.05, 0.15, "Lost causes\n不可救", LRED),
            (0.75, 0.15, "Sleeping dogs\n反效果", LBLUE)]
    for x, y, t, fc in quad:
        ax.text(x, y, t, ha="center", va="center", fontsize=9, color=DARK,
                bbox=dict(boxstyle="round,pad=0.3", fc=fc, ec="none"))
    ax.add_patch(FancyBboxPatch((0.52, 0.42), 0.42, 0.42,
                                boxstyle="round,pad=0.02", fill=False,
                                edgecolor=AMBER, lw=2, ls="--"))
    styled_ax(ax, "转化概率 p", "增量 τ", "增量四象限与投放决策")
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "图35-1.png")


def fig_36_1():
    fig, ax = new("因果系统五层架构", (0, 12), (0, 7))
    layers = [("决策层", "策略 / C4", LBLUE),
              ("估计层", "效应估计 / C3", LGREEN),
              ("识别层", "识别泛函 / C3", LAMBER),
              ("表示层", "因果图 / C1-C2", LGREEN),
              ("数据层", "数据集 / C1", LBLUE)]
    ys = [5.4, 4.2, 3.0, 1.8, 0.6]
    for (name, sub, fc), y in zip(layers, ys):
        box(ax, 2.0, y, 5.0, 0.9, name, fc=fc, ec=BLUE, fs=10)
        ax.text(7.4, y + 0.45, sub, ha="left", va="center", fontsize=9.5, color=GRAY)
    for i in range(4):
        arrow(ax, 4.5, ys[i + 1] + 0.45, 4.5, ys[i] + 0.02)
    note(ax, 9.8, 3.0, "工件流：数据集 → 图 →\n识别泛函 → 估计 → 策略", fs=9.5)
    save(fig, "图36-1.png")


def fig_37_1():
    fig = plt.figure(figsize=(8, 5))
    ax1 = fig.add_axes([0.08, 0.15, 0.34, 0.6])
    ax2 = fig.add_axes([0.56, 0.15, 0.34, 0.6])
    rng = np.random.default_rng(7)
    X = rng.normal(0, 1, 300)
    Y = rng.normal(0, 1, 300)
    ax1.scatter(X, Y, color=BLUE, s=16, alpha=0.6)
    ax1.set_title("全样本：X, Y 无相关", fontsize=9.5, color=DARK)
    C = X + Y + rng.normal(0, 0.3, 300)
    mask = C > 0.8
    ax2.scatter(X[mask], Y[mask], color=RED, s=16, alpha=0.7)
    ax2.set_title("条件于 C=1：呈明显负相关", fontsize=9.5, color=RED)
    for ax_ in (ax1, ax2):
        styled_ax(ax_, "X", "Y", None)
    fig.text(0.5, 0.93, "对撞偏差：X → C ← Y，条件于对撞点打开虚假路径",
             ha="center", fontsize=10.5, color=DARK, weight="bold", transform=fig.transFigure)
    save(fig, "图37-1.png")


def fig_38_1():
    fig, ax = new("因果智能与 AGI 能力的关系", (0, 12), (0, 7))
    p = {"C1": (6, 5.4), "C2": (3.2, 4.0), "C3": (8.8, 4.0),
         "C4": (6, 2.2)}
    edge(ax, p["C1"], (6, 3.8), GREEN)
    ax.add_patch(Circle((6, 3.5), 0.7, facecolor=DARK, edgecolor=DARK))
    ax.text(6, 3.5, "AGI", ha="center", va="center", fontsize=11, color="white", weight="bold")
    for k, (x, y) in p.items():
        node(ax, x, y, k, GREEN, fs=10)
    others = [("感知", 0.8, 5.6), ("记忆", 11.2, 5.6),
              ("规划", 0.8, 1.2), ("语言", 11.2, 1.2), ("具身", 6, 0.5)]
    for t, x, y in others:
        note(ax, x, y, t, fs=9, bbox=True)
    note(ax, 6, 6.4, "因果是「必要非充分」的基石", fs=9.5, color=RED)
    save(fig, "图38-1.png")


def fig_39_1():
    fig, ax = new("自动化因果发现流程", (0, 12), (0, 7))
    steps = ["观测数据\nC1", "PC/评分\n搜索 C2", "CPDAG\n(可逆边)", "LLM 先验\n时间顺序",
             "定向 DAG\nC2", "假设+不确定性\nC1/C2"]
    flow(ax, steps, y=3.2, h=1.3, w=1.75,
         colors=[LBLUE, LGREEN, LAMBER, LAMBER, LGREEN, LBLUE], gap=0.15)
    note(ax, 6, 5.6, "观测数据经搜索与先验注入，输出定向图与假设说明", fs=9.5)
    save(fig, "图39-1.png")


def fig_40_1():
    fig, ax = new("开放问题地图", (0, 12), (0, 7))
    cols = ["C1 表示", "C2 发现", "C3 效应", "C4 决策"]
    rows = ["Level 3\n反事实", "Level 2\n干预", "Level 1\n关联"]
    xs = [2.4, 4.8, 7.2, 9.6]
    ys = [5.2, 3.5, 1.8]
    for j, c in enumerate(cols):
        ax.text(xs[j], 6.2, c, ha="center", fontsize=9.5, color=DARK, weight="bold")
    for i, r in enumerate(rows):
        ax.text(0.7, ys[i], r, ha="center", va="center", fontsize=9.5, color=DARK, weight="bold")
    probs = {(0, 0): "40.5", (0, 1): "40.2", (0, 2): "40.8", (0, 3): "40.10",
             (1, 0): "40.4", (1, 1): "40.1", (1, 2): "40.6", (1, 3): "40.9",
             (2, 0): "40.3", (2, 1): "40.7", (2, 2): "", (2, 3): ""}
    for (i, j), t in probs.items():
        fc = LRED if t in ("40.1", "40.5", "40.10") else LBLUE
        box(ax, xs[j] - 0.9, ys[i] - 0.5, 1.8, 1.0, t or "·",
            fc=fc if t else "white", ec=BLUE, fs=9.5)
    note(ax, 6, 0.4, "未竟之图：按三层之梯 × 四层能力定位开放问题", fs=9, color=GRAY, bbox=False)
    save(fig, "图40-1.png")


def fig_41_1():
    fig, ax = new("全书闭环：从关联到理解", (0, 12), (0, 7))
    for i, (t, c) in enumerate([("关联", BLUE), ("干预", GREEN), ("反事实", AMBER)]):
        y = 1.2 + i * 1.6
        w = 5.5 - i * 0.9
        box(ax, 3.2, y, w, 1.0, t, fc=c, ec=c, fs=11, tc="white")
        if i < 2:
            arrow(ax, 3.2 + w / 2, y + 1.02, 3.2 + w / 2, y + 1.56)
    ax.text(3.2, 6.4, "从关联到理解", ha="center", fontsize=11, color=DARK, weight="bold")
    note(ax, 0.6, 5.0, "第 1 章\n立框架", fs=9.5, color=BLUE)
    note(ax, 10.4, 2.0, "第 41 章\n合框架", fs=9.5, color=GREEN)
    topics = ["因果发现", "效应识别", "反事实", "决策"]
    for i, t in enumerate(topics):
        ax.text(9.6, 5.2 - i * 0.9, "→ " + t, ha="left", fontsize=9, color=GRAY)
    arrow(ax, 9.6, 1.4, 4.0, 1.4, color=GRAY, rad=0.1)
    save(fig, "图41-1.png")


ALL = [fig_1_2, fig_1_3, fig_1_4, fig_2_1, fig_2_2, fig_3_1, fig_3_2, fig_3_3,
       fig_4_1, fig_4_2, fig_5_1, fig_6_1, fig_7_1, fig_8_1, fig_9_1,
       fig_10_1, fig_11_1, fig_12_1, fig_13_1, fig_14_1, fig_15_1, fig_16_1,
       fig_17_1, fig_18_1, fig_19_1, fig_20_1, fig_21_1, fig_22_1, fig_22_2,
       fig_23_1, fig_23_2, fig_24_1, fig_24_2, fig_25_1, fig_25_2, fig_26_1,
       fig_27_1, fig_28_1, fig_29_1, fig_30_1, fig_31_1, fig_32_1, fig_33_1,
       fig_34_1, fig_35_1, fig_36_1, fig_37_1, fig_38_1, fig_39_1, fig_40_1,
       fig_41_1]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    print("全部配图生成完成，共 %d 张。" % len(ALL))
