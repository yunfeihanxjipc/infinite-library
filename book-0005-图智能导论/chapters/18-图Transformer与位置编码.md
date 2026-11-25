# 第 18 章　图 Transformer 与位置编码

第 10—17 章的图神经网络以**局部消息传递**为核心：节点只能聚合 $L$ 跳邻域的信息。这带来两个根本限制：一是**长程依赖**——相距较远的节点需堆叠很多层才能相互作用，而过平滑（第 13 章）又限制了层数；二是**表达力上限**——消息传递不超过 1-WL 测试（第 10 章）。Transformer 在序列建模中的成功启发我们：用**全局注意力**（global attention）让任意两节点直接交互，从而一步覆盖全图。本章处理**图 Transformer**（Graph Transformer）及其关键配套——**位置编码**（positional encoding）。

本章先给出图上注意力的形式化与位置信息的必要性（18.1 节），推导结构/拉普拉斯位置编码（18.2 节）与 Graphormer（18.3 节），分析复杂度（18.4 节），给出数值算例（18.5 节），梳理技术谱系（18.6 节），最后讨论边界并承上启下（18.7 节）。

## 18.1　图上注意力与位置信息的必要性

**定义 18.1（图自注意力）** 给定节点特征 $\mathbf{X}\in\mathbb{R}^{n\times d}$，图自注意力层为

$$
\mathbf{Q}=\mathbf{X}\mathbf{W}_Q,\quad \mathbf{K}=\mathbf{X}\mathbf{W}_K,\quad \mathbf{V}=\mathbf{X}\mathbf{W}_V,
$$
$$
\mathrm{Att}(\mathbf{X})=\mathrm{softmax}\!\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}\right)\mathbf{V}. \tag{18-1}
$$

式 (18-1) 与标准 Transformer 完全相同——因为注意力本身不依赖图结构。**关键问题**：若不加结构信息，式 (18-1) 对任意节点排列等变，却无法区分「这条边是否存在」「节点在图中的位置」。因此图 Transformer 必须注入位置编码。

**直觉解释。** 标准 Transformer 用正弦/可学习位置编码告诉模型「词的先后顺序」；图上没有天然顺序，必须用**结构位置**代替：节点到参考点的图距离、拉普拉斯特征向量、最短路径等。位置编码是把图结构「翻译」成注意力可利用的数值信号。

> 【图 18-1　图注意力与位置编码示意】（原图见 figures/图18-1.png）：左侧全连接注意力（所有节点对），右侧叠加拉普拉斯位置编码后，注意力权重按结构距离着色。
>
> ![图 18-1　图注意力与位置编码示意](figures/图18-1.png)

## 18.2　结构与拉普拉斯位置编码

**结构位置编码。** 最直观的编码是节点到其他节点的**最短路径距离**（shortest path distance）。设 $\delta(v,u)$ 为 $v,u$ 的图距离，取一组锚点（landmark）$r_1,\ldots,r_k$，节点 $v$ 的编码为

$$
\mathbf{p}_v=\big(\delta(v,r_1),\delta(v,r_2),\ldots,\delta(v,r_k)\big)\in\mathbb{R}^k. \tag{18-2}
$$

锚点常取随机节点或度最高的节点。式 (18-2) 给出「节点相对若干参考点的结构坐标」，类似 GPS 定位——故这类方法也称**图 GPS**。

**拉普拉斯位置编码（Laplacian PE）。** 利用第 3 章归一化拉普拉斯 $\tilde{\mathbf{L}}=\mathbf{I}-\tilde{\mathbf{D}}^{-1/2}\tilde{\mathbf{A}}\tilde{\mathbf{D}}^{-1/2}$ 的特征分解

$$
\tilde{\mathbf{L}}=\mathbf{U}\boldsymbol{\Lambda}\mathbf{U}^{\top},\quad \boldsymbol{\Lambda}=\mathrm{diag}(\lambda_1,\ldots,\lambda_n), \tag{18-3}
$$

取最小的 $k$ 个非零特征值对应特征向量作为位置编码：$\mathbf{P}=\mathbf{U}_{[:,1:k]}$，第 $v$ 行 $\mathbf{p}_v$ 即其位置。拉普拉斯特征向量是图上的「傅里叶基」，低频特征向量刻画节点的平滑结构位置——与第 11 章谱域 GCN 同源，但这里用作**位置信号**而非滤波器。

**严格性质（置换等变/不变）。** 拉普拉斯特征向量在节点重排下按同一置换重排（符号不定），故 $\mathbf{p}_v$ 满足等变性；但特征向量的符号任意（$\mathbf{u}$ 与 $-\mathbf{u}$ 等价），训练时需处理符号翻转——可用随机翻转增强或取绝对值。这是拉普拉斯 PE 的实现要点。

## 18.3　Graphormer

**Graphormer** 把结构信息以三种偏置注入注意力，避免显式位置编码的符号问题。

**中心性编码（centrality encoding）。** 用节点度编码重要性：$\mathbf{x}_v\leftarrow\mathbf{x}_v+\mathbf{c}_{\deg(v)}$，其中 $\mathbf{c}$ 是可学习嵌入。度衡量节点在结构中的中心地位。

**空间编码（spatial encoding）。** 把最短路径距离作为注意力偏置：

$$
A_{vu}=\frac{(\mathbf{x}_v\mathbf{W}_Q)^{\top}(\mathbf{x}_u\mathbf{W}_K)}{\sqrt{d}}+b_{\delta(v,u)}, \tag{18-4}
$$

其中 $b_{\delta(v,u)}$ 是依赖距离的**可学习标量偏置**（按距离查表）。式 (18-4) 让模型偏好距离近的节点对，同时保留远距离交互能力——这正是全局注意力优于局部消息传递之处。

**边编码（edge encoding）。** 对连接 $v,u$ 的最短路径 $\pi=(e_1,\ldots,e_m)$，沿路径累积边特征：

$$
c_{vu}=\frac{1}{m}\sum_{i=1}^{m}\big(\mathbf{w}_{e_i}\cdot\mathbf{e}_{e_i}\big), \tag{18-5}
$$

其中 $\mathbf{e}_{e_i}$ 是边特征，$\mathbf{w}$ 是可学习权重。$c_{vu}$ 作为额外偏置加入 $A_{vu}$。三类编码叠加使 Graphormer 在分子性质预测等任务上达到当时最优。

## 18.4　复杂度分析

标准自注意力式 (18-1) 的复杂度为 $O(n^2d)$（$n$ 节点全连接），而消息传递 GNN 为 $O(|E|d)$。对稀疏大图（$|E|\ll n^2$），图 Transformer 显著更贵。这催生**稀疏 Transformer** 与**线性注意力**变体：

$$
\mathrm{Att}(\mathbf{X})\approx\phi(\mathbf{Q})\big(\phi(\mathbf{K})^{\top}\mathbf{V}\big),\quad \phi(\cdot)=\mathrm{elu}(\cdot)+1, \tag{18-6}
$$

把复杂度从 $O(n^2d)$ 降为 $O(nd^2)$（当 $d\ll n$）。此外 BigBird、PerFormer 等用稀疏/随机注意力模式，在保留表达力的同时降至近线性。实际系统常采用「局部消息传递 + 全局 Transformer」混合架构（第 29 章图基础模型）。

## 18.5　数值算例

**例 18.1（拉普拉斯 PE 手算）** 设路径图 $P_3$：$1-2-3$。归一化拉普拉斯

$$
\tilde{\mathbf{L}}=\begin{pmatrix}1&-0.707&0\\-0.707&1&-0.707\\0&-0.707&1\end{pmatrix}. \tag{18-7}
$$

其最小非零特征值 $\lambda_1\approx0.293$ 对应特征向量（归一化后）约为 $(0.5,0.707,0.5)^\top$。取该向量为 1 维位置编码：$p_1=0.5,p_2=0.707,p_3=0.5$——中间节点编码值最大，符合「中心节点」直觉；端点对称同值，符合路径图对称性。这验证了拉普拉斯 PE 能编码结构位置。

**例 18.2（空间编码偏置）** 设三节点链 $1-2-3$，$\delta(1,2)=1,\delta(1,3)=2$。取可学习偏置 $b_1=0.5,b_2=-0.3$。节点 1 对邻居 2 的注意力 logit 比对节点 3 高 $0.5-(-0.3)=0.8$，softmax 后权重显著偏向近邻——距离偏置实现了「局部性偏好」但仍是软的（节点 3 仍有非零权重），保留了长程通道。

### 18.5A　谱注意力与相对位置编码（SAN）

式 (18-1) 的全连接注意力若直接拼接绝对拉普拉斯 PE（$\mathbf{x}_v\leftarrow\mathbf{x}_v\|\mathbf{p}_v$）会引入**绝对位置**——同构图的不同节点被赋予不同编码，破坏置换等变性（第 18.7 节）。SAN（Kreuzer 等[6]）改用**相对位置编码**：注意力偏置只依赖两节点的**结构关系**（特征向量分量之差、特征值序号之差），在节点重排下不变。其简化形式为

$$
A_{vu}^{\mathrm{rel}}=\frac{(\mathbf{x}_v\mathbf{W}_Q)^{\top}(\mathbf{x}_u\mathbf{W}_K)}{\sqrt d}+\mathbf{x}_v^{\top}\mathbf{W}_{\mathrm{rel}}\,\mathbf{p}_u+\lambda\,\big(\phi(\mathbf{e}_{\lambda_v})\big)^{\top}\big(\phi(\mathbf{e}_{\lambda_u})\big), \tag{18-8}
$$

其中第一项是标准内容注意力，第二项是**相对位置项**（节点 $v$ 的特征与节点 $u$ 的位置编码 $\mathbf{p}_u$ 内积——「用我的视角看你在哪个位置」），第三项是**特征值相对项**：$\lambda_v,\lambda_u$ 是两节点在拉普拉斯谱中的主特征值序号，$\phi(\mathbf{e}_{\lambda})$ 是其可学习嵌入，$\lambda$ 为缩放。三项都只依赖 $(v,u)$ 的**相对结构**，对节点置换等变，避免了绝对 PE 的符号/编号问题。相对位置项 $\mathbf{x}_v^\top\mathbf{W}_{\mathrm{rel}}\mathbf{p}_u$ 在序列 Transformer 中对应「相对位移编码」，这里是它在图结构上的推广。

**例 18.8A（三节点全注意力手算）** 设三角形图 $1-2-3$（全连接），节点特征 $\mathbf{x}_1=(1,0)^\top,\mathbf{x}_2=(0,1)^\top,\mathbf{x}_3=(1,1)^\top$，$\mathbf{W}_Q=\mathbf{W}_K=\mathbf{I}$，$d=2$，忽略位置项先算纯内容注意力。则

$$
A_{11}=\frac{\mathbf{x}_1^\top\mathbf{x}_1}{\sqrt2}=\frac1{\sqrt2}\approx0.707,\quad
A_{12}=\frac{\mathbf{x}_1^\top\mathbf{x}_2}{\sqrt2}=0,\quad
A_{13}=\frac{\mathbf{x}_1^\top\mathbf{x}_3}{\sqrt2}=\frac1{\sqrt2}\approx0.707.
$$

节点 1 对三节点的 softmax 注意力：$A_{11},A_{13}$ 同为 0.707、$A_{12}=0$，故 $a_{11}=a_{13}=\frac{e^{0.707}}{2e^{0.707}+e^0}=\frac{2.028}{2(2.028)+1}=\frac{2.028}{5.056}\approx0.401$，$a_{12}\approx0.198$。节点 1 与节点 3 特征最像（$(1,0)$ 与 $(1,1)$ 同向分量多），故注意力均分于二者、少分给正交的节点 2。现在加入 18.2 的距离偏置 $b_\delta$：三角形中 $\delta(1,2)=\delta(1,3)=1$，偏置相同，注意力不变——这说明**距离偏置在等距图上不起区分作用**，需配合式 (18-8) 的特征向量相对项（节点 2 位于「两端之间」的谱位置与 1、3 不同）才能进一步区分。若改用路径图 $1-2-3$（$\delta(1,3)=2$），则 $b_1>b_2$ 使 $a_{13}$ 相对下降，恢复「局部性偏好」——数值上印证了「距离偏置 + 谱相对项」需按图结构配合，单一编码不足以覆盖所有几何。

## 18.6　技术谱系与变体

**表 18-1　图 Transformer 方法谱系**

| 方法 | 位置/结构编码 | 复杂度 | 代表文献 |
|------|--------------|--------|------|
| 拉普拉斯 PE Transformer | 拉普拉斯特征向量 | $O(n^2d)$ | Dwivedi 等 [1] |
| Graphormer | 中心性+空间+边编码 | $O(n^2d)$ | Ying 等 [2] |
| Graphormer 稀疏版 | 同上 + 稀疏 | 近线性 | 后续工作 [3] |
| Performer 图版 | 线性注意力 | $O(nd^2)$ | 基于 Choromanski 等 [4] |
| GraphGPS | 局部 MP + 全局注意力 | 混合 | Rampášek 等 [5] |
| SAN | 结构注意力网络 | $O(n^2d)$ | Kreuzer 等 [6] |

图 Transformer 沿「如何注入结构」分化：显式位置编码（拉普拉斯、结构编码）与注意力偏置（Graphormer 式）两条路线。前者理论清晰但有符号/锚点问题，后者实现稳健但需设计偏置函数。GraphGPS 等混合架构兼顾局部与全局，是当下的主流方向（第 29 章）。

### 18.6A　GraphGPS 混合架构与对 1-WL 的突破

纯全局注意力（式 18-1）表达力强但 $O(n^2d)$ 贵，且若不加结构信息则对所有节点对一视同仁、丢失局部感受野的归纳偏置。GraphGPS（Rampášek 等[5]）把**局部消息传递**与**带结构编码的全局注意力**并置在一个层内：

$$
\mathbf{h}_v^{\mathrm{new}}=\sigma\!\Big(\underbrace{\mathrm{MP}_v\big(\{\mathbf{h}_u:u\in N(v)\}\big)}_{\text{局部 1-WL 消息传递}}\;+\;\underbrace{\mathrm{Att}_v\big(\mathbf{h},\mathbf{p}\big)}_{\text{全局注意力（含式 18-8 相对位置）}}\Big), \tag{18-9}
$$

其中 $\mathrm{MP}_v$ 是第 10 章的局部聚合（受限于 1-WL 表达力），$\mathrm{Att}_v$ 是注入结构编码 $\mathbf{p}$ 的全局注意力（可超越 1-WL）。局部项保证「邻居结构」的强归纳偏置与 $O(|E|)$ 的稀疏计算，全局项提供「任意节点对」的长程交互与突破 1-WL 的通道，二者相加后**整体表达力由全局项主导**（只要全局注意力层数 $\ge1$ 且 PE 足够）。这正是混合架构优于「纯 GNN」与「纯 Transformer」两端的原因：纯 GNN 受 1-WL 上限、纯 Transformer 丢局部偏置且贵，GraphGPS 取其长。

**对 1-WL 上限的突破。** 第 12 章证明同构 MPNN（含 sum 读出的 GIN）不超过 1-WL 测试。图 Transformer 能否突破取决于**位置编码是否注入 1-WL 不可分辨的结构**：若 $\mathbf{p}$ 携带 1-WL 无法区分的结构信息（如 2-WL 才能分辨的「邻居多重集」），则 $\mathrm{Att}_v$ 借助 $\mathbf{p}$ 的区分力可分开 1-WL 同构的图——理论工作证明「Transformer + 足够强的 PE」可达到甚至超过 2-WL 的表达力。但结论**依赖 PE 选择**：拉普拉斯 PE 携带全局谱结构（强），仅用度（中心性编码）则偏弱。这与第 15 章「异质性通过类型维度突破 1-WL」同构——位置编码是图 Transformer 的「类型维度」：它给 1-WL 的聚合注入了额外的结构判别信息。表 18-1 中「表达力未完全突破 WL」（第 18.7 节）的边界正源于此：PE 不够强时，全局注意力也只是在 1-WL 同构图上做平滑。

**与第 13 章过平滑的互补。** 全局注意力一步覆盖全图，既**绕过长程依赖**（无需 $L$ 层堆叠）、又**绕过瓶颈**（不经过多步扩散），因此天然缓解第 13 章的过平滑与过压缩——注意力权重 $\alpha_{vu}$ 直接连接远端节点，长程信号不被多跳平均稀释。但注意力本身也有「过平滑」风险：多层自注意力在深层同样会让节点表示趋同（Transformer 的 over-smoothing），需 LayerNorm、残差与注意力稀疏化控制。图 Transformer 用「一步全局」换「层数自由」，是其相对局部 GNN 的核心优势，代价是二次复杂度（式 18-9 的全局项）。这也解释了第 13 章缓解方法谱系表中「图 Transformer」一行同时标注「解决过平滑 + 过压缩」的原因：注意力是这两种病理解法中唯一同时作用于两者的——残差/JK 只治过平滑、rewiring 只治过压缩，而全局注意力一步到位，故被第 13 章作为「承上启下」引向本章。

## 18.7　边界、讨论与承上启下

图 Transformer 的核心限制有四类，逐条展开：

**① 二次复杂度。** 全局注意力式 (18-1) 对全部 $n^2$ 节点对计算，$O(n^2d)$ 时间与 $O(n^2)$ 内存（存注意力矩阵）。对 $n=10^5$ 的图即 $10^{10}$ 量级，不可行。缓解路线有三：稀疏化（BigBird[3] 的滑窗 + 随机 + 全局 token 混合，PerFormer 的随机投影）、线性注意力（式 18-6 的 $\phi$-核，$O(nd^2)$）、采样（每节点只取 top-$k$ 注意力对象）。代价是「全局性」打折——采样后注意力实际只覆盖局部邻域，退化回局部 GNN，需在「全局表达力」与「可扩展性」间权衡。GraphGPS（式 18-9）的局部项 + 全局项设计正是为此：稀疏图用局部项主导、稠密小图才付全局项的代价。

**② 位置编码的不稳定性。** 拉普拉斯 PE（式 18-3）有两类实现难题。其一**符号翻转**：特征向量 $\mathbf{u}$ 与 $-\mathbf{u}$ 等价，数值对角化在不同运行中可能给出相反的符号，使同一图的 $\mathbf{p}_v$ 抖动；缓解办法有训练时随机翻转增强、取绝对值、或用「特征值排序 + 符号对齐」固定符号（按某一参考节点的分量符号统一）。其二**近似误差**：大图无法全量对角化 $O(n^3)$，须用 Lanczos 迭代只算前 $k$ 个特征对 $O(k|E|)$，但 Lanczos 的数值漂移会随 $k$ 增大累积，需重新正交化。SAN 的相对位置项（式 18-8）虽不直接存 $\mathbf{p}_v$，但特征值序号项仍依赖谱计算，同样受近似误差影响。

**③ 表达力未完全突破 WL。** 如 18.6A 所述，突破 1-WL 依赖 PE 注入 1-WL 不可分辨的结构。拉普拉斯 PE 携带全局谱结构、表达力强但计算重；仅中心性（度）编码则 1-WL 同构的图仍可能不可分。结论因此是「条件性」的：「Transformer 强于 GNN」仅在 PE 足够强时成立，实践中需对每个数据集验证 PE 是否带来增益，而非默认全局注意力一定更好。

**④ 小图过拟合。** 全局注意力在 $n^2$ 节点对上共享极少参数（注意力权重由 $\mathbf{W}_Q,\mathbf{W}_K,\mathbf{W}_V$ 生成），看似参数省，但**有效自由度**随 $n^2$ 增长——每个节点对都成为可被记忆的自由参数。在小数据集（图分类常见 $<10^3$ 张图）上，大图的 $n^2$ 交互易过拟合，需正则（dropout、注意力温度）、早停或数据增强（边扰动、节点特征噪声）。这是「全局注意力在小图上不一定优于局部 GNN」的根源，也与表 18-1 中各方法「在中等规模图上表现最好」的经验一致。

**位置编码的设计原则。** 综合上述边界，好的图位置编码应满足：**等变/不变**（节点重排下表示正确变换，避免绝对编号）、**结构敏感**（携带 1-WL 不可辨的结构）、**数值稳定**（无符号抖动、可近似）、**计算可行**（可 Lanczos/采样）。表 18-1 的各方法正是对这些原则的不同取舍：拉普拉斯 PE 强于「结构敏感 + 等变」但弱于「数值稳定」，Graphormer 偏置（式 18-4、18-5）强于「数值稳定 + 计算可行」但「结构敏感」依赖距离/边特征质量，SAN（式 18-8）试图四者兼顾但以谱计算为代价。选型应先问「这个图的哪类结构最判别」，再选编码。

此外，Transformer 的置换等变性依赖「不加绝对位置或正确加相对位置」，误用绝对编号（如节点 index）会破坏等变性——这是图 Transformer 实现中最易犯的错误：把「节点编号」当特征喂入，等于引入了与结构无关的人工序，使模型对节点重排敏感、丧失图学习的对称性。正确做法是所有结构信息都经 $\mathbf{p}$（PE）或偏置注入，且 $\mathbf{p}$ 本身对置换等变。

本章衔接第 3、11 章（谱理论与谱域 GCN 的位置编码同源）、第 10、13 章（本地消息传递与过平滑的互补）、第 29—31 章（图基础模型的主干架构）。下面第五篇（第 19—23 章）转向图推理，先讨论最经典的任务——链路预测。

## 本章小结

本章把全局注意力引入图学习，突破局部消息传递的长程限制。

我们首先给出图自注意力（式 18-1）与位置编码的必要性，阐明「结构位置」的直觉。接着推导结构位置编码（式 18-2）与拉普拉斯 PE（式 18-3）及其置换等变性，介绍 Graphormer 的三种编码（式 18-4、18-5），分析 $O(n^2d)$ 复杂度与线性注意力（式 18-6），并通过两个算例（式 18-7）验证位置编码与距离偏置的效果。最后梳理谱系（表 18-1）并讨论复杂度、编码不稳定、表达力、小图过拟合等边界。

我们还明确边界：二次复杂度、位置编码符号/近似问题、表达力的条件性、小图过拟合。这些辨析衔接第 3、10—11、13、29—31 章。

下一章进入第五篇，介绍链路预测——图推理最基本也是应用最广的任务。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[2]、[5]、[6]。

## 参考文献

[1] Dwivedi V P, Joshi C K, Luu A T, et al. Benchmarking graph neural networks. *JMLR*, 2023, 24(43): 1–48.

[2] Ying Z, He T, Chen J, et al. Do Transformers really perform badly for graph representation? *NeurIPS*, 2021.

[3] Zaheer M, Guruganesh G, Dubey K A, et al. Big Bird: Transformers for longer sequences. *NeurIPS*, 2020.

[4] Choromanski K, Likhosherstov V, Dower D, et al. Rethinking attention with Performers. *ICLR*, 2021.

[5] Rampášek M, Galkin V, Dwivedi V P, et al. Recipe for a general, powerful, scalable graph Transformer. *NeurIPS*, 2022.

[6] Kreuzer K, Beaini D, Hamilton W, et al. Rethinking graph transformers with spectral attention. *NeurIPS*, 2021.

[7] Yang J, Liu Z, Chen J, et al. Graphormer: A comprehensive survey. *arXiv:2312.04767*, 2023.

[8] Kim J, Park S, Lee J, et al. A survey on graph transformers: Taxonomy, applications, and challenges. *IEEE Access*, 2024, 12: 45678–45701.
