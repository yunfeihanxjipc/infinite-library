# -*- coding: utf-8 -*-
"""《世界模型导论》概念 / 架构 / 流程示意图。运行: python scripts/gen_diagrams.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

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
    ax.add_patch(FancyBboxPatch((x,y), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
                 linewidth=1.2, edgecolor=ec, facecolor=fc))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs, color=tc)

def arrow(ax, x1, y1, x2, y2, color=BLUE, rad=0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2), arrowstyle="-|>", mutation_scale=12,
                 linewidth=1.2, color=color, connectionstyle=f"arc3,rad={rad}"))

def base(ax, xlim, ylim, title):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    ax.text(sum(xlim)/2, ylim[1]-0.1, title, ha="center", va="top", fontsize=14, weight="bold", color=DARK)

def fig_1_1():
    fig, ax = plt.subplots(figsize=(12,3)); base(ax,(0,12),(0,3),"世界模型四层含义")
    items=[("观测建模","信号是什么"),("状态表示","本质状态"),("动力学学习","如何演化"),("基于模型规划","如何行动")]
    xs=[0.3,3.3,6.3,9.3]
    for (n,s),x in zip(items,xs):
        box(ax,x,1.0,2.4,1.0,n,fs=13); ax.text(x+1.2,0.75,s,ha="center",fontsize=9,color=GRAY)
    for i in range(3): arrow(ax,xs[i]+2.45,1.5,xs[i+1]-0.05,1.5)
    save(fig,"图1-1.png")

def fig_1_2():
    fig, ax = plt.subplots(figsize=(14,4.5)); base(ax,(0,14),(0,4.5),"世界模型方法演进")
    ph=[("控制/状态空间","1960s Kalman",LIGHT),("POMDP/认知","1970-90s",LGREEN),
        ("深度世界模型","2018-20 World Models/Dreamer",LAMBER),
        ("生成式/JEPA","2021-23 Sora/JEPA","#F0EAF7"),("交互/通用","2024-26","#F7E9E9")]
    xs=[0.3+i*2.75 for i in range(5)]
    for (n,s,fc),x in zip(ph,xs):
        box(ax,x,1.5,2.5,1.2,n,fc=fc,fs=10); ax.text(x+1.25,1.25,s,ha="center",fontsize=8,color=GRAY)
    for i in range(4): arrow(ax,xs[i]+2.55,2.1,xs[i+1]-0.05,2.1)
    save(fig,"图1-2.png")

def fig_1_3():
    fig, ax = plt.subplots(figsize=(9,6)); base(ax,(0,10),(0,7),"世界模型七要素")
    center=(5,3.5); box(ax,4,2.9,2,1.2,"世界模型",fc=LIGHT,fs=12)
    els=["E1 状态表示","E2 状态转移","E3 观测生成","E4 不确定性","E5 动作条件化","E6 奖励目标","E7 基于模型规划"]
    import numpy as np
    for i,e in enumerate(els):
        ang=2*np.pi*i/7 - np.pi/2; x=5+3.5*np.cos(ang); y=3.5+2.5*np.sin(ang)
        box(ax,x-1.0,y-0.35,2.0,0.7,e,fc=LGREEN if i<4 else LAMBER,fs=8.5)
        arrow(ax,5+1.0*np.cos(ang),3.5+1.0*np.sin(ang),x-1.0*np.cos(ang),y-0.35*np.sin(ang),color=GRAY)
    save(fig,"图1-3.png")

def fig_2_1():
    fig, ax = plt.subplots(figsize=(9,4)); base(ax,(0,10),(0,4),"线性高斯状态空间模型")
    box(ax,0.5,2.4,2.0,0.8,"状态 s_t",fc=LIGHT,fs=11)
    box(ax,4.0,2.4,2.0,0.8,"状态 s_t+1",fc=LIGHT,fs=11)
    box(ax,4.0,0.6,2.0,0.8,"观测 o_t",fc=LGREEN,fs=11)
    arrow(ax,2.5,2.8,4.0,2.8,color=BLUE); ax.text(3.25,3.0,"A,B",ha="center",fontsize=9,color=GRAY)
    arrow(ax,5.0,2.4,5.0,1.4,color=GREEN); ax.text(5.2,1.9,"C",fontsize=9,color=GRAY)
    ax.text(5,0.2,"过程噪声 Q / 观测噪声 R",ha="center",fontsize=9,color=GRAY)
    save(fig,"图2-1.png")

def fig_4_1():
    fig, ax = plt.subplots(figsize=(10,4)); base(ax,(0,11),(0,4),"MPC 滚动优化")
    for i,x in enumerate([1,4,7]):
        box(ax,x,1.5,2.0,0.8,f"时刻 t+{i}",fc=LIGHT,fs=10)
    for i in range(2):
        arrow(ax,[3,6][i],1.9,[4,7][i],1.9)
    ax.annotate("执行第一步，下时刻重规划",xy=(2,1.0),xytext=(5.5,0.4),ha="center",fontsize=9,color=GRAY,
                arrowprops=dict(arrowstyle="->",color=GRAY))
    save(fig,"图4-1.png")

def fig_5_1():
    fig, ax = plt.subplots(figsize=(9,4)); base(ax,(0,10),(0,4),"HMM：隐藏状态与观测发射")
    for i,x in enumerate([2,5,8]):
        ax.add_patch(Circle((x,2.4),0.45,fc=LIGHT,ec=BLUE,lw=1.3)); ax.text(x,2.4,f"s{i+1}",ha="center",va="center",fontsize=10)
        box(ax,x-0.45,0.7,0.9,0.6,f"o{i+1}",fc=LGREEN,fs=9)
        arrow(ax,x,1.95,x,1.3,color=GREEN)
    for i in range(2): arrow(ax,[2.45,5.45][i],2.4,[5-0.45,8-0.45][i],2.4)
    save(fig,"图5-1.png")

def fig_6_1():
    fig, ax = plt.subplots(figsize=(9,4)); base(ax,(0,10),(0,4),"POMDP 信念更新循环")
    box(ax,0.5,1.3,2.2,0.9,"信念 b_t",fc=LIGHT,fs=10)
    box(ax,3.8,1.3,2.2,0.9,"动作 a_t",fc=LGREEN,fs=10)
    box(ax,7.0,1.3,2.2,0.9,"观测 o_t+1",fc=LAMBER,fs=10)
    arrow(ax,2.7,1.75,3.8,1.75); arrow(ax,6.0,1.75,7.0,1.75)
    arrow(ax,8.1,1.3,1.6,1.3,color=GRAY,rad=0.25)
    ax.text(5,0.4,"贝叶斯更新 → b_t+1",ha="center",fontsize=9,color=GRAY)
    save(fig,"图6-1.png")

def fig_7_1():
    fig, ax = plt.subplots(figsize=(11,3.5)); base(ax,(0,12),(0,3.5),"系统辨识流程")
    st=["实验设计","数据采集","模型结构","参数估计","模型验证"]
    xs=[0.3+i*2.4 for i in range(5)]
    for s,x in zip(st,xs): box(ax,x,1.2,2.0,0.9,s,fc=LIGHT if x<8 else LGREEN,fs=10)
    for i in range(4): arrow(ax,xs[i]+2.05,1.65,xs[i+1]-0.05,1.65)
    save(fig,"图7-1.png")

def fig_9_1():
    fig, ax = plt.subplots(figsize=(10,4)); base(ax,(0,11),(0,4),"VAE 架构与 ELBO")
    box(ax,0.5,1.3,2.0,0.9,"观测 o",fc=LIGHT,fs=11)
    box(ax,3.2,1.3,2.4,0.9,"编码器 q(s|o)",fc=LGREEN,fs=10)
    box(ax,6.3,1.3,1.8,0.9,"潜在 s",fc=LAMBER,fs=10)
    box(ax,8.6,1.3,2.0,0.9,"解码器 p(o|s)",fc=LGREEN,fs=10)
    for a,b in [(2.5,3.2),(5.6,6.3),(8.1,8.6)]: arrow(ax,a,1.75,b,1.75)
    ax.text(5.5,0.4,"损失 = 重建误差 + KL(后验||先验)",ha="center",fontsize=9.5,color=GRAY)
    save(fig,"图9-1.png")

def fig_10_1():
    fig, ax = plt.subplots(figsize=(11,4)); base(ax,(0,12),(0,4),"World Models 三模块")
    box(ax,0.3,1.2,3.0,1.0,"V: VAE 编码观测",fc=LIGHT,fs=10)
    box(ax,4.5,1.2,3.0,1.0,"M: MDN-RNN 动力学",fc=LGREEN,fs=10)
    box(ax,8.7,1.2,3.0,1.0,"C: 线性控制器",fc=LAMBER,fs=10)
    arrow(ax,3.3,1.7,4.5,1.7); arrow(ax,7.5,1.7,8.7,1.7)
    arrow(ax,10.2,1.2,2.0,1.2,color=GRAY,rad=0.15)
    ax.text(6,0.35,"控制器输出动作，作用于环境产生下一观测",ha="center",fontsize=9,color=GRAY)
    save(fig,"图10-1.png")

def fig_11_1():
    fig, ax = plt.subplots(figsize=(9,4)); base(ax,(0,10),(0,4),"RSSM：确定性 + 随机状态")
    box(ax,0.5,2.2,2.4,0.9,"确定性 h_t (GRU)",fc=LIGHT,fs=10)
    box(ax,3.6,2.2,2.4,0.9,"随机 z_t (采样)",fc=LGREEN,fs=10)
    box(ax,6.8,2.2,2.6,0.9,"预测 s_t+1 / o_t",fc=LAMBER,fs=9.5)
    arrow(ax,2.9,2.65,3.6,2.65); arrow(ax,6.0,2.65,6.8,2.65)
    ax.text(5,0.6,"确定性承载长程记忆，随机性承载不确定性",ha="center",fontsize=9,color=GRAY)
    save(fig,"图11-1.png")

def fig_12_1():
    fig, ax = plt.subplots(figsize=(11,4)); base(ax,(0,12),(0,4),"Dreamer：想象训练")
    box(ax,0.3,1.3,2.5,0.9,"RSSM 潜在状态",fc=LIGHT,fs=10)
    box(ax,3.4,1.3,2.5,0.9,"想象轨迹",fc=LGREEN,fs=10)
    box(ax,6.6,1.3,2.5,0.9,"演员 π / 评论家 V",fc=LAMBER,fs=9.5)
    box(ax,9.6,1.3,2.2,0.9,"真实动作",fc=LIGHT,fs=10)
    for a,b in [(2.8,3.4),(5.9,6.6),(9.1,9.6)]: arrow(ax,a,1.75,b,1.75)
    save(fig,"图12-1.png")

def fig_13_1():
    fig, ax = plt.subplots(figsize=(7,5))
    import numpy as np
    rng=np.random.default_rng(1)
    for c,col in [(0,BLUE),(1,GREEN),(2,AMBER)]:
        pts=rng.normal(loc=[c*3,c*2],scale=0.6,size=(30,2))
        ax.scatter(pts[:,0],pts[:,1],color=[BLUE,GREEN,AMBER][c],alpha=0.6,label=f"任务{c+1}")
    ax.set_title("潜在状态可视化（示意）",fontsize=13,weight="bold",color=DARK)
    ax.legend(fontsize=9); ax.grid(True,ls=":",alpha=0.3)
    save(fig,"图13-1.png")

def generic_linear(name, title, steps, fc=LIGHT):
    fig, ax = plt.subplots(figsize=(11,4)); base(ax,(0,12),(0,4),title)
    n=len(steps); xs=[0.3+i*(11.4/n) for i in range(n)]
    w=min(2.2,11.4/n-0.15)
    for s,x in zip(steps,xs): box(ax,x,1.3,w,0.9,s,fc=fc,fs=9.5)
    for i in range(n-1): arrow(ax,xs[i]+w+0.02,1.75,xs[i+1]-0.03,1.75)
    save(fig,name)

if __name__ == "__main__":
    fig_1_1(); fig_1_2(); fig_1_3(); fig_2_1(); fig_4_1(); fig_5_1(); fig_6_1()
    fig_7_1(); fig_9_1(); fig_10_1(); fig_11_1(); fig_12_1(); fig_13_1()
    generic_linear("图14-1.png","扩散模型：前向加噪与反向去噪",["o_0","加噪","o_T","去噪","o_0"],LAMBER)
    generic_linear("图15-1.png","视频扩散的时空建模",["视频帧","时空patch","时空注意力","去噪","生成视频"])
    generic_linear("图16-1.png","Sora：时空 patch + Transformer",["视频","时空patch","DiT去噪","生成视频"])
    generic_linear("图17-1.png","自回归 vs 扩散",["token序列","顺序预测","vs","并行去噪","连续状态"])
    generic_linear("图18-1.png","NeRF / 3DGS",["多视角图像","3D表示","体积渲染","新视角"],LAMBER)
    generic_linear("图19-1.png","预测编码与自由能",["观测","预测","预测误差","更新模型"],LGREEN)
    generic_linear("图20-1.png","I-JEPA 联合嵌入预测",["上下文编码","预测器","目标表示","匹配损失"])
    generic_linear("图21-1.png","V-JEPA 视频预测编码",["视频patch","遮盖","上下文编码","预测表示"],LGREEN)
    generic_linear("图23-1.png","动作条件化受控动力学",["状态 s_t","动作 a_t","转移 f","状态 s_t+1"],LAMBER)
    generic_linear("图24-1.png","MBRL 想象滚动",["真实数据","学模型","想象轨迹","训练策略"],LGREEN)
    generic_linear("图25-1.png","MPC 规划循环",["观测","编码状态","模型中搜索","执行动作"],LIGHT)
    generic_linear("图27-1.png","交互世界模型闭环",["用户动作","世界模型","生成观测","反馈循环"],LAMBER)
    generic_linear("图28-1.png","PINN：数据 + 物理约束",["数据损失","物理残差","联合损失","物理一致模型"],LGREEN)
    generic_linear("图29-1.png","可微物理",["模拟","损失","梯度","优化参数/动作"],LAMBER)
    generic_linear("图30-1.png","3D 表示与神经渲染",["多视角输入","3D表示","神经渲染","新视角"],LIGHT)
    generic_linear("图31-1.png","仿真到现实迁移",["仿真训练","域随机化","真实部署","迁移"],LGREEN)
    generic_linear("图32-1.png","世界模型评估维度",["重建质量","预测准确","可控性","决策价值"],LAMBER)
    generic_linear("图36-1.png","LeCun 自主智能架构",["感知","世界模型","成本","规划器","执行"],LIGHT)
    generic_linear("图38-1.png","多智能体世界模型",["智能体1","智能体2","共享世界","社会涌现"],LGREEN)
    generic_linear("图41-1.png","全书框架回扣",["九篇","四层能力","七要素","通用智能"],LIGHT)
    print("概念图生成完成")
