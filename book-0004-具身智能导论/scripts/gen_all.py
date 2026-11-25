# -*- coding: utf-8 -*-
"""《具身智能导论》配图脚本。运行 python scripts/gen_figures.py 与 gen_diagrams.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)
BLUE="#2C5F8A"; LIGHT="#E8F0F7"; GREEN="#2E7D5B"; LGREEN="#E6F2EA"
AMBER="#B07D2B"; LAMBER="#F8EFDD"; RED="#A33B3B"; GRAY="#5A5A5A"; DARK="#1A3350"

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("已生成:", name)

def box(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=10, tc=DARK):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.05",
                 linewidth=1.2,edgecolor=ec,facecolor=fc))
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,color=tc)

def arrow(ax, x1,y1,x2,y2, color=BLUE, rad=0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=12,
                 linewidth=1.2,color=color,connectionstyle=f"arc3,rad={rad}"))

def base(ax, xlim, ylim, title):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    ax.text(sum(xlim)/2, ylim[1]-0.1, title, ha="center", va="top", fontsize=14, weight="bold", color=DARK)

def flow(name, title, steps, fc=LIGHT):
    fig, ax = plt.subplots(figsize=(11,4)); base(ax,(0,12),(0,4),title)
    n=len(steps); xs=[0.3+i*(11.4/n) for i in range(n)]; w=min(2.2,11.4/n-0.15)
    for s,x in zip(steps,xs): box(ax,x,1.3,w,0.9,s,fc=fc,fs=9.5)
    for i in range(n-1): arrow(ax,xs[i]+w+0.02,1.75,xs[i+1]-0.03,1.75)
    save(fig,name)

def fig_1_1():
    fig,ax=plt.subplots(figsize=(11,4)); base(ax,(0,12),(0,4),"具身智能四层能力与闭环")
    items=[("感知","世界状态"),("理解","语义/任务"),("规划","行动序列"),("执行","精确动作")]
    xs=[0.3,3.3,6.3,9.3]
    for (n,s),x in zip(items,xs):
        box(ax,x,1.4,2.4,0.9,n,fs=12); ax.text(x+1.2,1.15,s,ha="center",fontsize=9,color=GRAY)
    for i in range(3): arrow(ax,xs[i]+2.45,1.85,xs[i+1]-0.05,1.85)
    arrow(ax,10.5,1.4,1.5,1.4,color=GRAY,rad=0.25)
    ax.text(6,0.35,"执行改变世界，新感知修正理解（闭环）",ha="center",fontsize=9,color=GRAY)
    save(fig,"图1-1.png")

def fig_1_3():
    fig,ax=plt.subplots(figsize=(9,4)); base(ax,(0,10),(0,4),"感知—认知—行动闭环")
    for i,(n,fc) in enumerate([("感知",LIGHT),("认知",LGREEN),("行动",LAMBER)]):
        box(ax,1+i*3,1.3,2.2,0.9,n,fc=fc,fs=12)
    arrow(ax,3.2,1.75,4,1.75); arrow(ax,6.2,1.75,7,1.75)
    arrow(ax,8.1,1.3,2.1,1.3,color=GRAY,rad=0.25)
    save(fig,"图1-3.png")

def fig_13_1():
    fig,ax=plt.subplots(figsize=(10,4)); base(ax,(0,11),(0,4),"抓取与灵巧操作")
    flow_steps=["视觉定位","位姿估计","抓取综合","轨迹规划","力控执行"]
    flow("图13-1.png","抓取与灵巧操作",flow_steps,LGREEN)

if __name__ == "__main__":
    figs = {
      "图1-1.png": fig_1_1, "图1-3.png": fig_1_3,
    }
    fig_1_1(); fig_1_3()
    flow("图1-2.png","具身智能历史演进",["控制论/行为主义","概率机器人","深度学习","VLA/基础模型"],LIGHT)
    flow("图2-1.png","具身认知核心主张",["身体结构","感知能力","环境交互","智能涌现"],LGREEN)
    flow("图3-1.png","刚体变换与坐标系",["基座系","连杆系","末端系","齐次变换"],LIGHT)
    flow("图4-1.png","反馈控制闭环",["期望","误差","控制器","对象","输出"],LIGHT)
    flow("图5-1.png","视觉感知流水线",["图像","检测/分割","位姿估计","下游任务"],LIGHT)
    flow("图6-1.png","触觉与力感知",["接触","触觉传感","力反馈","抓握调整"],LGREEN)
    flow("图7-1.png","SLAM系统流程",["传感器","前端里程计","后端优化","建图/回环"],LIGHT)
    flow("图8-1.png","传感器融合与滤波",["多传感器","预测","更新","状态估计"],LGREEN)
    flow("图9-1.png","场景图与语义接地",["感知物体","关系抽取","场景图","任务推理"],LAMBER)
    flow("图10-1.png","构型空间与路径规划",["C-space","采样","避碰","路径"],LIGHT)
    flow("图10-2.png","RRT采样规划",["随机采样","最近节点","扩展","到达目标"],LGREEN)
    flow("图11-1.png","全身控制框架",["任务规划","全身控制","关节力矩","执行"],LIGHT)
    flow("图12-1.png","MPC轨迹优化",["状态","滚动优化","约束","控制序列"],LAMBER)
    flow("图13-1.png","抓取与灵巧操作",["视觉定位","抓取综合","轨迹规划","力控执行"],LGREEN)
    flow("图14-1.png","移动与导航",["定位","全局规划","局部避障","底盘控制"],LIGHT)
    flow("图15-1.png","行为克隆与DAgger",["专家示范","学策略","聚合数据","重训"],LIGHT)
    flow("图16-1.png","模仿vs逆强化学习",["示范","学动作(BC)","学奖励(IRL)","RL优化"],LGREEN)
    flow("图17-1.png","扩散策略",["观测","条件扩散","动作序列","去噪生成"],LAMBER)
    flow("图18-1.png","遥操作数据采集",["操作员","主端设备","从端机器人","数据记录"],LIGHT)
    flow("图19-1.png","机器人RL循环",["状态","策略","动作","奖励","更新"],LGREEN)
    flow("图20-1.png","仿真到现实迁移",["仿真训练","缩小差距","真实部署","微调"],LIGHT)
    flow("图21-1.png","域随机化",["参数分布","多仿真环境","鲁棒策略","真实迁移"],LAMBER)
    flow("图22-1.png","离线强化学习",["固定数据","保守Q","学策略","部署"],LGREEN)
    flow("图23-1.png","技能组合泛化",["技能库","组合","新任务","泛化"],LIGHT)
    flow("图24-1.png","VLM在机器人",["图像+语言","VLM","开放词汇感知","推理"],LIGHT)
    flow("图25-1.png","VLA模型架构",["视觉编码","语言编码","融合","动作生成"],LGREEN)
    flow("图26-1.png","通用机器人策略",["单一模型","多机器人","多任务","泛化"],LIGHT)
    flow("图27-1.png","语言指令到动作",["语言","解析","分解","接地","动作"],LAMBER)
    flow("图28-1.png","具身基础模型",["大规模预训练","适配","多任务","通用"],LGREEN)
    flow("图29-1.png","机器人仿真器",["物理引擎","渲染","传感器","机器人模型"],LIGHT)
    flow("图30-1.png","现实差距与域迁移",["仿真域","差异","迁移方法","真实域"],LAMBER)
    flow("图31-1.png","数据飞轮",["部署","收集数据","训练","改进"],LGREEN)
    flow("图32-1.png","世界模型与具身学习",["交互","学世界模型","想象学习","部署"],LIGHT)
    flow("图33-1.png","具身评估维度",["成功率","效率","鲁棒性","泛化","安全"],LIGHT)
    flow("图34-1.png","数据规模与能力",["数据量","质量","多样性","能力"],LGREEN)
    flow("图35-1.png","安全与可靠性框架",["安全约束","运行时监控","故障恢复","人机共处"],LRED if False else LAMBER)
    flow("图36-1.png","具身系统工程",["感知","规划","控制","执行","运维"],LIGHT)
    flow("图37-1.png","人形机器人形态",["人形","轮式","四足","权衡"],LGREEN)
    flow("图38-1.png","具身智能与通用智能",["离身(LLM)","具身","汇合","AGI"],LIGHT)
    flow("图41-1.png","全书框架回扣",["九篇","四层能力","闭环","通用智能"],LIGHT)
    # 数据图
    fig,ax=plt.subplots(figsize=(7,5))
    steps=np.arange(1,11); curve=1-0.5*np.exp(-steps/3)
    ax.plot(steps,curve,"o-",color=GREEN,lw=2)
    ax.set_xlabel("数据规模"); ax.set_ylabel("成功率（示意）"); ax.set_title("数据规模与能力",fontsize=13,color=DARK,weight="bold")
    ax.grid(True,ls=":",alpha=0.4); save(fig,"图34-1.png")
    print("配图生成完成")
