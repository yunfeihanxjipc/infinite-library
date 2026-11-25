# 第 5 章　隐马尔可夫模型与卡尔曼滤波

第一篇建立了理论基础。第二篇（第 5—8 章）梳理经典世界模型——在深度学习之前，控制论与统计学已发展出成熟的世界建模方法。本章从两个奠基性模型开始：隐马尔可夫模型（HMM）与卡尔曼滤波。它们是第 9—13 章深度潜在变量模型的理论原型：VAE 是 HMM 的连续潜在推广，RSSM 的随机状态承继卡尔曼的贝叶斯滤波思想。

## 5.1　隐马尔可夫模型

**定义 5.1（HMM）**　隐马尔可夫模型由初始分布 $\pi$、转移矩阵 $\mathbf{A}$（$a_{ij}=P(s_{t+1}=j\mid s_t=i)$）与发射矩阵 $\mathbf{B}$（$b_{ik}=P(o_t=k\mid s_t=i)$）参数化。状态 $s_t$ 隐藏，通过观测 $o_t$ 间接可见。联合分布分解：

$$
P(o_{1:T},s_{1:T})=P(s_1)\prod_{t=2}^{T}P(s_t\mid s_{t-1})\prod_{t=1}^{T}P(o_t\mid s_t). \tag{5-1}
$$

**三个基本问题。**

1. **评估**：计算 $P(o_{1:T})$——前向算法；
2. **解码**：找最可能状态序列 $\hat{s}_{1:T}$——维特比算法；
3. **学习**：估计 $\pi,\mathbf{A},\mathbf{B}$——Baum-Welch（EM）算法。

**前向算法。** 定义 $\alpha_t(j)=P(o_{1:t},s_t=j)$，递推：

$$
\alpha_{t+1}(j)=\Big[\sum_i\alpha_t(i)a_{ij}\Big]b_{j,o_{t+1}}. \tag{5-2}
$$

**维特比算法。** 定义 $\delta_t(j)=\max_{s_{1:t-1}}P(s_{1:t-1},s_t=j,o_{1:t})$，递推（与第 8 章类似）：

$$
\delta_{t+1}(j)=\Big[\max_i\delta_t(i)a_{ij}\Big]b_{j,o_{t+1}}. \tag{5-3}
$$

维特比把前向算法的「求和」换成「取最大」，并记录每步 argmax 的路径指针，回溯即得最可能状态序列。它本质是一个在 $O(T|\mathcal{S}|^2)$ 内完成的**最大后验（MAP）解码**，与第 8 章 Viterbi 解码、第 24 章序列决策的序列解码器同构。

**后向算法与后验概率。** 前向算法给出 $P(o_{1:t},s_t)$，但若还想问「在整条观测 $o_{1:T}$ 已知下，$t$ 时刻处于状态 $j$ 的概率是多少」，需要**后向概率** $\beta_t(j)=P(o_{t+1:T}\mid s_t=j)$，递推

$$
\beta_T(j)=1,\qquad \beta_t(i)=\sum_j a_{ij}\,b_{j,o_{t+1}}\,\beta_{t+1}(j). \tag{5-4}
$$

由前向 $\alpha$ 与后向 $\beta$ 可得**滤波后验**与**平滑后验**：

$$
\gamma_t(j)=P(s_t=j\mid o_{1:T})=\frac{\alpha_t(j)\beta_t(j)}{\sum_k\alpha_t(k)\beta_t(k)},\qquad
\xi_t(i,j)=P(s_t=i,s_{t+1}=j\mid o_{1:T})=\frac{\alpha_t(i)a_{ij}b_{j,o_{t+1}}\beta_{t+1}(j)}{P(o_{1:T})}. \tag{5-5}
$$

$\gamma_t$ 是「单时刻」后验（类比卡尔曼滤波的 $p(s_t\mid o_{1:t})$），$\xi_t$ 是「相邻两时刻」的联合后验（类比状态转移的充分统计量）。这两个量正是 Baum–Welch 算法的原料。

**Baum–Welch（EM）学习。** 三个基本问题中的「学习」没有闭式解，用 EM 迭代：E 步用当前参数算出 $\gamma_t,\xi_t$（即把隐状态当作缺失数据求其充分统计量），M 步在「状态已知」下极大化似然，得重估公式

$$
\hat a_{ij}=\frac{\sum_{t=1}^{T-1}\xi_t(i,j)}{\sum_{t=1}^{T-1}\gamma_t(i)},\qquad
\hat\pi_i=\gamma_1(i),\qquad
\hat b_{ik}=\frac{\sum_{t:o_t=k}\gamma_t(i)}{\sum_{t=1}^{T}\gamma_t(i)}. \tag{5-6}
$$

E 步与 M 步交替保证似然单调不减（与第 13 章式 (13-9) 的预测误差分解、第 9 章 EM 同源）。但 EM 只能保证收敛到**局部**极大，对初值敏感，且状态数 $|\mathcal{S}|$ 需事先指定（实际中用 BIC 或交叉验证选）。

**例 5.1（天气 HMM）**　隐藏状态 {晴, 雨}，观测 {带伞, 不带伞}。转移 $P(\text{雨}\mid\text{晴})=0.3$，发射 $P(\text{带伞}\mid\text{雨})=0.8$。给定一周观测，前向算法算观测概率，维特比解码最可能的天气序列——这是从观测推断隐藏世界状态的原型。

**例 5.6（前向—后向手算：两天天气）**　设状态 $S_t\in\{晴,雨\}$，初始 $\pi=(0.7,0.3)$，转移 $\mathbf A=\begin{pmatrix}0.7&0.3\\0.4&0.6\end{pmatrix}$（晴→晴 0.7、晴→雨 0.3；雨→晴 0.4、雨→雨 0.6），发射：$P(\text{带伞}\mid晴)=0.2$、$P(\text{带伞}\mid雨)=0.8$、$P(\text{不带伞}\mid晴)=0.8$、$P(\text{不带伞}\mid雨)=0.2$。观测两天：$o_1=$带伞、$o_2=$不带伞。
- **前向**：$\alpha_1=(0.7\times0.2,\ 0.3\times0.8)=(0.14,0.24)$。$\alpha_2(晴)=[\alpha_1(晴)0.7+\alpha_1(雨)0.4]\times0.8=[0.14\times0.7+0.24\times0.4]\times0.8=[0.098+0.096]\times0.8=0.1552$；$\alpha_2(雨)=[0.14\times0.3+0.24\times0.6]\times0.2=[0.042+0.144]\times0.2=0.0372$。故 $P(o_{1:2})=\alpha_2(晴)+\alpha_2(雨)=0.1552+0.0372=0.1924$。
- **后向**：$\beta_2=(1,1)$。$\beta_1(晴)=0.7\times0.2\times1+0.3\times0.8\times1=0.14+0.24=0.38$；$\beta_1(雨)=0.4\times0.2+0.6\times0.8=0.08+0.48=0.56$。
- **滤波后验**（只用 $o_1$）：$\gamma_1(j)\propto\alpha_1(j)$，即 $P(S_1\mid o_1)=(0.14,0.24)/0.38=(0.368,0.632)$——看到「带伞」后，「雨」的后验从先验 0.3 升到 0.632。
- **平滑后验**（用 $o_{1:2}$）：$\gamma_2(晴)\propto\alpha_2(晴)\beta_2(晴)=0.1552$，$\gamma_2(雨)\propto0.0372$，归一化得 $P(S_2\mid o_{1:2})=(0.1552,0.0372)/0.1924=(0.807,0.193)$——第二天「不带伞」把「晴」的后验拉回 0.807。

这个算例展示了 HMM 推断的核心：**观测如何逐步移动对隐状态的后验**。前向给出「截至 $t$」的滤波后验（实时），后向前向结合给出「全序列」的平滑后验（事后），二者与卡尔曼滤波的 $\hat s_{t\mid t}$ 与 $\hat s_{t\mid T}$ 一一对应——离散概率向量版与连续高斯版是同一台机器。

> 【图 5-1　HMM 的状态转移与观测发射】（原图见 figures/图5-1.png）：隐藏状态链 + 观测发射。
>
> ![图 5-1　HMM 的状态转移与观测发射](figures/图5-1.png)

## 5.2　卡尔曼滤波

**定义 5.2（卡尔曼滤波）**　对第 2 章定义的线性高斯 SSM，卡尔曼滤波递归计算状态后验 $p(s_t\mid o_{1:t})=\mathcal{N}(\hat{s}_t,\mathbf{P}_t)$。两步：

**预测：**

$$
\begin{aligned}
\hat{s}_{t\mid t-1}&=\mathbf{A}\hat{s}_{t-1}+\mathbf{B}a_{t-1},\\
\mathbf{P}_{t\mid t-1}&=\mathbf{A}\mathbf{P}_{t-1}\mathbf{A}^\top+\mathbf{Q}.
\end{aligned} \tag{5-7}
$$

**更新（用观测 $o_t$）：**

$$
\begin{aligned}
\mathbf{K}_t&=\mathbf{P}_{t\mid t-1}\mathbf{C}^\top(\mathbf{C}\mathbf{P}_{t\mid t-1}\mathbf{C}^\top+\mathbf{R})^{-1},\\
\hat{s}_t&=\hat{s}_{t\mid t-1}+\mathbf{K}_t(o_t-\mathbf{C}\hat{s}_{t\mid t-1}),\\
\mathbf{P}_t&=(\mathbf{I}-\mathbf{K}_t\mathbf{C})\mathbf{P}_{t\mid t-1}.
\end{aligned} \tag{5-8}
$$

$\mathbf{K}_t$ 是卡尔曼增益，决定观测残差 $o_t-\mathbf{C}\hat{s}_{t\mid t-1}$ 对状态估计的修正强度——它自动平衡预测与观测的信任度（按各自不确定性加权）。

**两种推导。** 卡尔曼滤波可从贝叶斯推断（高斯后验的解析更新）或最小均方误差（LMMSE 估计）两个角度推导，二者等价。贝叶斯视角揭示其本质：用观测把先验 $\mathcal{N}(\hat{s}_{t\mid t-1},\mathbf{P}_{t\mid t-1})$ 更新为后验。更具体地，在预测分布下，$(\mathbf s_t,\mathbf o_t)$ 服从联合高斯
$$
\begin{pmatrix}\mathbf s_t\\ \mathbf o_t\end{pmatrix}\Big|\,o_{1:t-1}\sim N\!\left(\begin{pmatrix}\hat{\mathbf s}_{t\mid t-1}\\ \mathbf C\hat{\mathbf s}_{t\mid t-1}\end{pmatrix},\begin{pmatrix}\mathbf P_{t\mid t-1}&\mathbf P_{t\mid t-1}\mathbf C^\top\\ \mathbf C\mathbf P_{t\mid t-1}&\mathbf C\mathbf P_{t\mid t-1}\mathbf C^\top+\mathbf R\end{pmatrix}\right),
$$
对其作高斯条件化（标准公式 $\mathbb E[\mathbf s\mid\mathbf o]=\mu_s+\Sigma_{so}\Sigma_{oo}^{-1}(\mathbf o-\mu_o)$）即直接给出式 (5-8) 的均值更新 $\hat{\mathbf s}_t=\hat{\mathbf s}_{t\mid t-1}+\mathbf K_t(\mathbf o_t-\mathbf C\hat{\mathbf s}_{t\mid t-1})$ 与协方差更新 $\mathbf P_t=(\mathbf I-\mathbf K_t\mathbf C)\mathbf P_{t\mid t-1}$，其中增益 $\mathbf K_t=\mathbf P_{t\mid t-1}\mathbf C^\top(\mathbf C\mathbf P_{t\mid t-1}\mathbf C^\top+\mathbf R)^{-1}$。可见卡尔曼滤波**就是高斯贝叶斯更新**：先验是预测分布，似然是观测的高斯核，后验是二者按协方差加权的融合。这一视角把卡尔曼滤波与第 3 章的精度加权（式 3-3）、第 9 章的 VAE 后验推断统一在「高斯—高斯条件化」之下。

**例 5.2（一维卡尔曼滤波手算）**　设 $A=1,B=0,C=1,Q=0.1,R=0.5$，$P_0=1,\hat{s}_0=0$，观测 $o_1=1.2$。预测：$\hat{s}_{1\mid0}=0$，$P_{1\mid0}=1+0.1=1.1$。增益：$K_1=1.1/(1.1+0.5)=0.6875$。更新：$\hat{s}_1=0+0.6875\times1.2=0.825$，$P_1=(1-0.6875)\times1.1=0.34375$。滤波把初始不确定（$P=1$）收缩到 $P=0.34$，并朝观测方向修正状态。

**例 5.5（卡尔曼两步递推：多步数值迭代）**　沿用上例参数 $A=1,C=1,Q=0.1,R=0.5$，连续观测 $o_1=1.2,\ o_2=1.1,\ o_3=0.9,\ o_4=1.0$，逐期执行「预测—更新」：
- $t=1$：预测 $\hat s_{1\mid0}=0,\ P_{1\mid0}=1.1$；增益 $K_1=1.1/1.6=0.6875$；更新 $\hat s_1=0.825,\ P_1=0.34375$。
- $t=2$：预测 $\hat s_{2\mid1}=0.825,\ P_{2\mid1}=0.34375+0.1=0.44375$；$K_2=0.44375/0.94375\approx0.4702$；更新 $\hat s_2=0.825+0.4702\times(1.1-0.825)\approx0.954,\ P_2=0.44375\times0.5298\approx0.2351$。
- $t=3$：预测 $P_{3\mid2}=0.3351$；$K_3=0.3351/0.8351\approx0.4013$；更新 $\hat s_3=0.954+0.4013\times(0.9-0.954)\approx0.932,\ P_3\approx0.2004$。
- $t=4$：预测 $P_{4\mid3}=0.3004$；$K_4\approx0.3755$；更新 $\hat s_4\approx0.950,\ P_4\approx0.1881$。

观察三点：其一，**增益单调下降**（$0.6875\to0.4702\to0.4013\to0.3755$）——随着累积观测，状态估计越来越可靠，滤波器越来越信任自己的预测、对新观测「打折」；其二，**后验协方差单调收缩**（$1\to0.34\to0.24\to0.20\to0.19$）并向一个稳态值收敛，该稳态是代数 Riccati 方程 $p=(p+0.1)\cdot 1/(p+0.1+0.5)$ 的正解；其三，估计值 $\hat s_t$ 在观测波动中「平滑」地跟随，而非逐点跳变——这正是「滤波」一词的物理含义。这个多步算例是第 13 章 RSSM 的确定性部分 $h_{t+1}=f(h_t,a_t,z_t)$ 在线更新的标量原型。

**最小方差推导（增益的另一种来源）。** 增益 $\mathbf K_t$ 也可不依赖高斯假设、纯由最小均方误差导出。设只允许形如 $\hat{\mathbf s}_t=\hat{\mathbf s}_{t\mid t-1}+\mathbf K(\mathbf o_t-\mathbf C\hat{\mathbf s}_{t\mid t-1})$ 的线性更新（它对新息无偏），估计误差协方差为
$$
\mathbf P(\mathbf K)=(\mathbf I-\mathbf K\mathbf C)\mathbf P_{t\mid t-1}(\mathbf I-\mathbf K\mathbf C)^\top+\mathbf K\mathbf R\mathbf K^\top. \tag{5-9}
$$
对 $\mathbf K$ 求迹并配方，使 $\mathrm{tr}\,\mathbf P(\mathbf K)$ 最小的 $\mathbf K$ 恰为 $\mathbf K_t=\mathbf P_{t\mid t-1}\mathbf C^\top(\mathbf C\mathbf P_{t\mid t-1}\mathbf C^\top+\mathbf R)^{-1}$，与式 (5-8) 的贝叶斯形式完全一致。两种推导的殊途同归说明：**在线性高斯下，「贝叶斯后验均值」与「最小方差线性估计」是同一件事**——前者要求高斯性，后者只需二阶矩，故卡尔曼滤波是更广意义上的最优线性无偏估计器（BLUE）。

**平滑（RTS）。** 若允许用整条序列 $o_{1:T}$ 回看过去状态，精度更高。Rauch–Tung–Striebel 平滑器先做前向卡尔曼滤波，再后向递推：
$$
\mathbf J_t=\mathbf P_{t\mid t}\mathbf A^\top\mathbf P_{t+1\mid t}^{-1},\qquad
\hat{\mathbf s}_{t\mid T}=\hat{\mathbf s}_{t\mid t}+\mathbf J_t\big(\hat{\mathbf s}_{t+1\mid T}-\hat{\mathbf s}_{t+1\mid t}\big). \tag{5-10}
$$
这与 HMM 的前向—后向（式 5-4、5-5）完全同构：HMM 的 $\gamma_t=\alpha_t\beta_t/P(o)$ 是离散版的平滑后验，卡尔曼的 $\hat s_{t\mid T}$ 是连续高斯版的平滑后验。这一同构是本章最重要的统一线索：**HMM 与卡尔曼滤波是同一套「前向—后向—平滑」贝叶斯机器在离散与连续状态空间下的两个实例**。

**表 5-1　HMM 与卡尔曼滤波对照**

| 方面 | HMM | 卡尔曼滤波 |
|------|-----|-----------|
| 状态 | 离散 | 连续高斯 |
| 观测 | 离散/连续 | 连续高斯 |
| 推断 | 前向-后向（离散） | 解析高斯更新 |
| 地位 | 离散潜在模型原型 | 连续潜在模型原型 |

> 【图 5-2　卡尔曼滤波迭代收敛】（原图见 figures/图5-2.png）：状态估计与不确定性随观测逐步收敛的曲线。
>
> ![图 5-2　卡尔曼滤波迭代收敛](figures/图5-2.png)

## 5.3　扩展与无迹卡尔曼滤波

**扩展卡尔曼滤波（EKF）。** 非线性系统 $s_{t+1}=f(s_t,a_t)+\xi_t$、$o_t=g(s_t)+\eta_t$，用雅可比矩阵在估计点线性化：

$$
\mathbf{F}_t=\frac{\partial f}{\partial s}\Big|_{\hat{s}_t},\qquad \mathbf{H}_t=\frac{\partial g}{\partial s}\Big|_{\hat{s}_t},
$$

再把 $\mathbf{F}_t,\mathbf{H}_t$ 代入式 (5-7)、(5-8)。EKF 简单但线性化误差可能累积。

**无迹卡尔曼滤波（UKF）。** 用一组确定性采样点（sigma points）捕捉高斯分布的传播，无需解析雅可比，对强非线性更稳健。

**粒子滤波。** 用带权粒子表示任意后验分布，适合非高斯、多峰情形——是更通用的序贯蒙特卡洛方法。

**例 5.3（EKF 用于倒立摆）**　倒立摆动力学非线性（$\sin\phi$），在_current_角度处线性化得雅可比 $\mathbf{F}_t$，套用 EKF 估计角度与角速度——这是基于非线性世界模型的在线状态估计。

## 5.4　卡尔曼滤波作为世界模型

从七要素看卡尔曼滤波：E1 状态表示（高斯状态 $\hat{s},\mathbf{P}$）、E2 状态转移（$\mathbf{A},\mathbf{B}$）、E3 观测生成（$\mathbf{C}$）、E4 不确定性（协方差 $\mathbf{P}$）、E5 动作条件化（$\mathbf{B}a_t$）。它具备前五要素，但缺 E6（奖励）与 E7（规划）——需结合 LQR（第 4 章）或 MPC（第 25 章）。

**例 5.4（卡尔曼 + LQR = 完整闭环）**　卡尔曼滤波估计状态（E1–E5），LQR 用估计状态算最优控制（E7），二者结合（LQG）构成完整的基于模型智能体——这是经典控制的世界模型范式。

## 5.5　边界与讨论

**线性高斯的限制。** 卡尔曼滤波依赖线性高斯假设，真实系统常违反；EKF/UKF/粒子滤波缓解但各有代价（线性化误差、采样开销、粒子退化）。具体地：EKF 只保留一阶信息，当非线性函数曲率大（如倒立摆在大角度下的 $\sin\phi$）时，雅可比近似偏差会**沿时间累积**，使协方差低估、滤波器过度自信；UKF 用 $2n+1$ 个 sigma 点传播二阶信息，更稳健但仍假设分布近似高斯，对多峰后验失效；粒子滤波用 $N$ 个带权样本近似任意分布，理论上无高斯限制，但样本数 $N$ 需远大于状态维 $n$ 才不退化，且权值随时间集中（粒子退化），需重采样——其计算代价 $O(N)$ 在高维下迅速不可承受。三者构成「精度—计算」的权衡谱系：线性高斯下卡尔曼最优且最省，强非线性下粒子滤波最通用但最贵。

**HMM 的离散瓶颈。** HMM 的状态数 $|\mathcal{S}|$ 必须有限且预先指定，转移与发射都是参数化的概率表——这限制它刻画连续、高维的隐变量。前向—后向复杂度 $O(T|\mathcal{S}|^2)$、维特比 $O(T|\mathcal{S}|^2)$，随状态数平方增长，难以扩展到真实感知（像素、连续位置）。这正是第 9 章 VAE 把离散隐状态换成**连续高斯潜在**、第 13 章 RSSM 用循环网络建模**高维确定性 + 随机**状态的动力：把「离散状态表」推广为「可学习的连续动力学」。

**与后续章节的联系。** HMM 与卡尔曼是深度潜在模型的原型：VAE（第 9 章）推广到连续非线性，RSSM（第 13 章）结合随机与确定性状态。本章的贝叶斯滤波思想贯穿第 9、11—13 章；前向—后向—平滑的三件套（式 5-4、5-5、5-10）在离散与连续两侧同构出现，是理解全书「世界模型 = 隐状态 + 贝叶斯推断」这一主线的钥匙。

下一章讨论 POMDP——当状态不可完全观测时的决策理论。

## 本章小结

本章论述两个经典世界模型——HMM 与卡尔曼滤波——并揭示它们是同一台「前向—后向—平滑」贝叶斯机器在离散与连续状态空间下的两个实例。

我们首先给出 HMM 的联合分布分解（式 5-1）与三个基本问题，推导前向（式 5-2）、维特比（式 5-3）、后向（式 5-4）算法，以及由 $\alpha,\beta$ 构造的滤波/平滑后验（式 5-5）与 Baum–Welch 的 EM 重估公式（式 5-6）。用两天天气算例（例 5.6）手算前向—后向，展示「带伞→不带伞」如何把「雨」的后验从 0.632 拉回 0.807。然后推导卡尔曼滤波的预测—更新两步（式 5-7、5-8），用联合高斯条件化（贝叶斯视角）与最小方差配方（式 5-9）两种途径交叉验证增益，并给出 RTS 平滑（式 5-10）。多步数值算例（例 5.5）展示了增益单调下降、协方差向稳态 Riccati 解收缩的滤波行为。

我们介绍 EKF（雅可比线性化）、UKF（sigma 点）、粒子滤波（序贯蒙特卡洛）三种非线性扩展，从七要素分析卡尔曼滤波（具备 E1–E5，缺 E6、E7），指出卡尔曼 + LQR = LQG 构成完整闭环。

边界上：HMM 受限于离散有限状态、复杂度 $O(T|\mathcal{S}|^2)$；卡尔曼受限于线性高斯，EKF/UKF/粒子滤波各有精度—计算权衡。这些辨析衔接第 4、6、7、9、11—13 章，并点明前向—后向—平滑三件套是全书「隐状态 + 贝叶斯推断」主线的钥匙。

下一章讨论 POMDP——当状态不可完全观测时的决策理论。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[2]、[3]、[4]、[5]。

## 参考文献

[1] Rabiner L R. A tutorial on hidden Markov models and selected applications in speech recognition. *Proceedings of the IEEE*, 1989, 77(2): 257–286.

[2] Kalman R E. A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 1960, 82(1): 35–45.

[3] Welch G, Bishop G. An Introduction to the Kalman Filter. *UNC TR 95-041*, 2006.

[4] Julier S J, Uhlmann J K. Unscented filtering and nonlinear estimation. *Proceedings of the IEEE*, 2004, 92(3): 401–422.

[5] Doucet A, de Freitas N, Gordon N, eds. *Sequential Monte Carlo Methods in Practice*. Springer, 2001.

[6] Ghahramani Z. An introduction to hidden Markov models and Bayesian networks. *IJPRAI*, 2001, 15(1): 9–42.

[7] Stengel R F. *Optimal Control and Estimation*. Dover, 1994.

[8] Sutton R S, Barto A G. *Reinforcement Learning: An Introduction*. 2nd ed. MIT Press, 2018.
