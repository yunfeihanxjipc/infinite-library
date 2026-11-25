# 第 12 章　模型预测控制与轨迹优化

第 10 章的规划给出路径，第 11 章的控制器跟踪轨迹。本章深入**模型预测控制**（model predictive control，MPC）在机器人中的实现——它在有限时域内基于动力学模型（第 3 章）滚动优化控制序列（见《世界模型导论》第 8、25 章），能显式处理约束与非线性，是机器人高级控制的主流方法。本章先给出 MPC 的标准公式与滚动机制（12.1 节），推导直接/间接法与 DDP/iLQR（12.2—12.3 节），讨论接触丰富任务的特殊困难（12.4 节），给出数值算例（12.5 节），梳理谱系（12.6 节），最后辨析边界并承上启下（12.7 节）。

## 12.1　引入动机与机器人 MPC

**动机。** 第 10 章的路径规划忽略动力学，第 11 章的反馈控制不预测未来约束。MPC 把两者结合：在每个控制周期求解一个有限时域最优控制问题，只执行第一步，下一周期用新观测重新求解（**滚动时域**，receding horizon）。这带来三大好处：① 显式处理状态/控制约束（关节限位、力矩上限、摩擦锥、避碰）；② 对扰动与模型误差有反馈校正（每步重规划）；③ 天然适用于非线性、多变量系统——这正是机器人所需的。

**直觉解释。** MPC 就像开车时不断「重新规划路线」：你不会在出发时定死一条路线开到底，而是每隔几秒看一眼当前位置与周围车流，重新规划接下来一小段的最优走法，然后只执行最近的一步——下一秒再看再规划。这样即使有人加塞（扰动）或走错路（模型误差），也能及时纠正。有限时域 $H$ 对应「只看未来几步」，滚动重规划对应「边走边看」。

**定义 12.1（机器人 MPC）**　在时刻 $t$ 求解有限时域约束最优控制：

$$
\begin{aligned}
\min_{\{u_k\}_{k=0}^{H-1}}\quad & J=\sum_{k=0}^{H-1}\ell(x_k,u_k)+\ell_f(x_H)\\
\mathrm{s.t.}\quad & x_{k+1}=f(x_k,u_k),\ x_0=x_t,\\
& x_k\in\mathcal{X},\ u_k\in\mathcal{U}.
\end{aligned} \tag{12-1}
$$

其中 $x$ 为状态（关节角与速度，或质心状态），$u$ 为控制（力矩、接触力或速度指令），$\ell$ 为阶段代价（跟踪误差 + 控制能量），$\ell_f$ 为终端代价，$\mathcal{X},\mathcal{U}$ 为约束集。求解后取 $u_0^*$ 施加，下一时刻以新的 $x_{t+1}$ 重解——式 (12-1) 每周期求解一次。

**稳定性机制。** 滚动时域提供隐式反馈：若实际状态偏离预测，下一周期优化从新状态出发，相当于闭环。终端代价 $\ell_f$（或终端约束集）可提供稳定性保证（类似的 Lyapunov 论证见第 4 章）——这是 MPC 区别于开环轨迹优化的关键。

### 12.1A　终端约束与终端集：稳定性的显式保证

仅靠终端代价 $\ell_f$ 的稳定性论证较松，**终端集 + 终端控制器**给出更强的递推可行性保证。设存在一个终端控制律 $u_f$ 与终端集 $\mathcal X_f\subseteq\mathcal X$，使得：① $\mathcal X_f$ 在 $u_f$ 下**不变**（$x\in\mathcal X_f\Rightarrow f(x,u_f(x))\in\mathcal X_f$）；② $\ell_f$ 是**离散 Lyapunov 函数**（$\ell_f(f(x,u_f(x)))\le\ell_f(x)-\ell(x,u_f(x))$）；③ 终端约束 $x_H\in\mathcal X_f$ 加入式 (12-1)。则对任意可行初态，MPC 解的存在性可递推证明（当前解的后 $H-1$ 步 + $u_f$ 一步构成下一时刻的可行解），闭环稳定性由 $\ell_f$ 的 Lyapunov 性保证。对线性系统，$\mathcal X_f$ 常取 $u_f$ 的**最大不变集**（MI Set，可用半代数/线性不等式求解）；对非线性系统，可用 Lyapunov 子水平集 $V(x)\le c$ 近似。工程上，终端集的大小直接决定「预测时域 $H$ 需要多长才能到达稳定区」：$H$ 短则须靠终端集「兜底」，$H$ 长则终端集可缩小——这是第 12.7 节「计算预算 vs 预测视野」折中的具体抓手，也与第 4 章 Lyapunov 稳定性、第 19 章 RL 的安全约束（控制屏障）在理论上同源。

> 【图 12-1　MPC 轨迹优化】（原图见 figures/图12-1.png）：横轴为时间，展示 $t$ 与 $t+1$ 时刻两次求解的预测轨迹（虚线）与实际执行（实线），并标注约束集与滚动窗口。
>
> ![图 12-1　MPC 轨迹优化](figures/图12-1.png)

## 12.2　轨迹优化：直接法与间接法

求解式 (12-1) 有两大路径。

**间接法**（indirect method）：先用庞特里亚金最大值原理（Pontryagin's maximum principle）导出最优性必要条件——状态方程、协态方程与控制最优性条件，得到两点边值问题（BVP），再数值求解。优点是精度高；缺点是对初值敏感、难处理不等式约束。最优控制的条件为

$$
\lambda_k=\nabla_x\ell+\nabla_x f^\top\lambda_{k+1},\quad \nabla_u\ell+\nabla_u f^\top\lambda_{k+1}=0, \tag{12-2}
$$

其中 $\lambda_k$ 为协态（costate）。

**直接法**（direct method）：把轨迹离散为有限维决策变量（每个时刻的状态与控制），把最优控制问题转化为非线性规划（NLP）：

$$
\min_{\mathbf{z}}\ F(\mathbf{z})\quad \mathrm{s.t.}\quad c(\mathbf{z})=0,\ g(\mathbf{z})\le0,\quad \mathbf{z}=(x_0,\dots,x_H,u_0,\dots,u_{H-1}). \tag{12-3}
$$

直接法又分**直接配点法**（collocation，状态与控制都作变量，动力学为约束）与**直接单发法**（shooting，只把控制作变量，状态由积分得到）。优点是鲁棒、易加约束；缺点是变量多、计算量大（但机器人短时域 $H$ 小，可接受）。TrajectoryOptimization（TrajOpt，第 10 章）与 CasADi/IPOPT 是典型实现。

**表 12-1　直接法与间接法对比**

| 方面 | 间接法 | 直接法 |
|------|------|------|
| 优化对象 | 协态 + 控制（连续 BVP） | 离散变量（NLP） |
| 精度 | 高 | 依赖离散粒度 |
| 约束处理 | 困难 | 自然（不等式入 NLP） |
| 初值敏感性 | 高 | 低 |
| 机器人应用 | 较少 | 主流 |

## 12.3　DDP 与 iLQR

**微分动态规划**（differential dynamic programming，DDP）是利用二阶近似的高效轨迹优化算法，适合机器人非线性系统。围绕当前轨迹 $\{\bar{x}_k,\bar{u}_k\}$ 对代价与动力学做二阶/一阶展开：

$$
Q_k=\ell(x_k,u_k)+V_{k+1}(f(x_k,u_k)), \tag{12-4}
$$

其中值函数近似 $V_k(x)\approx \frac12\delta x^\top\mathbf{V}_{k}\delta x+\mathbf{v}_k^\top\delta x$。对 $Q_k$ 在 $(\bar{x}_k,\bar{u}_k)$ 处二次化：

$$
Q_k\approx \frac12\begin{bmatrix}\delta x\\ \delta u\end{bmatrix}^\top
\underbrace{\begin{bmatrix}\mathbf{Q}_{xx}&\mathbf{Q}_{xu}\\ \mathbf{Q}_{ux}&\mathbf{Q}_{uu}\end{bmatrix}}_{\text{二阶导}}
\begin{bmatrix}\delta x\\ \delta u\end{bmatrix}
+\begin{bmatrix}\mathbf{Q}_x\\ \mathbf{Q}_u\end{bmatrix}^\top
\begin{bmatrix}\delta x\\ \delta u\end{bmatrix}. \tag{12-5}
$$

最小化式 (12-5) 得局部控制修正（含反馈项）：

$$
\delta u_k^*=\mathbf{k}_k+\mathbf{K}_k\delta x_k,\quad \mathbf{k}_k=-\mathbf{Q}_{uu}^{-1}\mathbf{Q}_u,\quad \mathbf{K}_k=-\mathbf{Q}_{uu}^{-1}\mathbf{Q}_{ux}. \tag{12-6}
$$

**iLQR**（iterative LQR）是 DDP 的简化：对动力学只做一阶近似、忽略值函数的二阶项（$\mathbf{V}_k$ 的二阶导贡献），用 LQR 反向递推求增益，再正向线搜索更新轨迹。iLQR 计算更轻、实现更简单，是机器人中最常用的二阶轨迹优化器。**控制受限 DDP**（control-limited DDP）通过投影或约束处理把 $u$ 限制在 Box 内（如力矩限幅）。DDP 与第 11 章 LQR 的关系：iLQR 是 LQR 在非线性系统上的迭代推广，式 (12-6) 的 $\mathbf{K}_k$ 即局部 LQR 反馈增益。

## 12.4　接触丰富任务

**挑战。** 行走、抓取、跳跃等任务涉及**接触切换**：系统动力学在接触建立/断开瞬间不连续（$f$ 是混合的），导致式 (12-1) 的梯度不连续、优化困难。主要处理方法：① **显式接触调度**——预先指定各时刻哪些接触激活，把问题转为光滑子问题序列；② **互补约束**——用线性互补问题（LCP）建模「接触力 ≥ 0、穿透距离 ≥ 0、两者互补」，嵌入 NLP（数学规划互补问题，MCP）；③ **混合动力学规划**——把模式序列作为离散决策，结合 MIP（混合整数规划）；④ **软接触模型**——用光滑的弹簧—阻尼近似接触，避免不连续（牺牲真实性）。

**例 12.1（四足机器人 MPC）**　用简化质心动力学（single rigid body model）：状态 $x=(\mathbf{p}_{\mathrm{com}},\boldsymbol{\Theta},\mathbf{v},\boldsymbol{\omega})$，控制 $u$ 为四条腿的接触力 $\{\mathbf{f}_i\}_{i=1}^4$。MPC 在 $H=10$、步长为 $0.03\,\mathrm{s}$ 的短时域内优化接触力与躯干轨迹，约束为摩擦锥 $\|\mathbf{f}_{i,t}\|\le\mu f_{i,n}$ 与单足力上下限。每 $30\,\mathrm{ms}$ 重解一次（约 $30\,\mathrm{Hz}$），底层 WBC（第 11 章）把接触力转为关节力矩——实时适应不平地面与推挤扰动。

### 12.4A　接触建模的四类形式化

12.4 节列出四类处理方法，这里把它们的**数学结构**对比清楚，说明为何各有适用域。① **显式接触调度**把「哪些接触在哪些时段激活」作为离散决策 $\{m_k\in\mathcal M\}$（$m_k$ 为接触模式），在每个固定模式下系统是光滑的，式 (12-1) 退化为普通 NLP；模式切换用混合自动机描述。优点是每个子问题光滑、可用 DDP/iLQR；缺点是模式序列须预先枚举或在线搜索，组合爆炸。② **互补约束**用线性互补（LCP）刻画「接触力非负、穿透非负、二者互补」：$\mathbf f\ge0,\ d\ge0,\ \mathbf f\circ d=0$（Hadamard 积），把它嵌入 NLP 得**数学规划互补问题（MCP）**；MCP 的非凸性来自互补项，常用 NLP 求解器的「斜率法」或「logarithmic barrier」近似。③ **混合整数规划（MIP）**把接触开关写成二元变量 $z_i\in\{0,1\}$，用大 M 法线性化接触/非接触两种模式，交给 MIP 求解器——表达力最强，但组合复杂度最高、实时性最差。④ **软接触**用光滑弹簧—阻尼 $f=k(d_{\mathrm{rest}}-d)+c\,\dot d$ 替代硬接触，使 $f$ 处处可微，DDP 的二阶导存在；代价是「穿透深度」非物理、力在 $d=d_{\mathrm{rest}}$ 处不突变，对「碰撞—弹跳」类任务失真。实践中：行走/抓取等「接触时序已知」的任务用①或②；「接触时序未知、需在线决定」的任务用③；需要二阶导数、实时性高而精度可稍降的场合用④。这四类与第 11 章的接触力 QP（式 11-5 的零空间投影）正交：QP 在「给定接触模式」下分配力，MPC 在「预测时域」里决定「何时切换模式」——二者构成第 11.4 节 WBC 的「上层 MPC + 底层 WBC」分层。

## 12.5　数值算例

**例 12.2（一维 LQR 步的反向递推）**　设线性系统 $x_{k+1}=x_k+u_k$，阶段代价 $\ell=x_k^2+u_k^2$，时域 $H=2$，终端 $V_2(x)=x^2$（即 $\mathbf{V}_2=2$ 以 $\frac12\mathbf{V}x^2$ 记法则 $\mathbf{V}_2=2$）。按式 (12-4、12-5) 反向递推标量 Riccati：

$$
\mathbf{V}_1=\mathbf{Q}+\mathbf{A}^\top\mathbf{V}_2\mathbf{A}-\mathbf{A}^\top\mathbf{V}_2\mathbf{B}(\mathbf{R}+\mathbf{B}^\top\mathbf{V}_2\mathbf{B})^{-1}\mathbf{B}^\top\mathbf{V}_2\mathbf{A}=2+2-\frac{2\cdot2}{1+2}=4-\frac43=\frac83, \tag{12-7}
$$

增益 $K_1=-(\mathbf{R}+\mathbf{B}^\top\mathbf{V}_2\mathbf{B})^{-1}\mathbf{B}^\top\mathbf{V}_2\mathbf{A}=-2/3$。对初态 $x_0=1$，首步控制 $u_0=K_0x_0=-0.6$（$K_0$ 由 $\mathbf{V}_0$ 类似算得）——这展示 iLQR 反向递推的算术流程。

**例 12.3（摩擦锥约束的数值检验）**　四足机器人某足法向力 $f_n=50\,\mathrm{N}$，摩擦系数 $\mu=0.6$，则切向力上限 $\mu f_n=30\,\mathrm{N}$。若 MPC 解出 $f_t=(18,12)\,\mathrm{N}$，则 $\|f_t\|=\sqrt{18^2+12^2}=\sqrt{468}\approx21.6<30$——约束满足；若 $f_t=(25,20)$，$\|f_t\|\approx32.0>30$——违反摩擦锥，足会打滑，求解器须投影回锥内。这接触约束是四足 MPC 的核心。

### 12.5A　MPC 的 QP 形式与 iLQR 线搜索

例 12.2 展示了 DDP 的 Riccati 递推，这里把式 (12-1) 在「线性化动力学 + 二次代价」下写成**标准 QP**，并补上 iLQR 的线搜索。对一维线性系统 $x_{k+1}=a x_k+b u_k$、代价 $\ell=(x_k-x_{\mathrm{ref}})^2+(u_k-u_{\mathrm{ref}})^2$，在「控制无界、状态无约束」时式 (12-1) 等价于 QP

$$
\min_{\mathbf u,\mathbf x}\ \tfrac12\begin{bmatrix}\mathbf x\\\mathbf u\end{bmatrix}^{\!\top}\!\begin{bmatrix}\mathbf Q&\mathbf 0\\\mathbf 0&\mathbf R\end{bmatrix}\!\begin{bmatrix}\mathbf x\\\mathbf u\end{bmatrix}+\mathbf l^{\!\top}\begin{bmatrix}\mathbf x\\\mathbf u\end{bmatrix}\quad \mathrm{s.t.}\ \mathbf x_{k+1}=a x_k+b u_k,\ x_0=x_t, \tag{12-8}
$$

其中 $\mathbf x=(x_0,\dots,x_H)^\top$、$\mathbf u=(u_0,\dots,u_{H-1})^\top$ 堆叠成决策变量，$\mathbf Q,\mathbf R$ 为对角权重阵，$\mathbf l$ 为参考项线性化。这是**等式约束 QP**，可用内点法或消元法求解；加入 Box 约束 $u_k^{\min}\le u_k\le u_k^{\max}$ 与状态约束 $x_k\in\mathcal X$ 后变为不等式 QP，求解器（如 OSQP、qpOASES、acados 的 HPIPM）在毫秒级出解。iLQR 的**线搜索**保证每次全局步不增代价：沿方向 $\delta u=\mathbf k+\mathbf K\delta x$ 取步长 $\alpha\in(0,1]$，要求新代价满足 Armijo 条件 $J(\bar u+\alpha\,\delta u)\le J(\bar u)+\alpha\,c_1\,\nabla J^{\!\top}\delta u$（$c_1<1$），不满足则 $\alpha\leftarrow\alpha/2$ 重试。这使 iLQR 在初值远离最优时仍单调下降，是「二阶局部近似 + 一阶全局安全」的结合。

**例 12.4（线性 MPC 一步的 QP 手算）**　取 $a=1,b=1$（$x_{k+1}=x_k+u_k$）、$H=1$、$x_t=1$、参考 $x_{\mathrm{ref}}=0$，权重 $Q=2,R=1$，无约束。式 (12-8) 展开为 $\min_{u_0}\ (x_1)^2+(u_0)^2$，$x_1=1+u_0$，即 $\min_{u_0}(1+u_0)^2+u_0^2=2u_0^2+2u_0+1$。令导数 $4u_0+2=0$ 得 $u_0^*=-0.5$，则 $x_1^*=0.5$，代价 $J^*=(0.5)^2+(-0.5)^2=0.5$。执行 $u_0^*=-0.5$ 后状态到 $x_1=0.5$；下一时刻以 $x_t=0.5$ 重解，$u_0^*=-0.25$、$x_1=0.25$——状态指数衰减到参考 $0$。这正是 MPC「每步重解 + 只执行第一步」的闭环：开环最优 $u$ 序列 $(-0.5,-0.25,-0.125,\dots)$ 逐次截断为单步，反馈校正由「下一时刻从新状态重解」隐式提供。对比开环（一次性执行整条序列不重解）：若 $x_0$ 有 $+0.1$ 的初始误差，开环会把误差带到末端，而 MPC 每步重解都把误差拉回——这就是式 (12-1) 滚动机制的定量体现。

## 12.6　技术谱系与变体

**表 12-2　机器人轨迹优化/MPC 谱系**

| 方法 | 类型 | 核心 | 优势 | 局限 |
|------|------|------|------|------|
| LQR/iLQR/DDP | 间接/二阶 | 值函数二次近似（式 12-4—12-6） | 高效、带反馈 | 局部最优、需初值 |
| TrajOpt/CHOMP | 直接优化 | NLP/梯度下降（第 10 章） | 约束灵活 | 计算量较大 |
| 显式 MPC | 直接/多参数 | 预解显式控制律 | 极快 | 仅小规模/线性 |
| 接触 MPC | 混合/互补 | 接触调度 + 锥约束 | 处理行走抓取 | 非光滑、难实时 |
| 学习增强 MPC | 数据驱动 | 学模型/代价/初值（第 19—23、32 章） | 少建模、快 | 分布外风险 |

变体联系：iLQR 用一阶动力学 + LQR 递推（式 12-6）；DDP 保留二阶动力学项；控制受限版本加 Box 约束；与模型学习（第 32 章）结合学 $f$ 可缓解模型误差。

## 12.7　边界与讨论

**其一，模型精度与计算预算。** 式 (12-1) 的 $f$ 来自第 3 章建模，摩擦、柔性、接触误差导致预测偏差；增大 $H$ 提升预测但增加求解负担——实时性（数百 Hz）迫使 $H$ 很小（10—30 步）。**其二，接触仍是难题。** 非光滑动力学使 DDP 的二阶导数不存在，需光滑近似或混合整数——这是当前研究前沿。**其三，局部最优。** iLQR/DDP 从初值出发做局部优化，差初值导致失败；实践中用上一周期解作热启动。**其四，与学习的融合。** 学动力学模型（第 32 章）、学代价、学初始解可缓解建模负担，但引入分布外风险（第 15 章分布漂移的类比）。

**承上启下。** 本章衔接第 3 章（动力学 $f$）、第 4 章（LQR）、第 10—11 章（路径与 WBC）、第 19—23 章（RL 控制）、第 29 与 32 章（仿真与模型学习）以及《世界模型导论》第 25 章（模型中的规划）。

### 12.7A　计算预算与实时性

式 (12-1) 的求解代价随 $H$ 与决策维数 $d$ 增长：直接法变量数 $\sim d_x H+d_u H$，NLP 每步代价近似 $O(N^3)$（$N$ 为变量数）或更少（稀疏 QP 内点法）。机器人实时性（1 kHz 控制环）迫使 $H$ 取 10–30 步、步长 $10$–$50\,\mathrm{ms}$。工程上有五类加速手段：① **热启动**——用上一周期解作初值，iLQR/DDP 的局部近似使其 1–3 次迭代即收敛，把「从零优化」降为「局部修正」；② **稀疏结构**——动力学约束把 Hessian/约束 Jacobian 变成块带状，Cholesky 分解复杂度降为非零元量级（与第 7 章式 (7-7) 的稀疏图优化同理）；③ **代码生成**——CasADi/IPOPT 或 acados 对固定 $H$ 的 QP/NLP 做符号化编译，把运行时优化降为一次稀疏 Cholesky，单步 $<1\,\mathrm{ms}$，是嵌入式 MPC 的主流；④ **降维**——对线性系统用**显式 MPC** 把 $x\mapsto u_0$ 的控制律预解成分片仿射函数，运行时查表 $O(1)$，代价是片数随维数指数增长、仅适用小规模线性问题；⑤ **学习增强的初值/模型**——用神经网络学 $f$（动力学残差）或学初值，减少迭代次数，但须处理分布外风险。这五类与第 11 章 WBC 的 1 kHz QP 求解、第 7 章 SLAM 后端的多前沿优化共享「稀疏 + 增量 + 代码生成」的数值优化底座——**实时最优控制、实时图优化、实时滤波在数值方法上是同一类问题**。

## 本章小结

本章论述模型预测控制与轨迹优化，给出第 10—11 章的规划—控制之上的滚动优化框架。

我们首先给出 MPC 的标准公式与滚动机制（定义 12.1，式 12-1），并在 12.1A 节补充终端约束与终端集对稳定性的显式保证。接着对比直接法与间接法（式 12-2、12-3，表 12-1），推导 DDP/iLQR 的二次近似与反馈增益（式 12-4—12-6）。随后讨论接触丰富任务的困难，12.4A 节把显式调度、互补约束、MIP 与软接触四类形式化的数学结构对比清楚；并用 Riccati 递推（式 12-7，例 12.2）、摩擦锥检验（例 12.3）与 QP 手算（式 12-8，例 12.4）展示数值流程，12.5A 节补充 iLQR 的线搜索机制，12.7A 节讨论热启动、稀疏结构与代码生成等实时化手段，最后梳理谱系（表 12-2）。

我们还明确边界：模型精度与计算预算、接触非光滑、局部最优与学习融合。这些辨析衔接第 3—4、10—11、19—23、29、32 章与《世界模型导论》第 25 章。

下一章讨论机器人执行层的高峰——灵巧操作，把本章的轨迹优化与第 11 章的力控用于抓取与装配。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[2]、[3]。

## 参考文献

[1] Rawlings J B, Mayne D Q. *Model Predictive Control: Theory and Design*. Nob Hill, 2009.

[2] Tassa Y, Doron Y, Manevich A, et al. Control-limited differential dynamic programming. *ICRA*, 2014.

[3] Li T, Wensing P M, Todorov E. Generalized iterative LQR for constrained nonlinear optimal control problems. *ICRA*, 2023.

[4] Mayne D Q, Seron M M, Rakovic S V. Robust model predictive control of constrained linear systems with bounded disturbances. *Automatica*, 2005, 41(2): 219–224.

[5] Verschueren R, Frison G, Kvasnica M, et al. acados: a modular open-source framework for fast embedded optimal control. *Mathematical Programming Computation*, 2022, 14: 147–183.

[6] Di Carlo J, Wensing P M, Katz B, et al. Dynamic whole-body locomotion through contact: A survey. *IJRR*, 2021, 40(2–3): 361–396.

[7] Chen Y, Todorov E. Complementary dynamics via generalized constraints. *ACM SIGGRAPH*, 2021, 40(4): 1–14.

[8] Hertle N, Dontchev A L, Veliotis S. Convergence of iLQR for nonlinear optimal control. *Automatica*, 2024, 162: 111501.

[9] Mayne D Q, Rawlings J B, Rao C V, Scokaert P O M. Constrained model predictive control: Stability and optimality. *Automatica*, 2000, 36(6): 789–814.

[10] Bemporad A, Morari M. Robust feasibility for constrained model predictive control. *IEEE Transactions on Automatic Control*, 1999, 44(5): 836–841.

[11] Rawlings J B, Mayne D Q, Diehl M. *Model Predictive Control: Theory, Computation, and Design*. 2nd ed. Hoboken: Wiley, 2017.

[12] Tassa Y, Erez T, Todorov E. Synthesis and stabilization of complex behaviors through online trajectory optimization. *IEEE ICRA*, 2012: 4906–4913.
