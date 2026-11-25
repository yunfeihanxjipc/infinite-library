# -*- coding: utf-8 -*-
"""《科学智能导论》配图脚本。

运行：python scripts/gen_all.py
将正文引用的全部图号绘制为学术风格概念图，输出到 figures/图X-Y.png。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Rectangle, Wedge
import numpy as np

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
LGRAY = "#EEF1F4"
DARK = "#1A3350"


# ---------- 通用辅助函数 ----------
def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("已生成:", name)


def new(ax_title, figsize=(8, 5), xlim=(0, 12), ylim=(0, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.text(sum(xlim) / 2, ylim[1] - 0.15, ax_title, ha="center", va="top",
            fontsize=14, weight="bold", color=DARK)
    return fig, ax


def box(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=10, tc=DARK, lw=1.2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=lw, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc)


def arrow(ax, x1, y1, x2, y2, color=BLUE, rad=0, lw=1.5, ms=12):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=ms,
        linewidth=lw, color=color, connectionstyle=f"arc3,rad={rad}"))


def circle(ax, x, y, r, text, fc=LIGHT, ec=BLUE, fs=10, tc=DARK):
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, linewidth=1.3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc)


def label(ax, x, y, text, fs=10, color=GRAY, ha="center", va="center", weight="normal"):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color, weight=weight)


def flow(name, title, steps, fc=LIGHT, figsize=(8, 5), y=3.5, fs=9.5):
    """水平流程：多个方框依次箭头连接。"""
    fig, ax = new(title, figsize=figsize)
    n = len(steps)
    x0, x1 = 0.5, 11.5
    span = x1 - x0
    w = min(2.0, span / n - 0.25)
    gap = (span - n * w) / (n + 1)
    xs = [x0 + gap + i * (w + gap) for i in range(n)]
    for s, x in zip(steps, xs):
        box(ax, x, y - 0.5, w, 1.0, s, fc=fc, fs=fs)
    for i in range(n - 1):
        arrow(ax, xs[i] + w + 0.03, y, xs[i + 1] - 0.03, y)
    save(fig, name)


def two_path(name, title, top_steps, bottom_steps, top_name, bottom_name,
             tc=BLUE, bc=GREEN):
    """上下两条并行路径。"""
    fig, ax = new(title)
    label(ax, 0.4, 5.6, top_name, fs=11, color=tc, ha="left", weight="bold")
    label(ax, 0.4, 3.1, bottom_name, fs=11, color=bc, ha="left", weight="bold")
    for steps, yy, fc, ec in [(top_steps, 5.0, LIGHT, BLUE),
                              (bottom_steps, 2.5, LGREEN, GREEN)]:
        n = len(steps)
        w = min(2.1, 10.8 / n - 0.25)
        gap = (10.8 - n * w) / (n + 1)
        xs = [0.9 + gap + i * (w + gap) for i in range(n)]
        for s, x in zip(steps, xs):
            box(ax, x, yy - 0.45, w, 0.9, s, fc=fc, ec=ec, fs=9)
        for i in range(n - 1):
            arrow(ax, xs[i] + w + 0.03, yy, xs[i + 1] - 0.03, yy, color=ec)
    save(fig, name)


def curve_plot(name, title, xlabel, ylabel, series, x=None, legend=True):
    """系列曲线图。series: [(y, color, label), ...]"""
    fig, ax = plt.subplots(figsize=(8, 5))
    if x is None:
        x = np.arange(1, len(series[0][0]) + 1)
    for y, color, lab in series:
        ax.plot(x, y, "o-", color=color, lw=2, markersize=4, label=lab)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=14, color=DARK, weight="bold")
    ax.grid(True, ls=":", alpha=0.4)
    if legend:
        ax.legend(fontsize=9)
    save(fig, name)


# ---------- 各图绘制 ----------
def f_1_1():
    fig, ax = new("科学智能的四层能力")
    items = [("数据", "观测与整理", LIGHT, BLUE), ("建模", "规律与表征", LGREEN, GREEN),
             ("发现", "假设与推理", LAMBER, AMBER), ("实验", "验证与闭环", LRED, RED)]
    xs = [0.5, 3.4, 6.3, 9.2]
    for (n, s, fc, ec), x in zip(items, xs):
        box(ax, x, 3.4, 2.3, 1.3, n, fc=fc, ec=ec, fs=13)
        label(ax, x + 1.15, 3.0, s, fs=10)
    for i in range(3):
        arrow(ax, xs[i] + 2.35, 4.05, xs[i + 1] - 0.05, 4.05)
    arrow(ax, 10.35, 3.3, 1.65, 3.3, color=GRAY, rad=0.25)
    label(ax, 6, 1.8, "实验反馈驱动新一轮数据获取（闭环）", fs=10, color=GRAY)
    save(fig, "图1-1.png")


def f_1_2():
    fig, ax = new("科学发现循环")
    items = [("观察", LIGHT, BLUE), ("假设", LGREEN, GREEN),
             ("建模", LAMBER, AMBER), ("验证", LRED, RED)]
    cx, cy, r = 6, 4, 2.4
    pts = []
    for i in range(4):
        a = np.pi / 2 + i * np.pi / 2
        pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))
    for (txt, fc, ec), (x, y) in zip(items, pts):
        circle(ax, x, y, 1.0, txt, fc=fc, ec=ec, fs=11)
    for i in range(4):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 4]
        arrow(ax, x1, y1, x2, y2, rad=-0.12)
    label(ax, 6, 4, "科学发现", fs=10, color=DARK, weight="bold")
    label(ax, 6, 0.7, "验证结果成为新的观察，循环上升", fs=10, color=GRAY)
    save(fig, "图1-2.png")


def f_1_3():
    fig, ax = new("从科学计算到 AI for Science 的历史脉络")
    years = ["1940s", "1970s", "1990s", "2010s", "2020s"]
    events = ["数值计算\n与仿真", "专家系统\n与符号推理", "机器学习\n兴起", "深度学习\n突破", "AI for\nScience"]
    ax.plot([0.8, 11.2], [4, 4], color=GRAY, lw=2)
    xs = np.linspace(1.3, 10.7, 5)
    colors = [BLUE, GREEN, AMBER, RED, BLUE]
    for i, (x, y, e, c) in enumerate(zip(xs, years, events, colors)):
        ax.add_patch(Circle((x, 4), 0.12, color=c, zorder=3))
        up = 4.5 if i % 2 == 0 else 2.0
        box(ax, x - 0.95, up, 1.9, 1.1, e, fc=LIGHT, ec=c, fs=8.5)
        ax.plot([x, x], [4, up + (0 if i % 2 == 0 else 1.1)], color=GRAY, ls=":", lw=1)
        label(ax, x, 3.6 if i % 2 == 0 else 5.85, y, fs=9, color=c, weight="bold")
    save(fig, "图1-3.png")


def f_3_1():
    fig, ax = new("有限差分网格与离散格式")
    # 网格
    for i in range(11):
        ax.plot([1 + i * 0.5, 1 + i * 0.5], [1.5, 6], color="#B8C6D4", lw=0.8)
        ax.plot([1, 6], [1.5 + i * 0.45, 1.5 + i * 0.45], color="#B8C6D4", lw=0.8)
    ax.add_patch(Rectangle((1, 1.5), 5, 4.5, fill=False, ec=BLUE, lw=1.5))
    xi, yi = 3.5, 3.6
    ax.add_patch(Circle((xi, yi), 0.12, color=RED, zorder=4))
    for dx, dy, txt in [(-1, 0, "i−1"), (1, 0, "i+1"), (0, 1, "j+1"), (0, -1, "j−1")]:
        ax.add_patch(Circle((xi + dx * 0.5, yi + dy * 0.45), 0.09, color=BLUE, zorder=4))
        label(ax, xi + dx * 0.65, yi + dy * 0.62, txt, fs=8, color=DARK)
    label(ax, 8.7, 5.0, "中心差分", fs=11, color=DARK, weight="bold", ha="left")
    label(ax, 8.7, 4.3, "du/dx = (u(i+1)-u(i-1))/(2 dx)", fs=9.5, color=BLUE, ha="left")
    label(ax, 8.7, 3.5, "d2u/dx2 = (u(i+1)-2u(i)+u(i-1))/dx2", fs=9.5, color=GREEN, ha="left")
    label(ax, 8.7, 2.6, "dx, dt：离散步长", fs=9.5, color=GRAY, ha="left")
    save(fig, "图3-1.png")


def f_3_2():
    # 顶盖驱动方腔流涡量示意（等高线）
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 1, 120)
    y = np.linspace(0, 1, 120)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.pi * X) * np.sin(np.pi * Y) + 0.4 * np.sin(2 * np.pi * X) * np.sin(2 * np.pi * Y)
    cs = ax.contourf(X, Y, Z, levels=14, cmap="RdBu_r")
    ax.contour(X, Y, Z, levels=10, colors="white", linewidths=0.4, alpha=0.6)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("Navier–Stokes 数值解（顶盖驱动方腔流涡量场）", fontsize=13, color=DARK, weight="bold")
    fig.colorbar(cs, ax=ax, label="涡量（示意）")
    save(fig, "图3-2.png")


def f_4_1():
    fig, ax = new("数据同化循环")
    items = [("背景场", LIGHT, BLUE), ("观测", LGREEN, GREEN),
             ("分析场", LAMBER, AMBER), ("预报", LRED, RED)]
    cx, cy, r = 6, 4, 2.3
    pts = [(cx + r * np.cos(np.pi / 2 + i * np.pi / 2),
            cy + r * np.sin(np.pi / 2 + i * np.pi / 2)) for i in range(4)]
    for (txt, fc, ec), (x, y) in zip(items, pts):
        circle(ax, x, y, 0.95, txt, fc=fc, ec=ec, fs=11)
    for i in range(4):
        arrow(ax, *pts[i], *pts[(i + 1) % 4], rad=-0.1)
    label(ax, 6, 4, "同化", fs=10, color=DARK, weight="bold")
    label(ax, 6, 0.8, "分析场作为下一时刻背景场，循环滚动", fs=10, color=GRAY)
    save(fig, "图4-1.png")


def f_5_1():
    fig, ax = new("PINN 残差网络")
    box(ax, 0.4, 3.5, 1.6, 1.0, "输入 (x,t)", fc=LIGHT, fs=10)
    box(ax, 2.6, 3.5, 2.0, 1.0, "全连接网络", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 5.2, 3.5, 1.6, 1.0, "预测 u_hat", fc=LAMBER, ec=AMBER, fs=11)
    arrow(ax, 2.0, 4.0, 2.6, 4.0)
    arrow(ax, 4.6, 4.0, 5.2, 4.0)
    # 自动微分分支
    box(ax, 5.2, 1.6, 2.4, 1.0, "自动微分", fc=LRED, ec=RED, fs=10)
    box(ax, 8.3, 1.5, 3.2, 1.2, "残差 r = d(u_hat)/dt\n+ N[u_hat]", fc=LRED, ec=RED, fs=9)
    arrow(ax, 6.0, 3.5, 6.0, 2.6, color=RED)
    arrow(ax, 7.6, 2.1, 8.3, 2.1, color=RED)
    # 损失
    box(ax, 8.3, 4.6, 2.8, 1.2, "损失 = 数据项\n+ 物理残差项", fc=LIGHT, fs=10)
    arrow(ax, 6.8, 4.0, 8.3, 5.2, color=BLUE)
    arrow(ax, 9.6, 2.6, 9.6, 4.6, color=RED)
    save(fig, "图5-1.png")


def f_5_2():
    steps = np.arange(1, 201)
    total = 1.0 * np.exp(-steps / 40) + 0.02
    data = 0.6 * np.exp(-steps / 30) + 0.01
    phys = 0.5 * np.exp(-steps / 55) + 0.01
    curve_plot("图5-2.png", "PINN 求解流体问题的损失收敛", "训练步数",
               "损失（对数示意）",
               [(total, BLUE, "总损失"), (data, GREEN, "数据损失"), (phys, AMBER, "物理损失")])


def f_6_1():
    fig, ax = new("傅里叶神经算子（FNO）结构")
    box(ax, 0.3, 3.3, 1.7, 1.2, "输入 a(x)", fc=LIGHT, fs=10)
    box(ax, 2.4, 3.3, 1.6, 1.2, "升维 P", fc=LGREEN, ec=GREEN, fs=10)
    ax.add_patch(Rectangle((4.3, 2.2), 4.0, 3.4, fill=False, ec=BLUE, lw=1.5, ls="--"))
    label(ax, 6.3, 5.4, "傅里叶层 x L", fs=10, color=BLUE, weight="bold")
    for i, y in enumerate([4.4, 3.4, 2.6]):
        box(ax, 4.6, y - 0.3, 3.4, 0.6, "FFT → 频谱滤波 → IFFT" if i == 0 else "逐点变换 + 残差",
            fc=LIGHT, ec=BLUE, fs=8)
    box(ax, 8.7, 3.3, 1.6, 1.2, "降维 Q", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 10.7, 3.3, 1.2, 1.2, "u(x)", fc=LAMBER, ec=AMBER, fs=11)
    arrow(ax, 2.0, 3.9, 2.4, 3.9)
    arrow(ax, 4.0, 3.9, 4.3, 3.9)
    arrow(ax, 8.3, 3.9, 8.7, 3.9)
    arrow(ax, 10.3, 3.9, 10.7, 3.9)
    save(fig, "图6-1.png")


def f_6_2():
    fig, ax = new("DeepONet 分支/主干网络")
    # 分支网络
    label(ax, 3.0, 6.6, "分支网络（Branch）", fs=11, color=BLUE, weight="bold")
    box(ax, 0.6, 5.4, 2.0, 0.8, "函数 u", fc=LIGHT, fs=10)
    box(ax, 3.2, 5.4, 2.0, 0.8, "传感器编码", fc=LIGHT, fs=9)
    box(ax, 5.8, 5.4, 1.8, 0.8, "b1 ... bp", fc=LIGHT, fs=10)
    arrow(ax, 2.6, 5.8, 3.2, 5.8); arrow(ax, 5.2, 5.8, 5.8, 5.8)
    # 主干网络
    label(ax, 3.0, 4.3, "主干网络（Trunk）", fs=11, color=GREEN, weight="bold")
    box(ax, 0.6, 3.1, 2.0, 0.8, "位置 y", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 3.2, 3.1, 2.0, 0.8, "坐标编码", fc=LGREEN, ec=GREEN, fs=9)
    box(ax, 5.8, 3.1, 1.8, 0.8, "t1 ... tp", fc=LGREEN, ec=GREEN, fs=10)
    arrow(ax, 2.6, 3.5, 3.2, 3.5); arrow(ax, 5.2, 3.5, 5.8, 3.5)
    # 合并
    box(ax, 9.0, 4.3, 2.4, 1.4, "内积求和\nG(u)(y)=sum(bi*ti)", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 7.6, 5.8, 9.0, 5.0, color=BLUE)
    arrow(ax, 7.6, 3.5, 9.0, 4.0, color=GREEN)
    save(fig, "图6-2.png")


def f_7_1():
    fig, ax = new("物理归纳偏置谱系")
    items = [("硬约束", "严格满足守恒律\n（如保守格式）", LRED, RED),
             ("软约束", "损失函数惩罚\n（如 PINN）", LAMBER, AMBER),
             ("架构偏置", "等变/不变结构\n（如 GNN）", LGREEN, GREEN),
             ("数据偏置", "先验分布\n（如生成模型）", LIGHT, BLUE)]
    xs = [0.5, 3.4, 6.3, 9.2]
    for (n, s, fc, ec), x in zip(items, xs):
        box(ax, x, 3.5, 2.3, 1.6, n + "\n" + s, fc=fc, ec=ec, fs=8.5)
    ax.annotate("约束强度递增 →", xy=(11.0, 2.6), xytext=(1.0, 2.6),
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5),
                fontsize=10, color=GRAY, va="center")
    label(ax, 6, 1.6, "物理知识由强到弱嵌入模型", fs=10, color=GRAY)
    save(fig, "图7-1.png")


def f_8_1():
    x = np.linspace(0.5, 6, 60)
    true = np.sin(x)
    noisy = true + 0.25 * np.random.default_rng(0).normal(size=len(x))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, true, "-", color=GREEN, lw=2, label="真值")
    ax.plot(x, noisy, "o", color=RED, markersize=3, alpha=0.6, label="含噪观测")
    xd = np.linspace(0.5, 6, 200)
    unreg = np.sin(xd) + 0.3 * np.sin(12 * xd)
    reg = np.sin(xd) + 0.05 * np.sin(6 * xd)
    ax.plot(xd, unreg, "--", color=RED, lw=1.5, label="无正则（振荡）")
    ax.plot(xd, reg, ":", color=BLUE, lw=2, label="正则化后")
    ax.set_title("反问题病态性与正则化效果", fontsize=14, color=DARK, weight="bold")
    ax.legend(fontsize=9); ax.grid(True, ls=":", alpha=0.4)
    save(fig, "图8-1.png")


def f_8_2():
    two_path("图8-2.png", "数据同化的变分与序贯两条路径",
             ["背景场", "代价函数 J", "最小化迭代", "分析场"],
             ["背景场", "观测更新", "卡尔曼增益", "分析场"],
             "变分方法（4D-Var）", "序贯方法（Kalman/EnKF）",
             tc=BLUE, bc=GREEN)


def f_9_1():
    fig, ax = new("多尺度建模的层次结构")
    levels = [("宏观连续介质", "有限元 / 连续方程", LGRAY, GRAY),
              ("细观表征元", "均匀化 / 本构", LIGHT, BLUE),
              ("微观分子/原子", "分子动力学", LGREEN, GREEN),
              ("量子电子尺度", "第一性原理", LAMBER, AMBER)]
    ys = [5.8, 4.2, 2.6, 1.0]
    for (n, s, fc, ec), y in zip(levels, ys):
        box(ax, 2.0, y - 0.55, 5.0, 1.1, n + "：" + s, fc=fc, ec=ec, fs=10)
    for i in range(3):
        arrow(ax, 4.5, ys[i] - 0.55, 4.5, ys[i + 1] + 0.55, color=BLUE)
    label(ax, 9.2, 5.0, "自上而下：均匀化", fs=10, color=BLUE)
    label(ax, 9.2, 4.0, "自下而上：粗粒化", fs=10, color=GREEN)
    label(ax, 9.2, 3.0, "跨尺度耦合是关键", fs=10, color=GRAY)
    save(fig, "图9-1.png")


def f_9_2():
    fig, ax = new("降阶模型流程与能量捕获")
    steps = ["高维快照", "POD/SVD", "低维基函数", "Galerkin 投影", "快速降阶模型"]
    xs = [0.5, 2.8, 5.1, 7.4, 9.7]
    for s, x in zip(steps, xs):
        box(ax, x, 4.0, 1.9, 1.0, s, fc=LIGHT, fs=8.5)
    for i in range(4):
        arrow(ax, xs[i] + 1.95, 4.5, xs[i + 1] - 0.05, 4.5)
    # 能量捕获柱状图
    energy = np.cumsum(np.array([0.55, 0.25, 0.12, 0.05, 0.03]))
    bars = [0.55, 0.25, 0.12, 0.05, 0.03]
    bxs = [1.0, 3.3, 5.6, 7.9, 10.2]
    for b, x in zip(bars, bxs):
        ax.add_patch(Rectangle((x, 1.3), 1.0, b * 3.0, facecolor=GREEN, edgecolor=GREEN, alpha=0.8))
        label(ax, x + 0.5, 1.2, f"{int(b*100)}%", fs=8, color=GRAY)
    label(ax, 6, 0.7, "前几个模态即可捕获大部分能量", fs=10, color=GRAY)
    save(fig, "图9-2.png")


def f_10_1():
    fig, ax = new("消息传递神经网络示意")
    # 分子图
    pos = [(3.0, 5.0), (4.5, 5.8), (5.0, 4.2), (3.5, 3.5), (2.0, 4.0), (6.0, 5.0)]
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (2, 3)]
    for i, j in edges:
        ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]], color=GRAY, lw=2, zorder=1)
    for k, (x, y) in enumerate(pos):
        c = RED if k == 0 else BLUE
        ax.add_patch(Circle((x, y), 0.28, fc=c, ec="white", lw=1.2, zorder=3))
        label(ax, x, y, "C" if k else "O", fs=8, color="white", weight="bold")
    label(ax, 4.0, 2.3, "原子=节点，化学键=边", fs=9, color=GRAY)
    # 消息传递
    box(ax, 8.0, 5.2, 3.2, 0.9, "邻居消息 m_ij", fc=LIGHT, fs=10)
    box(ax, 8.0, 3.9, 3.2, 0.9, "聚合求和 m_ij", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 8.0, 2.6, 3.2, 0.9, "更新节点 h_i", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 9.6, 5.2, 9.6, 4.8); arrow(ax, 9.6, 3.9, 9.6, 3.5)
    label(ax, 9.6, 6.4, "多轮消息传递", fs=10, color=DARK, weight="bold")
    save(fig, "图10-1.png")


def f_10_2():
    flow("图10-2.png", "分子表示到性质预测的流水线",
         ["分子结构", "图/指纹表示", "MPNN 编码", "读出层", "性质预测"],
         fc=LIGHT, figsize=(8, 5), fs=8.5)


def f_11_1():
    fig, ax = new("AlphaFold2 的信息流")
    steps = [("MSA 表示", LIGHT, BLUE), ("成对表示", LGREEN, GREEN),
             ("Evoformer", LAMBER, AMBER), ("结构模块", LRED, RED)]
    xs = [0.5, 3.3, 6.1, 8.9]
    for (n, fc, ec), x in zip(steps, xs):
        box(ax, x, 4.0, 2.3, 1.2, n, fc=fc, ec=ec, fs=10)
    for i in range(3):
        arrow(ax, xs[i] + 2.35, 4.6, xs[i + 1] - 0.05, 4.6)
    box(ax, 8.9, 2.0, 2.3, 1.0, "3D 结构 + pLDDT", fc=LIGHT, fs=9)
    arrow(ax, 10.05, 4.0, 10.05, 3.0, color=RED)
    label(ax, 6.0, 1.1, "序列与进化信息 → 端到端结构预测", fs=10, color=GRAY)
    save(fig, "图11-1.png")


def f_11_2():
    two_path("图11-2.png", "蛋白质语言模型的掩码预测与迁移",
             ["蛋白质序列", "随机掩码", "语言模型", "重建残基"],
             ["预训练模型", "下游任务微调", "功能/结构预测", "迁移收益"],
             "掩码预训练（自监督）", "迁移到下游任务",
             tc=BLUE, bc=GREEN)


def f_12_1():
    fig, ax = new("图像重建的正反问题")
    box(ax, 0.5, 3.5, 2.2, 1.0, "真实图像 x", fc=LIGHT, fs=10)
    box(ax, 4.9, 3.5, 2.2, 1.0, "观测 y = A x + 噪声", fc=LGREEN, ec=GREEN, fs=9.5)
    box(ax, 9.3, 3.5, 2.2, 1.0, "重建 x_hat", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 2.7, 4.0, 4.9, 4.0)
    label(ax, 3.8, 4.3, "正问题 A", fs=9, color=BLUE)
    arrow(ax, 7.1, 4.0, 9.3, 4.0)
    label(ax, 8.2, 4.3, "反问题 A 的逆", fs=9, color=RED)
    label(ax, 6, 2.4, "反问题往往病态：需先验/正则化约束解空间", fs=10, color=GRAY)
    save(fig, "图12-1.png")


def f_12_2():
    fig, ax = new("图像配准示意")
    rng = np.random.default_rng(1)
    ax.add_patch(Rectangle((1.0, 2.0), 3.0, 3.0, fill=False, ec=BLUE, lw=2))
    ax.add_patch(Rectangle((5.0, 2.0), 3.0, 3.0, fill=False, ec=GREEN, lw=2))
    ax.add_patch(Rectangle((8.8, 2.0), 3.0, 3.0, fill=False, ec=AMBER, lw=2))
    # 特征点
    for x0, c in [(1.0, BLUE), (5.0, GREEN), (8.8, AMBER)]:
        pts = rng.uniform(0.3, 2.7, (4, 2)) + [x0 + 0.2, 2.2]
        ax.scatter(pts[:, 0], pts[:, 1], color=c, s=40, zorder=3)
    ax.add_patch(Circle((2.5, 3.5), 0.9, fill=False, ec=RED, lw=1.5, ls="--"))
    ax.add_patch(Circle((6.5, 3.5), 0.9, fill=False, ec=RED, lw=1.5, ls="--"))
    arrow(ax, 4.1, 3.5, 4.9, 3.5, color=RED)
    arrow(ax, 8.1, 3.5, 8.7, 3.5, color=RED)
    label(ax, 2.5, 5.5, "参考图像", fs=10, color=BLUE)
    label(ax, 6.5, 5.5, "待配准图像", fs=10, color=GREEN)
    label(ax, 10.3, 5.5, "变换对齐", fs=10, color=AMBER)
    label(ax, 6.5, 1.3, "求空间变换 T，使两图像特征对齐", fs=10, color=GRAY)
    save(fig, "图12-2.png")


def f_13_1():
    fig, ax = new("多模态对齐与融合框架")
    for y, n, c, fc in [(5.2, "图像模态", BLUE, LIGHT), (3.6, "文本模态", GREEN, LGREEN),
                        (2.0, "其他模态", AMBER, LAMBER)]:
        box(ax, 0.5, y - 0.4, 1.8, 0.8, n, fc=fc, ec=c, fs=9)
        box(ax, 3.0, y - 0.4, 2.2, 0.8, "模态编码器", fc=fc, ec=c, fs=9)
        arrow(ax, 2.3, y, 3.0, y, color=c)
        arrow(ax, 5.2, y, 6.8, 4.0, color=c)
    box(ax, 6.8, 3.4, 2.4, 1.2, "对齐\n（对比学习）", fc=LIGHT, fs=10)
    box(ax, 10.0, 3.4, 1.8, 1.2, "融合\n表示", fc=LRED, ec=RED, fs=10)
    arrow(ax, 9.2, 4.0, 10.0, 4.0)
    save(fig, "图13-1.png")


def f_13_2():
    fig, ax = new("科学多模态融合的应用")
    apps = [("显微图像\n+ 基因表达", LIGHT, BLUE), ("遥感 + 气象\n+ 地面观测", LGREEN, GREEN),
            ("谱图 + 文献\n+ 实验记录", LAMBER, AMBER), ("临床影像\n+ 文本报告", LRED, RED)]
    xs = [0.5, 3.5, 6.5, 9.5]
    for (n, fc, ec), x in zip(apps, xs):
        box(ax, x, 3.2, 2.5, 1.8, n, fc=fc, ec=ec, fs=9.5)
    label(ax, 6, 5.6, "多模态融合：互补信息 → 更可靠的科学结论", fs=11, color=DARK, weight="bold")
    label(ax, 6, 2.0, "融合方式：早期拼接 / 晚期决策 / 跨模态注意力", fs=10, color=GRAY)
    save(fig, "图13-2.png")


def f_14_1():
    fig, ax = new("科学自监督表示学习框架")
    box(ax, 0.5, 3.6, 2.4, 1.2, "无标注\n科学数据", fc=LIGHT, fs=10)
    box(ax, 3.6, 3.6, 2.4, 1.2, "构造预文本\n（掩码/对比）", fc=LGREEN, ec=GREEN, fs=9)
    box(ax, 6.7, 3.6, 2.4, 1.2, "预训练编码器", fc=LAMBER, ec=AMBER, fs=10)
    box(ax, 9.8, 3.6, 1.8, 1.2, "表示\n迁移", fc=LRED, ec=RED, fs=10)
    for x1, x2, c in [(2.9, 3.6, BLUE), (6.0, 6.7, GREEN), (9.1, 9.8, AMBER)]:
        arrow(ax, x1, 4.2, x2, 4.2, color=c)
    label(ax, 6, 2.2, "无需人工标注，利用数据自身结构学习通用表示", fs=10, color=GRAY)
    save(fig, "图14-1.png")


def f_14_2():
    fig, ax = new("表示学习与全书结构")
    center = (6, 4)
    circle(ax, *center, 1.4, "表示学习", fc=LAMBER, ec=AMBER, fs=11)
    items = [("数据篇", 3.0, 6.0, BLUE, LIGHT), ("建模篇", 9.0, 6.0, GREEN, LGREEN),
             ("发现篇", 3.0, 2.0, AMBER, LAMBER), ("实验篇", 9.0, 2.0, RED, LRED)]
    for n, x, y, ec, fc in items:
        box(ax, x - 1.0, y - 0.5, 2.0, 1.0, n, fc=fc, ec=ec, fs=10)
        arrow(ax, x, y, center[0], center[1], color=ec, rad=0)
    label(ax, 6, 1.0, "表示学习贯穿四篇，是连接各能力的主线", fs=10, color=GRAY)
    save(fig, "图14-2.png")


def f_15_1():
    fig, ax = new("科学基础模型的预训练—适配范式")
    box(ax, 0.4, 3.6, 2.6, 1.4, "海量科学数据\n预训练", fc=LIGHT, fs=10)
    box(ax, 3.8, 3.6, 3.0, 1.4, "通用科学基础模型\n（大模型）", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 7.7, 4.6, 3.6, 1.0, "微调 / 提示 / 适配器", fc=LAMBER, ec=AMBER, fs=9.5)
    box(ax, 7.7, 2.8, 3.6, 1.0, "下游科学任务", fc=LRED, ec=RED, fs=9.5)
    arrow(ax, 3.0, 4.3, 3.8, 4.3)
    arrow(ax, 6.8, 4.3, 7.7, 5.1)
    arrow(ax, 9.5, 4.6, 9.5, 3.8, color=AMBER)
    save(fig, "图15-1.png")


def f_15_2():
    two_path("图15-2.png", "通用基础模型与科学基础模型的对比",
             ["海量文本/图像", "通用预训练", "对话/生成/推理", "面向大众应用"],
             ["科学数据/方程", "物理/结构约束", "发现/预测/设计", "面向科研闭环"],
             "通用基础模型", "科学基础模型", tc=BLUE, bc=GREEN)


def f_16_1():
    fig, ax = new("分子基础模型的预训练与下游适配")
    box(ax, 0.4, 3.7, 2.4, 1.2, "大规模分子库\n预训练", fc=LIGHT, fs=9.5)
    box(ax, 3.4, 3.7, 2.8, 1.2, "分子基础模型\n（图/序列）", fc=LGREEN, ec=GREEN, fs=9.5)
    arrow(ax, 2.8, 4.3, 3.4, 4.3)
    tasks = [("性质预测", 7.0, 5.4, BLUE, LIGHT), ("分子生成", 7.0, 3.9, GREEN, LGREEN),
             ("逆合成", 9.6, 5.4, AMBER, LAMBER), ("相互作用", 9.6, 3.9, RED, LRED)]
    for n, x, y, ec, fc in tasks:
        box(ax, x, y - 0.45, 2.2, 0.9, n, fc=fc, ec=ec, fs=9)
    for x, y in [(7.0, 5.4), (7.0, 3.9), (9.6, 5.4), (9.6, 3.9)]:
        arrow(ax, 6.2, 4.3, x, y, color=GRAY)
    save(fig, "图16-1.png")


def f_17_1():
    fig, ax = new("蛋白质语言模型的掩码预训练")
    seq = "M K V L F G A R T P D E"
    toks = seq.split()
    xs = [0.6 + i * 0.95 for i in range(len(toks))]
    for i, (x, t) in enumerate(zip(xs, toks)):
        fc, ec, tc = (LRED, RED, RED) if i in (4, 7) else (LIGHT, BLUE, DARK)
        box(ax, x, 4.5, 0.8, 0.9, t if i not in (4, 7) else "[M]", fc=fc, ec=ec, tc=tc, fs=9)
    box(ax, 4.0, 2.6, 4.0, 1.0, "蛋白质语言模型\n预测被掩残基", fc=LGREEN, ec=GREEN, fs=10)
    arrow(ax, xs[4] + 0.4, 4.5, 5.2, 3.6, color=RED)
    arrow(ax, xs[7] + 0.4, 4.5, 6.8, 3.6, color=RED)
    label(ax, 6, 1.6, "自监督学习进化信息，迁移到结构/功能预测", fs=10, color=GRAY)
    save(fig, "图17-1.png")


def f_18_1():
    fig, ax = new("地球系统基础模型的自回归预报")
    box(ax, 0.4, 3.7, 2.2, 1.2, "初始场\n（多变量）", fc=LIGHT, fs=10)
    box(ax, 3.2, 3.7, 2.6, 1.2, "地球系统\n基础模型", fc=LGREEN, ec=GREEN, fs=10)
    box(ax, 6.4, 3.7, 2.2, 1.2, "预报 t+dt", fc=LAMBER, ec=AMBER, fs=10)
    arrow(ax, 2.6, 4.3, 3.2, 4.3)
    arrow(ax, 5.8, 4.3, 6.4, 4.3)
    arrow(ax, 8.6, 4.3, 10.6, 4.3, color=RED)
    box(ax, 10.0, 3.7, 1.6, 1.2, "反馈\n为输入", fc=LRED, ec=RED, fs=9)
    arrow(ax, 10.8, 3.7, 10.8, 2.2, color=RED, rad=0)
    arrow(ax, 10.8, 2.2, 4.5, 2.2, color=RED, rad=0)
    arrow(ax, 4.5, 2.2, 4.5, 3.7, color=RED)
    label(ax, 6, 1.2, "自回归滚动：预报结果作为下一时刻输入", fs=10, color=GRAY)
    save(fig, "图18-1.png")


def f_18_2():
    flow("图18-2.png", "数据同化在预报闭环中的位置",
         ["背景预报", "观测数据", "数据同化", "分析场", "再预报"],
         fc=LIGHT, fs=9)


def f_19_1():
    fig, ax = new("科学大语言模型的整体架构")
    layers = [("输入层", "文献/数据/指令", LIGHT, BLUE, 5.6),
              ("编码层", "科学语料预训练", LGREEN, GREEN, 4.4),
              ("推理层", "工具调用/检索", LAMBER, AMBER, 3.2),
              ("输出层", "假设/代码/解释", LRED, RED, 2.0)]
    for n, s, fc, ec, y in layers:
        box(ax, 2.5, y - 0.45, 7.0, 0.9, n + "：" + s, fc=fc, ec=ec, fs=10)
    for i in range(3):
        arrow(ax, 6.0, layers[i][4] - 0.45, 6.0, layers[i + 1][4] + 0.45, color=BLUE)
    label(ax, 11.0, 4.5, "科学\n知识\n增强", fs=10, color=GRAY, va="center")
    save(fig, "图19-1.png")


def f_20_1():
    two_path("图20-1.png", "符号回归的两种搜索范式",
             ["表达式空间", "遗传编程", "适应度评估", "最优方程"],
             ["表达式空间", "强化学习", "奖励优化", "最优方程"],
             "遗传编程（GP）", "强化学习（RL）", tc=BLUE, bc=GREEN)


def f_21_1():
    flow("图21-1.png", "从数据发现物理定律的流程",
         ["观测数据", "候选项库", "稀疏回归", "方程发现", "实验验证"],
         fc=LIGHT, fs=9)


def f_22_1():
    fig, ax = new("黑箱与灰箱模型的物理一致性对照")
    ax.add_patch(Rectangle((0.8, 1.8), 4.4, 4.2, fill=False, ec=RED, lw=2, ls="--"))
    ax.add_patch(Rectangle((6.8, 1.8), 4.4, 4.2, fill=False, ec=GREEN, lw=2))
    label(ax, 3.0, 5.5, "黑箱模型", fs=12, color=RED, weight="bold")
    label(ax, 9.0, 5.5, "灰箱模型", fs=12, color=GREEN, weight="bold")
    for txt, y, c in [("预测精度高", 4.2, GRAY), ("物理一致性弱", 3.3, RED),
                      ("外推不可靠", 2.4, RED)]:
        label(ax, 3.0, y, txt, fs=10, color=c)
    for txt, y, c in [("嵌入物理结构", 4.2, GREEN), ("物理一致性强", 3.3, GREEN),
                      ("外推更稳健", 2.4, GREEN)]:
        label(ax, 9.0, y, txt, fs=10, color=c)
    label(ax, 6.0, 0.9, "灰箱在精度与可解释性之间取得平衡", fs=10, color=GRAY)
    save(fig, "图22-1.png")


def f_23_1():
    fig, ax = new("大模型假设生成的三条机制")
    items = [("知识重组", "检索+组合已有知识", LIGHT, BLUE),
             ("类比推理", "跨领域结构映射", LGREEN, GREEN),
             ("数据驱动归纳", "从观测归纳规律", LAMBER, AMBER)]
    xs = [0.5, 4.3, 8.1]
    for (n, s, fc, ec), x in zip(items, xs):
        box(ax, x, 4.0, 3.2, 1.8, n + "\n" + s, fc=fc, ec=ec, fs=9.5)
        arrow(ax, x + 1.6, 4.0, 6.0, 2.6, color=ec)
    box(ax, 4.6, 1.2, 2.8, 1.0, "候选科学假设", fc=LRED, ec=RED, fs=10)
    save(fig, "图23-1.png")


def f_24_1():
    fig, ax = new("自动化实验室三层架构与闭环")
    layers = [("任务层", "实验设计与目标", LIGHT, BLUE, 5.4),
              ("调度层", "流程编排与优化", LGREEN, GREEN, 3.8),
              ("执行层", "机器人与仪器", LAMBER, AMBER, 2.2)]
    for n, s, fc, ec, y in layers:
        box(ax, 2.0, y - 0.5, 5.0, 1.0, n + "：" + s, fc=fc, ec=ec, fs=10)
    for i in range(2):
        arrow(ax, 4.5, layers[i][4] - 0.5, 4.5, layers[i + 1][4] + 0.5)
    box(ax, 9.0, 3.8, 2.6, 1.4, "数据反馈\n闭环优化", fc=LRED, ec=RED, fs=10)
    arrow(ax, 7.0, 2.2, 9.0, 3.4, color=RED)
    arrow(ax, 9.0, 4.4, 7.0, 5.4, color=RED)
    save(fig, "图24-1.png")


def f_25_1():
    fig, ax = new("主动学习闭环与采集函数")
    items = [("已标注数据", LIGHT, BLUE), ("训练模型", LGREEN, GREEN),
             ("采集函数", LAMBER, AMBER), ("选新样本", LRED, RED)]
    cx, cy, r = 6, 4, 2.3
    pts = [(cx + r * np.cos(np.pi / 2 + i * np.pi / 2),
            cy + r * np.sin(np.pi / 2 + i * np.pi / 2)) for i in range(4)]
    for (n, fc, ec), (x, y) in zip(items, pts):
        circle(ax, x, y, 0.95, n, fc=fc, ec=ec, fs=9)
    for i in range(4):
        arrow(ax, *pts[i], *pts[(i + 1) % 4], rad=-0.1)
    label(ax, 6, 4, "AL", fs=10, color=DARK, weight="bold")
    label(ax, 6, 0.9, "采集函数权衡探索与利用，优先标注高价值样本", fs=10, color=GRAY)
    save(fig, "图25-1.png")


def f_26_1():
    fig, ax = new("贝叶斯优化一轮迭代")
    x = np.linspace(0, 10, 300)
    f = np.sin(x / 1.5) * 2 + x * 0.15
    mu = f + 0.3 * np.sin(x * 1.2)
    sigma = 0.8 + 0.2 * np.sin(x / 2)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, mu, "-", color=BLUE, lw=2, label="代理模型均值")
    ax.fill_between(x, mu - sigma, mu + sigma, color=BLUE, alpha=0.15, label="置信区间")
    xi = 6.3
    ax.axvline(xi, color=RED, ls="--", lw=1.5, label="采集函数最大点")
    ax.scatter([xi], [np.interp(xi, x, mu)], color=RED, s=60, zorder=5)
    ax.set_title("贝叶斯优化一轮迭代", fontsize=14, color=DARK, weight="bold")
    ax.set_xlabel("超参数"); ax.set_ylabel("目标（示意）")
    ax.legend(fontsize=9); ax.grid(True, ls=":", alpha=0.4)
    save(fig, "图26-1.png")


def f_27_1():
    fig, ax = new("机器人科学家的自主实验循环")
    items = [("假设", LIGHT, BLUE), ("设计实验", LGREEN, GREEN),
             ("执行", LAMBER, AMBER), ("分析数据", LRED, RED), ("更新模型", LGRAY, GRAY)]
    cx, cy, r = 6, 4, 2.5
    pts = [(cx + r * np.cos(-np.pi / 2 + i * 2 * np.pi / 5),
            cy + r * np.sin(-np.pi / 2 + i * 2 * np.pi / 5)) for i in range(5)]
    for (n, fc, ec), (x, y) in zip(items, pts):
        circle(ax, x, y, 0.9, n, fc=fc, ec=ec, fs=9)
    for i in range(5):
        arrow(ax, *pts[i], *pts[(i + 1) % 5], rad=-0.08)
    label(ax, 6, 4, "自主循环", fs=9, color=DARK, weight="bold")
    save(fig, "图27-1.png")


def f_28_1():
    fig, ax = new("AI Scientist 的自动化科学发现闭环")
    items = [("文献调研", LIGHT, BLUE), ("假设生成", LGREEN, GREEN),
             ("实验设计", LAMBER, AMBER), ("执行验证", LRED, RED),
             ("论文撰写", LGRAY, GRAY), ("评审迭代", LIGHT, BLUE)]
    cx, cy, r = 6, 4, 2.5
    pts = [(cx + r * np.cos(-np.pi / 2 + i * np.pi / 3),
            cy + r * np.sin(-np.pi / 2 + i * np.pi / 3)) for i in range(6)]
    for (n, fc, ec), (x, y) in zip(items, pts):
        circle(ax, x, y, 0.82, n, fc=fc, ec=ec, fs=8.5)
    for i in range(6):
        arrow(ax, *pts[i], *pts[(i + 1) % 6], rad=-0.07)
    label(ax, 6, 4, "AI\nScientist", fs=9, color=DARK, weight="bold")
    save(fig, "图28-1.png")


def f_29_1():
    fig, ax = new("假设空间中的探索与利用")
    rng = np.random.default_rng(3)
    ax.scatter(rng.uniform(1, 11, 40), rng.uniform(1.5, 6.5, 40),
               color=LIGHT, ec=GRAY, s=60, label="未知假设")
    known = rng.uniform(1, 11, 12)
    knowny = rng.uniform(1.5, 6.5, 12)
    ax.scatter(known, knowny, color=GREEN, s=80, label="已验证")
    ax.scatter([7.5], [4.5], color=RED, s=140, marker="*", label="探索前沿")
    arrow(ax, 6.0, 5.5, 7.4, 4.6, color=RED)
    ax.set_xlim(0, 12); ax.set_ylim(0.8, 7.2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("假设空间中的探索与利用", fontsize=14, color=DARK, weight="bold")
    ax.legend(fontsize=9, loc="lower left")
    save(fig, "图29-1.png")


def f_30_1():
    flow("图30-1.png", "闭环验证的流程",
         ["生成假设", "预测结果", "设计实验", "执行验证", "反馈修正"],
         fc=LIGHT, fs=9)


def f_31_1():
    fig, ax = new("自动论文与知识综合流程")
    steps = [("实验结果", LIGHT, BLUE), ("图表生成", LGREEN, GREEN),
             ("草稿撰写", LAMBER, AMBER), ("引用综合", LRED, RED), ("成稿", LGRAY, GRAY)]
    xs = [0.5, 2.9, 5.3, 7.7, 10.1]
    for (n, fc, ec), x in zip(steps, xs):
        box(ax, x, 3.7, 1.9, 1.1, n, fc=fc, ec=ec, fs=9)
    for i in range(4):
        arrow(ax, xs[i] + 1.95, 4.25, xs[i + 1] - 0.05, 4.25)
    label(ax, 6, 2.2, "结构化组织证据，自动追溯来源，减少拼接错误", fs=10, color=GRAY)
    save(fig, "图31-1.png")


def f_32_1():
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111, polar=True)
    labels = ["预测精度", "可解释性", "泛化能力", "验证充分性"]
    vals = [0.85, 0.6, 0.75, 0.7]
    angles = np.linspace(0, 2 * np.pi, 4, endpoint=False).tolist()
    vals += vals[:1]; angles += angles[:1]
    ax.plot(angles, vals, color=BLUE, lw=2)
    ax.fill(angles, vals, color=BLUE, alpha=0.2)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_title("科学智能的四维评估雷达图", fontsize=14, color=DARK, weight="bold", pad=18)
    save(fig, "图32-1.png")


def f_33_1():
    fig, ax = new("可复现性的三个层次")
    items = [("代码可复现", "环境/依赖固定，代码可运行", LIGHT, BLUE, 5.4),
             ("结果可复现", "相同数据得到相同结论", LGREEN, GREEN, 3.8),
             ("结论可复现", "独立团队重复验证成立", LAMBER, AMBER, 2.2)]
    for n, s, fc, ec, y in items:
        box(ax, 2.0, y - 0.6, 8.0, 1.2, n + "：" + s, fc=fc, ec=ec, fs=10)
    for i in range(2):
        arrow(ax, 6.0, items[i][4] - 0.6, 6.0, items[i + 1][4] + 0.6)
    label(ax, 6, 0.9, "层次越高，证据越强", fs=10, color=GRAY)
    save(fig, "图33-1.png")


def f_34_1():
    fig, ax = new("科学智能的数据—基准—工具生态")
    center = (6, 4)
    circle(ax, *center, 1.3, "科学智能\n生态", fc=LAMBER, ec=AMBER, fs=10)
    around = [("数据", 3.0, 6.0, BLUE, LIGHT), ("基准", 9.0, 6.0, GREEN, LGREEN),
              ("工具", 9.0, 2.0, RED, LRED), ("社区", 3.0, 2.0, AMBER, LAMBER)]
    for n, x, y, ec, fc in around:
        box(ax, x - 1.0, y - 0.5, 2.0, 1.0, n, fc=fc, ec=ec, fs=10)
        arrow(ax, x, y, center[0], center[1], color=ec)
    save(fig, "图34-1.png")


def f_35_1():
    fig, ax = new("科学智能工程平台的五层架构")
    layers = [("交互层", "自然语言/可视化", LIGHT, BLUE, 5.8),
              ("应用层", "任务与智能体", LGREEN, GREEN, 4.6),
              ("模型层", "基础模型/工具", LAMBER, AMBER, 3.4),
              ("数据层", "数据湖/知识库", LRED, RED, 2.2),
              ("基础设施层", "算力/存储/网络", LGRAY, GRAY, 1.0)]
    for n, s, fc, ec, y in layers:
        box(ax, 2.5, y - 0.45, 7.0, 0.9, n + "：" + s, fc=fc, ec=ec, fs=10)
    save(fig, "图35-1.png")


def f_36_1():
    x = np.linspace(0, 10, 100)
    train = x
    test = x * 0.9 + 2
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, train, "-", color=BLUE, lw=2, label="训练分布关系")
    ax.plot(x[60:], test[60:], "--", color=RED, lw=2, label="分布偏移后关系")
    ax.axvspan(6, 10, color=RED, alpha=0.08)
    ax.annotate("外推区域：性能下降", xy=(8, 8), xytext=(4.5, 9.2),
                arrowprops=dict(arrowstyle="->", color=RED), color=RED, fontsize=10)
    ax.set_title("分布偏移与外推失效示意", fontsize=14, color=DARK, weight="bold")
    ax.set_xlabel("输入特征"); ax.set_ylabel("目标")
    ax.legend(fontsize=9); ax.grid(True, ls=":", alpha=0.4)
    save(fig, "图36-1.png")


def f_37_1():
    fig, ax = new("第五范式：数据—模拟—AI 三元融合", figsize=(8, 5.2))
    c1, c2, c3 = (4.4, 5.0), (7.6, 5.0), (6.0, 2.6)
    r = 2.1
    for (x, y), fc, ec, lab in [(c1, BLUE, BLUE, "观测数据"),
                                (c2, GREEN, GREEN, "机理模拟"),
                                (c3, AMBER, AMBER, "AI 模型")]:
        ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, alpha=0.22, lw=2))
    label(ax, 3.2, 6.4, "观测数据", fs=10, color=BLUE)
    label(ax, 8.8, 6.4, "机理模拟", fs=10, color=GREEN)
    label(ax, 6.0, 1.0, "AI 模型", fs=10, color=AMBER)
    label(ax, 6.0, 4.5, "第五范式\n可微分融合", fs=10, color=DARK, weight="bold")
    label(ax, 5.0, 5.8, "数据同化", fs=8, color=GRAY)
    label(ax, 7.0, 5.8, "物理约束", fs=8, color=GRAY)
    label(ax, 6.0, 3.2, "仿真加速", fs=8, color=GRAY)
    save(fig, "图37-1.png")


def f_38_1():
    fig, ax = new("跨领域泛化的表示几何")
    rng = np.random.default_rng(5)
    ax.add_patch(Ellipse((3.5, 4.5), 4, 3, facecolor=LIGHT, ec=BLUE, alpha=0.6))
    ax.add_patch(Ellipse((8.5, 4.5), 4, 3, facecolor=LGREEN, ec=GREEN, alpha=0.6))
    ax.scatter(rng.normal(3.5, 0.5, 20), rng.normal(4.5, 0.4, 20), color=BLUE, s=25, alpha=0.7)
    ax.scatter(rng.normal(8.5, 0.5, 20), rng.normal(4.5, 0.4, 20), color=GREEN, s=25, alpha=0.7)
    ax.add_patch(FancyArrowPatch((5.2, 4.5), (6.8, 4.5), arrowstyle="<->",
                                 mutation_scale=14, color=RED, lw=2))
    label(ax, 3.5, 6.2, "领域 A", fs=10, color=BLUE)
    label(ax, 8.5, 6.2, "领域 B", fs=10, color=GREEN)
    label(ax, 6.0, 3.4, "共享表示空间", fs=10, color=RED)
    label(ax, 6.0, 1.5, "对齐的几何结构支撑跨领域迁移", fs=10, color=GRAY)
    save(fig, "图38-1.png")


def f_39_1():
    fig, ax = new("人机能力互补与协作误差")
    box(ax, 1.0, 4.6, 3.2, 1.6, "AI：规模计算\n模式发现", fc=LIGHT, ec=BLUE, fs=10)
    box(ax, 7.8, 4.6, 3.2, 1.6, "人类：直觉判断\n价值权衡", fc=LGREEN, ec=GREEN, fs=10)
    arrow(ax, 4.2, 5.4, 7.8, 5.4, color=BLUE)
    arrow(ax, 7.8, 4.4, 4.2, 4.4, color=GREEN)
    box(ax, 4.4, 1.8, 3.2, 1.2, "协作增益", fc=LAMBER, ec=AMBER, fs=11)
    arrow(ax, 6.0, 4.6, 6.0, 3.0, color=AMBER)
    label(ax, 6.0, 1.0, "警惕协作误差：过度依赖或认知偏移", fs=10, color=RED)
    save(fig, "图39-1.png")


def f_40_1():
    fig, ax = new("发现真实性的四重判据")
    items = [("可复现", LIGHT, BLUE), ("可解释", LGREEN, GREEN),
             ("可预测", LAMBER, AMBER), ("可干预", LRED, RED)]
    xs = [0.5, 3.4, 6.3, 9.2]
    for (n, fc, ec), x in zip(items, xs):
        box(ax, x, 3.3, 2.3, 1.6, n, fc=fc, ec=ec, fs=12)
        label(ax, x + 1.15, 2.9, "判据", fs=9, color=GRAY)
    label(ax, 6, 5.6, "同时满足多重判据，发现才更可信", fs=11, color=DARK, weight="bold")
    label(ax, 6, 1.7, "可复现 × 可解释 × 可预测 × 可干预", fs=10, color=GRAY)
    save(fig, "图40-1.png")


def f_41_1():
    fig, ax = plt.subplots(figsize=(8, 5))
    chapters = [f"第{i}篇" for i in range(1, 10)]
    caps = ["数据", "建模", "发现", "实验"]
    mat = np.array([
        [2, 1, 0, 0], [2, 1, 0, 0], [1, 2, 0, 0],
        [2, 1, 1, 0], [1, 2, 1, 0], [1, 2, 1, 0],
        [0, 1, 2, 1], [0, 1, 2, 2], [0, 0, 1, 2],
    ])
    cmap = matplotlib.colors.ListedColormap(["#F4F7FA", LIGHT, BLUE])
    ax.imshow(mat.T, cmap=cmap, aspect="auto", origin="lower")
    ax.set_xticks(range(9)); ax.set_xticklabels(chapters, fontsize=9)
    ax.set_yticks(range(4)); ax.set_yticklabels(caps, fontsize=11)
    ax.set_xlabel("全书九篇", fontsize=11); ax.set_ylabel("四层能力", fontsize=11)
    for i in range(9):
        for j in range(4):
            ax.text(i, j, str(mat[i, j]) if mat[i, j] else "", ha="center", va="center",
                    color="white" if mat[i, j] == 2 else DARK, fontsize=10)
    ax.set_title("九篇×四层能力全景图", fontsize=14, color=DARK, weight="bold", pad=12)
    save(fig, "图41-1.png")


FIGURES = {
    "图1-1.png": f_1_1, "图1-2.png": f_1_2, "图1-3.png": f_1_3,
    "图3-1.png": f_3_1, "图3-2.png": f_3_2, "图4-1.png": f_4_1,
    "图5-1.png": f_5_1, "图5-2.png": f_5_2, "图6-1.png": f_6_1,
    "图6-2.png": f_6_2, "图7-1.png": f_7_1, "图8-1.png": f_8_1,
    "图8-2.png": f_8_2, "图9-1.png": f_9_1, "图9-2.png": f_9_2,
    "图10-1.png": f_10_1, "图10-2.png": f_10_2, "图11-1.png": f_11_1,
    "图11-2.png": f_11_2, "图12-1.png": f_12_1, "图12-2.png": f_12_2,
    "图13-1.png": f_13_1, "图13-2.png": f_13_2, "图14-1.png": f_14_1,
    "图14-2.png": f_14_2, "图15-1.png": f_15_1, "图15-2.png": f_15_2,
    "图16-1.png": f_16_1, "图17-1.png": f_17_1, "图18-1.png": f_18_1,
    "图18-2.png": f_18_2, "图19-1.png": f_19_1, "图20-1.png": f_20_1,
    "图21-1.png": f_21_1, "图22-1.png": f_22_1, "图23-1.png": f_23_1,
    "图24-1.png": f_24_1, "图25-1.png": f_25_1, "图26-1.png": f_26_1,
    "图27-1.png": f_27_1, "图28-1.png": f_28_1, "图29-1.png": f_29_1,
    "图30-1.png": f_30_1, "图31-1.png": f_31_1, "图32-1.png": f_32_1,
    "图33-1.png": f_33_1, "图34-1.png": f_34_1, "图35-1.png": f_35_1,
    "图36-1.png": f_36_1, "图37-1.png": f_37_1, "图38-1.png": f_38_1,
    "图39-1.png": f_39_1, "图40-1.png": f_40_1, "图41-1.png": f_41_1,
}


if __name__ == "__main__":
    for name, fn in FIGURES.items():
        fn()
    print(f"全部完成：共生成 {len(FIGURES)} 张配图，输出目录：{OUT}")
