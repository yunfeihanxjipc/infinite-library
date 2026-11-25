# -*- coding: utf-8 -*-
"""《智能体与多智能体系统导论》配图脚本。
运行：python scripts/gen_all.py
输出：figures/图X-Y.png（文件名严格匹配正文引用）。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)

# 统一配色
BLUE = "#2C5F8A"; LBLUE = "#E8F0F7"
GREEN = "#2E7D5B"; LGREEN = "#E6F2EA"
AMBER = "#B07D2B"; LAMBER = "#F8EFDD"
RED = "#A33B3B"; LRED = "#F6E4E4"
GRAY = "#5A5A5A"; LGRAY = "#EFEFEF"
DARK = "#1A3350"
PALETTE = [BLUE, GREEN, AMBER, RED]


# ---------- 通用辅助函数 ----------
def new_ax(title, xlim=(0, 12), ylim=(0, 7), figsize=(8, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.text(sum(xlim) / 2, ylim[1] - 0.15, title, ha="center", va="top",
            fontsize=14, weight="bold", color=DARK)
    return fig, ax


def box(ax, x, y, w, h, text, fc=LBLUE, ec=BLUE, fs=10, tc=DARK, lw=1.2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=lw, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, wrap=True)


def arrow(ax, x1, y1, x2, y2, color=BLUE, rad=0, lw=1.5, ms=13):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=ms,
        linewidth=lw, color=color,
        connectionstyle="arc3,rad=%s" % rad))


def circle(ax, x, y, r, text, fc=LBLUE, ec=BLUE, fs=9, tc=DARK):
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, linewidth=1.3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc)


def save(fig, num, title=None):
    name = "图%s.png" % num
    fig.savefig(os.path.join(OUT, name), dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("已生成:", name)


def palette_fc(i):
    return [LBLUE, LGREEN, LAMBER, LRED][i % 4]


def palette_ec(i):
    return PALETTE[i % 4]


# ---------- 通用图型 ----------
def flow(num, title, steps, note=None):
    """水平/两行流程链。"""
    fig, ax = new_ax(title)
    n = len(steps)
    per_row = min(n, 5) if n > 5 else n
    rows = (n + per_row - 1) // per_row
    w = 10.5 / per_row - 0.25
    idx = 0
    for r in range(rows):
        row_steps = steps[r * per_row:(r + 1) * per_row]
        y = 4.2 - r * 2.0
        xs = [0.6 + i * (10.5 / per_row) for i in range(len(row_steps))]
        for i, s in enumerate(row_steps):
            box(ax, xs[i], y, w, 1.1, s, fc=palette_fc(idx % 4),
                ec=palette_ec(idx % 4), fs=9.5)
            idx += 1
        for i in range(len(row_steps) - 1):
            arrow(ax, xs[i] + w + 0.03, y + 0.55, xs[i + 1] - 0.05, y + 0.55)
        if rows > 1 and r < rows - 1:
            arrow(ax, xs[-1] + w / 2, y, xs[-1] + w / 2, y - 0.9, color=GRAY, rad=0)
    if note:
        ax.text(6, 0.35, note, ha="center", fontsize=9, color=GRAY)
    save(fig, num, title)


def cycle(num, title, steps, note=None, figsize=(8, 5)):
    """环形循环图。"""
    fig, ax = new_ax(title, (0, 12), (0, 8), figsize)
    n = len(steps)
    cx, cy, rx, ry = 6.0, 4.3, 4.0, 2.5
    pos = []
    for i in range(n):
        a = np.pi / 2 - i * 2 * np.pi / n
        pos.append((cx + rx * np.cos(a), cy + ry * np.sin(a)))
    for i, (s, (x, y)) in enumerate(zip(steps, pos)):
        box(ax, x - 1.25, y - 0.5, 2.5, 1.0, s, fc=palette_fc(i),
            ec=palette_ec(i), fs=9.5)
    for i in range(n):
        x1, y1 = pos[i]
        x2, y2 = pos[(i + 1) % n]
        arrow(ax, x1 + 0.3 * (x2 - x1), y1 + 0.3 * (y2 - y1) - 0.1,
              x2 - 0.3 * (x2 - x1), y2 - 0.3 * (y2 - y1) + 0.1, rad=0)
    if note:
        ax.text(6, 0.4, note, ha="center", fontsize=9, color=GRAY)
    save(fig, num, title)


def layers(num, title, items, note=None):
    """纵向分层架构图，items=[(左标题, 右说明), ...]。"""
    fig, ax = new_ax(title, (0, 12), (0, 8))
    n = len(items)
    h = 5.4 / n
    for i, (t, s) in enumerate(items):
        y = 6.2 - i * (h + 0.15)
        box(ax, 1.0, y, 10.0, h, "%s：%s" % (t, s), fc=palette_fc(i),
            ec=palette_ec(i), fs=10)
        if i < n - 1:
            arrow(ax, 6.0, y - 0.05, 6.0, y - 0.15 + 0.02, color=GRAY, lw=1.0)
    if note:
        ax.text(6, 0.35, note, ha="center", fontsize=9, color=GRAY)
    save(fig, num, title)


def compare(num, title, left_title, left_items, right_title, right_items, note=None):
    """左右对比图。"""
    fig, ax = new_ax(title, (0, 12), (0, 8))
    box(ax, 0.5, 5.6, 5.0, 0.8, left_title, fc=LBLUE, ec=BLUE, fs=11)
    box(ax, 6.5, 5.6, 5.0, 0.8, right_title, fc=LGREEN, ec=GREEN, fs=11)
    for col, items, ec in [(0.5, left_items, BLUE), (6.5, right_items, GREEN)]:
        for i, s in enumerate(items):
            box(ax, col, 4.2 - i * 1.0, 5.0, 0.8, s,
                fc=palette_fc(i), ec=palette_ec(i), fs=9)
    if note:
        ax.text(6, 0.35, note, ha="center", fontsize=9, color=GRAY)
    save(fig, num, title)


def network(num, title, nodes, edges, note=None):
    """多智能体网络拓扑图。nodes=[(label,x,y,color_idx)], edges=[(i,j)]。"""
    fig, ax = new_ax(title, (0, 12), (0, 8))
    pts = []
    for label, x, y, ci in nodes:
        circle(ax, x, y, 0.55, label, fc=palette_fc(ci), ec=palette_ec(ci), fs=8.5)
        pts.append((x, y))
    for i, j in edges:
        x1, y1 = pts[i]; x2, y2 = pts[j]
        arrow(ax, x1, y1, x2, y2, color=GRAY, lw=1.0, ms=10)
    if note:
        ax.text(6, 0.35, note, ha="center", fontsize=9, color=GRAY)
    save(fig, num, title)


def tree(num, title, root, levels, note=None):
    """树状分解图。levels=[[(label,x)...], ...]。"""
    fig, ax = new_ax(title, (0, 12), (0, 8))
    box(ax, 5.0, 6.2, 2.0, 0.9, root, fc=LBLUE, ec=BLUE, fs=10)
    all_levels = [[(root, 6.0, 6.2)]] + [levels_node(l, i) for i, l in enumerate(levels)]
    for li in range(1, len(all_levels)):
        prev = all_levels[li - 1]
        cur = all_levels[li]
        xs = sorted(p[1] for p in cur)
        gap = min([b - a for a, b in zip(xs, xs[1:])] + [9])
        w = min(2.0, max(1.0, gap - 0.25))
        for label, x, y in cur:
            px = min(prev, key=lambda p: abs(p[1] - x))[1]
            arrow(ax, px, prev[0][2], x, y + 0.4, color=GRAY, lw=1.0, ms=10)
            box(ax, x - w / 2, y, w, 0.8, label, fc=palette_fc(li - 1),
                ec=palette_ec(li - 1), fs=9)
    if note:
        ax.text(6, 0.35, note, ha="center", fontsize=9, color=GRAY)
    save(fig, num, title)


def levels_node(lst, depth):
    """把 [(label, x), ...] 转成带 y 坐标的节点。"""
    y = 4.8 - depth * 1.9
    return [(lab, x, y) for lab, x in lst]


def matrix(num, title, rows, cols, note=None):
    """产业落地矩阵 / 二维定位图（散点+象限）。"""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_title(title, fontsize=14, weight="bold", color=DARK, pad=12)
    xs = np.random.RandomState(7).uniform(1, 9, len(rows))
    ys = np.random.RandomState(11).uniform(1, 9, len(rows))
    colors = [palette_ec(i) for i in range(len(rows))]
    ax.scatter(xs, ys, s=180, c=colors, alpha=0.85, edgecolors="white", linewidths=1.2)
    for x, y, lab in zip(xs, ys, rows):
        ax.annotate(lab, (x, y), xytext=(5, 4), textcoords="offset points", fontsize=9)
    ax.axhline(5, color=GRAY, ls=":", lw=0.8)
    ax.axvline(5, color=GRAY, ls=":", lw=0.8)
    ax.set_xlabel(cols[0]); ax.set_ylabel(cols[1]); ax.grid(True, ls=":", alpha=0.3)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    if note:
        ax.text(0.5, -0.18, note, transform=ax.transAxes, fontsize=9, color=GRAY)
    save(fig, num, title)


def curve(num, title, xlabel, ylabel, kind="decay", note=None):
    """示意曲线：衰减 / 增长 / 均衡。"""
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 10, 100)
    if kind == "decay":
        y = 0.15 + 0.8 * np.exp(-x / 2.5)
    elif kind == "growth":
        y = 0.9 * (1 - np.exp(-x / 2.5))
    else:
        y = 0.5 + 0.35 * np.sin(x * 0.6)
    ax.plot(x, y, color=BLUE, lw=2.2)
    if kind == "equilibrium":
        ax.axhline(0.5, color=GREEN, ls="--", lw=1.2)
        ax.text(9.5, 0.52, "均衡", color=GREEN, fontsize=9, ha="right")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=14, weight="bold", color=DARK, pad=12)
    ax.grid(True, ls=":", alpha=0.4)
    if note:
        ax.text(0.02, 0.05, note, transform=ax.transAxes, fontsize=9, color=GRAY)
    save(fig, num, title)


# ---------- 41 张图的具体绘制 ----------
def gen_all():
    # 1-1 四层能力与感知—推理—行动—记忆环路
    fig, ax = new_ax("四层能力与感知—推理—行动—记忆环路", (0, 12), (0, 8))
    items = [("感知", "环境与状态输入"), ("推理", "理解与规划"),
             ("行动", "工具与执行的输出"), ("记忆", "经验与知识沉淀")]
    xs = [0.6, 3.5, 6.4, 9.3]
    for i, ((n, s), x) in enumerate(zip(items, xs)):
        box(ax, x, 3.4, 2.5, 1.1, n, fc=palette_fc(i), ec=palette_ec(i), fs=12)
        ax.text(x + 1.25, 3.1, s, ha="center", fontsize=8.5, color=GRAY)
    for i in range(3):
        arrow(ax, xs[i] + 2.55, 3.95, xs[i + 1] - 0.05, 3.95)
    arrow(ax, 10.55, 3.4, 1.85, 3.4, color=GRAY, rad=0.28)
    ax.text(6, 1.6, "行动改变环境，新感知经记忆修正推理（闭环）",
            ha="center", fontsize=9.5, color=GRAY)
    save(fig, "1-1")

    # 2-1 MDP 与 Bellman 备份
    cycle("2-1", "MDP 与 Bellman 备份",
          ["状态 s", "动作 a", "奖励 r", "下一状态 s'"],
          note="V(s) = max E[r + γV(s')]，价值经备份沿状态—动作链反向传播")

    # 3-1 STRIPS 规划与前向搜索
    flow("3-1", "STRIPS 规划与前向搜索",
         ["初始状态", "适用动作", "状态转移", "目标判定"],
         note="前向搜索在状态空间中逐步应用带前提与效果的动作，直至达到目标")

    # 4-1 纳什均衡与反应曲线
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 10, 200)
    ax.plot(x, 8 - 0.8 * x, color=BLUE, lw=2, label="玩家甲反应曲线")
    ax.plot(x, 7 - 0.7 * x, color=GREEN, lw=2, label="玩家乙反应曲线")
    ax.plot(5.0, 4.0, "o", color=RED, ms=10)
    ax.annotate("纳什均衡", (5, 4), xytext=(6, 5), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_xlabel("玩家甲策略"); ax.set_ylabel("玩家乙策略")
    ax.set_title("纳什均衡与反应曲线", fontsize=14, weight="bold", color=DARK)
    ax.legend(loc="upper right", fontsize=9); ax.grid(True, ls=":", alpha=0.4)
    save(fig, "4-1")

    # 5-1 大语言模型智能体四层架构
    layers("5-1", "大语言模型智能体四层架构",
           [("决策层", "目标理解、推理与规划"),
            ("记忆层", "短期上下文与长期经验"),
            ("工具层", "函数调用、API 与外部服务"),
            ("执行层", "动作生成与环境交互")])

    # 6-1 上下文窗口的构成与增长
    fig, ax = new_ax("上下文窗口的构成与增长", (0, 12), (0, 8))
    segs = [("系统指令", 2.0, BLUE), ("任务说明", 2.6, GREEN),
            ("历史对话", 3.2, AMBER), ("工具结果", 2.4, RED)]
    x = 0.6
    for lab, w, c in segs:
        box(ax, x, 3.4, w, 1.2, lab, fc="white", ec=c, fs=9.5)
        x += w + 0.05
    ax.annotate("窗口容量增长 →", xy=(11, 2.3), xytext=(0.6, 2.3),
                fontsize=10, color=GRAY,
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5))
    ax.text(6, 1.3, "更长的上下文容纳更多历史与工具结果，但需压缩与筛选",
            ha="center", fontsize=9.5, color=GRAY)
    save(fig, "6-1")

    # 7-1 ReAct 推理—行动循环
    cycle("7-1", "ReAct 推理—行动循环",
          ["思考 Thought", "行动 Action", "观察 Observation"],
          note="推理与行动交替进行：观察结果反馈进下一轮思考，直至完成任务")

    # 8-1 智能体框架的功能分层
    layers("8-1", "智能体框架的功能分层",
           [("应用层", "任务编排与多智能体协同"),
            ("能力层", "规划、工具调用、记忆与反思"),
            ("运行时层", "调度、状态管理与错误恢复"),
            ("接口层", "模型、工具与环境的统一接入")])

    # 9-1 智能体评估指标体系
    fig, ax = new_ax("智能体评估指标体系", (0, 12), (0, 8))
    dims = [("任务完成", "成功率 / 效率"), ("推理质量", "正确 / 一致"),
            ("工具使用", "准确 / 规范"), ("鲁棒安全", "抗扰 / 对齐")]
    for i, (t, s) in enumerate(dims):
        a = np.pi / 2 - i * np.pi / 2
        x, y = 6 + 4 * np.cos(a), 4.2 + 2.5 * np.sin(a)
        circle(ax, x, y, 0.85, str(i + 1), fc=palette_fc(i), ec=palette_ec(i), fs=12)
        ax.text(x, y - 1.15, "%s\n%s" % (t, s), ha="center", fontsize=8.5, color=DARK)
        if i > 0:
            pa = np.pi / 2 - (i - 1) * np.pi / 2
            arrow(ax, 6 + 4 * np.cos(pa), 4.2 + 2.5 * np.sin(pa), x, y,
                  color=GRAY, lw=1.0)
    arrow(ax, 6 + 4 * np.cos(3 * np.pi / 2), 4.2 + 2.5 * np.sin(3 * np.pi / 2),
          6 + 4, 4.2, color=GRAY, lw=1.0)
    save(fig, "9-1")

    # 10-1 思维链与自我一致性
    flow("10-1", "思维链与自我一致性",
         ["问题输入", "多条推理路径", "答案汇总", "多数投票"],
         note="采样多条思维链并对答案投票，以一致性提升推理可靠性")

    # 11-1 任务分解与层次规划
    tree("11-1", "任务分解与层次规划", "总目标",
         [[("子任务A", 2.5), ("子任务B", 6.0), ("子任务C", 9.5)],
          [("A1", 2.5), ("A2", 4.0), ("B1", 6.0), ("C1", 9.5)]],
         note="高层目标逐层拆解为可执行的原子子任务")

    # 12-1 思维树与自我反思
    tree("12-1", "思维树与自我反思", "问题",
         [[("思路1", 2.5), ("思路2", 6.0), ("思路3", 9.5)],
          [("评估1", 2.5), ("回溯反思", 6.0), ("评估3", 9.5)]],
         note="对每条思路评估打分，反思后保留优质分支、剪除劣枝")

    # 13-1 世界模型辅助规划闭环
    cycle("13-1", "世界模型辅助规划闭环",
          ["观察", "世界模型预测", "规划行动", "执行与反馈"],
          note="智能体在内部模型中预演后果，再据真实反馈校正模型")

    # 14-1 规划成功率随长度的衰减
    curve("14-1", "规划成功率随长度的衰减", "规划步数（长度）", "成功率",
          kind="decay", note="任务链越长，误差累积导致成功率下降")

    # 15-1 工具调用与函数调用流程
    flow("15-1", "工具调用与函数调用流程",
         ["意图识别", "参数生成", "函数调用", "结果解析"],
         note="模型输出结构化调用请求，执行后把结果回填上下文")

    # 16-1 代码生成—执行—反馈循环
    cycle("16-1", "代码生成—执行—反馈循环",
          ["生成代码", "沙箱执行", "错误/反馈", "修正代码"],
          note="执行结果（含报错）作为反馈驱动迭代修正，直至通过验证")

    # 17-1 网页与 GUI 智能体的操作循环
    cycle("17-1", "网页与 GUI 智能体的操作循环",
          ["读取界面", "定位元素", "执行操作", "观察变化"],
          note="通过感知界面状态、定位目标元素并操作，循环推进任务")

    # 18-1 外部服务集成架构
    layers("18-1", "外部服务集成架构",
           [("智能体核心", "编排与决策"),
            ("适配与鉴权", "接口封装与凭证管理"),
            ("服务总线", "检索、数据库、第三方 API"),
            ("外部系统", "业务应用与数据源")])

    # 19-1 验证与回滚流程
    flow("19-1", "验证与回滚流程",
         ["执行前快照", "执行操作", "结果验证", "失败回滚"],
         note="预置快照与验证关卡，异常时回滚到一致状态")

    # 20-1 智能体记忆分层架构
    layers("20-1", "智能体记忆分层架构",
           [("感觉记忆", "瞬时感官输入"),
            ("工作记忆", "当前上下文与任务状态"),
            ("情景记忆", "过往交互与事件"),
            ("语义记忆", "结构化知识与经验")])

    # 21-1 工作记忆与压缩
    flow("21-1", "工作记忆与压缩",
         ["上下文累积", "重要性评估", "摘要与压缩", "保留关键项"],
         note="当上下文接近容量上限时，压缩与筛选以保留关键信息")

    # 22-1 长期记忆的写入与检索流程
    flow("22-1", "长期记忆的写入与检索流程",
         ["经验提取", "向量化存储", "相似度检索", "注入上下文"],
         note="经验写入向量库，需要时按相关性检索并注入工作记忆")

    # 23-1 经验学习与自我改进的闭环
    cycle("23-1", "经验学习与自我改进的闭环",
          ["执行任务", "反思成败", "提炼经验", "更新策略"],
          note="从执行轨迹中提炼可复用经验，持续迭代策略")

    # 24-1 中心化与去中心化结构对比
    compare("24-1", "中心化与去中心化结构对比",
            "中心化", ["单一协调器", "统一调度", "信息汇聚", "瓶颈与单点"],
            "去中心化", ["对等智能体", "局部决策", "协商通信", "鲁棒但更难协调"])

    # 25-1 层级式与扁平式多智能体组织
    compare("25-1", "层级式与扁平式多智能体组织",
            "层级式", ["管理—执行分层", "指令自上而下", "职责清晰", "决策链较长"],
            "扁平式", ["智能体对等", "自主协商", "响应快速", "协调成本高"])

    # 26-1 合同网协议的协商流程
    cycle("26-1", "合同网协议的协商流程",
          ["任务招标", "智能体投标", "评标授标", "履约执行"],
          note="管理方发布任务，候选方投标，择优授标后执行并回报")

    # 27-1 多智能体辩论与投票的聚合流程
    fig, ax = new_ax("多智能体辩论与投票的聚合流程", (0, 12), (0, 8))
    for i in range(4):
        x = 1.5 + i * 3.0
        circle(ax, x, 5.2, 0.55, "A%d" % (i + 1),
               fc=palette_fc(i), ec=palette_ec(i), fs=9)
        arrow(ax, x, 4.65, 6.0, 2.9, color=GRAY, lw=1.0)
    box(ax, 4.8, 1.9, 2.4, 1.0, "投票/聚合", fc=LAMBER, ec=AMBER, fs=10)
    ax.text(6, 0.5, "多智能体提出并辩论观点，经投票或加权聚合形成共识",
            ha="center", fontsize=9, color=GRAY)
    save(fig, "27-1")

    # 28-1 值分解与集中式训练分散式执行
    compare("28-1", "值分解与集中式训练分散式执行",
            "集中式训练", ["全局状态信息", "联合价值函数", "协调更充分", "训练开销大"],
            "分散式执行", ["局部观测输入", "个体价值分解", "可扩展性强", "协调受限"])

    # 29-1 生成式智能体的社会模拟
    network("29-1", "生成式智能体的社会模拟",
            [("A", 3, 5.5, 0), ("B", 6, 6.2, 1), ("C", 9, 5.2, 2),
             ("D", 4.5, 3.0, 3), ("E", 7.5, 3.2, 0), ("F", 6.0, 1.6, 1)],
            [(0, 1), (1, 2), (0, 3), (1, 4), (2, 4), (3, 4), (3, 5), (4, 5)],
            note="多个生成式智能体在交互中涌现社会行为与群体模式")

    # 30-1 MCP 与 A2A 的分层协议栈
    layers("30-1", "MCP 与 A2A 的分层协议栈",
           [("应用层", "智能体与业务编排"),
            ("A2A 层", "智能体间发现与协作"),
            ("MCP 层", "工具与资源的统一接入"),
            ("传输层", "消息、会话与安全")])

    # 31-1 智能体互联网的发现与调用流程
    flow("31-1", "智能体互联网的发现与调用流程",
         ["能力注册", "服务发现", "协商调用", "结果返回"],
         note="智能体在开放网络中发现彼此能力，按协议协商并完成调用")

    # 32-1 智能体身份、权限与信任框架
    fig, ax = new_ax("智能体身份、权限与信任框架", (0, 12), (0, 8))
    circle(ax, 6, 4.3, 1.3, "可信\n智能体", fc=LBLUE, ec=BLUE, fs=11)
    labels = [("身份", 2.0, 6.0), ("权限", 10.0, 6.0), ("审计", 2.0, 2.2), ("声誉", 10.0, 2.2)]
    for i, (lab, x, y) in enumerate(labels):
        circle(ax, x, y, 0.75, lab, fc=palette_fc(i), ec=palette_ec(i), fs=10)
        arrow(ax, x, y, 6, 4.3, color=GRAY, lw=1.0)
    save(fig, "32-1")

    # 33-1 智能体服务市场的供需均衡
    curve("33-1", "智能体服务市场的供需均衡", "服务价格", "供给 / 需求",
          kind="equilibrium", note="供需曲线交点决定市场均衡价格与交易量")

    # 34-1 智能体评估的多维指标体系
    dims = ["任务成功率", "效率", "鲁棒性", "泛化", "安全性", "对齐", "成本", "可解释"]
    fig, ax = plt.subplots(figsize=(8, 5), subplot_kw=dict(polar=True))
    n = len(dims)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values = [0.8, 0.65, 0.7, 0.6, 0.9, 0.75, 0.85, 0.7]
    values += values[:1]; angles += angles[:1]
    ax.plot(angles, values, color=BLUE, lw=2)
    ax.fill(angles, values, color=BLUE, alpha=0.25)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(dims, fontsize=9)
    ax.set_title("智能体评估的多维指标体系", fontsize=14, weight="bold", color=DARK, pad=16)
    save(fig, "34-1")

    # 35-1 奖励攻击的形成机制
    flow("35-1", "奖励攻击的形成机制",
         ["代理指标设定", "智能体优化指标", "偏离真实目标", "奖励被操纵"],
         note="优化代理指标可能钻空子，导致指标高而真实目标未达成")

    # 36-1 智能体安全的纵深防御
    layers("36-1", "智能体安全的纵深防御",
           [("对齐层", "指令与价值对齐"),
            ("输入层", "提示注入与越权防护"),
            ("执行层", "最小权限与沙箱隔离"),
            ("监控层", "运行时审计与拦截")])

    # 37-1 智能体治理的多层框架
    layers("37-1", "智能体治理的多层框架",
           [("国际与法规", "合规与责任界定"),
            ("组织层", "政策与风险管理"),
            ("系统层", "审计与可追溯"),
            ("个体层", "透明与人类监督")])

    # 38-1 自主智能体的产业落地矩阵
    matrix("38-1", "自主智能体的产业落地矩阵",
           ["客服", "研发", "运营", "金融", "医疗", "教育", "制造"],
           ("技术成熟度", "自主程度"),
           note="横轴为技术成熟度，纵轴为自主程度")

    # 39-1 自主性的三维与通用智能
    fig, ax = plt.subplots(figsize=(8, 5), subplot_kw=dict(projection="3d"))
    ax.set_title("自主性的三维与通用智能", fontsize=14, weight="bold", color=DARK, pad=12)
    ax.scatter([0.8, 0.5, 0.9], [0.6, 0.85, 0.3], [0.7, 0.5, 0.9],
               c=[BLUE, GREEN, AMBER], s=160)
    ax.set_xlabel("自主决策"); ax.set_ylabel("泛化能力"); ax.set_zlabel("适应性")
    save(fig, "39-1")

    # 40-1 开放问题全景图
    fig, ax = new_ax("开放问题全景图", (0, 12), (0, 8))
    qs = ["可靠性", "对齐", "安全", "评估", "幻觉", "记忆", "协作", "成本", "治理"]
    for i, q in enumerate(qs):
        a = np.pi / 2 - i * 2 * np.pi / len(qs)
        x, y = 6 + 4 * np.cos(a), 4.2 + 2.6 * np.sin(a)
        circle(ax, x, y, 0.8, q, fc=palette_fc(i), ec=palette_ec(i), fs=8.5)
    circle(ax, 6, 4.2, 1.1, "开放\n问题", fc=LRED, ec=RED, fs=10)
    save(fig, "40-1")

    # 41-1 全书理论地图
    flow("41-1", "全书理论地图",
         ["基础理论", "单体架构", "工具与记忆", "多智能体系统", "安全治理与展望"],
         note="从决策与规划基础出发，经单体能力、工具与记忆，走向多智能体与治理")

    print("配图生成完成：共 41 张")


if __name__ == "__main__":
    gen_all()
