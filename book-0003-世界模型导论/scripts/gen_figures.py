# -*- coding: utf-8 -*-
"""《世界模型导论》数据类配图。运行: python scripts/gen_figures.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)
BLUE = "#2C5F8A"; GREEN = "#2E7D5B"; AMBER = "#B07D2B"; RED = "#A33B3B"; GRAY = "#5A5A5A"; DARK = "#1A3350"

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("已生成:", name)

# 图5-2 卡尔曼滤波收敛
def fig_5_2():
    fig, ax = plt.subplots(figsize=(7.2, 5))
    t = np.arange(1, 21)
    uncertainty = 1.0 / np.sqrt(t)  # 不确定性收缩
    ax.plot(t, uncertainty, "o-", color=BLUE, lw=2, ms=4, label="状态估计不确定性")
    ax.set_xlabel("观测步数 t", fontsize=11); ax.set_ylabel("不确定性 (标准差)", fontsize=11)
    ax.set_title("卡尔曼滤波：不确定性随观测收缩", fontsize=13, weight="bold", color=DARK)
    ax.grid(True, ls=":", alpha=0.4); ax.legend(fontsize=10)
    save(fig, "图5-2.png")

# 图12-2 MBRL 样本效率
def fig_12_2():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    steps = np.linspace(0, 1e6, 100)
    mbrl = 1 - np.exp(-steps / 1.5e5)
    model_free = 1 - np.exp(-steps / 8e5)
    ax.plot(steps, mbrl, color=BLUE, lw=2, label="基于模型（Dreamer）")
    ax.plot(steps, model_free, color=AMBER, lw=2, ls="--", label="无模型 RL")
    ax.set_xlabel("真实环境交互步数", fontsize=11); ax.set_ylabel("相对性能", fontsize=11)
    ax.set_title("样本效率：MBRL vs 无模型 RL（示意）", fontsize=13, weight="bold", color=DARK)
    ax.grid(True, ls=":", alpha=0.4); ax.legend(fontsize=10)
    save(fig, "图12-2.png")

# 图33-1 误差累积
def fig_33_1():
    fig, ax = plt.subplots(figsize=(7.2, 5))
    steps = np.arange(1, 51)
    err = 0.01 * (1.08 ** steps)  # 指数增长
    ax.plot(steps, err, color=RED, lw=2)
    ax.axhline(1.0, color=GRAY, ls="--", lw=1.2, label="可用阈值")
    ax.set_xlabel("滚动预测步数", fontsize=11); ax.set_ylabel("预测误差（示意）", fontsize=11)
    ax.set_title("长期滚动：误差指数累积", fontsize=13, weight="bold", color=DARK)
    ax.grid(True, ls=":", alpha=0.4); ax.legend(fontsize=10)
    save(fig, "图33-1.png")

# 图35-1 数据规模化
def fig_35_1():
    fig, ax = plt.subplots(figsize=(7.2, 5))
    data = np.logspace(3, 8, 50)
    perf = 1 - 2.0 * data ** (-0.15)
    ax.semilogx(data, perf, color=GREEN, lw=2)
    ax.set_xlabel("数据量（相对规模，对数）", fontsize=11); ax.set_ylabel("模型能力（示意）", fontsize=11)
    ax.set_title("世界模型的数据规模化", fontsize=13, weight="bold", color=DARK)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    save(fig, "图35-1.png")

if __name__ == "__main__":
    fig_5_2(); fig_12_2(); fig_33_1(); fig_35_1()
    print("数据图生成完成")
