# -*- coding: utf-8 -*-
"""生成《时序智能导论》第 1-4 章的概念图 / 流程图（精确中文标注，可复现）。
数据类配图见 gen_figures.py；本脚本负责概念 / 流程 / 时间轴等示意图。
运行: python scripts/gen_diagrams.py  -> 输出到 figures/
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

BLUE = "#2C5F8A"
LIGHT = "#E8F0F7"
GREEN = "#2E7D5B"
LGREEN = "#E6F2EA"
AMBER = "#8A6D2F"
LAMBER = "#F6F0DF"
GRAY = "#5A5A5A"
DARK = "#1A3350"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("已生成:", name)


def box(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=11, lw=1.4, tc=DARK):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                       linewidth=lw, edgecolor=ec, facecolor=fc)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc)
    return p


def arrow(ax, x1, y1, x2, y2, text=None, color=BLUE, fs=9):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
                        linewidth=1.3, color=color)
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.1, text, ha="center", va="bottom",
                fontsize=fs, color=GRAY)


# ---------- 图 1-1 时序智能的四层含义 ----------
def fig_1_1():
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    ax.text(6, 2.95, "时序智能的四层含义", ha="center", va="center",
            fontsize=14, weight="bold", color=DARK)
    items = [("预测", "历史 → 未来"), ("分析", "识别趋势 / 季节 / 异常"),
             ("建模", "学习动力学 f"), ("决策", "选择最优行动")]
    xs = [0.3, 3.3, 6.3, 9.3]
    w, h, y = 2.4, 1.1, 1.4
    for (name, sub), x in zip(items, xs):
        box(ax, x, y, w, h, name, fs=15)
        ax.text(x + w / 2, y - 0.18, sub, ha="center", va="top", fontsize=9.5, color=GRAY)
    for i in range(3):
        arrow(ax, xs[i] + w + 0.06, y + h / 2, xs[i + 1] - 0.06, y + h / 2)
    save(fig, "图1-1.png")


# ---------- 图 1-2 方法论演进时间轴 ----------
def fig_1_2():
    fig, ax = plt.subplots(figsize=(13, 4.4))
    ax.set_xlim(1895, 2032)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    ax.text(1963, 4.05, "时序预测方法论的演进", ha="center", va="center",
            fontsize=14, weight="bold", color=DARK)
    phases = [
        (1900, 1927, "经验与外推", "#DCE6EF"),
        (1927, 1975, "统计建模", "#C8DDF0"),
        (1975, 2012, "机器学习与计量", "#B7D3EC"),
        (2012, 2022, "深度学习", "#9CC4E6"),
        (2022, 2028, "基础模型与智能", "#7FB2DE"),
    ]
    for x0, x1, name, c in phases:
        ax.add_patch(Rectangle((x0, 1.75), x1 - x0, 0.55, facecolor=c,
                               edgecolor="white", linewidth=1))
        ax.text((x0 + x1) / 2, 2.02, name, ha="center", va="center",
                fontsize=9.5, color=DARK)
    ax.plot([1900, 2028], [1.62, 1.62], color=BLUE, linewidth=1.6)
    for yr in [1900, 1925, 1950, 1975, 2000, 2025]:
        ax.plot([yr, yr], [1.55, 1.69], color=BLUE, linewidth=1)
        ax.text(yr, 1.38, str(yr), ha="center", va="top", fontsize=8.5, color=GRAY)
    marks = [
        (1927, "1927 Yule\n自回归", 2.75),
        (1970, "1970\nBox-Jenkins", 3.35),
        (1982, "1982 ARCH", 2.75),
        (1997, "1997 LSTM", 3.35),
        (2017, "2017\nTransformer", 2.75),
        (2021, "2021 Informer", 3.35),
        (2023, "2023\n时序大模型", 2.75),
    ]
    for yr, lab, ly in marks:
        ax.plot([yr, yr], [1.75, ly - 0.28], color=GRAY, linewidth=0.8, linestyle=":")
        ax.plot(yr, 1.75, "o", color=BLUE, markersize=5)
        ax.text(yr, ly, lab, ha="center", va="bottom", fontsize=8.5, color=DARK)
    save(fig, "图1-2.png")


# ---------- 图 3-1 平稳性检验联合判断流程 ----------
def fig_3_1():
    fig, ax = plt.subplots(figsize=(12, 6.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.text(6, 5.85, "平稳性检验联合判断流程", ha="center", va="center",
            fontsize=13.5, weight="bold", color=DARK)
    box(ax, 4.6, 5.05, 2.8, 0.66, "输入序列", fc=LGREEN, ec=GREEN, fs=12)
    box(ax, 0.6, 3.55, 4.3, 0.95, "ADF / PP 检验\n原假设：存在单位根（不平稳）", fc=LIGHT, ec=BLUE, fs=10.5)
    box(ax, 7.1, 3.55, 4.3, 0.95, "KPSS 检验\n原假设：序列平稳", fc=LIGHT, ec=BLUE, fs=10.5)
    arrow(ax, 5.4, 5.05, 2.75, 4.5)
    arrow(ax, 6.6, 5.05, 9.25, 4.5)
    box(ax, 4.35, 2.55, 3.3, 0.8, "结论是否一致？", fc=LAMBER, ec=AMBER, fs=11.5)
    arrow(ax, 2.75, 3.55, 5.2, 3.35)
    arrow(ax, 9.25, 3.55, 6.8, 3.35)
    box(ax, 0.2, 0.7, 3.5, 1.0, "均指向平稳\n→ 直接建模", fc=LGREEN, ec=GREEN, fs=10.5)
    box(ax, 4.25, 0.7, 3.5, 1.0, "均指向不平稳\n→ 一阶差分后再建模", fc=LIGHT, ec=BLUE, fs=10.5)
    box(ax, 8.3, 0.7, 3.5, 1.0, "结论矛盾\n→ 查结构突变 / 长记忆", fc=LAMBER, ec=AMBER, fs=10.5)
    arrow(ax, 5.1, 2.55, 1.95, 1.7, text="一致")
    arrow(ax, 6.0, 2.55, 6.0, 1.7, text="一致")
    arrow(ax, 6.9, 2.55, 10.05, 1.7, text="矛盾")
    save(fig, "图3-1.png")


# ---------- 图 4-2 可预测性判定流程 ----------
def fig_4_2():
    fig, ax = plt.subplots(figsize=(7.2, 9.6))
    ax.set_xlim(0, 7.2)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.text(3.6, 10.6, "可预测性判定流程", ha="center", va="center",
            fontsize=13.5, weight="bold", color=DARK)
    steps = [
        ("输入序列", LIGHT, BLUE),
        ("随机 / 混沌判别\n替代数据检验、关联维数", LIGHT, BLUE),
        ("若为混沌：估计 Lyapunov 指数\n得可预测时域（正比于 1/λ）", LAMBER, AMBER),
        ("熵 / 复杂度度量\nSampEn、排列熵 PE", LIGHT, BLUE),
        ("条件熵估计\nH(y_{t+h} | y_{1:t}) 给出固有误差下界", LIGHT, BLUE),
        ("输出：可预测性评级\n与预测时域上限", LGREEN, GREEN),
    ]
    w, h = 5.4, 1.15
    x = (7.2 - w) / 2
    ys = [9.1, 7.4, 5.7, 4.0, 2.3, 0.6]
    for (txt, fc, ec), y in zip(steps, ys):
        box(ax, x, y, w, h, txt, fc=fc, ec=ec, fs=10.5)
    for i in range(len(ys) - 1):
        arrow(ax, 3.6, ys[i], 3.6, ys[i + 1] + h)
    save(fig, "图4-2.png")


# ---------- 图 18-1 LSTM 单元结构（精确重绘，公式由 mathtext 渲染） ----------
def fig_18_1():
    fig, ax = plt.subplots(figsize=(12, 6.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.text(6, 6.08, "LSTM 单元：三个 sigmoid 门、一个 tanh 候选与细胞状态传送带",
            ha="center", fontsize=14, weight="bold", color=DARK)

    gates = [(1.9, "遗忘门  $f$\n$\\sigma$"), (4.0, "输入门  $i$\n$\\sigma$"),
             (6.1, "候选  $\\tilde c$\n$\\tanh$"), (8.2, "输出门  $o$\n$\\sigma$")]
    for x, t in gates:
        box(ax, x, 4.35, 1.9, 1.0, t, fs=11)
    ax.text(6, 4.05, "四者均由 $h_{t-1}$ 与 $x_t$ 计算", ha="center", fontsize=9.5, color=GRAY)

    # 细胞状态主线与两个逐元素算子
    ax.annotate("", xy=(11.3, 2.85), xytext=(0.7, 2.85),
                arrowprops=dict(arrowstyle="-|>", lw=2.6, color=BLUE))
    ax.text(0.55, 2.85, "$c_{t-1}$", ha="right", va="center", fontsize=13, color=DARK)
    ax.text(11.45, 2.85, "$c_t$", ha="left", va="center", fontsize=13, color=DARK)
    for x, s in [(3.0, "$\\otimes$"), (5.6, "$\\oplus$")]:
        ax.add_patch(Circle((x, 2.85), 0.28, fc="white", ec=BLUE, lw=1.6))
        ax.text(x, 2.85, s, ha="center", va="center", fontsize=13, color=DARK)
    ax.text(3.0, 3.35, "乘遗忘门", ha="center", fontsize=9, color=GRAY)
    ax.text(5.6, 3.35, "加输入信息", ha="center", fontsize=9, color=GRAY)
    ax.text(6, 2.32, "细胞状态沿加法路径传递，梯度近似恒等", ha="center", fontsize=10, color=GRAY)

    ax.text(6, 1.55, "$c_t = f\\odot c_{t-1} + i\\odot\\tilde c$,  $\\qquad h_t = o\\odot\\tanh(c_t)$",
            ha="center", fontsize=13, color=DARK)
    ax.text(6, 0.75, "输入：$h_{t-1},\\ x_t,\\ c_{t-1}$     输出：$h_t,\\ c_t$",
            ha="center", fontsize=10.5, color=GRAY)
    save(fig, "图18-1.png")


# ---------- 图 20-1 Transformer 编码器与缩放点积注意力 ----------
def fig_20_1():
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    ax.text(3.1, 6.9, "编码器层", ha="center", fontsize=13, weight="bold", color=DARK)
    ax.text(9.0, 6.9, "缩放点积注意力", ha="center", fontsize=13, weight="bold", color=DARK)
    ax.plot([5.9, 5.9], [0.3, 6.6], color="#CCCCCC", lw=1.2, ls="--")

    layers = ["输入嵌入 + 位置编码", "多头自注意力", "残差与层归一化 Add&Norm",
              "前馈网络 FFN", "残差与层归一化 Add&Norm"]
    ys = [5.6, 4.45, 3.3, 2.15, 1.0]
    for txt, y in zip(layers, ys):
        box(ax, 0.6, y, 4.6, 0.78, txt, fs=10.5)
    for i in range(4):
        arrow(ax, 2.9, ys[i], 2.9, ys[i + 1] + 0.78)
    # 残差跳连示意
    ax.plot([0.45, 0.45], [ys[1] + 0.39, ys[2] + 0.39], color=GREEN, lw=1.2, ls="--")
    ax.plot([0.45, 0.45], [ys[3] + 0.39, ys[4] + 0.39], color=GREEN, lw=1.2, ls="--")
    ax.text(0.3, 3.7, "残差", ha="right", va="center", fontsize=9, color=GREEN, rotation=90)

    # 右侧缩放点积注意力计算流
    box(ax, 6.4, 5.55, 1.55, 0.72, "$Q$  查询", fs=11)
    box(ax, 6.4, 4.55, 1.55, 0.72, "$K$  键", fs=11)
    box(ax, 6.4, 3.55, 1.55, 0.72, "$V$  值", fs=11)
    box(ax, 8.5, 4.9, 2.6, 0.9, "$\\dfrac{QK^{\\top}}{\\sqrt{d_k}}$", fs=14)
    box(ax, 8.5, 3.55, 2.6, 0.72, "$\\mathrm{softmax}$", fs=12)
    box(ax, 11.25, 3.55, 1.1, 0.72, "$\\otimes V$", fs=11)
    arrow(ax, 7.95, 5.9, 8.5, 5.3)
    arrow(ax, 7.95, 4.9, 8.5, 5.15)
    arrow(ax, 9.8, 4.9, 9.8, 4.27)
    arrow(ax, 11.1, 3.9, 11.25, 3.9)
    arrow(ax, 7.95, 3.9, 8.5, 3.9)
    # 注意力矩阵热力图（深色=高权重）
    ax2 = fig.add_axes([0.70, 0.09, 0.20, 0.26])
    rng = np.random.default_rng(7)
    m = rng.uniform(0.15, 0.95, (6, 6))
    np.fill_diagonal(m, 1.0)
    ax2.imshow(m, cmap="Blues", vmin=0, vmax=1)
    ax2.set_xticks(range(6)); ax2.set_yticks(range(6))
    ax2.set_xticklabels([str(i) for i in range(1, 7)], fontsize=8)
    ax2.set_yticklabels([str(i) for i in range(1, 7)], fontsize=8)
    ax2.set_xlabel("键位置", fontsize=9); ax2.set_ylabel("查询位置", fontsize=9)
    ax2.set_title("注意力矩阵（深色＝高权重）", fontsize=9.5, color=DARK)
    save(fig, "图20-1.png")


# ---------- 图 20-2 多头注意力与 O(T²) 复杂度来源 ----------
def fig_20_2():
    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.text(3.2, 6.05, "多头：把注意力拆到 $h$ 个子空间并行", ha="center",
            fontsize=12.5, weight="bold", color=DARK)
    ax.text(9.2, 6.05, "注意力矩阵：规模随 $T$ 平方增长", ha="center",
            fontsize=12.5, weight="bold", color=DARK)
    ax.plot([6.2, 6.2], [0.3, 5.8], color="#CCCCCC", lw=1.2, ls="--")

    for i, y in enumerate([4.6, 3.5, 2.4]):
        box(ax, 0.5, y, 2.3, 0.78, "第 %d 个头" % (i + 1), fs=10.5)
        arrow(ax, 2.8, y + 0.39, 3.5, y + 0.39)
    box(ax, 3.5, 2.4, 2.0, 2.98, "拼接\nConcat\n\n线性投影\n$W^{O}$", fs=11)
    ax.text(3.2, 1.75, "$h$ 个头各自学习不同的依赖子空间", ha="center", fontsize=9.5, color=GRAY)

    ax2 = fig.add_axes([0.575, 0.16, 0.26, 0.52])
    T = 12
    m = np.fromfunction(lambda i, j: np.exp(-np.abs(i - j) / 3.0), (T, T))
    ax2.imshow(m, cmap="Blues", vmin=0, vmax=1)
    ax2.set_xticks([0, 5, 11]); ax2.set_xticklabels(["1", "6", "$T$"], fontsize=9)
    ax2.set_yticks([0, 5, 11]); ax2.set_yticklabels(["1", "6", "$T$"], fontsize=9)
    ax2.set_xlabel("键（长度 $T$）", fontsize=9.5); ax2.set_ylabel("查询（长度 $T$）", fontsize=9.5)
    ax2.set_title("$T\\times T$ 注意力矩阵", fontsize=10.5, color=DARK)
    ax.text(9.2, 1.15, "计算与内存：$O(T^2 d)$，长序列的平方瓶颈", ha="center",
            fontsize=11, color=DARK)
    ax.text(9.2, 0.65, "第 21 章的稀疏 / 低秩 / 频域近似即压缩此矩阵", ha="center",
            fontsize=9.5, color=GRAY)
    save(fig, "图20-2.png")


# ---------- 图 26-1 时序 token 化的三条路线（精确重绘，标注可核对） ----------
def fig_26_1():
    fig, ax = plt.subplots(figsize=(13, 6.4))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.text(6.5, 6.05, "时序 token 化的三条路线", ha="center", fontsize=15, weight="bold", color=DARK)
    for x in (4.35, 8.7):
        ax.plot([x, x], [0.35, 5.65], color="#CCCCCC", lw=1.2, ls="--")

    # ① 补丁投影
    ax.text(2.35, 5.55, "① 补丁投影（连续向量）", ha="center", fontsize=12, weight="bold", color=DARK)
    for j in range(6):
        ax.add_patch(Rectangle((0.55, 3.55 + j * 0.32), 1.15, 0.28, fc=LIGHT, ec=BLUE, lw=1.0))
    ax.text(0.35, 4.35, "序\n列", ha="center", va="center", fontsize=10, color=GRAY)
    arrow(ax, 1.75, 4.35, 2.15, 4.35)
    box(ax, 2.15, 3.95, 1.05, 0.8, "线性层", fs=10)
    arrow(ax, 3.2, 4.35, 3.55, 4.35)
    box(ax, 3.55, 3.95, 0.72, 0.8, "token", fs=9.5)
    ax.text(2.35, 3.2, "切块 → 投影 → 连续向量", ha="center", fontsize=9.5, color=GRAY)
    ax.text(2.35, 2.35, "$N=\\lfloor (L-P)/S\\rfloor+1$ 个 token", ha="center", fontsize=11, color=DARK)
    ax.text(2.35, 1.75, "词表：无（连续表示）", ha="center", fontsize=10, color=DARK)
    ax.text(2.35, 1.15, "信息损失：低", ha="center", fontsize=10, color=GREEN)

    # ② 分箱量化
    ax.text(6.5, 5.55, "② 分箱量化（离散 id）", ha="center", fontsize=12, weight="bold", color=DARK)
    box(ax, 4.6, 3.95, 1.0, 0.8, "归一化\n数值", fs=9.5)
    arrow(ax, 5.6, 4.35, 5.9, 4.35)
    box(ax, 5.9, 3.95, 1.05, 0.8, "分箱区间", fs=9.5)
    arrow(ax, 6.95, 4.35, 7.2, 4.35)
    box(ax, 7.2, 3.95, 1.2, 0.8, "离散 id", fs=9.5)
    ax.text(6.5, 3.2, "交叉熵训练 / 反量化还原", ha="center", fontsize=9.5, color=GRAY)
    ax.text(6.5, 2.35, "每个值 1 个 token，词表大小 $B$", ha="center", fontsize=11, color=DARK)
    ax.text(6.5, 1.75, "信息损失：量化误差 $\\leq\\frac{b_{\\max}-b_{\\min}}{2B}$", ha="center", fontsize=10, color=DARK)
    ax.text(6.5, 1.15, "需先归一化、存在超界值", ha="center", fontsize=10, color=AMBER)

    # ③ 频域 token
    ax.text(10.85, 5.55, "③ 频域 token", ha="center", fontsize=12, weight="bold", color=DARK)
    t = np.linspace(0, 4 * np.pi, 200)
    ax.plot(8.95 + 0.85 * (t / (4 * np.pi)), 4.35 + 0.34 * np.sin(t) + 0.12 * np.sin(3 * t), color=BLUE, lw=1.6)
    ax.text(9.35, 3.65, "波形", ha="center", fontsize=10, color=GRAY)
    arrow(ax, 9.85, 4.35, 10.1, 4.35)
    box(ax, 10.1, 3.95, 1.0, 0.8, "FFT\n选主频", fs=9.5)
    arrow(ax, 11.1, 4.35, 11.35, 4.35)
    box(ax, 11.35, 3.95, 0.9, 0.8, "token", fs=9.5)
    ax.text(10.85, 3.2, "频谱稀疏化 → 主频分量", ha="center", fontsize=9.5, color=GRAY)
    ax.text(10.85, 2.35, "$F$ 个 token（主频数）", ha="center", fontsize=11, color=DARK)
    ax.text(10.85, 1.75, "词表：无（连续表示）", ha="center", fontsize=10, color=DARK)
    ax.text(10.85, 1.15, "信息损失：丢弃弱频", ha="center", fontsize=10, color=AMBER)
    save(fig, "图26-1.png")


if __name__ == "__main__":
    fig_1_1()
    fig_1_2()
    fig_3_1()
    fig_4_2()
    fig_18_1()
    fig_20_1()
    fig_20_2()
    fig_26_1()
    print("\n概念 / 流程图与精确架构图生成完毕。")
