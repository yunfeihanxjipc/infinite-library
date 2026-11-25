# 第 7 章　SLAM 与定位

第 5—6 章的感知回答「世界里有什么」：物体在哪、是什么、能否抓取。本章回答另一个同等根本的问题：**机器人在哪里？** 同时定位与建图（Simultaneous Localization and Mapping，SLAM）让机器人在未知环境中运动时，一边构建环境地图，一边估计自身位姿。SLAM 是移动机器人自主的基础，也是第 1 章「感知—认知」闭环的核心环节：没有位姿，视觉 detections（第 5 章）无法变换到世界坐标，规划（第 10 章）与控制（第 11 章）也就失去参照。

本章先给出 SLAM 的概率形式与「鸡生蛋」困境（7.1 节）；然后分别介绍视觉 SLAM 与激光 SLAM 的流水线（7.2 节）；接着推导图优化与回环检测的数学（7.3 节）；介绍基于粒子滤波的概率定位 MCL（7.4 节）；通过位姿图优化的数值算例落地（7.5 节）；给出方法谱系表（7.6 节）；最后讨论 SLAM 的边界（7.7 节）与承上启下（7.8 节）。

## 7.1　SLAM 问题的概率形式

**定义 7.1（SLAM）**　给定传感器观测序列 $\{o_t\}$ 与控制输入 $\{u_t\}$，同时估计机器人轨迹 $\{x_t\}$ 与环境地图 $m$：

$$
p(x_{1:T},m\mid o_{1:T},u_{1:T}). \tag{7-1}
$$

这是一个「鸡生蛋」困境：定位需要已知地图（由观测反推位姿），建图需要已知位姿（把观测拼进地图），二者互相依赖。SLAM 通过**联合估计**破解这一循环：把轨迹与地图作为同一个概率问题的未知量，利用观测间的共享信息同时求解。

**因子图视角。** 在因子图（factor graph）中，式 (7-1) 分解为运动因子的乘积：

$$
p(x_{1:T},m\mid o_{1:T},u_{1:T})\propto\underbrace{\prod_t p(x_t\mid x_{t-1},u_t)}_{\text{运动模型}}\ \underbrace{\prod_{i}p(o_i\mid x_{t_i},m_i)}_{\text{观测模型}}. \tag{7-2}
$$

运动因子连接相邻位姿（来自里程计或 IMU），观测因子连接位姿与地图地标（来自相机或激光的观测）。式 (7-2) 把 SLAM 变成图上的推理问题：前端负责建立因子（数据关联），后端负责在给定因子下求最大后验（MAP）估计。

## 7.2　视觉 SLAM 与激光 SLAM

**视觉 SLAM（visual SLAM）。** 以摄像头为传感器，典型流水线为：特征提取与匹配（ORB 等）→ 视觉里程计（估计相邻帧运动，用对极几何或 PnP，第 5.2 节）→ 后端优化（BA，bundle adjustment，联合优化位姿与三维点）→ 回环检测 → 建图。代表系统 ORB-SLAM[2]。优势是信息丰富、成本低；劣势是对光照与纹理敏感，弱纹理或快速运动易丢失跟踪。

**激光 SLAM（lidar SLAM）。** 以激光雷达为传感器，通过扫描匹配（scan matching，如 ICP 迭代最近点）估计位姿，构建占据栅格地图（occupancy grid），后端用位姿图优化。代表系统 Cartographer[3]、LOAM。优势是测距精确、对光照不敏感；劣势是长走廊等几何退化环境中匹配歧义，且缺少语义信息。

> 【图 7-1　SLAM 系统流程】（原图见 figures/图7-1.png）：绘制「传感器→前端里程计→后端图优化→回环检测→地图构建」的流水线，标注视觉与激光两条分支及式 (7-2) 的因子对应关系。
>
> ![图 7-1　SLAM 系统流程](figures/图7-1.png)

## 7.3　回环检测与图优化

**回环检测（loop closure）。** 机器人回到曾访问地点时，识别出「旧地方」并添加一条约束——这是 SLAM 的关键。没有回环，里程计误差随时间累积（漂移），地图无限发散；有了回环，漂移被全局修正。视觉用词袋模型（BoW）做外观相似性检测，激光用局部地图匹配。回环需谨慎验证，错误回环会「拉坏」全局地图。

**位姿图优化（pose graph optimization）。** 把位姿 $\{x_t\}$ 作为节点，相邻帧的相对位姿约束与回环约束作为边。每条边 $ij$ 提供相对位姿测量 $\mathbf{z}_{ij}$（来自里程计或回环匹配），对应的残差为

$$
\mathbf{e}_{ij}=\log\!\Big(\mathbf{z}_{ij}^{-1}\ \mathbf{x}_i^{-1}\mathbf{x}_j\Big)\in\mathfrak{se}(3), \tag{7-3}
$$

其中 $\log$ 是 SE(3) 上的对数映射（第 3.1 节），把位姿差映射到李代数。优化目标是最小化所有边的加权平方误差：

$$
\mathbf{x}^{*}=\arg\min_{\mathbf{x}}\ \sum_{(i,j)}\mathbf{e}_{ij}^\top\boldsymbol{\Omega}_{ij}\mathbf{e}_{ij}, \tag{7-4}
$$

其中 $\boldsymbol{\Omega}_{ij}$ 为信息矩阵（协方差的逆），衡量约束的可信度。这是非线性最小二乘问题，用 Gauss-Newton 或 Levenberg-Marquardt 迭代求解，稀疏性使大规模图可实时优化。

**例 7.1（回环消除漂移的数值）**　机器人沿直线运动，每步真实位移 $1.0\,\mathrm{m}$，里程计有 $+2\%$ 系统误差，即每步估计 $1.02\,\mathrm{m}$。走 100 步后，估计位置 $102.0\,\mathrm{m}$，真实位置 $100.0\,\mathrm{m}$，漂移 $2.0\,\mathrm{m}$。若在第 100 步检测到回到起点附近的回环（观测到相同地标），回环约束把 $x_{100}$ 与 $x_0$ 的位置差约束为真实值（约 0），式 (7-4) 的优化把累积的 $2.0\,\mathrm{m}$ 漂移按信息权重均摊到 100 个位姿节点上，每个节点被修正约 $0.02\,\mathrm{m}$——全局地图恢复一致。这直观展示了回环如何把「局部准确、全局漂移」的里程计变成全局一致的地图。

## 7.4　概率机器人定位：MCL

**定义 7.2（蒙特卡洛定位，MCL）**　在**已知地图**中定位（不同于 SLAM 的建图），用一组带权粒子 $\{x_t^{(i)},w_t^{(i)}\}_{i=1}^N$ 近似机器人位姿后验 $p(x_t\mid o_{\le t},u_{<t},m)$。每个粒子代表一个可能的位姿假设，算法循环三步：① **运动更新**：按运动模型 $p(x_t\mid x_{t-1},u_t)$ 传播每个粒子（加入噪声）；② **观测更新**：按观测似然 $p(o_t\mid x_t^{(i)},m)$ 调整粒子权重（与地图一致的位姿权重高）；③ **重采样**：按权重重新抽取粒子，舍弃低权重假设。自适应 MCL（amcl）还能在「机器人被绑架」（位姿突变）时注入随机粒子恢复。

**MCL 与 SLAM 的关系。** MCL 解决「地图已知时的定位」，SLAM 解决「地图未知时的定位+建图」。MCL 是第 8 章粒子滤波（定义 8.2）在定位问题上的直接应用，也是概率机器人学[1]的经典成果。

## 7.5　数值算例：位姿图的最小二乘求解

**例 7.2（一维位姿图优化）**　为展示式 (7-4) 的求解，考虑一维简化版：三个位姿 $x_0=0,x_1,x_2$，两个里程计约束 $z_{01}=1.0,\ z_{12}=1.0$（单位方差，$\Omega=1$），一个回环约束 $z_{02}=2.0$（单位方差）。定义残差 $e_{01}=x_1-x_0-z_{01}=x_1-1$，$e_{12}=x_2-x_1-1$，$e_{02}=x_2-x_0-2=x_2-2$。目标函数

$$
J=(x_1-1)^2+(x_2-x_1-1)^2+(x_2-2)^2. \tag{7-5}
$$

令偏导为零：$\partial J/\partial x_1=2(x_1-1)-2(x_2-x_1-1)=0\Rightarrow 2x_1-x_2=0$；$\partial J/\partial x_2=2(x_2-x_1-1)+2(x_2-2)=0\Rightarrow -x_1+2x_2=3$。联立解得 $x_1=1.0,\ x_2=2.0$——与真实值一致。若里程计约束有偏（如 $z_{01}=1.1$），无回环时 $x_2=2.2$（漂移），加入回环 $z_{02}=2.0$ 后解为 $x_1\approx1.033,\ x_2\approx2.033$，漂移被回环吸收。这个一维例子完整展示了位姿图优化的机制，高维 SE(3) 情形只是把它推广到李群上的非线性最小二乘。

### 7.5A　SLAM 的可辨识性与 CRLB

联合后验 (7-1) 的精度并非由观测数量单独决定，而受**可辨识性**（identifiability）约束——这是 SLAM 区别于普通状态估计的根本性质。设以 $\boldsymbol\theta=(\mathbf x_{1:T},\mathbf m)$ 表示全部未知量，观测 $o_{1:T}$ 的**费舍尔信息矩阵**（Fisher information matrix）为

$$
\mathbf F=\mathbb E\Big[\nabla_{\boldsymbol\theta}\log p(o_{1:T}\mid\boldsymbol\theta)^{\!\top}\,\nabla_{\boldsymbol\theta}\log p(o_{1:T}\mid\boldsymbol\theta)\Big], \tag{7-6}
$$

则 Cramér–Rao 下界（CRLB）断言：任何无偏估计量 $\hat{\boldsymbol\theta}$ 的协方差满足 $\mathrm{Cov}(\hat{\boldsymbol\theta})\succeq\mathbf F^{-1}$（$\mathbf F$ 须满秩）。SLAM 的特殊性在于：仅含里程计（运动因子）而无回环观测时，信息矩阵关于**全局刚体变换**（2D 为平面平移与旋转，共 3 维）不变——把轨迹与整张地图一起平移或旋转，所有运动残差 (7-3) 都不变。因此 $\mathbf F$ 秩亏 $\geq3$，不存在全局一致的无偏估计；引入回环观测或固定先验（锚定一个位姿）才能消去零空间、使 $\mathbf F$ 恢复满秩。这解释了工程上「固定 $x_0$ 再优化」与「必须至少一个回环」两条规则的概率根源：二者都在为信息矩阵补齐零空间方向。Grisetti 等的 SLAM 教程[9] 对 EKF-SLAM 的信息矩阵与 CRLB 分析进一步表明，即使锚定先验，信息沿「远离锚点方向」仍随里程计链长累积退化——地图边缘的位姿协方差显著大于靠近回环处。这一结论直接指导了回环检测的优先级设计（优先闭合远端回环）与第 8 章协方差传播的解读。

**例 7.3（链式定位的 CRLB 量化）**　把 1D 位姿链简化为 $T$ 个位姿、每步里程计方差 $\sigma^2$、固定 $x_0=0$。仅用里程计时，第 $k$ 个位姿是 $k$ 个独立里程计的累加，其方差 $\mathrm{Var}(x_k)=k\sigma^2$——这就是式 (7-6) 在链式结构下信息矩阵对角元的倒数（信息沿链稀释为 $1/(k\sigma^2)$）。取 $T=100$、$\sigma=0.1\,\mathrm{m}$，则无回环时末端 $\mathrm{Var}(x_{100})=100\times0.01=1.0\,\mathrm{m}^2$，即 $\pm1\,\mathrm{m}$ 的标准差，与例 7.1 的 $2\%$ 漂移一致。若在第 100 步加一条方差 $\sigma_{\mathrm{loop}}^2=0.01\,\mathrm{m}^2$（1 cm 精度）的回环约束 $x_{100}\approx0$，则末端有效信息为里程计链信息 $1/1.0$ 与回环信息 $1/0.01$ 之和 $=1+100=101$，$\mathrm{Var}(x_{100})\approx0.0099\,\mathrm{m}^2$，标准差降到约 $0.1\,\mathrm{m}$——回环把末端不确定度压了两个数量级，这正是式 (7-6) 信息相加在高斯情形的直观体现，也与第 8 章式 (8-8) 的精度加权融合完全同构。

### 7.5B　Gauss-Newton 线性化与稀疏求解

式 (7-4) 是非线性最小二乘，其标准迭代是 Gauss-Newton。把位姿参数化为「当前估计 + 李代数增量」$\mathbf x_i\leftarrow\mathbf x_i\oplus\boldsymbol\delta_i$（$\oplus$ 为 SE(3) 增量作用），对 $\mathbf e_{ij}(\boldsymbol\delta)$ 在 $\boldsymbol\delta=0$ 处一阶展开，记各边雅可比 $\mathbf J_{ij}=\partial\mathbf e_{ij}/\partial\boldsymbol\delta$，则每个 Newton 步求解**正规方程**（normal equations）

$$
\mathbf H\,\boldsymbol\delta=\mathbf b,\qquad \mathbf H=\sum_{(i,j)}\mathbf J_{ij}^{\!\top}\boldsymbol\Omega_{ij}\mathbf J_{ij},\quad \mathbf b=-\sum_{(i,j)}\mathbf J_{ij}^{\!\top}\boldsymbol\Omega_{ij}\mathbf e_{ij}, \tag{7-7}
$$

迭代至 $\boldsymbol\delta$ 足够小。$\mathbf H$ 是稀疏的带状/块对角结构：每个位姿节点只与其里程计邻居及回环对象相连，故 $\mathbf H$ 非零块数远小于 $N^2$（$N$ 为节点数）。求解大规模稀疏 $\mathbf H$ 的标准工具是 **Cholesky 稀疏分解**（复杂度接近非零元数目）与**多前沿（multifrontal）方法**（GTSAM[10]、Ceres）；对增量更新（新增一帧观测），iSAM2[11] 的 Bayes 树增量重分解可把单步代价降到 $O(1)$ 量级，从而支持在线 SLAM。Levenberg–Marquardt（LM）则在式 (7-7) 右端加 $\boldsymbol\lambda\,\mathrm{diag}(\mathbf H)$ 阻尼项，在 Gauss-Newton 步与梯度下降之间自适应切换，对初值更鲁棒。工程上，回环边的信息矩阵 $\boldsymbol\Omega$ 通常取**回环观测协方差的逆并乘以折扣系数**（折扣因子 $\rho\in(0,1)$），以抑制错误回环对全局解的污染——折扣越小，回环对轨迹的「拉力」越弱，是鲁棒性与收敛速度的折中。激光前端的扫描匹配则以 ICP（迭代最近点）[12] 为典型：交替「最近点搜索—求刚体变换—更新」，正是式 (7-4) 在「单帧配准」上的简化版，其收敛性与式 (7-7) 的 Gauss-Newton 同根同源。

## 7.6　技术谱系与变体

**表 7-1　视觉 SLAM vs 激光 SLAM**

| 方面 | 视觉 SLAM | 激光 SLAM |
|------|-----------|-----------|
| 传感器 | 单目/双目/RGB-D 相机 | 2D/3D 激光雷达 |
| 前端 | 特征匹配、光流、PnP | 扫描匹配（ICP、NDT） |
| 后端 | BA、位姿图优化 | 位姿图优化、子图匹配 |
| 地图 | 点云、半稠密深度 | 占据栅格、点云 |
| 优势 | 信息丰富、廉价、含语义 | 精确、鲁棒、光照无关 |
| 劣势 | 光照/纹理敏感、尺度歧义 | 退化环境、无语义、昂贵 |
| 代表 | ORB-SLAM[2] | Cartographer[3]、LOAM |

**表 7-2　SLAM 与定位方法谱系**

| 方法 | 地图 | 估计器 | 代表 | 章节 |
|------|------|--------|------|------|
| EKF-SLAM | 地标 | 扩展卡尔曼滤波 | 早期主流 | 7.1、第 8 章 |
| 视觉 SLAM | 特征点/稠密 | BA + 图优化 | ORB-SLAM | 7.2、7.3 |
| 激光 SLAM | 栅格/点云 | 扫描匹配 + 图优化 | Cartographer | 7.2 |
| MCL/AMCL | 已知栅格图 | 粒子滤波 | amcl | 7.4、第 8 章 |
| 神经 SLAM | 隐式特征 | 网络 + 图优化 | Neural SLAM | 7.7、第 30 章 |

## 7.7　边界与讨论

SLAM 面临三类根本挑战：① **动态环境**——传统 SLAM 假设静态世界，而真实场景有人和移动物体，需动态点剔除或语义 SLAM；② **退化场景**——长走廊、空旷空间缺乏可区分的几何/纹理约束，导致定位退化；③ **实时性与累积误差**——大规模地图的后端优化计算量大，需滑动窗口与稀疏化。当前前沿把深度学习引入 SLAM：用网络提取更鲁棒的特征、用 NeRF 构建可渲染的隐式地图（第 30 章）、用语义信息辅助数据关联。这些「神经 SLAM」方法在保持几何一致性的同时，赋予地图语义与泛化能力。

**边界辨析。** SLAM 的「定位」与第 8 章的「状态估计」是同一问题的两端：SLAM 侧重未知地图中的联合估计与全局一致性，状态估计侧重滤波框架下的实时递推；二者在因子图视角下统一（式 7-2）。这些辨析衔接第 3、5、8、10、14、30 章。

### 7.7A　实时性与滑动窗口

全图优化 (7-4) 的代价随节点数 $N$ 近似线性到二次增长（取决于稀疏分解策略），对嵌入式平台仍是负担。工程上采用三重手段：① **前端—后端分级**——前端里程计以 100 Hz 增量估计位姿（仅用最近 $K$ 帧局部），后端以 1–10 Hz 在更大窗口上做全局 BA/位姿图优化，二者通过「局部一致性」解耦，使端到端延迟可控；② **子图化（submap）**——把地图切分为局部子图（如 Cartographer 的 submap[3]），前端只与当前子图对齐，回环时再触发全局重优化，把单步计算限制在常数子图内；③ **滑动窗口与边缘化（marginalization）**——丢弃窗口外的旧位姿，但保留其「被边缘化后对剩余状态的等效先验」（Schur 补形式的稀疏信息块），避免信息丢失。边缘化的等效先验正是式 (7-6) 的费舍尔信息在子集上的 Schur 补：对联合信息阵按「保留/丢弃」分块消元，得到的保留块即新先验。设把信息阵分块为保留块 $\mathbf H_{\mathrm{ss}}$ 与待边缘化块 $\mathbf H_{\mathrm{dd}}$，则边缘化后保留状态的等效信息为其 **Schur 补**

$$
\mathbf H_{\mathrm{ss}}^{\,\mathrm{marg}}=\mathbf H_{\mathrm{ss}}-\mathbf H_{\mathrm{sd}}\,\mathbf H_{\mathrm{dd}}^{-1}\,\mathbf H_{\mathrm{ds}}, \tag{7-8}
$$

右端对角块正是「用已丢弃的 $\mathbf H_{\mathrm{dd}}$ 消元」所得的等效精度。这解释了为何「删旧帧」不损失精度（在 Gaussian 假设下），只是把旧信息以紧凑先验形式继承下来，与第 8 章 8.2 节卡尔曼预测步的「先验传递」思想同构。数值上，式 (7-8) 即例 7.3 中「链信息 + 回环信息」相加的矩阵形式：当丢弃中间节点时，其里程计信息被吸收进相邻保留节点的等效先验，精度沿图稀疏传播——这是 iSAM2 增量求解的核心代数操作，也是 SLAM 后端能在线扩展而无需重算全图的根本原因。

## 7.8　承上启下

本章给出机器人「在哪里」的答案：SLAM 联合估计位姿与地图，回环消除漂移，图优化保证全局一致性。但 SLAM 输出的是带噪的位姿与地图，且机器人还需融合 IMU、轮速计、视觉等多源信息——这正是第 8 章状态估计与传感器融合的主题。

## 本章小结

本章论述 SLAM 与定位，回答「机器人在哪里」这一自主的基础问题。

我们首先给出 SLAM 的概率形式（式 7-1）与因子图分解（式 7-2），解释定位与建图互相依赖的「鸡生蛋」困境。接着介绍视觉/激光 SLAM 的流水线并以表 7-1 对照；然后推导图优化中的位姿残差（式 7-3）与最小二乘目标（式 7-4），以回环漂移算例（例 7.1）与一维位姿图求解（例 7.2）展示机制；还介绍已知地图下的 MCL 概率定位。7.5A 节补充了 SLAM 的可辨识性与 Cramér–Rao 下界（式 7-6），说明回环与锚定先验为何是全局一致性的必要前提；7.5B 节给出 Gauss-Newton 正规方程（式 7-7）与稀疏求解、边缘化机制，解释了后端为何可实时；7.7A 节讨论前端—后端分级、子图化与滑动窗口等实时化手段。我们以表 7-1、7-2 梳理视觉/激光 SLAM 与定位方法谱系。

我们还明确边界：动态环境、退化场景与实时性仍是挑战，神经 SLAM 是前沿；并辨析 SLAM 与状态估计在因子图视角下的统一。这些辨析衔接第 3、5、8、10、14、30 章。

下一章讨论状态估计与传感器融合，把多源带噪信息提炼为一致的状态信念。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[2]、[3]、[4]。

## 参考文献

[1] Thrun S, Burgard W, Fox D. *Probabilistic Robotics*. MIT Press, 2005.

[2] Mur-Artal R, Montiel J M M, Tardós J D. ORB-SLAM: A versatile and accurate monocular SLAM system. *IEEE Transactions on Robotics*, 2015, 31(5): 1147–1163.

[3] Hess W, Kohler D, Rapp H, et al. Real-time loop closure in 2D LIDAR SLAM. *IEEE ICRA*, 2016: 1271–1278.

[4] Cadena C, Carlone L, Carrillo H, et al. Past, present, and future of simultaneous localization and mapping: Toward the robust-perception age. *IEEE Transactions on Robotics*, 2016, 32(6): 1309–1332.

[5] Shan T, Englot B. LeGO-LOAM: Lightweight and ground-optimized lidar odometry and mapping on variable terrain. *IEEE/RSJ IROS*, 2018: 4758–4765.

[6] Engel J, Schöps T, Cremers D. LSD-SLAM: Large-scale direct monocular SLAM. *ECCV*, 2014: 834–849.

[7] Zhang Q, Hu R, Guo S, et al. Neural SLAM: Learning to explore with external memory. *arXiv:1706.09520*, 2017.

[8] Zhu A, Yuan Z, Nozawa S, et al. NeRF-SLAM: Real-time dense monocular SLAM with neural radiance fields. *arXiv:2210.13641*, 2022.

[9] Grisetti G, Kummerle S, Burgard W, et al. A tutorial on the SLAM problem. *IEEE Robotics & Automation Magazine*, 2007, 14(2): 99–110.

[10] Dellaert F. The factor graph for visual SLAM. *IEEE Transactions on Robotics*, 2017, 33(2): 424–427.

[11] Kaess M, Johannsson H, Roberts R, et al. iSAM2: Incremental smoothing and mapping using the Bayes tree. *International Journal of Robotics Research*, 2012, 31(2): 216–235.

[12] Besl P J, McKay N D. A method for registration of 3-D shapes. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 1992, 14(2): 239–256.
