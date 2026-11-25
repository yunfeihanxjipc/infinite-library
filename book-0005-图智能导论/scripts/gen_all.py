# -*- coding: utf-8 -*-
"""《图智能导论》配图脚本。运行: python scripts/gen_all.py

用 matplotlib 为正文引用的全部图号生成「学术风格概念图」，
输出到 figures/图X-Y.png，文件名严格匹配正文引用。
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.max_open_warning"] = 60

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "figures")
os.makedirs(OUT, exist_ok=True)

# 统一配色
BLUE = "#2C5F8A"
LIGHT = "#E8F0F7"
GREEN = "#2E7D5B"
LGREEN = "#E6F2EA"
AMBER = "#B07D2B"
LAMBER = "#F8EFDD"
RED = "#A33B3B"
LRED = "#F7E9E9"
PURPLE = "#6A4C93"
LPURPLE = "#F0EAF7"
GRAY = "#5A5A5A"
DARK = "#1A3350"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("已生成:", name)


def base(ax, xlim, ylim, title):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.text(sum(xlim) / 2, ylim[1] - 0.05, title, ha="center", va="top",
            fontsize=15, weight="bold", color=DARK)


# ---------- 通用辅助函数 ----------

def draw_box(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=10, tc=DARK, lw=1.2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=lw, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, linespacing=1.2)


def draw_arrow(ax, x1, y1, x2, y2, color=BLUE, rad=0, fs=None, label=None, lw=1.3):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13,
        linewidth=lw, color=color, connectionstyle=f"arc3,rad={rad}"))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.08, label,
                ha="center", va="bottom", fontsize=fs or 9, color=GRAY)


def draw_flow(name, title, steps, colors=None, fs=10, figsize=(11, 3.6)):
    """水平流程：steps 为字符串列表，colors 为等长配色列表。"""
    fig, ax = plt.subplots(figsize=figsize)
    xlim, ylim = (0, 12), (0, 3.6)
    base(ax, xlim, ylim, title)
    n = len(steps)
    margin = 0.3
    gap = 0.35
    w = (12 - 2 * margin - gap * (n - 1)) / n
    xs = [margin + i * (w + gap) for i in range(n)]
    colors = colors or [LIGHT] * n
    y, h = 1.35, 1.0
    for s, x, c in zip(steps, xs, colors):
        draw_box(ax, x, y, w, h, s, fc=c, fs=fs)
    for i in range(n - 1):
        draw_arrow(ax, xs[i] + w + 0.02, y + h / 2, xs[i + 1] - 0.04, y + h / 2)
    save(fig, name)


def draw_layers(name, title, layers, figsize=(8, 5.2)):
    """垂直层级堆叠：layers 为 (标签, 配色) 列表，自下而上。"""
    fig, ax = plt.subplots(figsize=figsize)
    base(ax, (0, 10), (0, 8), title)
    n = len(layers)
    h = 1.0
    gap = 0.18
    total = n * h + (n - 1) * gap
    y0 = (7.0 - total) / 2
    w = 6.0
    x = (10 - w) / 2
    for i, (label, fc) in enumerate(layers):
        draw_box(ax, x, y0 + i * (h + gap), w, h, label, fc=fc, fs=11)
    save(fig, name)


def draw_network(name, title, nodes, edges, node_colors=None, labels=None,
                 seed=0, figsize=(8, 5)):
    """网络节点连线图。nodes: {id:(x,y)}; edges: [(u,v),...]。"""
    fig, ax = plt.subplots(figsize=figsize)
    base(ax, (0, 10), (0, 7), title)
    node_colors = node_colors or {}
    for u, v in edges:
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        draw_arrow(ax, x1, y1, x2, y2, color=GRAY, lw=1.1, rad=0.0)
    for nid, (x, y) in nodes.items():
        fc = node_colors.get(nid, LIGHT)
        ax.add_patch(Circle((x, y), 0.42, fc=fc, ec=BLUE, lw=1.4, zorder=3))
        ax.text(x, y, labels.get(nid, str(nid)) if labels else str(nid),
                ha="center", va="center", fontsize=10, color=DARK, zorder=4)
    save(fig, name)


def draw_curve(name, title, curves, xlabel="", ylabel="", xlim=(0, 10), ylim=(0, 1),
               figsize=(7.2, 4.6)):
    """多条曲线：curves 为 (x, y, 颜色, 标签) 列表。"""
    fig, ax = plt.subplots(figsize=figsize)
    for x, y, c, lab in curves:
        ax.plot(x, y, "o-" if len(x) <= 12 else "-", color=c, lw=2,
                markersize=5, label=lab)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=14, weight="bold", color=DARK)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.grid(True, ls=":", alpha=0.4)
    if any(lab for _, _, _, lab in curves):
        ax.legend(fontsize=9, loc="best")
    save(fig, name)


def ring_nodes(ax, cx, cy, r, n, texts, fc=LIGHT, ec=BLUE, fs=9, r_node=0.45):
    pts = []
    for i in range(n):
        ang = 2 * math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    pts2 = pts
    for i in range(n):
        x, y = pts2[i]
        ax.add_patch(Circle((x, y), r_node, fc=fc, ec=ec, lw=1.3, zorder=3))
        ax.text(x, y, texts[i] if i < len(texts) else str(i),
                ha="center", va="center", fontsize=fs, color=DARK, zorder=4)
    return pts2


# ================= 各图绘制函数 =================

def fig_1_1():
    """图 1-1 图智能四层能力与全书篇章地图"""
    fig, ax = plt.subplots(figsize=(11, 4.6))
    base(ax, (0, 12), (0, 4.6), "图智能四层能力与全书篇章地图")
    items = [("基础理论", "图论/谱/游走", LIGHT),
             ("表示学习", "嵌入/GNN/等变", LGREEN),
             ("系统与训练", "预训练/基础模型", LAMBER),
             ("应用与前沿", "分子/推荐/世界模型", LPURPLE)]
    xs = [0.4, 3.4, 6.4, 9.4]
    for (name, sub, fc), x in zip(items, xs):
        draw_box(ax, x, 1.7, 2.4, 1.1, name, fc=fc, fs=12)
        ax.text(x + 1.2, 1.4, sub, ha="center", fontsize=9, color=GRAY)
    for i in range(3):
        draw_arrow(ax, xs[i] + 2.45, 2.25, xs[i + 1] - 0.05, 2.25)
    ax.text(6, 0.45, "基础 -> 表示 -> 系统 -> 应用，层层递进", ha="center", fontsize=10, color=GRAY)
    save(fig, "图1-1.png")


def fig_2_1():
    """图 2-1 路径图 P4 与其三大矩阵"""
    fig, ax = plt.subplots(figsize=(10, 4.4))
    base(ax, (0, 12), (0, 4.4), "路径图 P4 与其三大矩阵")
    nodes = {1: (1.5, 2.6), 2: (3.2, 2.6), 3: (4.9, 2.6), 4: (6.6, 2.6)}
    nc = {1: LIGHT, 2: LGREEN, 3: LGREEN, 4: LIGHT}
    for u, v in [(1, 2), (2, 3), (3, 4)]:
        x1, y1 = nodes[u]; x2, y2 = nodes[v]
        draw_arrow(ax, x1 + 0.45, y1, x2 - 0.45, y2, color=BLUE, lw=1.5)
    for nid, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 0.42, fc=nc[nid], ec=BLUE, lw=1.4))
        ax.text(x, y, "v" + str(nid), ha="center", va="center", fontsize=11, color=DARK)
    draw_box(ax, 8.0, 2.9, 3.4, 1.0, "邻接矩阵 A\n(0/1 连接)", fc=LIGHT, fs=10)
    draw_box(ax, 8.0, 1.6, 3.4, 1.0, "度矩阵 D\n(对角)", fc=LGREEN, fs=10)
    draw_box(ax, 8.0, 0.3, 3.4, 1.0, "拉普拉斯 L = D - A", fc=LAMBER, fs=10)
    save(fig, "图2-1.png")


def fig_3_1():
    """图 3-1 图拉普拉斯谱与频率响应"""
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    k = np.arange(1, 11)
    low = 1.0 / (1.0 + k)
    high = k / (1.0 + k)
    draw_curve("图3-1.png", "图拉普拉斯谱与频率响应",
               [(k, low, BLUE, "低频(平滑)"), (k, high, AMBER, "高频(剧烈)")],
               xlabel="拉普拉斯特征向量序号", ylabel="频率响应", figsize=(7.6, 4.6))


def fig_4_1():
    """图 4-1 随机游走、PageRank 与图扩散"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图4-1.png", "随机游走、PageRank 与图扩散",
              ["随机游走", "转移矩阵 P", "平稳分布", "PageRank 排序", "图扩散"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_5_1():
    """图 5-1 传统图特征与图核"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图5-1.png", "传统图特征与图核",
              ["图/子图", "手工特征", "图核函数 K", "SVM 分类", "预测"],
              [LIGHT, LGREEN, LAMBER, LGREEN, LIGHT], fs=10)


def fig_6_1():
    """图 6-1 DeepWalk 与 node2vec"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图6-1.png", "DeepWalk 与 node2vec",
              ["图", "随机游走序列", "Skip-gram", "节点向量", "下游任务"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_7_1():
    """图 7-1 TransE、TransR 与 RotatE 的几何"""
    fig, ax = plt.subplots(figsize=(11, 4.3))
    base(ax, (0, 12), (0, 4.3), "TransE、TransR 与 RotatE 的几何")
    titles = [("TransE", "h + r ≈ t\n平移"),
              ("TransR", "在关系空间\n平移"),
              ("RotatE", "复数平面\n旋转")]
    xs = [0.4, 4.3, 8.2]
    for (t, s), x in zip(titles, xs):
        draw_box(ax, x, 1.4, 3.4, 1.8, t + "\n" + s, fc=LIGHT if x < 4 else LGREEN, fs=11)
    save(fig, "图7-1.png")


def fig_8_1():
    """图 8-1 欧氏与双曲嵌入对比"""
    fig, ax = plt.subplots(figsize=(9, 4.6))
    base(ax, (0, 12), (0, 4.6), "欧氏与双曲嵌入对比")
    draw_box(ax, 0.6, 1.2, 5.0, 2.4, "欧氏空间\n体积随半径多项式增长\n适合同质保真图", fc=LIGHT, fs=11)
    draw_box(ax, 6.4, 1.2, 5.0, 2.4, "双曲空间\n体积随半径指数增长\n适合树/层级结构", fc=LGREEN, fs=11)
    save(fig, "图8-1.png")


def fig_9_1():
    """图 9-1 标签传播过程"""
    fig, ax = plt.subplots(figsize=(8, 5))
    # 固定网格布局，避免随机排布造成节点重叠
    nodes = {0: (1.6, 1.2), 1: (1.6, 2.6), 2: (3.6, 3.6), 3: (5.6, 4.6),
             4: (7.6, 4.6), 5: (8.4, 2.6), 6: (3.6, 1.4), 7: (5.6, 1.4),
             8: (7.0, 1.4), 9: (3.6, 5.6), 10: (5.6, 6.0), 11: (7.6, 5.8)}
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 7),
             (7, 8), (2, 9), (9, 10), (10, 11), (5, 8)]
    nc = {}
    for i in nodes:
        nc[i] = LAMBER if i < 2 else (LGREEN if i < 5 else LIGHT)
    draw_network("图9-1.png", "标签传播过程", nodes, edges, node_colors=nc,
                 labels={i: ("L" if i < 2 else ("?" if i >= 5 else "~")) for i in nodes})


def fig_10_1():
    """图 10-1 消息传递框架"""
    fig, ax = plt.subplots(figsize=(11, 4.4))
    base(ax, (0, 12), (0, 4.4), "消息传递框架 (MPNN)")
    steps = [("消息 Message", LIGHT), ("聚合 Aggregate", LGREEN),
             ("更新 Update", LAMBER), ("读出 Readout", LPURPLE)]
    xs = [0.4, 3.4, 6.4, 9.4]
    for (t, fc), x in zip(steps, xs):
        draw_box(ax, x, 1.6, 2.4, 1.1, t, fc=fc, fs=11)
    for i in range(3):
        draw_arrow(ax, xs[i] + 2.45, 2.15, xs[i + 1] - 0.05, 2.15)
    draw_arrow(ax, 10.6, 1.6, 1.6, 1.6, color=GRAY, rad=0.25, label="K 层迭代")
    save(fig, "图10-1.png")


def fig_11_1():
    """图 11-1 谱卷积到 GCN 的演化"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图11-1.png", "谱卷积到 GCN 的演化",
              ["图谱卷积", "切比雪夫近似", "一阶近似", "GCN", "归一化邻接"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_12_1():
    """图 12-1 GAT 注意力机制"""
    fig, ax = plt.subplots(figsize=(8.5, 5))
    nodes = {0: (5.0, 1.4), 1: (2.0, 4.2), 2: (5.0, 4.8), 3: (8.0, 4.2)}
    edges = [(1, 0), (2, 0), (3, 0)]
    nc = {0: LAMBER, 1: LIGHT, 2: LIGHT, 3: LIGHT}
    fig, ax = plt.subplots(figsize=(8.5, 5))
    base(ax, (0, 10), (0, 7), "GAT 注意力机制")
    for u, v, a in [(1, 0, 0.2), (2, 0, 0.5), (3, 0, 0.3)]:
        x1, y1 = nodes[u]; x2, y2 = nodes[v]
        draw_arrow(ax, x1, y1, x2, y2, color=RED, lw=1.5 + 3 * a,
                   label="a=" + str(a))
    for nid, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 0.45, fc=nc[nid], ec=BLUE, lw=1.4, zorder=3))
        ax.text(x, y, {0: "i", 1: "j1", 2: "j2", 3: "j3"}[nid],
                ha="center", va="center", fontsize=11, color=DARK, zorder=4)
    ax.text(5, 0.4, "邻居权重由注意力系数 a_ij 决定", ha="center", fontsize=10, color=GRAY)
    save(fig, "图12-1.png")


def fig_13_1():
    """图 13-1 过平滑与缓解"""
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    layers = np.arange(1, 11)
    plain = np.exp(-layers / 2.5)
    resid = 0.3 + 0.7 * np.exp(-layers / 6.0)
    draw_curve("图13-1.png", "过平滑与缓解",
               [(layers, plain, RED, "普通 GCN(过平滑)"),
                (layers, resid, GREEN, "残差/归一化(缓解)")],
               xlabel="网络层数", ylabel="节点区分度", figsize=(7.6, 4.6))


def fig_14_1():
    """图 14-1 读出与层次池化"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图14-1.png", "读出与层次池化",
              ["节点表示", "聚类分配", "层次池化", "图表示", "预测"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_15_1():
    """图 15-1 异质图与元路径示例"""
    fig, ax = plt.subplots(figsize=(8.5, 5))
    nodes = {"A1": (2, 4.5), "A2": (2, 2.0), "P1": (5, 4.5), "P2": (5, 2.0), "C1": (8, 3.2)}
    edges = [("A1", "P1"), ("A2", "P1"), ("A2", "P2"), ("P1", "C1"), ("P2", "C1")]
    nc = {}
    for k in nodes:
        nc[k] = LIGHT if k.startswith("A") else (LGREEN if k.startswith("P") else LAMBER)
    fig, ax = plt.subplots(figsize=(8.5, 5))
    base(ax, (0, 10), (0, 7), "异质图与元路径示例 (作者-论文-会议)")
    for u, v in edges:
        draw_arrow(ax, *nodes[u], *nodes[v], color=GRAY, lw=1.2)
    for k, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 0.55, fc=nc[k], ec=BLUE, lw=1.4, zorder=3))
        ax.text(x, y, {"A1": "作者1", "A2": "作者2", "P1": "论文1", "P2": "论文2", "C1": "会议"}[k],
                ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    ax.text(5, 0.5, "元路径: 作者 - 论文 - 作者 (APA)", ha="center", fontsize=10, color=RED)
    save(fig, "图15-1.png")


def fig_16_1():
    """图 16-1 离散快照与连续事件流"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图16-1.png", "离散快照与连续事件流",
              ["时间切分", "快照图序列", "动态 GNN", "时序表示", "预测"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_17_1():
    """图 17-1 普通图、超图与单纯复形对比"""
    fig, ax = plt.subplots(figsize=(11, 4.4))
    base(ax, (0, 12), (0, 4.4), "普通图、超图与单纯复形对比")
    items = [("普通图", "边连接两个节点", LIGHT),
             ("超图", "超边连接多个节点", LGREEN),
             ("单纯复形", "单形嵌套(点/边/面)", LAMBER)]
    xs = [0.4, 4.3, 8.2]
    for (t, s, fc), x in zip(items, xs):
        draw_box(ax, x, 1.4, 3.4, 1.8, t + "\n" + s, fc=fc, fs=11)
    save(fig, "图17-1.png")


def fig_18_1():
    """图 18-1 图注意力与位置编码示意"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图18-1.png", "图注意力与位置编码示意",
              ["节点特征", "结构/位置编码", "自注意力", "图 Transformer", "表示"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_19_1():
    """图 19-1 链路预测范式对比"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图19-1.png", "链路预测范式对比",
              ["已知边", "负采样", "打分函数", "排序", "新链路"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_20_1():
    """图 20-1 图生成三大范式"""
    fig, ax = plt.subplots(figsize=(11, 4.4))
    base(ax, (0, 12), (0, 4.4), "图生成三大范式")
    items = [("自回归", "逐边/逐点生成", LIGHT),
             ("VAE / 流", "隐空间解码", LGREEN),
             ("扩散模型", "加噪去噪生成", LAMBER)]
    xs = [0.4, 4.3, 8.2]
    for (t, s, fc), x in zip(items, xs):
        draw_box(ax, x, 1.4, 3.4, 1.8, t + "\n" + s, fc=fc, fs=11)
    save(fig, "图20-1.png")


def fig_21_1():
    """图 21-1 图分类管线"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图21-1.png", "图分类管线",
              ["输入图", "GNN 编码", "读出池化", "图向量", "分类"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_22_1():
    """图 22-1 知识图谱规则推理示意"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图22-1.png", "知识图谱规则推理示意",
              ["三元组事实", "规则 mining", "路径推理", "新事实", "置信度"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_23_1():
    """图 23-1 谱聚类的拉普拉斯谱"""
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    k = np.arange(1, 11)
    lam = 0.05 + 0.9 * (k - 1) / 9.0
    draw_curve("图23-1.png", "谱聚类的拉普拉斯谱",
               [(k, lam, BLUE, "特征值 λ")],
               xlabel="特征值序号", ylabel="拉普拉斯特征值", figsize=(7.6, 4.6))
    # 叠加前 k 小特征值标记
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.plot(k, lam, "o-", color=BLUE, lw=2, label="特征值 λ")
    ax.axvspan(0.8, 3.2, color=GREEN, alpha=0.15, label="前 k 小(聚类信号)")
    ax.set_xlabel("特征值序号", fontsize=11)
    ax.set_ylabel("拉普拉斯特征值", fontsize=11)
    ax.set_title("谱聚类的拉普拉斯谱", fontsize=14, weight="bold", color=DARK)
    ax.grid(True, ls=":", alpha=0.4)
    ax.legend(fontsize=9)
    save(fig, "图23-1.png")


def fig_24_1():
    """图 24-1 E(n)-等变消息传递"""
    fig, ax = plt.subplots(figsize=(9, 4.6))
    base(ax, (0, 12), (0, 4.6), "E(n)-等变消息传递")
    draw_box(ax, 0.5, 1.4, 3.0, 1.4, "坐标 x_i\n标量特征 h_i", fc=LIGHT, fs=11)
    draw_box(ax, 4.5, 1.4, 3.0, 1.4, "相对位移\nx_i - x_j", fc=LGREEN, fs=11)
    draw_box(ax, 8.5, 1.4, 3.0, 1.4, "等变更新\n(旋转平移不变)", fc=LAMBER, fs=11)
    draw_arrow(ax, 3.5, 2.1, 4.5, 2.1)
    draw_arrow(ax, 7.5, 2.1, 8.5, 2.1)
    ax.text(6, 0.5, "几何变换下预测随之等变，保持物理正确性", ha="center", fontsize=10, color=GRAY)
    save(fig, "图24-1.png")


def fig_25_1():
    """图 25-1 几何域上的卷积"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图25-1.png", "几何域上的卷积",
              ["流形/图域", "局部邻域", "测地线/权重", "卷积核", "特征"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_26_1():
    """图 26-1 Vietoris–Rips 复形随尺度增长"""
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    eps = np.arange(1, 11)
    h = np.zeros_like(eps, dtype=float)
    h[2:5] = 1  # 一维洞在中间尺度出现又消失
    draw_curve("图26-1.png", "Vietoris–Rips 复形随尺度增长",
               [(eps, h, BLUE, "H1 持续(拓扑特征)")],
               xlabel="尺度 epsilon", ylabel="拓扑特征数量", figsize=(7.6, 4.6))


def fig_27_1():
    """图 27-1 等变分子性质预测管线"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图27-1.png", "等变分子性质预测管线",
              ["分子构象", "原子图", "等变 GNN", "不变读出", "性质预测"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_28_1():
    """图 28-1 图对比学习框架"""
    fig, ax = plt.subplots(figsize=(11, 4.4))
    base(ax, (0, 12), (0, 4.4), "图对比学习框架")
    items = [("图增强", "扰动/子图", LIGHT),
             ("双编码器", "同一图两视图", LGREEN),
             ("正/负对", "InfoNCE", LAMBER),
             ("对齐+均匀", "预训练表示", LPURPLE)]
    xs = [0.4, 3.4, 6.4, 9.4]
    for (t, s, fc), x in zip(items, xs):
        draw_box(ax, x, 1.6, 2.4, 1.1, t + "\n" + s, fc=fc, fs=10)
    for i in range(3):
        draw_arrow(ax, xs[i] + 2.45, 2.15, xs[i + 1] - 0.05, 2.15)
    save(fig, "图28-1.png")


def fig_29_1():
    """图 29-1 图基础模型总体架构"""
    fig, ax = plt.subplots(figsize=(8.5, 5.6))
    draw_layers("图29-1.png", "图基础模型总体架构",
                [("任务头/提示 Prompt", LPURPLE),
                 ("大规模预训练 Backbone", LAMBER),
                 ("图 Transformer / GNN", LGREEN),
                 ("通用图 Token 化", LIGHT)], figsize=(8.5, 5.6))


def fig_30_1():
    """图 30-1 图与大语言模型的三种接口"""
    fig, ax = plt.subplots(figsize=(11, 4.4))
    base(ax, (0, 12), (0, 4.4), "图与大语言模型的三种接口")
    items = [("图作为文本", "序列化输入 LLM", LIGHT),
             ("LLM 作为编码器", "文本特征入 GNN", LGREEN),
             ("图作为工具", "LLM 调用图推理", LAMBER)]
    xs = [0.4, 4.3, 8.2]
    for (t, s, fc), x in zip(items, xs):
        draw_box(ax, x, 1.4, 3.4, 1.8, t + "\n" + s, fc=fc, fs=11)
    save(fig, "图30-1.png")


def fig_31_1():
    """图 31-1 跨域评估协议流程"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图31-1.png", "跨域评估协议流程",
              ["源域训练", "分布偏移", "目标域适配", "域外测试", "鲁棒性"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_32_1():
    """图 32-1 二部图上的多层协同过滤"""
    fig, ax = plt.subplots(figsize=(8.5, 5))
    users = {"U1": (2, 5.0), "U2": (2, 3.0), "U3": (2, 1.0)}
    items = {"I1": (8, 4.5), "I2": (8, 2.5)}
    nodes = {**users, **items}
    edges = [("U1", "I1"), ("U1", "I2"), ("U2", "I1"), ("U3", "I2")]
    nc = {}
    for k in nodes:
        nc[k] = LIGHT if k.startswith("U") else LGREEN
    fig, ax = plt.subplots(figsize=(8.5, 5))
    base(ax, (0, 10), (0, 7), "二部图上的多层协同过滤")
    for u, v in edges:
        draw_arrow(ax, *nodes[u], *nodes[v], color=GRAY, lw=1.2)
    for k, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 0.5, fc=nc[k], ec=BLUE, lw=1.4, zorder=3))
        ax.text(x, y, k, ha="center", va="center", fontsize=10, color=DARK, zorder=4)
    ax.text(5, 0.35, "用户-物品二部图：多层传播捕捉高阶协同信号", ha="center", fontsize=10, color=GRAY)
    save(fig, "图32-1.png")


def fig_33_1():
    """图 33-1 分子图上的消息传递与性质预测"""
    fig, ax = plt.subplots(figsize=(9, 4.6))
    nodes = {0: (2.5, 4.3), 1: (5.0, 5.0), 2: (7.5, 4.3), 3: (5.0, 2.0)}
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    nc = {0: LGREEN, 1: LIGHT, 2: LGREEN, 3: LIGHT}
    fig, ax = plt.subplots(figsize=(9, 4.6))
    base(ax, (0, 10), (0, 7), "分子图上的消息传递与性质预测")
    for u, v in edges:
        draw_arrow(ax, *nodes[u], *nodes[v], color=GRAY, lw=1.4)
    for k, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 0.5, fc=nc[k], ec=BLUE, lw=1.4, zorder=3))
        ax.text(x, y, {0: "C", 1: "O", 2: "N", 3: "C"}[k],
                ha="center", va="center", fontsize=11, color=DARK, zorder=4)
    draw_box(ax, 0.5, 0.4, 9.0, 0.9, "原子图 -> 消息传递 -> 分子指纹 -> 性质预测", fc=LAMBER, fs=10)
    save(fig, "图33-1.png")


def fig_34_1():
    """图 34-1 社交网络中的欺诈团伙模式"""
    fig, ax = plt.subplots(figsize=(8.5, 5))
    # 固定布局：左侧红色欺诈团伙，中部琥珀嫌疑，右侧蓝色正常节点
    nodes = {0: (1.6, 4.6), 1: (3.0, 4.6), 2: (3.0, 3.0), 3: (1.6, 3.0),
             4: (4.8, 4.0), 5: (6.0, 4.6), 6: (6.0, 3.2),
             7: (5.2, 1.8), 8: (6.6, 1.6), 9: (8.0, 1.8), 10: (8.2, 3.0),
             11: (7.4, 5.4), 12: (2.0, 1.4)}
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3),
             (4, 5), (5, 6), (6, 4),
             (7, 8), (8, 9), (9, 10), (10, 7), (7, 9),
             (2, 4), (4, 7)]
    nc = {}
    for i in nodes:
        nc[i] = LRED if i < 4 else (LAMBER if i < 7 else LIGHT)
    draw_network("图34-1.png", "社交网络中的欺诈团伙模式", nodes, edges,
                 node_colors=nc,
                 labels={i: ("F" if i < 4 else ("?" if i < 7 else "N")) for i in nodes},
                 figsize=(8.5, 5))


def fig_35_1():
    """图 35-1 知识图谱四任务全景"""
    fig, ax = plt.subplots(figsize=(9, 5))
    base(ax, (0, 10), (0, 7), "知识图谱四任务全景")
    ring_nodes(ax, 5, 3.6, 1.9, 4,
               ["链接预测", "实体识别", "关系抽取", "问答"], fc=LGREEN, fs=10, r_node=0.95)
    draw_box(ax, 3.8, 3.0, 2.4, 1.2, "知识图谱\n推理与应用", fc=LAMBER, fs=11)
    save(fig, "图35-1.png")


def fig_36_1():
    """图 36-1 图系统工程栈"""
    fig, ax = plt.subplots(figsize=(8.5, 5.6))
    draw_layers("图36-1.png", "图系统工程栈",
                [("应用与监控", LPURPLE),
                 ("训练与推理框架", LAMBER),
                 ("图学习与算法层", LGREEN),
                 ("图存储与采样层", LIGHT),
                 ("数据/图数据库", "#E8F0F7")], figsize=(8.5, 5.6))


def fig_37_1():
    """图 37-1 多模态图融合架构"""
    fig, ax = plt.subplots(figsize=(11, 4.4))
    base(ax, (0, 12), (0, 4.4), "多模态图融合架构")
    items = [("文本/图像", "编码为特征", LIGHT),
             ("图结构", "关系建模", LGREEN),
             ("跨模态对齐", "统一表示", LAMBER),
             ("融合推理", "多模态任务", LPURPLE)]
    xs = [0.4, 3.4, 6.4, 9.4]
    for (t, s, fc), x in zip(items, xs):
        draw_box(ax, x, 1.6, 2.4, 1.1, t + "\n" + s, fc=fc, fs=10)
    for i in range(3):
        draw_arrow(ax, xs[i] + 2.45, 2.15, xs[i + 1] - 0.05, 2.15)
    save(fig, "图37-1.png")


def fig_38_1():
    """图 38-1 图世界模型闭环"""
    fig, ax = plt.subplots(figsize=(11, 4.4))
    base(ax, (0, 12), (0, 4.4), "图世界模型闭环")
    steps = [("观测图", LIGHT), ("图世界模型", LGREEN),
             ("状态预测", LAMBER), ("动作/干预", LPURPLE)]
    xs = [0.4, 3.4, 6.4, 9.4]
    for (t, fc), x in zip(steps, xs):
        draw_box(ax, x, 1.6, 2.4, 1.1, t, fc=fc, fs=11)
    for i in range(3):
        draw_arrow(ax, xs[i] + 2.45, 2.15, xs[i + 1] - 0.05, 2.15)
    draw_arrow(ax, 10.6, 1.6, 1.6, 1.6, color=GRAY, rad=0.25, label="闭环反馈")
    save(fig, "图38-1.png")


def fig_39_1():
    """图 39-1 WL 层级与 GNN 表达力"""
    fig, ax = plt.subplots(figsize=(11, 4))
    draw_flow("图39-1.png", "WL 层级与 GNN 表达力",
              ["1-WL 测试", "邻域聚合", "GNN 表达力", "高阶 WL", "更表达模型"],
              [LIGHT, LGREEN, LGREEN, LAMBER, LPURPLE], fs=10)


def fig_40_1():
    """图 40-1 四类开放问题关系图"""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    base(ax, (0, 10), (0, 7.5), "四类开放问题关系图")
    ring_nodes(ax, 5, 3.9, 2.0, 4,
               ["表达力", "可扩展性", "鲁棒性", "可解释性"],
               fc=LGREEN, fs=10, r_node=1.0)
    draw_box(ax, 3.9, 3.2, 2.2, 1.2, "图智能\n开放问题", fc=LAMBER, fs=11)
    save(fig, "图40-1.png")


def fig_41_1():
    """图 41-1 九篇×四层闭环地图"""
    fig, ax = plt.subplots(figsize=(8.5, 5.6))
    draw_layers("图41-1.png", "九篇 × 四层闭环地图",
                [("结语与开放问题", LPURPLE),
                 ("应用与前沿", LAMBER),
                 ("系统与训练", LGREEN),
                 ("表示学习", LGREEN),
                 ("基础理论", LIGHT)], figsize=(8.5, 5.6))


def main():
    fig_1_1(); fig_2_1(); fig_3_1(); fig_4_1(); fig_5_1(); fig_6_1()
    fig_7_1(); fig_8_1(); fig_9_1(); fig_10_1(); fig_11_1(); fig_12_1()
    fig_13_1(); fig_14_1(); fig_15_1(); fig_16_1(); fig_17_1(); fig_18_1()
    fig_19_1(); fig_20_1(); fig_21_1(); fig_22_1(); fig_23_1(); fig_24_1()
    fig_25_1(); fig_26_1(); fig_27_1(); fig_28_1(); fig_29_1(); fig_30_1()
    fig_31_1(); fig_32_1(); fig_33_1(); fig_34_1(); fig_35_1(); fig_36_1()
    fig_37_1(); fig_38_1(); fig_39_1(); fig_40_1(); fig_41_1()
    print("配图生成完成，共 41 张")


if __name__ == "__main__":
    main()
