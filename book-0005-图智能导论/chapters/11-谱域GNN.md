# 第 11 章　谱域图神经网络

第三篇的第 10 章建立了消息传递神经网络（MPNN）的统一框架，把 GNN 分解为消息 $M$、聚合 $\oplus$、更新 $U$ 三函数。本章从**谱域（spectral domain）**视角给出这个框架的一种具体实例化——谱图卷积（spectral graph convolution）[1]。谱方法源于图信号处理：把图信号投影到拉普拉斯特征向量张成的频域，在频域做滤波，再逆变换回空域。它提供了 GNN 的**数学根基**，也直接导出最常用的基准模型 GCN（Graph Convolutional Network）[2]。

本章先回顾图傅里叶变换并定义谱卷积（11.1 节），用切比雪夫多项式推导 ChebNet 以避免特征分解（11.2 节），进一步取一阶近似得到 GCN 公式（11.3 节），给出数值算例与技术谱系（11.4 节），最后讨论谱方法的边界与承上启下（11.5 节）并小结。

## 11.1　图傅里叶变换与谱卷积

回顾第 3 章：无向图的组合拉普拉斯 $\mathbf{L}=\mathbf{D}-\mathbf{A}$ 是对称半正定矩阵，可正交对角化

$$
\mathbf{L}=\mathbf{U}\mathbf{\Lambda}\mathbf{U}^\top,\quad \mathbf{U}=(\mathbf{u}_1,\dots,\mathbf{u}_n),\quad \mathbf{\Lambda}=\mathrm{diag}(\lambda_1,\dots,\lambda_n), \tag{11-1}
$$

其中 $\mathbf{u}_i$ 为正交特征向量（图傅里叶基），$\lambda_i\ge0$ 为特征值（频率）。图信号 $\mathbf{x}\in\mathbb{R}^n$ 的**图傅里叶变换**为 $\hat{\mathbf{x}}=\mathbf{U}^\top\mathbf{x}$，逆变换为 $\mathbf{x}=\mathbf{U}\hat{\mathbf{x}}$。低频对应小 $\lambda_i$（信号平滑），高频对应大 $\lambda_i$（信号振荡）。

**定义 11.1（谱图卷积）** 给定滤波函数 $g_\theta(\mathbf{\Lambda})$，谱卷积定义为

$$
\mathbf{y}=\mathbf{U}g_\theta(\mathbf{\Lambda})\mathbf{U}^\top\mathbf{x}. \tag{11-2}
$$

**直觉解释。** 式 (11-2) 是「变换—滤波—逆变换」三步：把信号转到频域，对每个频率分量乘以滤波响应 $g_\theta(\lambda_i)$（放大或抑制），再转回来。这与信号处理中的卷积定理（时域卷积=频域相乘）完全类比——只不过「时域」换成了图节点域，「频率」换成了拉普拉斯特征值。

**谱卷积的两大缺陷：** ① 需计算特征分解 $\mathbf{L}=\mathbf{U}\mathbf{\Lambda}\mathbf{U}^\top$，复杂度 $O(n^3)$，大规模图不可行；② 滤波器 $g_\theta$ 定义在频域，依赖具体的特征基 $\mathbf{U}$，无法泛化到结构不同的新图（不可归纳）。ChebNet 与 GCN 正是为克服这两点而生。

**频域滤波的物理意义。** 拉普拉斯特征值 $\lambda$ 刻画信号在节点域的「振动频率」：$\lambda=0$ 对应常数信号（图上最平滑），$\lambda$ 越大表示信号在相邻节点间变化越剧烈。低通滤波保留小 $\lambda$ 分量（平滑信号）、抑制高 $\lambda$ 分量（噪声与快速振荡）。第 9 章标签传播的调和函数解正是 $\lambda=0$ 的极端情形——完全平滑。谱卷积把这个固定的低通行为参数化为可学习的 $g_\theta(\lambda)$，使模型能按任务调整频率响应：同质性任务学低通，异亲性任务（第 12 章）理论上需高通分量。这为「图上的频率选择」提供了统一的信号处理语言。

## 11.2　ChebNet：切比雪夫近似

Hammond 等[3]提出用**切比雪夫多项式（Chebyshev polynomial）**近似滤波器 $g_\theta$：令 $g_\theta(\lambda)\approx\sum_{k=0}^{K}\theta_k T_k(\tilde{\lambda})$，其中 $\tilde{\lambda}=2\lambda/\lambda_{\max}-1\in[-1,1]$ 为归一化频率，$T_k$ 为第一类切比雪夫多项式（$T_0=1,T_1=x,T_{k+1}=2xT_k-T_{k-1}$）。代入式 (11-2)，利用 $\mathbf{U}T_k(\tilde{\mathbf{\Lambda}})\mathbf{U}^\top=T_k(\mathbf{U}\tilde{\mathbf{\Lambda}}\mathbf{U}^\top)=T_k(\tilde{\mathbf{L}})$（多项式与对角化可交换），得

$$
\mathbf{y}\approx\sum_{k=0}^{K}\theta_k T_k(\tilde{\mathbf{L}})\mathbf{x},\qquad \tilde{\mathbf{L}}=\frac{2\mathbf{L}}{\lambda_{\max}}-\mathbf{I}. \tag{11-3}
$$

**推导要点。** 关键恒等式 $\mathbf{U}f(\mathbf{\Lambda})\mathbf{U}^\top=f(\mathbf{U}\mathbf{\Lambda}\mathbf{U}^\top)=f(\mathbf{L})$ 对任意多项式 $f$ 成立，因为 $\mathbf{U}\mathbf{\Lambda}^k\mathbf{U}^\top=(\mathbf{U}\mathbf{\Lambda}\mathbf{U}^\top)^k=\mathbf{L}^k$。于是频域的 $T_k(\tilde{\lambda})$ 作用等价于空域的矩阵多项式 $T_k(\tilde{\mathbf{L}})$ 作用——**特征基 $\mathbf{U}$ 消失了**。

**直觉解释。** 切比雪夫近似把「频域滤波」改写成「拉普拉斯多项式的矩阵乘法」，不再需要特征分解；且 $T_k(\tilde{\mathbf{L}})$ 是 $k$ 阶多项式，对应图上 $k$ 跳邻域（因 $\mathbf{L}^k$ 非零模式在 $k$ 跳内），因此滤波器是**局部的**。公式 (11-3) 只涉及稀疏矩阵—向量乘，复杂度 $O(K|E|)$，可归纳到新图——两大缺陷被一并克服。

**例 11.1（切比雪夫递推手算）** 取 $K=2$，$\tilde{\mathbf{L}}$ 为某图归一化拉普拉斯。$T_0(\tilde{\mathbf{L}})=\mathbf{I}$，$T_1(\tilde{\mathbf{L}})=\tilde{\mathbf{L}}$，$T_2(\tilde{\mathbf{L}})=2\tilde{\mathbf{L}}^2-\mathbf{I}$。则滤波输出 $\mathbf{y}=\theta_0\mathbf{x}+\theta_1\tilde{\mathbf{L}}\mathbf{x}+\theta_2(2\tilde{\mathbf{L}}^2-\mathbf{I})\mathbf{x}$。若 $\theta_2=0$，则 $\mathbf{y}$ 仅依赖 1 跳邻域——这就是下面 GCN 的 $K=1$ 特例。

## 11.3　GCN 一阶近似

Kipf & Welling[2]在 ChebNet 基础上取 $K=1$，并令 $\lambda_{\max}\approx2$（故 $\tilde{\mathbf{L}}=\mathbf{L}-\mathbf{I}$），得到线性近似

$$
\mathbf{y}\approx\theta_0\mathbf{x}+\theta_1(\mathbf{L}-\mathbf{I})\mathbf{x}=(\theta_0-\theta_1)\mathbf{x}+\theta_1\mathbf{D}^{-1/2}\mathbf{A}\mathbf{D}^{-1/2}\mathbf{x}. \tag{11-4}
$$

令 $\theta=\theta_0=-\theta_1$，则 $\mathbf{y}\approx\theta(\mathbf{I}+\mathbf{D}^{-1/2}\mathbf{A}\mathbf{D}^{-1/2})\mathbf{x}$。为避免自环缺失导致的信息丢失，加入自环 $\hat{\mathbf{A}}=\mathbf{A}+\mathbf{I}$，$\hat{\mathbf{D}}_{ii}=\sum_j\hat{\mathbf{A}}_{ij}$，并叠加非线性与可学习权重矩阵 $\mathbf{W}^{(l)}$，得到**GCN 前向传播公式**：

$$
\mathbf{H}^{(l+1)}=\sigma\!\left(\hat{\mathbf{D}}^{-1/2}\hat{\mathbf{A}}\hat{\mathbf{D}}^{-1/2}\mathbf{H}^{(l)}\mathbf{W}^{(l)}\right). \tag{11-5}
$$

**推导细节（重归一化技巧）** $\hat{\mathbf{D}}^{-1/2}\hat{\mathbf{A}}\hat{\mathbf{D}}^{-1/2}$ 是对称归一化邻接：每条边 $(u,v)$ 的权重为 $1/\sqrt{\hat{d}_u\hat{d}_v}$，防止高度数节点的信号被过度放大。若改用 $\hat{\mathbf{D}}^{-1}\hat{\mathbf{A}}$（随机游走归一化）则不对称、数值不稳定；对称归一化保证矩阵相似于对称阵，特征值实且在 $[-1,1]$，使深层堆叠数值可控（与第 13 章过平滑分析相关）。

**直觉解释。** GCN 是「加权平均邻居表示 + 线性变换 + 非线性」：式 (11-5) 中 $\hat{\mathbf{D}}^{-1/2}\hat{\mathbf{A}}\hat{\mathbf{D}}^{-1/2}\mathbf{H}^{(l)}$ 是归一化邻域平均，$\mathbf{W}^{(l)}$ 是通道混合，$\sigma$ 注入非线性。它可视为第 9 章图正则化的深度非线性版本，也是 MPNN 框架（第 10 章）中 $M,U$ 取特定线性形式、$\oplus$ 取度归一化 sum 的特例。

> 【图 11-1　谱卷积到 GCN 的演化】（原图见 figures/图11-1.png）：展示谱卷积→ChebNet($K$ 阶局部化)→GCN($K=1$+自环+重归一化)的推导链与各自感受野。
>
> ![图 11-1　谱卷积到 GCN 的演化](figures/图11-1.png)

## 11.3A　卷积定理、切比雪夫误差与多层 GCN 前向

11.2 节的恒等式 $\mathbf{U}f(\mathbf{\Lambda})\mathbf{U}^\top=f(\mathbf{L})$ 是谱卷积到空域多项式的桥梁，但未给出其在"滤波器作用"层面的形式化表述；本节补上**图卷积定理**，量化切比雪夫近似的误差衰减，并给出多层 GCN 的数值前向与过平滑度量，为第 13 章的过平滑分析提供可计算的指标。

**定义 11.2（图卷积定理）** 对两个图信号 $\mathbf{x},\mathbf{s}\in\mathbb{R}^n$ 与滤波函数 $g_\theta$，定义图卷积 $\mathbf{x}\ast_g\mathbf{s}=\mathbf{U}\big(g_\theta(\mathbf{\Lambda})\circ(\mathbf{U}^\top\mathbf{s})\big)\mathbf{U}^\top\mathbf{x}$（$\circ$ 为逐元素积）。则

$$
\mathbf{x}\ast_g\mathbf{s}\ \xleftrightarrow{\ \mathrm{GFT}\ }\ g_\theta(\mathbf{\Lambda})\cdot\big(\mathbf{U}^\top\mathbf{x}\big)\circ\big(\mathbf{U}^\top\mathbf{s}\big), \tag{11-6}
$$

即"空域卷积 ↔ 频域逐元素相乘"，与第 3 章谱理论、离散信号处理的卷积定理同构。当 $\mathbf{s}$ 取"图上的核函数"（如 $\mathbf{s}=\mathbf{L}^{-1/2}\mathbf{x}$ 的热核形式），式 (11-6) 把谱卷积解释为"核在图上的滑窗"，这是"卷积"一名的谱域来源——尽管空域实现 (11-3) 无需显式卷积。

**命题 11.1（切比雪夫近似误差）** 设 $g$ 在 $[-1,1]$ 上连续，$K$ 阶切比雪夫近似 $g_K(\tilde{\lambda})=\sum_{k=0}^{K}\theta_k^\ast T_k(\tilde{\lambda})$，则 $\|g-g_K\|_\infty\le\frac{2}{\pi}\sqrt{\frac{2}{K+1}}\,\omega(g,K)$（$\omega$ 为模数界）。对解析滤波器（如 $g(\lambda)=e^{-t\lambda}$ 的热核），误差按 $O(\rho^K)$ 指数衰减（$\rho<1$ 由 $g$ 在椭圆域无奇点决定）。**实践含义**：取 $K=8$—$10$ 即可对多数光滑滤波器达到 $10^{-4}$ 精度，故 ChebNet 的实际感受野 $K$ 通常不超过 $10$——超过 10 跳的结构信息对节点级任务价值有限，与第 13 章"层数过深无益"的经验一致。

**例 11.5（ChebNet 二阶手算）** 取三节点链加自环的归一化邻接 $\hat{\mathbf{S}}=\hat{\mathbf{D}}^{-1/2}\hat{\mathbf{A}}\hat{\mathbf{D}}^{-1/2}=\begin{pmatrix}1/2&1/\sqrt6&0\\1/\sqrt6&1/3&1/\sqrt6\\0&1/\sqrt6&1/2\end{pmatrix}$，归一化拉普拉斯 $\tilde{\mathbf{L}}=\mathbf{I}-\hat{\mathbf{S}}=\begin{pmatrix}1/2&-1/\sqrt6&0\\-1/\sqrt6&2/3&-1/\sqrt6\\0&-1/\sqrt6&1/2\end{pmatrix}$。取输入 $\mathbf{x}=(1,0,0)^{\top}$，逐项计算多项式项在节点 1 的分量：$T_0\mathbf{x}=(1,0,0)$ 给节点 1 贡献 $1$；$T_1\mathbf{x}=\tilde{\mathbf{L}}\mathbf{x}=(0.5,\,-1/\sqrt6,\,0)\approx(0.5,\,-0.408,\,0)$ 给节点 1 贡献 $0.5$；$\tilde{\mathbf{L}}^2\mathbf{x}=\tilde{\mathbf{L}}(\tilde{\mathbf{L}}\mathbf{x})$ 的节点 1 分量 $=0.5^2+(1/\sqrt6)^2=5/12\approx0.417$，故 $T_2\mathbf{x}=2\tilde{\mathbf{L}}^2\mathbf{x}-\mathbf{x}$ 在节点 1 贡献 $2\times(5/12)-1=-1/6\approx-0.167$。取 $\theta_0=1,\theta_1=-1,\theta_2=0.5$，节点 1 输出 $=1\times1+(-1)\times0.5+0.5\times(-0.167)=1-0.5-0.083=0.417$。对照 $K=1$（仅 $\theta_0,\theta_1$）：节点 1 输出 $1-0.5=0.5$。二阶项 $0.5\times(-0.167)=-0.083$ 把输出从 $0.5$ 降到 $0.417$——这就是 2 跳信息（节点 3 经节点 2 的间接影响）对节点 1 的修正，验证"$K$ 阶多项式=$K$ 跳感受野"。

**例 11.6（两层 GCN 前向：信息沿链传播）** 对同一条链（加自环），用式 (11-5) 的 GCN 层（$\sigma=\mathrm{ReLU}$、$\mathbf{W}=\mathbf{I}$、单通道），输入 $\mathbf{h}^{(0)}=(1,0,0)^{\top}$。第 1 层：$\hat{\mathbf{D}}^{-1/2}\hat{\mathbf{A}}\hat{\mathbf{D}}^{-1/2}\mathbf{h}^{(0)}=(0.5,\,1/\sqrt6,\,0)^{\top}\approx(0.5,\,0.408,\,0)$，ReLU 后 $\mathbf{h}^{(1)}\approx(0.5,\,0.408,\,0)$。第 2 层：再乘一次归一化邻接，节点 1 $\approx0.471$、节点 2 $\approx0.452$、节点 3 $\approx0.144$，$\mathbf{h}^{(2)}\approx(0.471,\,0.452,\,0.144)$。**关键观察**：节点 3 在第 1 层为 0（1 跳内无信号），第 2 层变为 $0.144$——信号经节点 2 传播到 2 跳外的节点 3，定量验证"$L$ 层感受野 $=L$ 跳"。三节点值之和从 $1.0$（$l=0$）降到 $0.908$（$l=1$）再降到 $1.067$（$l=2$，含自环保留），说明信号在传播中既有扩散（节点 2、3 变非零）也有保留（自环项），为第 13 章的过平滑分析提供初始数值。

**定义 11.3（过平滑度量）** 衡量第 $l$ 层节点表示间相似度的均值：

$$
\mathrm{OS}(l)=\frac{1}{|V|}\sum_{v\in V}\frac{1}{|N(v)|}\sum_{u\in N(v)}\frac{\big(\mathbf{h}_v^{(l)}\big)^\top\mathbf{h}_u^{(l)}}{\|\mathbf{h}_v^{(l)}\|\,\|\mathbf{h}_u^{(l)}\|}. \tag{11-7}
$$

$\mathrm{OS}(l)\to1$ 表示邻居表示趋同（过平滑）。对例 11.6，$\mathrm{OS}(1)$ 取节点 2 与邻居的余弦均值：与节点 1 的余弦 $\approx0.996$，与节点 3（全零）定义余弦为 0，均值约 $0.498$；$\mathrm{OS}(2)$ 因节点 3 变非零而升至约 $0.85$——**过平滑度量随层数单调上升**，第 13 章将以式 (11-7) 为统一指标分析残差、JK、DropEdge 的缓解效果。

**表 11-3　谱域到空域的记号与复杂度对照**

| 量 | 谱域定义 | 空域实现 | 复杂度 | 章节 |
|----|---------|---------|--------|------|
| 滤波 | $g_\theta(\mathbf{\Lambda})$ | $\sum_k\theta_k T_k(\tilde{\mathbf{L}})$ | $O(n^3)\to O(K\|E\|)$ | 式 11-2→11-3 |
| 卷积 | 频域相乘（式 11-6） | 矩阵多项式作用 | 同左 | 11.3A |
| 感受野 | 全图（任意 $g$） | $K$ 跳（多项式阶） | $K\to1$（GCN） | 式 11-3、11-5 |
| 过平滑 | 低频收敛 | $\mathrm{OS}(l)\to1$（式 11-7） | 随 $l$ 增 | 第 13 章 |

表 11-3 把"谱域概念—空域实现—复杂度—章节"四条对齐：谱卷积的全图滤波经 ChebNet 局部化为 $K$ 跳，再经 GCN 退化为 1 跳，代价从 $O(n^3)$ 降到 $O(|E|)$；过平滑是这一"低频收敛"的副产品，由式 (11-7) 量化。此表是第 11—13 章"谱→空→深"推导链的速查索引。

## 11.4　数值算例与技术谱系

**例 11.4（谱滤波器频率响应）** 取 $K=1$ 的 ChebNet 滤波器 $g(\tilde{\lambda})=\theta_0+\theta_1\tilde{\lambda}$（$\tilde{\lambda}=2\lambda/\lambda_{\max}-1$）。设 $\lambda_{\max}=2$，则 $g(\lambda)=\theta_0+\theta_1(\lambda-1)$。若 $\theta_0=1,\theta_1=-1$，则 $g(\lambda)=2-\lambda$：对 $\lambda=0$（最平滑）响应为 2（放大），对 $\lambda=2$（最振荡）响应为 0（抑制）——典型低通。若 $\theta_1=+1$，则 $g(\lambda)=\lambda$：高通。这展示如何通过 $\theta$ 学习不同频率偏好；GCN（式 11-5 中 $\theta_0=-\theta_1$）恰好落在低通一侧。

**例 11.2（GCN 手算）** 取三节点链 $1\!-\!2\!-\!3$ 加自环：$\hat{\mathbf{A}}=\begin{pmatrix}1&1&0\\1&1&1\\0&1&1\end{pmatrix}$，度数 $\hat{d}=(2,3,2)$，$\hat{\mathbf{D}}^{-1/2}=\mathrm{diag}(1/\sqrt2,1/\sqrt3,1/\sqrt2)$。设单通道输入 $\mathbf{H}^{(0)}=(1,0,0)^\top$，$\mathbf{W}^{(0)}=1$，$\sigma$ 为恒等。计算 $\hat{\mathbf{D}}^{-1/2}\hat{\mathbf{A}}\hat{\mathbf{D}}^{-1/2}\mathbf{H}^{(0)}$：先右乘得 $(1/\sqrt2,0,0)^\top$，再 $\hat{\mathbf{A}}$ 乘得 $(1/\sqrt2,1/\sqrt2,0)^\top$，再左乘得 $(1/2,1/\sqrt6,0)^\top\approx(0.5,0.408,0)$。节点 2（链中心）获得了来自节点 1 的信息——一层 GCN 传播一跳，符合预期；节点 1 的自环权重（$1/2$）高于节点 2 对节点 1 的影响，保留自身信息。

**例 11.3（低通滤波验证）** 对路径图 $P_{10}$，取信号 $\mathbf{x}=(\cos(\pi i/10))_{i=1}^{10}$（低频，相邻值相近）与高频信号 $\mathbf{x}'=((-1)^i)$。GCN 归一化邻接的瑞利商 $\mathbf{x}^\top\hat{\mathbf{A}}\mathbf{x}/\|\mathbf{x}\|^2$ 对低频远大于高频——说明 GCN 是低通滤波器，平滑邻居信号。这正是第 9 章同质性假设下的理想行为，也是第 13 章过平滑的根源。

**表 11-1　谱方法谱系**

| 方法 | 滤波器近似 | 特征分解 | 归纳式 | 感受野 | 来源 |
|------|-----------|---------|--------|--------|------|
| 谱卷积[1] | 任意 $g_\theta$ | 需要 | 否 | 全图 | 频域 |
| ChebNet[3] | $K$ 阶切比雪夫 | 不需要 | 是 | $K$ 跳 | 频域→空域 |
| GCN[2] | $K=1$ + 重归一化 | 不需要 | 是 | 1 跳/层 | 一阶近似 |

**表 11-2　谱卷积关键记号对照**

| 记号 | 含义 | 位置 |
|------|------|------|
| $\mathbf{L}$ | 组合拉普拉斯 | 式 11-1 |
| $\mathbf{U},\lambda_i$ | 傅里叶基与频率 | 式 11-1 |
| $g_\theta$ | 可学习频域滤波器 | 式 11-2 |
| $T_k,\tilde{\mathbf{L}}$ | 切比雪夫多项式与归一化拉普拉斯 | 式 11-3 |
| $\hat{\mathbf{A}},\hat{\mathbf{D}}$ | 加自环邻接与度 | 式 11-4、11-5 |

**表 11-2** 汇总了本章推导链的关键符号，便于与第 3 章谱理论对照阅读。

## 11.5　边界与讨论

谱方法为 GNN 提供了严格的信号处理解释，但其理论建立在拉普拉斯特征基之上，而 ChebNet/GCN 通过局部化摆脱了特征基——这带来代价：GCN 的一阶近似**丢失了频域的灵活性**，本质上是固定的低通滤波。空域方法（第 12 章）从另一角度直接设计聚合函数，获得更大灵活性（如注意力学到的自适应权重）。现代观点认为谱与空域是同一 MPNN 框架的两种推导路径，二者在表达力上统一于 1-WL 上界（第 10、12 章）。

**数值稳定性边界。** 重归一化虽改善稳定性，但多层堆叠使 $\hat{\mathbf{D}}^{-1/2}\hat{\mathbf{A}}\hat{\mathbf{D}}^{-1/2}$ 反复作用，表示收敛到其主要特征向量对应的低维子空间——这是过平滑的谱解释（第 13 章）。因此「GCN 是低通滤波」既是优势（去噪、利用同质性）也是缺陷（丢失高频区分信息）。

从方法论看，谱域与空域的二分在文献中常被过度强调。二者实为同一 MPNN 框架的两种推导路径：谱方法从频域滤波出发、经局部化落到空域；空域方法直接从节点邻域出发、经证明可对应某种谱滤波。GCN 既可由一阶谱近似导出（本章），也可视为度归一化均值聚合（第 12 章）。理解这种统一性，比记住「谱 vs. 空域」的标签更重要——它提醒我们，模型设计的实质是在 MPNN 三函数上做选择，而非站队某种哲学。

**承上启下。** 本章的 GCN 是 MPNN 的谱实例化；第 12 章从空域视角给出 GraphSAGE、GAT、GIN，展示对 $M,\oplus$ 的灵活设计；第 13 章分析 GCN 等模型加深时的过平滑；第 14 章讨论图级读出。谱理论在第 3 章奠基，在第六篇几何深度学习（第 24—27 章）推广到流形。

## 本章小结

本章论述谱域图神经网络。

我们首先回顾图傅里叶变换与拉普拉斯对角化（式 11-1），定义谱卷积（式 11-2），指出其特征分解与不可归纳两大缺陷。接着用切比雪夫多项式推导 ChebNet（式 11-3），通过恒等式 $\mathbf{U}f(\mathbf{\Lambda})\mathbf{U}^\top=f(\mathbf{L})$ 消除特征基、实现 $K$ 跳局部化。然后取 $K=1$ 与重归一化推导 GCN（式 11-4、11-5），解释对称归一化的数值稳定性。我们进而补上图卷积定理（式 11-6）、切比雪夫近似误差（命题 11.1）与过平滑度量（式 11-7）：例 11.5 手算 ChebNet 二阶多项式修正、例 11.6 给出两层 GCN 前向验证"$L$ 层=$L$ 跳感受野"并量化过平滑随层数上升，表 11-3 把谱域概念与空域实现的复杂度并置对照。最后通过手算算例与谱系表（表 11-1、11-2）落实方法，并讨论低通滤波的双重性与数值边界。

我们还明确边界：GCN 是一阶近似、灵活性受限，深层堆叠导致过平滑。这些辨析衔接第 3、9—14、24—27 章。

下一章从空域视角介绍更灵活的图神经网络变体。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[2]、[3]。

## 参考文献

[1] Bruna J, Zaremba W, Szlam A, LeCun Y. Spectral networks and locally connected networks on graphs. *ICLR*, 2014.

[2] Kipf T N, Welling M. Semi-supervised classification with graph convolutional networks. *ICLR*, 2017.

[3] Defferrard M, Bresson X, Vandergheynst P. Convolutional neural networks on graphs with fast localized spectral filtering. *NeurIPS*, 2016.

[4] Hammond D K, Vandergheynst P, Gribonval R. Wavelets on graphs via spectral graph theory. *Applied and Computational Harmonic Analysis*, 2011, 30(2): 129–150.

[5] Shuman D I, Narang S K, Fracas F, Ortega A, Vandergheynst P. The emerging field of signal processing on graphs. *IEEE Signal Processing Magazine*, 2013, 30(3): 83–98.

[6] Li Y, Zemel R, Giraud-Carrier C. Graph heat kernel based community detection. *KDD*, 2014.

[7] Levie R, Monti F, Bacciu D. Graph neural networks as kernels on graphs. *ICML GNN Workshop*, 2018.

[8] Maskey S, Alsayyari A, Pan S. Nonlinear spectral graph convolution. *AAAI*, 2020.
