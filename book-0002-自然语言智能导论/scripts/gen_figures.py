# -*- coding: utf-8 -*-
"""生成《自然语言智能导论》数据类配图（精确中文标注，可复现）。
概念 / 架构 / 流程示意图见 gen_diagrams.py。
运行: python scripts/gen_figures.py  -> 输出到 figures/
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

BLUE = "#2C5F8A"
GREEN = "#2E7D5B"
AMBER = "#B07D2B"
RED = "#A33B3B"
GRAY = "#5A5A5A"
DARK = "#1A3350"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("已生成:", name)


# ---------- 图 3-1 词频 Zipf 律 ----------
def fig_3_1():
    fig, ax = plt.subplots(figsize=(7.2, 5))
    r = np.arange(1, 1001)
    f = 1.0 / (r ** 1.0)
    ax.loglog(r, f, color=BLUE, lw=2, label="Zipf 律 $f(r)\\propto 1/r$")
    ax.loglog(r, 3000 / r ** 1.07, color=AMBER, lw=1.5, ls="--", alpha=0.8, label="实际语料（近似）")
    ax.set_xlabel("词频排名 $r$（对数）", fontsize=11)
    ax.set_ylabel("词频 $f(r)$（对数）", fontsize=11)
    ax.set_title("词频的 Zipf 律", fontsize=14, weight="bold", color=DARK)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    ax.legend(fontsize=10)
    save(fig, "图3-1.png")


# ---------- 图 3-2 熵率与序列长度 ----------
def fig_3_2():
    fig, ax = plt.subplots(figsize=(7.2, 5))
    n = np.arange(1, 21)
    h = 4.8 * np.exp(-n / 4.0) + 1.2  # 条件熵随上下文长度下降并趋于熵率
    ax.plot(n, h, "o-", color=BLUE, lw=2, ms=5)
    ax.axhline(1.2, color=RED, ls="--", lw=1.5, label="熵率 $h\\approx1.2$ bit/字符")
    ax.set_xlabel("上下文长度 $n$", fontsize=11)
    ax.set_ylabel("条件熵 $H(W_n\\mid W_{<n})$ (bit)", fontsize=11)
    ax.set_title("条件熵随上下文长度趋于熵率", fontsize=14, weight="bold", color=DARK)
    ax.grid(True, ls=":", alpha=0.4)
    ax.legend(fontsize=10)
    save(fig, "图3-2.png")


# ---------- 图 6-1 词共现矩阵 ----------
def fig_6_1():
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    words = ["我", "爱", "自然", "语言", "机器", "学习", "很", "美"]
    rng = np.random.default_rng(42)
    M = rng.integers(0, 6, size=(len(words), len(words)))
    np.fill_diagonal(M, 0)
    # 强化几个语义相关的共现
    M[3, 2] = M[2, 3] = 5  # 自然-语言
    M[4, 5] = M[5, 4] = 5  # 机器-学习
    im = ax.imshow(M, cmap="Blues")
    ax.set_xticks(range(len(words))); ax.set_xticklabels(words, fontsize=10)
    ax.set_yticks(range(len(words))); ax.set_yticklabels(words, fontsize=10)
    ax.set_xlabel("上下文词", fontsize=11); ax.set_ylabel("中心词", fontsize=11)
    ax.set_title("词—上下文共现矩阵（示意）", fontsize=14, weight="bold", color=DARK)
    for i in range(len(words)):
        for j in range(len(words)):
            if M[i, j] > 0:
                ax.text(j, i, str(M[i, j]), ha="center", va="center",
                        color="white" if M[i, j] > 3 else DARK, fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.8, label="共现次数")
    save(fig, "图6-1.png")


# ---------- 图 6-3 词向量空间的类比 ----------
def fig_6_3():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    pts = {
        "man": (1.0, 1.0), "woman": (1.0, 3.0),
        "king": (4.0, 1.0), "queen": (4.0, 3.0),
    }
    colors = [BLUE, GREEN, AMBER, RED]
    for (name, (x, y)), c in zip(pts.items(), colors):
        ax.scatter(x, y, s=140, color=c, zorder=3)
        ax.text(x + 0.12, y + 0.12, name, fontsize=12, weight="bold")
    # 平行向量
    ax.annotate("", xy=(1.0, 3.0), xytext=(1.0, 1.0),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.annotate("", xy=(4.0, 3.0), xytext=(4.0, 1.0),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    ax.annotate("", xy=(4.0, 1.0), xytext=(1.0, 1.0),
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5, ls="--"))
    ax.text(2.5, 0.6, "性别维度", ha="center", color=GRAY, fontsize=10)
    ax.text(2.5, 3.5, "$\\mathbf{v}_{king}-\\mathbf{v}_{man}+\\mathbf{v}_{woman}\\approx\\mathbf{v}_{queen}$",
            ha="center", fontsize=11, color=DARK)
    ax.set_xlim(0, 6); ax.set_ylim(0, 4.2)
    ax.set_title("词向量空间中的类比关系", fontsize=14, weight="bold", color=DARK)
    ax.grid(True, ls=":", alpha=0.3)
    save(fig, "图6-3.png")


# ---------- 图 11-1 CKY 算法填表 ----------
def fig_11_1():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.text(5, 9.6, "CKY 动态规划填表（自底向上）", ha="center",
            fontsize=14, weight="bold", color=DARK)
    n = 4
    cells = {
        (0, 0): "A\n(a)", (1, 1): "B\n(b)", (2, 2): "B\n(b)", (3, 3): "N\n(c)",
        (0, 1): "S", (1, 2): "X", (2, 3): "Y",
        (0, 2): "S", (1, 3): "Z", (0, 3): "ROOT",
    }
    x0, y0, cw, ch = 1.2, 1.0, 1.7, 1.1
    for (i, j), txt in cells.items():
        x = x0 + j * cw * 0.9
        y = y0 + (n - 1 - (j - i)) * ch * 0.85
        fc = "#E8F0F7" if (j - i) == 0 else "#E6F2EA"
        ax.add_patch(plt.Rectangle((x, y), cw * 0.85, ch * 0.8,
                                   fc=fc, ec=BLUE, lw=1.2))
        ax.text(x + cw * 0.42, y + ch * 0.4, txt, ha="center", va="center", fontsize=9)
    ax.text(5, 0.35, "先填对角线（长度1），再逐层填更长的区间 [i,j]",
            ha="center", fontsize=10, color=GRAY)
    save(fig, "图11-1.png")


# ---------- 图 15-1 N-gram 马尔可夫依赖 ----------
def fig_15_1():
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.text(5, 2.95, "N-gram 的马尔可夫依赖", ha="center",
            fontsize=14, weight="bold", color=DARK)
    xs = [1.2 + i * 1.1 for i in range(8)]
    words = ["w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8"]
    for x, w in zip(xs, words):
        ax.add_patch(plt.Circle((x, 1.5), 0.3, fc="#E8F0F7", ec=BLUE, lw=1.3))
        ax.text(x, 1.5, w, ha="center", va="center", fontsize=9)
    # bigram 依赖（相邻）
    for i in range(7):
        ax.annotate("", xy=(xs[i + 1] - 0.32, 1.5), xytext=(xs[i] + 0.32, 1.5),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
    # trigram 依赖（跨一个）
    for i in range(6):
        ax.annotate("", xy=(xs[i + 2] - 0.32, 1.85), xytext=(xs[i] + 0.32, 1.85),
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.2, connectionstyle="arc3,rad=0.15"))
    ax.text(5, 0.5, "绿：bigram（前1词）    红：trigram（前2词）",
            ha="center", fontsize=10, color=GRAY)
    save(fig, "图15-1.png")


# ---------- 图 15-2 平滑方法对比 ----------
def fig_15_2():
    fig, ax = plt.subplots(figsize=(8, 5))
    methods = ["MLE（无平滑）", "加一平滑", "Good-Turing", "Kneser-Ney"]
    seen = [0.30, 0.18, 0.24, 0.26]
    unseen = [0.0, 0.08, 0.05, 0.045]
    x = np.arange(len(methods)); w = 0.35
    ax.bar(x - w / 2, seen, w, color=BLUE, label="已见 N-gram 概率")
    ax.bar(x + w / 2, unseen, w, color=AMBER, label="未见 N-gram 概率")
    ax.set_xticks(x); ax.set_xticklabels(methods, fontsize=10)
    ax.set_ylabel("概率（示意）", fontsize=11)
    ax.set_title("平滑方法对已见 / 未见 N-gram 的概率重分配", fontsize=13, weight="bold", color=DARK)
    ax.legend(fontsize=10); ax.grid(True, axis="y", ls=":", alpha=0.4)
    save(fig, "图15-2.png")


# ---------- 图 24-1 涌现能力 ----------
def fig_24_1():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    scale = np.array([0.1, 0.5, 1, 5, 10, 50, 100, 200])  # B 参数
    # sigmoid 式突变
    acc = 100 / (1 + np.exp(-(np.log10(scale) - 1.7) * 5))
    ax.semilogx(scale, acc, "o-", color=BLUE, lw=2, ms=6)
    ax.axvline(50, color=RED, ls="--", lw=1.3, label="临界规模 ≈ 50B")
    ax.set_xlabel("模型参数量（B，对数）", fontsize=11)
    ax.set_ylabel("任务准确率 (%)", fontsize=11)
    ax.set_title("涌现能力：规模临界点后的突变式上升", fontsize=13, weight="bold", color=DARK)
    ax.grid(True, which="both", ls=":", alpha=0.4); ax.legend(fontsize=10)
    save(fig, "图24-1.png")


# ---------- 图 3-? Zipf 补充：留存 ----------
if __name__ == "__main__":
    fig_3_1(); fig_3_2(); fig_6_1(); fig_6_3()
    fig_11_1(); fig_15_1(); fig_15_2(); fig_24_1()
    print("数据图生成完成")
