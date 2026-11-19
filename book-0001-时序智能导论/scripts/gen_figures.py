# -*- coding: utf-8 -*-
"""《时序智能导论》数据类配图自动生成脚本。
只生成适合 matplotlib 的数据图；概念/架构/流程图仍留占位，建议用 Visio/PPT/TikZ。
运行: python scripts/gen_figures.py  -> 输出到 figures/
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("已生成:", name)


def acf(x, nlags=40):
    x = x - x.mean()
    n = len(x)
    out = np.zeros(nlags + 1)
    v = (x * x).sum()
    for k in range(nlags + 1):
        out[k] = (x[k:] @ x[: n - k]) / v
    return out


# ---------- 图 2-1 ACF ----------
def fig_2_1():
    np.random.seed(0)
    T = 500
    lags = 40
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
    band = 1.96 / np.sqrt(T)
    series = {
        "(a) 白噪声": np.random.normal(0, 1, T),
        "(b) AR(1) 正系数": None,
        "(c) 含季节周期": None,
    }
    ar = np.zeros(T)
    for t in range(1, T):
        ar[t] = 0.85 * ar[t - 1] + np.random.normal(0, 1)
    series["(b) AR(1) 正系数"] = ar
    t = np.arange(T)
    season = 3 * np.sin(2 * np.pi * t / 12) + np.random.normal(0, 0.6, T)
    series["(c) 含季节周期"] = season
    for ax, (title, x) in zip(axes, series.items()):
        a = acf(x, lags)
        ax.stem(range(lags + 1), a, basefmt=" ")
        ax.axhline(band, color="r", ls="--", lw=0.8)
        ax.axhline(-band, color="r", ls="--", lw=0.8)
        ax.set_title(title)
        ax.set_xlabel("滞后 k")
        ax.set_ylabel("ACF")
    save(fig, "图2-1.png")


# ---------- 图 3-2 周期图 ----------
def fig_3_2():
    np.random.seed(1)
    T = 240
    t = np.arange(T)
    x = 4 * np.sin(2 * np.pi * t / 12) + np.random.normal(0, 1, T)
    spec = np.abs(np.fft.rfft(x)) ** 2 / T
    freq = np.fft.rfftfreq(T, d=1)
    period = 1 / freq
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(period[1:], spec[1:])
    ax.set_xscale("log")
    ax.set_xlabel("周期（月）")
    ax.set_ylabel("谱密度（周期图）")
    ax.axvline(12, color="r", ls="--", lw=0.8)
    ax.annotate("年度季节峰 (12 个月)", xy=(12, spec[1:].max()), xytext=(30, spec[1:].max() * 0.8),
                arrowprops=dict(arrowstyle="->"))
    ax.set_title("含年度季节成分的月度序列周期图")
    save(fig, "图3-2.png")


# ---------- 图 3-3 STL 分解 ----------
def fig_3_3():
    np.random.seed(2)
    T = 240
    t = np.arange(T)
    trend = 20 + 0.05 * t + 0.0003 * t ** 2
    season = 8 * np.sin(2 * np.pi * t / 12) + 3 * np.cos(2 * np.pi * t / 6)
    resid = np.random.normal(0, 2, T)
    y = trend + season + resid
    # 简单分解：趋势用多项式拟合，季节用按周期平均
    trend_hat = np.polyval(np.polyfit(t, y, 2), t)
    detrend = y - trend_hat
    m = 12
    seas_hat = np.zeros(T)
    for i in range(m):
        idx = np.arange(i, T, m)
        seas_hat[idx] = detrend[idx].mean()
    resid_hat = y - trend_hat - seas_hat
    fig, axes = plt.subplots(4, 1, figsize=(9, 7), sharex=True)
    for ax, data, name in zip(axes, [y, trend_hat, seas_hat, resid_hat],
                              ["原始序列", "趋势分量", "季节分量", "残差分量"]):
        ax.plot(t, data, lw=0.9)
        ax.set_ylabel(name)
    axes[-1].set_xlabel("时间")
    save(fig, "图3-3.png")


# ---------- 图 4-1 Logistic 混沌 ----------
def fig_4_1():
    def logistic(x, r):
        return r * x * (1 - x)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    r = 4.0
    x1, x2 = 0.1, 0.1 + 1e-5
    T = 50
    tr1, tr2 = [x1], [x2]
    for _ in range(T):
        x1, x2 = logistic(x1, r), logistic(x2, r)
        tr1.append(x1)
        tr2.append(x2)
    ax = axes[0]
    ax.plot(tr1, lw=1.2, label="初值 0.1")
    ax.plot(tr2, lw=1.2, label="初值 0.1+1e-5", alpha=0.8)
    ax.set_xlabel("迭代步 t")
    ax.set_ylabel("x_t")
    ax.set_title("(a) 两条初值相近轨迹的分离")
    ax.legend()
    ax = axes[1]
    rs = np.linspace(2.5, 4.0, 1000)
    for rr in rs:
        x = 0.5
        for _ in range(300):
            x = logistic(x, rr)
        pts = []
        for _ in range(150):
            x = logistic(x, rr)
            pts.append(x)
        ax.plot([rr] * len(pts), pts, ",", color="k", ms=0.5)
    ax.set_xlabel("参数 r")
    ax.set_ylabel("x 的吸引子")
    ax.set_title("(b) 分岔图")
    save(fig, "图4-1.png")


# ---------- 图 5-2 探索性可视化 ----------
def fig_5_2():
    np.random.seed(3)
    T = 90
    t = np.arange(T)
    y = 50 + 0.15 * t + 6 * np.sin(2 * np.pi * t / 7) + np.random.normal(0, 1.5, T)
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    axes[0, 0].plot(t, y, lw=0.9)
    axes[0, 0].set_title("时间图")
    axes[0, 1].scatter(y[:-1], y[1:], s=8)
    axes[0, 1].set_xlabel("y_t")
    axes[0, 1].set_ylabel("y_{t+1}")
    axes[0, 1].set_title("滞后图 (k=1)")
    # 季节子序列（按周期7）
    ax = axes[1, 0]
    for i in range(7):
        idx = np.arange(i, T, 7)
        ax.plot(idx, y[idx], marker="o", ms=3, label=f"周{i}")
    ax.set_title("季节子序列图")
    # 日历热力图（星期 x 小时 合成）
    ax = axes[1, 1]
    hours = np.arange(24)
    days = np.arange(7)
    zz = 10 + 6 * np.sin(2 * np.pi * (hours - 8) / 24)[:, None] + \
         2 * np.array([1, 1.5, 2, 2.2, 2, 1.6, 1])[None, :]
    im = ax.imshow(zz, aspect="auto", cmap="viridis")
    ax.set_xticks(days)
    ax.set_yticks(range(0, 24, 4))
    ax.set_xlabel("星期")
    ax.set_ylabel("小时")
    ax.set_title("日历热力图")
    fig.colorbar(im, ax=ax, shrink=0.8)
    save(fig, "图5-2.png")


# ---------- 图 7-1 DTW 对齐 ----------
def fig_7_1():
    np.random.seed(4)
    t = np.linspace(0, 4 * np.pi, 60)
    a = np.sin(t)
    b = np.sin(t - 1.2)
    n = len(a)
    # DTW 路径
    D = np.full((n, n), np.inf)
    D[0, 0] = (a[0] - b[0]) ** 2
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            cost = (a[i] - b[j]) ** 2
            prev = []
            if i > 0:
                prev.append(D[i - 1, j])
            if j > 0:
                prev.append(D[i, j - 1])
            if i > 0 and j > 0:
                prev.append(D[i - 1, j - 1])
            D[i, j] = cost + min(prev)
    path = [(n - 1, n - 1)]
    i, j = n - 1, n - 1
    while i > 0 or j > 0:
        cands = []
        if i > 0:
            cands.append((D[i - 1, j], i - 1, j))
        if j > 0:
            cands.append((D[i, j - 1], i, j - 1))
        if i > 0 and j > 0:
            cands.append((D[i - 1, j - 1], i - 1, j - 1))
        _, i, j = min(cands)
        path.append((i, j))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(a, label="序列 A")
    axes[0].plot(b, label="序列 B (相位偏移)")
    axes[0].set_title("(a) 两条形态相似、相位错开的序列")
    axes[0].legend()
    ax = axes[1]
    ax.imshow(D, origin="lower", cmap="Blues", aspect="auto")
    py, px = zip(*path)
    ax.plot(px, py, color="r", lw=1)
    ax.set_title("(b) DTW 规整路径")
    ax.set_xlabel("序列 B 索引")
    ax.set_ylabel("序列 A 索引")
    save(fig, "图7-1.png")


# ---------- 图 9-1 CUSUM ----------
def fig_9_1():
    np.random.seed(5)
    T = 200
    shift = 80
    y = np.concatenate([np.random.normal(0, 1, shift), np.random.normal(1.2, 1, T - shift)])
    mu0 = 0.0
    kappa = 0.3
    S = np.zeros(T)
    s = 0
    for i in range(T):
        s = max(0, s + (y[i] - mu0) - kappa)
        S[i] = s
    h = 8
    fig, axes = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
    axes[0].plot(y, lw=0.8)
    axes[0].axvline(shift, color="g", ls="--", lw=0.8)
    axes[0].set_ylabel("观测 y_t")
    axes[1].plot(S, color="r", lw=1)
    axes[1].axhline(h, color="k", ls="--", lw=0.8, label="报警阈值 h")
    axes[1].set_ylabel("CUSUM S_t")
    axes[1].set_xlabel("时间")
    axes[1].legend()
    save(fig, "图9-1.png")


# ---------- 图 11-1 指数平滑权重衰减 ----------
def fig_11_1():
    j = np.arange(0, 25)
    fig, ax = plt.subplots(figsize=(8, 4))
    for alpha in [0.1, 0.3, 0.6]:
        w = alpha * (1 - alpha) ** j
        ax.plot(j, w, marker="o", ms=3, label=f"α = {alpha}")
    ax.set_xlabel("滞后 j")
    ax.set_ylabel("权重 α(1-α)^j")
    ax.set_title("简单指数平滑的权重衰减")
    ax.legend()
    save(fig, "图11-1.png")


# ---------- 图 15-1 GARCH 波动率 ----------
def fig_15_1():
    np.random.seed(6)
    T = 500
    omega, alpha, beta = 0.01, 0.08, 0.9
    sigma = np.zeros(T)
    eps = np.zeros(T)
    sigma[0] = np.sqrt(omega / (1 - alpha - beta))
    for t in range(1, T):
        sigma[t] = np.sqrt(omega + alpha * eps[t - 1] ** 2 + beta * sigma[t - 1] ** 2)
        eps[t] = sigma[t] * np.random.normal()
    fig, axes = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
    axes[0].plot(eps, lw=0.7)
    axes[0].set_ylabel("收益率")
    axes[1].plot(sigma, color="r", lw=0.9)
    axes[1].set_ylabel("条件波动率 σ_t")
    axes[1].set_xlabel("时间")
    save(fig, "图15-1.png")


# ---------- 图 16-1 Prophet 分解 ----------
def fig_16_1():
    np.random.seed(7)
    T = 300
    t = np.arange(T)
    trend = 20 + 0.06 * t + 0.0002 * t ** 2
    season = 5 * np.sin(2 * np.pi * t / 30) + 2 * np.cos(2 * np.pi * t / 7)
    holiday = np.zeros(T)
    holiday[[100, 200]] = 12  # 节假日尖峰
    resid = np.random.normal(0, 1.5, T)
    y = trend + season + holiday + resid
    fig, axes = plt.subplots(4, 1, figsize=(9, 7), sharex=True)
    for ax, data, name in zip(axes, [trend, season, holiday, resid],
                              ["趋势 g(t)", "季节 s(t)", "节假日 h(t)", "残差"]):
        ax.plot(t, data, lw=0.8)
        ax.set_ylabel(name)
    axes[0].set_title("Prophet 可分解分量")
    axes[-1].set_xlabel("时间")
    save(fig, "图16-1.png")


# ---------- 图 34-1 临界慢化 ----------
def fig_34_1():
    np.random.seed(8)
    T = 600
    x = np.zeros(T)
    x[0] = 0
    for t in range(1, T):
        phi = 0.5 if t < 200 else (0.9 if t < 400 else 0.98)
        x[t] = phi * x[t - 1] + np.random.normal(0, 1)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(x, lw=0.6)
    ax.axvline(200, color="g", ls="--", lw=0.8)
    ax.axvline(400, color="g", ls="--", lw=0.8)
    ax.text(100, x.max(), "φ=0.5", ha="center")
    ax.text(300, x.max(), "φ=0.9", ha="center")
    ax.text(500, x.max(), "φ=0.98 (接近临界)", ha="center")
    ax.set_xlabel("时间")
    ax.set_ylabel("系统状态 x_t")
    ax.set_title("临界慢化：接近临界点时恢复变慢、方差增大")
    save(fig, "图34-1.png")


# ---------- 图 37-1 采样混叠 ----------
def fig_37_1():
    f_high = 9.0
    fs = 10.0  # 欠采样
    t_fine = np.linspace(0, 2, 2000)
    y_fine = np.sin(2 * np.pi * f_high * t_fine)
    t_s = np.arange(0, 2, 1 / fs)
    y_s = np.sin(2 * np.pi * f_high * t_s)
    alias_f = abs(f_high - fs)  # 混叠出的低频
    y_alias = np.sin(2 * np.pi * alias_f * t_fine)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(t_fine, y_fine, lw=0.8, label=f"真实信号 (f={f_high} Hz)")
    ax.plot(t_s, y_s, "o", ms=4, label=f"采样点 (fs={fs} Hz)")
    ax.plot(t_fine, y_alias, ls="--", lw=1.2, label=f"混叠假象 (f={alias_f} Hz)")
    ax.set_xlabel("时间 (s)")
    ax.set_ylabel("幅度")
    ax.set_title("欠采样导致的混叠")
    ax.legend()
    save(fig, "图37-1.png")


if __name__ == "__main__":
    fig_2_1()
    fig_3_2()
    fig_3_3()
    fig_4_1()
    fig_5_2()
    fig_7_1()
    fig_9_1()
    fig_11_1()
    fig_15_1()
    fig_16_1()
    fig_34_1()
    fig_37_1()
    print("\n全部数据类配图生成完毕。")
