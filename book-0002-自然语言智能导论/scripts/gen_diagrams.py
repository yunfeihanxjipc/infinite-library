# -*- coding: utf-8 -*-
"""生成《自然语言智能导论》概念 / 架构 / 流程示意图（精确中文标注，可复现）。
数据类配图见 gen_figures.py。
运行: python scripts/gen_diagrams.py  -> 输出到 figures/
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

BLUE = "#2C5F8A"; LIGHT = "#E8F0F7"
GREEN = "#2E7D5B"; LGREEN = "#E6F2EA"
AMBER = "#B07D2B"; LAMBER = "#F8EFDD"
RED = "#A33B3B"; LRED = "#F7E9E9"
GRAY = "#5A5A5A"; DARK = "#1A3350"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("已生成:", name)


def box(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=10, lw=1.3, tc=DARK, rounded=True):
    style = "round,pad=0.02,rounding_size=0.05" if rounded else "square,pad=0"
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style,
                 linewidth=lw, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc)


def arrow(ax, x1, y1, x2, y2, text=None, color=BLUE, fs=8.5, rad=0, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=12, linewidth=1.2, color=color,
                 linestyle=ls, connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.12, text, ha="center", va="bottom",
                fontsize=fs, color=GRAY)


def base(ax, xlim, ylim, title):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    ax.text(sum(xlim) / 2, ylim[1] - 0.15, title, ha="center", va="top",
            fontsize=14, weight="bold", color=DARK)


# 1-1 四层含义
def f(n):
    return lambda: n
def fig_1_1():
    fig, ax = plt.subplots(figsize=(12, 3.2)); base(ax, (0, 12), (0, 3.2), "自然语言智能的四层含义")
    items = [("分析", "结构是什么？"), ("理解", "意义是什么？"), ("生成", "如何产生话语？"), ("交互", "如何达成意图？")]
    xs = [0.3, 3.3, 6.3, 9.3]; w, h, y = 2.4, 1.1, 1.2
    for (name, sub), x in zip(items, xs):
        box(ax, x, y, w, h, name, fs=15)
        ax.text(x + w / 2, y - 0.18, sub, ha="center", va="top", fontsize=9.5, color=GRAY)
    for i in range(3):
        arrow(ax, xs[i] + w + 0.05, y + h / 2, xs[i + 1] - 0.05, y + h / 2)
    save(fig, "图1-1.png")

# 1-2 时间轴
def fig_1_2():
    fig, ax = plt.subplots(figsize=(14, 4.6)); base(ax, (0, 14), (0, 4.6), "语言处理方法论的演进")
    phases = [
        ("规则与形式化", "1950s–80s\nChomsky 生成文法", LIGHT),
        ("统计方法", "1990s–2000s\n统计 MT / N-gram", LGREEN),
        ("神经与词向量", "2003–2017\nword2vec / RNN", LAMBER),
        ("预训练", "2018–2020\nTransformer / BERT", LRED),
        ("大模型与智能", "2020–2026\nLLM / RAG / 多模态", LIGHT),
    ]
    w = 2.5; xs = [0.3 + i * 2.75 for i in range(5)]; y = 1.5
    for (name, sub, fc), x in zip(phases, xs):
        box(ax, x, y, w, 1.3, name, fc=fc, fs=11)
        ax.text(x + w / 2, y - 0.2, sub, ha="center", va="top", fontsize=8.5, color=GRAY)
    for i in range(4):
        arrow(ax, xs[i] + w + 0.03, y + 0.65, xs[i + 1] - 0.03, y + 0.65)
    save(fig, "图1-2.png")

# 1-3 意义五层金字塔
def fig_1_3():
    fig, ax = plt.subplots(figsize=(8, 5)); base(ax, (0, 10), (0, 6), "意义的五层结构")
    layers = [("语用意义 M5", 1.6), ("指称意义 M4", 2.6), ("组合意义 M3", 3.6),
              ("分布意义 M2", 4.6), ("形式意义 M1", 5.6)]
    for i, (name, width) in enumerate(layers):
        y = 5.0 - i * 0.9
        box(ax, 5 - width / 2, y, width, 0.75, name,
            fc=[LRED, LAMBER, LGREEN, LIGHT, "#EEEEEE"][i], fs=10.5)
    save(fig, "图1-3.png")

# 1-4 统一案例处理链
def fig_1_4():
    fig, ax = plt.subplots(figsize=(13, 3)); base(ax, (0, 13), (0, 3), "统一案例：问答系统的处理链")
    steps = ["词法\n(8)", "句法\n(11)", "语义角色\n(12)", "语言模型\n(15-16)", "预训练\n(21)", "检索增强\n(30)", "对话智能体\n(37)"]
    w = 1.5; xs = [0.2 + i * 1.83 for i in range(7)]
    for s, x in zip(steps, xs):
        box(ax, x, 1.0, w, 0.9, s, fs=8.5)
    for i in range(6):
        arrow(ax, xs[i] + w + 0.02, 1.45, xs[i + 1] - 0.02, 1.45)
    save(fig, "图1-4.png")

# 2-1 Chomsky 层级
def fig_2_1():
    fig, ax = plt.subplots(figsize=(8, 5)); base(ax, (0, 10), (0, 6), "Chomsky 层级")
    layers = [("0型 递归可枚举（图灵机）", 8.4), ("1型 上下文相关（线性有界自动机）", 6.9),
              ("2型 上下文无关（下推自动机）", 5.4), ("3型 正则（有限自动机）", 3.9)]
    colors = ["#EEEEEE", LIGHT, LGREEN, LAMBER]
    for (name, width), c in zip(layers, colors):
        y = 4.9 - layers.index((name, width)) * 0.95
        box(ax, 5 - width / 2, y, width, 0.8, name, fc=c, fs=10)
    save(fig, "图2-1.png")

# 2-2 CFG 派生树
def fig_2_2():
    fig, ax = plt.subplots(figsize=(7, 5.5)); base(ax, (0, 10), (0, 7), "CFG 派生树（a + a × a）")
    nodes = {"S": (5, 6), "E": (5, 5), "E+T": (2.5, 4), "T": (7.5, 4), "T": (2.5, 3),
             "F": (7.5, 3), "a": (1.5, 2), "+": (3.5, 2), "T": (6.5, 2), "×": (8.5, 2),
             "F": (5.8, 1), "a": (7.2, 1), "a": (5.3, 0.2), "a": (6.3, 0.2)}
    # 简化示意
    tree = [("S", 5, 6.0), ("E", 5, 5.0), ("E+T", 2.5, 4.0), ("T", 7.5, 4.0),
            ("a", 1.5, 3.0), ("+", 3.5, 3.0), ("T×F", 7.5, 3.0),
            ("a", 6.5, 2.0), ("×", 8.5, 2.0), ("a", 7.5, 2.0)]
    for name, x, y in tree:
        box(ax, x - 0.6, y - 0.3, 1.2, 0.55, name, fs=9)
    edges = [(0,1),(1,2),(1,3),(2,4),(2,5),(3,6),(6,7),(6,8),(6,9)]
    for a_, b_ in edges:
        xa, ya = tree[a_][1], tree[a_][2] - 0.3
        xb, yb = tree[b_][1], tree[b_][2] + 0.25
        arrow(ax, xa, ya, xb, yb, color=GRAY)
    save(fig, "图2-2.png")

# 4-1 意义五层与篇目映射
def fig_4_1():
    fig, ax = plt.subplots(figsize=(10, 5)); base(ax, (0, 12), (0, 6), "意义五层与全书篇目映射")
    rows = [("M1 形式", "第2、10、11章", LIGHT), ("M2 分布", "第6、7、15-21章", LGREEN),
            ("M3 组合", "第12、13章", LAMBER), ("M4 指称", "第13、36章", LRED),
            ("M5 语用", "第14、28、37章", "#F0EAF7")]
    for i, (name, ch, c) in enumerate(rows):
        y = 5.0 - i * 0.95
        box(ax, 0.5, y, 2.6, 0.75, name, fc=c, fs=10.5)
        box(ax, 3.6, y, 5.5, 0.75, ch, fc="white", fs=10)
    ax.text(9.8, 3.0, "三个混淆命题：\n形式≠语义\n分布≠意义\n流畅≠忠实", fontsize=9, color=GRAY, va="center")
    save(fig, "图4-1.png")

# 5-1 词汇语义关系网络
def fig_5_1():
    fig, ax = plt.subplots(figsize=(8, 6)); base(ax, (0, 10), (0, 7), "词汇语义关系网络")
    pos = {"动物": (5, 5.5), "狗": (3, 3.8), "猫": (7, 3.8), "宠物": (5, 2.2), "狼": (1.5, 1.5)}
    for w, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.55, fc=LIGHT, ec=BLUE, lw=1.4))
        ax.text(x, y, w, ha="center", va="center", fontsize=11)
    edges = [("动物","狗","上位"), ("动物","猫","上位"), ("动物","狼","上位"), ("狗","宠物","相关"), ("猫","宠物","相关")]
    for a_, b_, t in edges:
        arrow(ax, *pos[a_], *pos[b_], text=t, color=GRAY, fs=8)
    save(fig, "图5-1.png")

# 6-2 word2vec 架构
def fig_6_2():
    fig, ax = plt.subplots(figsize=(11, 4)); base(ax, (0, 11), (0, 4), "word2vec：CBOW 与 Skip-gram")
    # CBOW
    ax.text(2.7, 3.5, "CBOW（上下文→中心）", ha="center", fontsize=11, weight="bold", color=GREEN)
    for i, x in enumerate([1.0, 1.8, 2.6]):
        box(ax, x, 1.6, 0.7, 0.6, f"w{i+1}", fc=LIGHT, fs=9)
        arrow(ax, x + 0.35, 1.6, 2.7, 0.8, color=GREEN)
    box(ax, 2.35, 0.3, 0.7, 0.5, "中心", fc=LGREEN, fs=9)
    # Skip-gram
    ax.text(8.0, 3.5, "Skip-gram（中心→上下文）", ha="center", fontsize=11, weight="bold", color=AMBER)
    box(ax, 7.65, 1.5, 0.7, 0.6, "中心", fc=LAMBER, fs=9)
    for i, x in enumerate([6.3, 8.8, 10.0]):
        arrow(ax, 8.0, 1.5, x + 0.35, 0.7, color=AMBER)
        box(ax, x, 0.2, 0.7, 0.5, f"w{i+1}", fc=LIGHT, fs=9)
    save(fig, "图6-2.png")

# 7-1 静态与上下文表示对比
def fig_7_1():
    fig, ax = plt.subplots(figsize=(10, 4.5)); base(ax, (0, 10), (0, 4.5), "静态词向量 vs 上下文表示")
    ax.text(2.5, 3.7, "静态（一词一向量）", ha="center", fontsize=11, weight="bold", color=BLUE)
    ax.add_patch(Circle((2.5, 2.2), 0.5, fc=LIGHT, ec=BLUE, lw=1.5))
    ax.text(2.5, 2.2, "银行", ha="center", va="center", fontsize=10)
    ax.text(2.5, 1.0, "金融义 / 河岸义\n挤在同一向量", ha="center", fontsize=9, color=GRAY)
    ax.text(7.5, 3.7, "上下文（随语境变化）", ha="center", fontsize=11, weight="bold", color=GREEN)
    ax.add_patch(Circle((6.3, 2.4), 0.45, fc=LGREEN, ec=GREEN, lw=1.5))
    ax.add_patch(Circle((8.7, 2.4), 0.45, fc=LAMBER, ec=AMBER, lw=1.5))
    ax.text(6.3, 2.4, "银行1", ha="center", va="center", fontsize=10)
    ax.text(8.7, 2.4, "银行2", ha="center", va="center", fontsize=10)
    ax.text(6.3, 1.5, "存款语境", ha="center", fontsize=9, color=GRAY)
    ax.text(8.7, 1.5, "河岸语境", ha="center", fontsize=9, color=GRAY)
    save(fig, "图7-1.png")

# 7-2 ELMo
def fig_7_2():
    fig, ax = plt.subplots(figsize=(9, 4)); base(ax, (0, 10), (0, 4), "ELMo 的双向 LM 表示")
    ax.text(5, 3.4, "词序列 w1 w2 w3 w4", ha="center", fontsize=10, color=GRAY)
    box(ax, 0.8, 1.5, 3.0, 0.7, "前向 LSTM（左→右）", fc=LIGHT, fs=10)
    box(ax, 6.2, 1.5, 3.0, 0.7, "后向 LSTM（右→左）", fc=LGREEN, fs=10)
    arrow(ax, 3.8, 1.85, 5.0, 1.85, color=BLUE)
    arrow(ax, 6.2, 1.85, 5.0, 1.85, color=GREEN)
    box(ax, 4.0, 0.5, 2.0, 0.6, "拼接 + 层加权", fc=LAMBER, fs=10)
    ax.text(5, 0.2, "→ ELMo 表示", ha="center", fontsize=9, color=GRAY)
    save(fig, "图7-2.png")

# 8-1 HMM
def fig_8_1():
    fig, ax = plt.subplots(figsize=(9, 3.5)); base(ax, (0, 10), (0, 3.5), "HMM 的序列标注")
    labels = ["y1", "y2", "y3", "y4"]; obs = ["x1", "x2", "x3", "x4"]
    xs = [1.5, 3.8, 6.1, 8.4]
    for x, l, o in zip(xs, labels, obs):
        ax.add_patch(Circle((x, 2.2), 0.35, fc=LIGHT, ec=BLUE, lw=1.3))
        ax.text(x, 2.2, l, ha="center", va="center", fontsize=10)
        box(ax, x - 0.35, 0.7, 0.7, 0.5, o, fc="white", fs=9)
        arrow(ax, x, 1.85, x, 1.2, color=GRAY)  # 发射
    for i in range(3):
        arrow(ax, xs[i] + 0.35, 2.2, xs[i+1] - 0.35, 2.2, color=GREEN)  # 转移
    ax.text(5, 0.25, "状态间转移（上）+ 状态到观测的发射（下）", ha="center", fontsize=9, color=GRAY)
    save(fig, "图8-1.png")

# 8-2 CRF
def fig_8_2():
    fig, ax = plt.subplots(figsize=(9, 3.5)); base(ax, (0, 10), (0, 3.5), "CRF 的序列标注")
    xs = [1.5, 3.8, 6.1, 8.4]
    for x in xs:
        box(ax, x - 0.5, 1.6, 1.0, 0.6, "yi", fc=LGREEN, fs=10)
    # 转移矩阵示意
    for i in range(3):
        arrow(ax, xs[i] + 0.5, 1.9, xs[i+1] - 0.5, 1.9, text="Aij", color=GREEN, fs=8)
    ax.text(5, 0.7, "判别式 P(y|x)：标签间转移 + 任意观测特征（非线性依赖）",
            ha="center", fontsize=9.5, color=GRAY)
    save(fig, "图8-2.png")

# 10-1 成分句法树
def fig_10_1():
    fig, ax = plt.subplots(figsize=(7, 5.5)); base(ax, (0, 10), (0, 7), "成分句法树")
    nodes = [("S", 5, 6.2), ("NP", 2.5, 5), ("VP", 7, 5), ("我", 2.5, 3.8),
             ("V", 6, 3.8), ("NP", 8, 3.8), ("喜欢", 6, 2.6), ("自然语言", 8, 2.6)]
    for name, x, y in nodes:
        box(ax, x - 0.7, y - 0.3, 1.4, 0.6, name, fc=LIGHT if name in ["S","NP","VP","V"] else "white", fs=9.5)
    edges = [(0,1),(0,2),(1,3),(2,4),(2,5),(4,6),(5,7)]
    for a_, b_ in edges:
        arrow(ax, nodes[a_][1], nodes[a_][2]-0.3, nodes[b_][1], nodes[b_][2]+0.3, color=GRAY)
    save(fig, "图10-1.png")

# 10-2 依存句法树
def fig_10_2():
    fig, ax = plt.subplots(figsize=(8, 3)); base(ax, (0, 10), (0, 3), "依存句法树")
    xs = [1.5, 4, 6.5, 8.8]; words = ["我", "喜欢", "自然语言", "。"]
    for x, w in zip(xs, words):
        ax.text(x, 1.0, w, ha="center", fontsize=12)
    ax.annotate("", xy=(4, 1.3), xytext=(4, 2.4), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))
    ax.text(4.2, 2.0, "ROOT", fontsize=9, color=BLUE)
    ax.annotate("", xy=(4, 1.3), xytext=(1.5, 1.3), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5, connectionstyle="arc3,rad=0.2"))
    ax.text(2.2, 1.6, "nsubj", fontsize=8.5, color=GREEN)
    ax.annotate("", xy=(6.5, 1.3), xytext=(4, 1.3), arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.5))
    ax.text(5.0, 1.5, "obj", fontsize=8.5, color=AMBER)
    save(fig, "图10-2.png")

# 10-3 句法歧义两棵树（简化）
def fig_10_3():
    fig, ax = plt.subplots(figsize=(10, 4)); base(ax, (0, 12), (0, 4), "句法歧义：附着歧义的两种树")
    ax.text(3, 3.2, "读法1：我用望远镜看", ha="center", fontsize=10, color=GREEN)
    ax.text(9, 3.2, "读法2：带望远镜的男人", ha="center", fontsize=10, color=AMBER)
    for cx, c in [(3, GREEN), (9, AMBER)]:
        box(ax, cx-1.5, 1.8, 3, 0.7, "VP: saw [PP]", fc=LGREEN if c==GREEN else LAMBER, fs=10)
        box(ax, cx-1.5, 0.7, 3, 0.7, "PP 附着对象不同", fc="white", fs=9)
        arrow(ax, cx, 1.8, cx, 1.4, color=c)
    save(fig, "图10-3.png")

# 11-2 移进归约
def fig_11_2():
    fig, ax = plt.subplots(figsize=(10, 3.5)); base(ax, (0, 11), (0, 3.5), "移进归约算法")
    box(ax, 0.5, 1.2, 3.5, 1.0, "栈：S / NP / V", fc=LIGHT, fs=10)
    box(ax, 6.5, 1.2, 3.5, 1.0, "输入缓冲：w1 w2 w3 …", fc=LGREEN, fs=10)
    arrow(ax, 6.5, 1.7, 4.2, 1.7, text="SHIFT", color=BLUE, fs=9)
    arrow(ax, 4.2, 1.2, 6.5, 1.2, text="REDUCE", color=AMBER, fs=9, rad=0.3)
    save(fig, "图11-2.png")

# 12-1 语义角色标注
def fig_12_1():
    fig, ax = plt.subplots(figsize=(9, 4)); base(ax, (0, 10), (0, 4), "语义角色标注（谓词：开）")
    box(ax, 4.0, 2.0, 2.0, 0.8, "开（谓词）", fc=LAMBER, fs=11)
    roles = [("张三", "ARG0 施事", 1.0, GREEN), ("门", "ARG1 受事", 7.0, BLUE),
             ("钥匙", "ARG2 工具", 1.0, AMBER), ("昨天", "AM-TMP", 7.0, GRAY)]
    for w, r, x, c in roles:
        y = 0.5 if x == 1.0 else 0.5
        box(ax, x, y, 2.0, 0.7, f"{w}\n{r}", fc="white", ec=c, fs=9)
    save(fig, "图12-1.png")

# 12-2 AMR
def fig_12_2():
    fig, ax = plt.subplots(figsize=(8, 4.5)); base(ax, (0, 10), (0, 5), "AMR 抽象意义表示")
    nodes = {"want": (5, 4), "person": (2.5, 2.5), "open": (6.5, 2.5), "door": (6.5, 1)}
    for name, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 0.5, fc=LIGHT, ec=BLUE, lw=1.4))
        ax.text(x, y, name, ha="center", va="center", fontsize=9.5)
    ax.text(3.5, 3.4, ":ARG0", fontsize=8.5, color=GREEN)
    arrow(ax, 4.6, 3.8, 3.0, 2.9, color=GREEN)
    ax.text(6.2, 3.4, ":ARG1", fontsize=8.5, color=AMBER)
    arrow(ax, 5.4, 3.8, 6.2, 2.9, color=AMBER)
    ax.text(7.1, 1.7, ":ARG1", fontsize=8.5, color=GRAY)
    arrow(ax, 6.5, 2.0, 6.5, 1.5, color=GRAY)
    save(fig, "图12-2.png")

# 13-1 λ-演算组合推导
def fig_13_1():
    fig, ax = plt.subplots(figsize=(11, 4)); base(ax, (0, 12), (0, 4), "λ-演算组合推导")
    steps = ["词项 λ-项", "函数应用", "β-归约", "整句逻辑形式"]
    xs = [0.3, 3.3, 6.3, 9.3]
    for s, x in zip(steps, xs):
        box(ax, x, 1.3, 2.4, 1.0, s, fc=LIGHT if x<9 else LGREEN, fs=10)
    for i in range(3):
        arrow(ax, xs[i]+2.45, 1.8, xs[i+1]-0.05, 1.8)
    save(fig, "图13-1.png")

# 16-1 前馈神经语言模型
def fig_16_1():
    fig, ax = plt.subplots(figsize=(10, 4)); base(ax, (0, 11), (0, 4), "前馈神经语言模型（NNLM）")
    box(ax, 0.5, 1.5, 2.2, 1.0, "词嵌入\n(拼接)", fc=LIGHT, fs=10)
    box(ax, 4.2, 1.5, 2.2, 1.0, "隐藏层\ntanh", fc=LGREEN, fs=10)
    box(ax, 8.0, 1.5, 2.2, 1.0, "输出层\nsoftmax", fc=LAMBER, fs=10)
    arrow(ax, 2.7, 2.0, 4.2, 2.0); arrow(ax, 6.4, 2.0, 8.0, 2.0)
    save(fig, "图16-1.png")

# 16-2 RNN 展开
def fig_16_2():
    fig, ax = plt.subplots(figsize=(10, 3.2)); base(ax, (0, 11), (0, 3.2), "RNN 语言模型（沿时间展开）")
    xs = [1.5, 4, 6.5, 9]
    for i, x in enumerate(xs):
        box(ax, x-0.7, 1.4, 1.4, 0.8, f"h{i+1}", fc=LIGHT, fs=10)
        ax.text(x, 0.7, f"w{i+1}", ha="center", fontsize=10, color=GRAY)
        arrow(ax, x, 1.2, x, 0.9, color=GRAY)
    for i in range(3):
        arrow(ax, xs[i]+0.7, 1.8, xs[i+1]-0.7, 1.8, color=GREEN)
    save(fig, "图16-2.png")

# 17-1 编码器-解码器
def fig_17_1():
    fig, ax = plt.subplots(figsize=(10, 4)); base(ax, (0, 11), (0, 4), "编码器—解码器（seq2seq）")
    box(ax, 0.5, 1.5, 2.5, 1.0, "编码器\n(读入 x)", fc=LIGHT, fs=10)
    box(ax, 4.0, 1.5, 2.0, 1.0, "上下文 c", fc=LAMBER, fs=10)
    box(ax, 6.8, 1.5, 2.5, 1.0, "解码器\n(生成 y)", fc=LGREEN, fs=10)
    arrow(ax, 3.0, 2.0, 4.0, 2.0); arrow(ax, 6.0, 2.0, 6.8, 2.0)
    save(fig, "图17-1.png")

# 17-2 注意力对齐热图
def fig_17_2():
    fig, ax = plt.subplots(figsize=(6.5, 5))
    import numpy as np
    A = np.array([[0.7,0.2,0.1],[0.15,0.6,0.25],[0.1,0.2,0.7]])
    im = ax.imshow(A, cmap="Blues")
    ax.set_xticks(range(3)); ax.set_xticklabels(["我","爱","NLP"])
    ax.set_yticks(range(3)); ax.set_yticklabels(["I","love","NLP"])
    ax.set_xlabel("源语言", fontsize=10); ax.set_ylabel("目标语言", fontsize=10)
    ax.set_title("注意力对齐热图", fontsize=13, weight="bold", color=DARK)
    for i in range(3):
        for j in range(3):
            ax.text(j,i,f"{A[i,j]:.2f}",ha="center",va="center",
                    color="white" if A[i,j]>0.5 else DARK, fontsize=10)
    fig.colorbar(im, ax=ax, shrink=0.8)
    save(fig, "图17-2.png")

# 18-1 统计机器翻译流水线
def fig_18_1():
    fig, ax = plt.subplots(figsize=(13, 3)); base(ax, (0, 13), (0, 3), "统计机器翻译流水线")
    steps = ["词对齐", "短语抽取", "调序", "语言模型", "解码输出"]
    xs = [0.3 + i*2.55 for i in range(5)]
    for s, x in zip(steps, xs):
        box(ax, x, 1.0, 2.1, 0.9, s, fc=LIGHT if x<8 else LGREEN, fs=10)
    for i in range(4):
        arrow(ax, xs[i]+2.15, 1.45, xs[i+1]-0.05, 1.45)
    save(fig, "图18-1.png")

# 19-1 预训练范式演进
def fig_19_1():
    fig, ax = plt.subplots(figsize=(11, 3.5)); base(ax, (0, 12), (0, 3.5), "预训练前夜的范式演进")
    steps = ["词向量\n(固定特征)", "上下文表示\n(附加特征)", "通用句子编码", "预训练+微调\n(可训练参数)"]
    xs = [0.3, 3.3, 6.3, 9.3]
    for s, x in zip(steps, xs):
        box(ax, x, 1.2, 2.4, 1.0, s, fc=LIGHT if x<9 else LGREEN, fs=9.5)
    for i in range(3):
        arrow(ax, xs[i]+2.45, 1.7, xs[i+1]-0.05, 1.7)
    save(fig, "图19-1.png")

# 20-1 缩放点积注意力
def fig_20_1():
    fig, ax = plt.subplots(figsize=(10, 4.5)); base(ax, (0, 11), (0, 4.5), "缩放点积注意力")
    box(ax, 0.5, 2.5, 1.6, 0.7, "Q", fc=LIGHT, fs=12)
    box(ax, 0.5, 1.4, 1.6, 0.7, "K", fc=LGREEN, fs=12)
    box(ax, 0.5, 0.3, 1.6, 0.7, "V", fc=LAMBER, fs=12)
    box(ax, 3.0, 2.0, 2.2, 0.8, "Q·K^T/√dk", fc="white", fs=10)
    box(ax, 6.0, 2.0, 1.8, 0.8, "softmax", fc="white", fs=10)
    box(ax, 8.5, 1.0, 2.0, 0.8, "×V 输出", fc=LGREEN, fs=10)
    arrow(ax, 2.1, 2.8, 3.0, 2.5, color=BLUE)
    arrow(ax, 2.1, 1.75, 3.0, 2.3, color=GREEN)
    arrow(ax, 5.2, 2.4, 6.0, 2.4)
    arrow(ax, 7.8, 2.4, 9.0, 1.7, color=AMBER)
    arrow(ax, 2.1, 0.65, 8.8, 1.2, color=AMBER, rad=0.15, ls="--")
    save(fig, "图20-1.png")

# 20-2 Transformer 架构
def fig_20_2():
    fig, ax = plt.subplots(figsize=(10, 6)); base(ax, (0, 11), (0, 6.5), "Transformer 整体架构")
    box(ax, 0.5, 3.0, 4.2, 2.4, "编码器 ×N\n自注意力 → FFN", fc=LIGHT, fs=11)
    box(ax, 6.3, 3.0, 4.2, 2.4, "解码器 ×N\n掩码注意力→交叉注意力→FFN", fc=LGREEN, fs=10)
    arrow(ax, 4.7, 4.2, 6.3, 4.2, text="K,V", color=BLUE, fs=9)
    box(ax, 3.5, 0.5, 4.0, 1.0, "输出层（线性 + softmax）", fc=LAMBER, fs=10)
    arrow(ax, 8.4, 3.0, 6.0, 1.5, color=GREEN)
    save(fig, "图20-2.png")

# 21-1 三种预训练范式
def fig_21_1():
    fig, ax = plt.subplots(figsize=(11, 4.5)); base(ax, (0, 12), (0, 4.5), "三种预训练范式")
    cards = [("GPT\n自回归", "单向·生成", LIGHT, BLUE),
             ("BERT\n自编码 MLM", "双向·理解", LGREEN, GREEN),
             ("T5\nseq2seq", "文本到文本", LAMBER, AMBER)]
    for i, (t, s, fc, ec) in enumerate(cards):
        x = 0.5 + i*3.9
        box(ax, x, 1.5, 3.4, 1.8, t+"\n"+s, fc=fc, ec=ec, fs=11)
    save(fig, "图21-1.png")

# 21-2 掩码语言模型
def fig_21_2():
    fig, ax = plt.subplots(figsize=(10, 3)); base(ax, (0, 11), (0, 3), "掩码语言模型（BERT）")
    toks = ["我", "[MASK]", "自然", "语言"]
    xs = [1.0, 3.2, 5.4, 7.6]
    for x, t in zip(xs, toks):
        box(ax, x, 1.3, 1.8, 0.8, t, fc=LRED if t=="[MASK]" else LIGHT,
            ec=RED if t=="[MASK]" else BLUE, fs=11)
    ax.annotate("双向上下文预测 → \"喜欢\"", xy=(4.1, 1.3), xytext=(9.5, 2.3),
                fontsize=10, color=GRAY, ha="center", arrowprops=dict(arrowstyle="->", color=GRAY))
    save(fig, "图21-2.png")

# 23-1 LoRA
def fig_23_1():
    fig, ax = plt.subplots(figsize=(10, 4)); base(ax, (0, 11), (0, 4), "LoRA 低秩适配")
    box(ax, 3.5, 2.4, 4.0, 1.0, "冻结权重 W0（d×k）", fc="#EEEEEE", ec=GRAY, fs=11)
    box(ax, 1.5, 0.5, 2.2, 0.8, "A（r×k）", fc=LIGHT, fs=10)
    box(ax, 7.3, 0.5, 2.2, 0.8, "B（d×r）", fc=LGREEN, fs=10)
    arrow(ax, 4.5, 2.4, 2.6, 1.3, color=BLUE)
    arrow(ax, 3.7, 0.9, 7.3, 0.9, color=GREEN)
    arrow(ax, 8.4, 1.3, 6.5, 2.4, color=GREEN)
    ax.text(5.5, 0.15, "W = W0 + (α/r)·BA，只训练 A、B", ha="center", fontsize=9.5, color=GRAY)
    save(fig, "图23-1.png")

# 26-1 规模化定律
def fig_26_1():
    fig, ax = plt.subplots(figsize=(7, 5))
    import numpy as np
    N = np.logspace(7, 11, 50)
    L = 2.0 + 10 * N ** (-0.076)
    ax.loglog(N, L, color=BLUE, lw=2)
    ax.set_xlabel("参数量 N", fontsize=11); ax.set_ylabel("损失 L", fontsize=11)
    ax.set_title("规模化定律：损失随参数幂律下降", fontsize=13, weight="bold", color=DARK)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    save(fig, "图26-1.png")

# 28-1 RLHF
def fig_28_1():
    fig, ax = plt.subplots(figsize=(12, 3.2)); base(ax, (0, 13), (0, 3.2), "RLHF 三阶段流程")
    steps = ["① SFT\n示范微调", "② 奖励模型\n学人类偏好", "③ PPO 优化\n+ KL 惩罚"]
    xs = [0.3, 4.6, 8.9]
    for s, x in zip(steps, xs):
        box(ax, x, 1.0, 3.4, 1.2, s, fc=LIGHT if x<8 else LGREEN, fs=10)
    for i in range(2):
        arrow(ax, xs[i]+3.45, 1.6, xs[i+1]-0.05, 1.6)
    save(fig, "图28-1.png")

# 28-2 RLHF vs DPO
def fig_28_2():
    fig, ax = plt.subplots(figsize=(10, 4)); base(ax, (0, 11), (0, 4), "RLHF 与 DPO 对照")
    box(ax, 0.5, 2.2, 4.5, 1.2, "RLHF：SFT → RM → PPO\n（三阶段）", fc=LIGHT, fs=10)
    box(ax, 6.0, 2.2, 4.5, 1.2, "DPO：直接用偏好数据\n优化策略（单阶段）", fc=LGREEN, fs=10)
    ax.text(5.5, 0.8, "理论等价，DPO 更简单稳定", ha="center", fontsize=10, color=GRAY)
    save(fig, "图28-2.png")

# 30-1 RAG
def fig_30_1():
    fig, ax = plt.subplots(figsize=(12, 3.5)); base(ax, (0, 13), (0, 3.5), "RAG 架构")
    box(ax, 0.3, 1.3, 2.0, 0.9, "查询 q", fc=LIGHT, fs=10)
    box(ax, 3.0, 1.3, 2.2, 0.9, "检索器", fc=LGREEN, fs=10)
    box(ax, 5.9, 2.2, 2.6, 0.8, "文档库 K", fc=LAMBER, fs=10)
    box(ax, 9.0, 1.3, 3.3, 0.9, "生成器（LLM）\n→ 带依据答案", fc=LIGHT, fs=10)
    arrow(ax, 2.3, 1.75, 3.0, 1.75)
    arrow(ax, 5.2, 1.75, 5.9, 2.5, color=GREEN)
    arrow(ax, 7.2, 2.2, 9.2, 1.9, color=AMBER)
    arrow(ax, 5.2, 1.6, 9.0, 1.6, color=GRAY, rad=0.1, ls="--")
    save(fig, "图30-1.png")

# 32-1 视觉-语言桥接
def fig_32_1():
    fig, ax = plt.subplots(figsize=(11, 3.2)); base(ax, (0, 12), (0, 3.2), "视觉—语言模型桥接")
    box(ax, 0.3, 1.1, 2.0, 0.9, "图像", fc=LIGHT, fs=10)
    box(ax, 3.0, 1.1, 2.2, 0.9, "视觉编码器\nViT", fc=LGREEN, fs=10)
    box(ax, 5.9, 1.1, 2.2, 0.9, "投影层\nConnector", fc=LAMBER, fs=10)
    box(ax, 8.8, 1.1, 2.8, 0.9, "语言模型 LLM\n→ 回答", fc=LIGHT, fs=10)
    arrow(ax, 2.3, 1.55, 3.0, 1.55); arrow(ax, 5.2, 1.55, 5.9, 1.55)
    arrow(ax, 8.1, 1.55, 8.8, 1.55)
    save(fig, "图32-1.png")

# 34-1 文生图扩散
def fig_34_1():
    fig, ax = plt.subplots(figsize=(11, 3.2)); base(ax, (0, 12), (0, 3.2), "文生图：文本条件引导的扩散生成")
    box(ax, 0.3, 2.2, 2.5, 0.8, "文本 prompt", fc=LIGHT, fs=10)
    ax.text(5.5, 2.9, "逐步去噪 q → x0", ha="center", fontsize=10, color=GRAY)
    stages = ["噪声 xT", "…", "图像 x0"]
    xs = [3.2, 6.0, 8.8]
    for s, x in zip(stages, xs):
        box(ax, x, 0.9, 2.0, 0.9, s, fc=LAMBER if s=="噪声 xT" else LGREEN, fs=10)
    arrow(ax, 2.8, 2.6, 4.0, 1.8, color=AMBER)
    for i in range(2):
        arrow(ax, xs[i]+2.05, 1.35, xs[i+1]-0.05, 1.35)
    save(fig, "图34-1.png")

# 35-1 原生多模态统一架构
def fig_35_1():
    fig, ax = plt.subplots(figsize=(11, 5)); base(ax, (0, 12), (0, 5), "原生多模态统一架构")
    mods = [("文本", 0.5, LIGHT), ("图像", 0.5, LGREEN), ("音频", 0.5, LAMBER)]
    for i, (name, x, fc) in enumerate(mods):
        y = 3.6 - i*1.0
        box(ax, 0.5, y, 1.8, 0.7, name, fc=fc, fs=10)
        arrow(ax, 2.3, y+0.35, 4.5, 2.4, color=GRAY)
    box(ax, 4.5, 1.9, 3.0, 1.0, "统一 token 空间", fc="#F0EAF7", ec=BLUE, fs=11)
    box(ax, 8.5, 1.9, 3.0, 1.0, "单一 Transformer", fc=LIGHT, fs=11)
    arrow(ax, 7.5, 2.4, 8.5, 2.4)
    save(fig, "图35-1.png")

# 42-1 全书框架回扣
def fig_42_1():
    fig, ax = plt.subplots(figsize=(10, 5)); base(ax, (0, 12), (0, 6), "全书框架回扣：九篇 × 四层 × 五层")
    rows = [("第一至五篇", "分析·生成", "M1–M2"), ("第六篇", "生成·交互", "M2–M3"),
            ("第七篇", "分析·生成", "跨模态"), ("第八篇", "交互·应用", "M4–M5"),
            ("第九篇", "反思", "框架回扣")]
    for i, (p, l, m) in enumerate(rows):
        y = 5.0 - i*0.95
        box(ax, 0.5, y, 3.0, 0.75, p, fc=LIGHT, fs=10)
        box(ax, 4.0, y, 3.0, 0.75, l, fc=LGREEN, fs=10)
        box(ax, 7.5, y, 3.0, 0.75, m, fc=LAMBER, fs=10)
    save(fig, "图42-1.png")


if __name__ == "__main__":
    figs = [fig_1_1, fig_1_2, fig_1_3, fig_1_4, fig_2_1, fig_2_2, fig_4_1,
            fig_5_1, fig_6_2, fig_7_1, fig_7_2, fig_8_1, fig_8_2,
            fig_10_1, fig_10_2, fig_10_3, fig_11_2, fig_12_1, fig_12_2,
            fig_13_1, fig_16_1, fig_16_2, fig_17_1, fig_17_2, fig_18_1,
            fig_19_1, fig_20_1, fig_20_2, fig_21_1, fig_21_2, fig_23_1,
            fig_26_1, fig_28_1, fig_28_2, fig_30_1, fig_32_1, fig_34_1,
            fig_35_1, fig_42_1]
    for fn in figs:
        try:
            fn()
        except Exception as e:
            print("失败:", fn.__name__, e)
    print("概念图生成完成")
