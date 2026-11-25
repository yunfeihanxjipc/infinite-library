# 第 20 章　注意力机制与 Transformer

第 19 章论证了预训练的历史必然，指出 Transformer 架构的突破是其中关键一环。本章正式介绍 Transformer[1]——当代自然语言处理的基石架构。Transformer 完全抛弃循环与卷积，只用**注意力机制**构建网络，实现了三点革命性突破：① 任意两位置直接连接，长程依赖建模更彻底；② 全序列并行计算，训练效率远高于 RNN（第 16 章）；③ 架构统一、可扩展，支撑了从 BERT、GPT 到今天大语言模型（第 21、26 章）的一切进展。

注意力机制的思想在第 17.2 章已作为"解码器读编码器状态"引入。本章将其提炼为一种独立的、通用的计算单元：**自注意力**（self-attention），让序列中每个位置直接关注所有位置，聚合全局信息。缩放点积注意力、多头注意力、位置编码、编码器—解码器堆叠，构成 Transformer 的完整图景。

本章是全书的 A 类核心章与架构枢纽：第 17 章的注意力在此深化，第 21 章的预训练在此架构上展开，第 26–30 章的大模型无不以 Transformer 为底座。本章先讲自注意力与缩放点积（20.1 节），再讲多头注意力与位置编码（20.2 节），介绍编码器与解码器（20.3 节），分析复杂度与长序列之困（20.4 节），并在边界与讨论中收束（20.5 节）。

## 20.1　自注意力：从内容寻址到缩放点积

**从注意力到自注意力。** 第 17.2 章的注意力中，查询来自解码器、键与值来自编码器（交叉注意力）。**自注意力**（self-attention）的关键：查询、键、值都来自**同一个序列**——序列中每个位置作为查询，去"关注"序列中所有位置（包括自己），从而聚合全局上下文。

**定义 20.1（缩放点积注意力）**　给定查询矩阵 $\mathbf{Q}\in\mathbb{R}^{n\times d_k}$、键矩阵 $\mathbf{K}\in\mathbb{R}^{m\times d_k}$、值矩阵 $\mathbf{V}\in\mathbb{R}^{m\times d_v}$，缩放点积注意力为

$$
\mathrm{Attention}(\mathbf{Q},\mathbf{K},\mathbf{V})=\mathrm{softmax}\!\left(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d_k}}\right)\mathbf{V}, \tag{20-1}
$$

其中 $\sqrt{d_k}$ 为缩放因子。对自注意力，$\mathbf{Q}=\mathbf{X}\mathbf{W}^Q,\mathbf{K}=\mathbf{X}\mathbf{W}^K,\mathbf{V}=\mathbf{X}\mathbf{W}^V$，$\mathbf{X}\in\mathbb{R}^{n\times d}$ 为输入序列表示，$\mathbf{W}^Q,\mathbf{W}^K,\mathbf{W}^V$ 为可学习投影。

**为何缩放 $\sqrt{d_k}$？** 当 $d_k$ 较大时，$\mathbf{Q}\mathbf{K}^\top$ 的点积方差随 $d_k$ 增大（若 $q,k$ 各分量独立、均值 0 方差 1，则点积方差为 $d_k$），使 softmax 输入过大、梯度饱和（softmax 进入饱和区，梯度接近 0）。除以 $\sqrt{d_k}$ 把方差拉回 1，稳定训练。

**推导：点积方差。** 设 $q,k\in\mathbb{R}^{d_k}$，各分量独立同分布，$\mathbb{E}[q_i]=\mathbb{E}[k_i]=0$，$\mathrm{Var}(q_i)=\mathrm{Var}(k_i)=1$。则

$$
\mathrm{Var}(q^\top k)=\mathrm{Var}\Big(\sum_{i=1}^{d_k}q_ik_i\Big)=\sum_{i=1}^{d_k}\mathrm{Var}(q_ik_i)=\sum_{i=1}^{d_k}1=d_k, \tag{20-2}
$$

故除以 $\sqrt{d_k}$ 后方差为 1。式 (20-2) 是缩放因子的理论依据。

**例 20.1（自注意力手算）**　设序列"我 爱 NLP"（$n=3$），$d_k=2$，投影后 $\mathbf{Q}=[\mathbf{q}_1;\mathbf{q}_2;\mathbf{q}_3]$、$\mathbf{K}=[\mathbf{k}_1;\mathbf{k}_2;\mathbf{k}_3]$。计算 scores $=\mathbf{Q}\mathbf{K}^\top/\sqrt{2}$（$3\times3$ 矩阵），每行 softmax 得注意力权重 $\alpha_{ij}$（第 $i$ 个位置对第 $j$ 个位置的关注），输出 $\mathbf{O}=\alpha\mathbf{V}$。表 20-1 给出注意力权重矩阵示意。

**表 20-1　自注意力权重矩阵（示意）**

| 查询\键 | 我 | 爱 | NLP |
|---------|----|----|-----|
| 我 | 0.6 | 0.3 | 0.1 |
| 爱 | 0.2 | 0.5 | 0.3 |
| NLP | 0.1 | 0.2 | 0.7 |

每个位置的输出是其对所有位置值的加权和——例如"爱"的输出 $=0.2\mathbf{v}_{\text{我}}+0.5\mathbf{v}_{\text{爱}}+0.3\mathbf{v}_{\text{NLP}}$，聚合了全局信息。

> 【图 20-1　缩放点积注意力】（原图见 figures/图20-1.png）：Q/K/V 计算、$\mathbf{Q}\mathbf{K}^\top/\sqrt{d_k}$、softmax、加权求和的流程图。
>
> ![图 20-1　缩放点积注意力](figures/图20-1.png)

## 20.2　多头注意力与位置编码

**多头注意力（multi-head attention）。** 单一注意力的表示能力有限。多头注意力并行运行 $h$ 个注意力"头"，每头在不同的子空间学习不同关系：

$$
\begin{aligned}
\mathrm{MultiHead}(\mathbf{Q},\mathbf{K},\mathbf{V})&=\mathrm{Concat}(\mathrm{head}_1,\dots,\mathrm{head}_h)\mathbf{W}^O,\\
\mathrm{head}_i&=\mathrm{Attention}(\mathbf{Q}\mathbf{W}_i^Q,\mathbf{K}\mathbf{W}_i^K,\mathbf{V}\mathbf{W}_i^V),
\end{aligned} \tag{20-3}
$$

其中 $\mathbf{W}_i^Q,\mathbf{W}_i^K,\mathbf{W}_i^V\in\mathbb{R}^{d\times d/h}$ 为每头的投影，$d/h$ 为每头维度（保持总计算量大致不变），$\mathbf{W}^O$ 为输出投影。不同头可关注不同关系（如一个头关注句法依存，另一个关注语义指称）——第 7.5 节的探测分析为此提供了证据。

**例 20.2（多头维度的数值设定）**　以原 Transformer 的 $d=512$、$h=8$ 为例：每头维度 $d/h=512/8=64$。每个头用 $64$ 维子空间独立算一遍式 (20-1) 的注意力，$8$ 个头并行后拼接成 $8\times64=512$ 维，再经 $\mathbf{W}^O\in\mathbb{R}^{512\times512}$ 投影回原维度。注意"每头维度 $d/h$"这一约定的意义：若每头用全 $d$ 维，总计算量将放大 $h$ 倍；用 $d/h$ 则保证多头与单头的**参数量与 FLOPs 大致相当**，多头的收益纯粹来自"多子空间分工"而非"算力堆叠"。实测中，把 $h$ 从 $1$ 增到 $8$ 通常带来小幅但稳定的 BLEU/准确率提升，而 $h$ 过大（如 $h=64$、每头仅 $8$ 维）反而因子空间过窄而退化——这解释了"多头适度"的工程经验。

**位置编码（positional encoding）。** 自注意力本身是**排列不变**的（打乱输入顺序，输出相应打乱，但无法区分位置）——它不知道词的先后顺序。位置编码把位置信息注入输入：

$$
\begin{aligned}
PE_{(pos,2i)}&=\sin(pos/10000^{2i/d}),\\
PE_{(pos,2i+1)}&=\cos(pos/10000^{2i/d}),\end{aligned} \tag{20-4}
$$

其中 $pos$ 为位置，$i$ 为维度索引。正弦余弦编码的优势：可泛化到训练时未见的长度，且相对位置可由线性变换表示（$PE_{pos+k}$ 可由 $PE_{pos}$ 线性组合得到）。"相对位置可线性表示"这一性质值得展开：设两位置 $p$、$q$，则 $PE_{p+k}$ 与 $PE_p$ 之间存在固定旋转矩阵 $R_k$（与 $p$ 无关），即 $PE_{p+k}=R_k\,PE_p$。这意味着模型只需用 $R_k$ 就能编码"两个词相距 $k$"这一相对关系，而无需记住绝对位置 $p$——这是正弦编码能外推到超长序列（训练时没见过 $n=10^5$，但 $R_k$ 仍可计算）的数学根源。实践中，可学习的位置嵌入、旋转位置编码 RoPE（第 27 章）与 ALiBi 等是其主要变体：RoPE 把上述旋转矩阵显式作用于 $\mathbf{Q}$、$\mathbf{K}$，在长上下文与推理稳定性上优于正弦编码，成为当代大模型的默认选择。

**例 20.3（位置编码的作用）**　没有位置编码，"我 爱 NLP"与"NLP 爱 我"的自注意力输出（在未投影前）难以区分词序——因为注意力只看内容相似度。加上位置编码后，每个词的表示含位置信息，模型能区分顺序。位置编码是 Transformer 建模序列的关键补丁。

**表 20-2　Transformer 核心组件**

| 组件 | 作用 | 公式 |
|------|------|------|
| 自注意力 | 全局信息聚合 | 式 (20-1) |
| 缩放 | 稳定梯度 | $\sqrt{d_k}$，式 (20-2) |
| 多头 | 多子空间关系 | 式 (20-3) |
| 位置编码 | 注入顺序 | 式 (20-4) |
| 前馈网络 | 逐位置非线性 | FFN |
| 残差 + LayerNorm | 稳定深层训练 | — |

## 20.3　Transformer 编码器与解码器

**编码器层。** Transformer 编码器由 $N$ 个相同层堆叠（原式 $N=6$），每层含两个子层：

1. **多头自注意力**子层：输入经多头自注意力聚合全局信息；
2. **前馈网络（FFN）**子层：$\mathrm{FFN}(x)=\max(0,x\mathbf{W}_1+\mathbf{b}_1)\mathbf{W}_2+\mathbf{b}_2$，逐位置应用。

每个子层外包残差连接与层归一化：$\mathrm{LayerNorm}(x+\mathrm{Sublayer}(x))$。残差连接缓解深层网络的梯度消失（第 16 章），LayerNorm 稳定训练。可把"子层 + 残差 + 归一化"统一写成一个算子：

$$
\mathrm{ResBlock}_{\mathrm{LN}}(x)=\mathrm{LayerNorm}\big(x+\mathrm{Sublayer}(x)\big), \qquad \mathrm{Sublayer}\in\{\mathrm{MultiHead},\ \mathrm{FFN}\}
$$
$$\tag{20-5}$$

其中 FFN 子层本身是逐位置的线性—ReLU—线性变换：

$$
\mathrm{FFN}(x)=\max(0,\,x\mathbf{W}_1+\mathbf{b}_1)\,\mathbf{W}_2+\mathbf{b}_2, \qquad \mathbf{W}_1\in\mathbb{R}^{d\times d_{ff}},\ \mathbf{W}_2\in\mathbb{R}^{d_{ff}\times d}
$$
$$\tag{20-6}$$

$d_{ff}$（前馈维度，原版取 $4d$）是逐位置非线性扩展的宽度——注意力负责"位置间信息交换"，FFN 负责"逐位置非线性加工"，二者交替堆叠构成 Transformer 的基本单元。注意 $\mathrm{ResBlock}_{\mathrm{LN}}$ 的残差项 $x$ 直接跳过子层，使深层网络反向传播时梯度有"高速公路"，这是 Transformer 能堆到几十甚至上百层而不退化的关键工程之一。

**解码器层。** 解码器也由 $N$ 个层堆叠，每层含三个子层：

1. **掩码多头自注意力**：只关注当前位置及之前的位置（用掩码遮蔽未来位置），保证自回归生成；
2. **交叉注意力**：查询来自解码器，键/值来自编码器输出（第 17.2 章的注意力）；
3. **前馈网络**。

同样配残差与 LayerNorm。解码器末端接线性层 + softmax 输出下一个词的概率。

**例 20.4（掩码自注意力）**　生成"I love NLP"时，解码器在生成"love"（位置 2）时，掩码使其只能关注 BOS、I（位置 1、2），不能"偷看"未来的"NLP"——这保证训练与推理的自回归一致性（对比第 17.4 节教师强制）。

**表 20-3　编码器 vs 解码器**

| 方面 | 编码器 | 解码器 |
|------|--------|--------|
| 自注意力 | 双向（无掩码） | 单向（掩码） |
| 交叉注意力 | 无 | 有（读编码器） |
| 用途 | 理解任务（BERT） | 生成任务（GPT、翻译） |

> 【图 20-2　Transformer 整体架构】（原图见 figures/图20-2.png）：编码器/解码器堆叠、多头注意力、FFN、残差与 LayerNorm、位置编码的完整架构图。
>
> ![图 20-2　Transformer 整体架构](figures/图20-2.png)

## 20.4　复杂度与长序列之困

**复杂度分析。** 自注意力的核心计算 $\mathbf{Q}\mathbf{K}^\top$ 是 $n\times n$ 矩阵乘法，复杂度 $O(n^2 d)$（$n$ 为序列长度，$d$ 为维度）；对比 RNN 的 $O(nd^2)$。当 $n\ll d$ 时 Transformer 更高效且并行；但当 $n$ 很大（长文档）时，$O(n^2)$ 的注意力矩阵成为瓶颈——这是"长序列之困"。两种架构谁优取决于 $n$ 与 $d$ 的相对大小，分界点在 $n=d$ 附近：

$$
O(n^2 d)\;\underset{?}{\lessgtr}\;O(nd^2)\quad\Longleftrightarrow\quad n\underset{?}{\lessgtr} d
$$
$$\tag{20-7}$$

即：短序列（$n<d$，如分类句子 $n\approx 50$、$d=1024$）Transformer 胜在并行与短路径；长序列（$n>d$，如长文档 $n=10^4$）RNN 的线性项反而更省，但 RNN 无法并行、路径长 $O(n)$，实际仍不占优。式 (20-7) 精确刻画了"Transformer 何时更优"的边界——它解释了为何 NLP（句子短）天然适配 Transformer，而长文档场景需要高效注意力来规避 $O(n^2)$。

**表 20-4　复杂度对照**

| 架构 | 每步复杂度 | 顺序操作 | 最大路径长度 |
|------|-----------|----------|--------------|
| RNN | $O(nd^2)$ | $O(n)$ | $O(n)$ |
| CNN | $O(knd^2)$ | $O(1)$ | $O(\log n)$ |
| Transformer | $O(n^2d)$ | $O(1)$ | $O(1)$ |

Transformer 的最大路径长度 $O(1)$（任意两位置直接连接）是其长程建模优势，但 $O(n^2)$ 的内存/计算是长序列瓶颈。

**高效注意力方向。** 为突破 $O(n^2)$，研究者提出稀疏注意力（Sparse Transformer、Longformer、BigBird）、线性注意力（Performer）、低秩近似、局部窗口 + 全局 token 等——这些将在《世界模型导论》《大模型系统与工程导论》中展开。这些方法可分三类：① 稀疏化（只算部分位置对，如局部窗口 + 少量全局位置）；② 低秩/核化（把 $\mathbf{Q}\mathbf{K}^\top$ 分解或近似，使其与 $n$ 线性相关）；③ 分块/流式（把长序列切块、跨块传递摘要）。三者都在"表达力"与"效率"之间做不同的权衡，本节仅指出问题的存在与大致方向。

**例 20.5（长文档的限制）**　标准 Transformer 的上下文长度通常有限（如 512、2048 token）。处理整本书或长对话时，需切分或高效注意力——这是长上下文大模型（第 27 章）的核心挑战。

**例 20.6（$O(n^2)$ 的数值直觉）**　设 $d=1024$，比较不同序列长度下注意力矩阵 $\mathbf{Q}\mathbf{K}^\top$ 的元素数 $n^2$ 与 FFN 每位置计算量 $d_{ff}\cdot d\approx 4d^2\approx4.2\times10^6$ 的相对规模：

**表 20-5　注意力矩阵规模随序列长度的增长**

| 序列长度 $n$ | 注意力元素 $n^2$ | 占 $d^2$ 的倍数 | 训练友好度 |
|------|------|------|------|
| 128 | $1.6\times10^4$ | $\approx0.02\,d^2$ | 轻松 |
| 1024 | $1.0\times10^6$ | $\approx1\,d^2$ | 舒适 |
| 8192 | $6.7\times10^7$ | $\approx65\,d^2$ | 内存压力 |
| 32768 | $1.07\times10^9$ | $\approx1040\,d^2$ | 需高效注意力 |

可见 $n$ 从 1024 增到 32768（32 倍），注意力矩阵从 $\approx1\,d^2$ 暴增到 $\approx1040\,d^2$（平方增长），很快压过 FFN 成为主导项。这正是式 (20-7) 中"长序列 $O(n^2)$ 瓶颈"的数值体现，也是 8K/32K 长上下文大模型（第 27 章）必须引入稀疏/线性/分块注意力的根本原因。

## 20.5　边界与讨论

Transformer 是当代 NLP 的基石，但须明确其边界。

**架构的统一与局限。** Transformer 统一了编码器（理解）、解码器（生成）、编码器—解码器（翻译）三种模式（第 21 章 BERT/GPT/T5），但 $O(n^2)$ 复杂度与对海量数据的依赖（第 26 章）是其代价。它不是万能的——在超长序列、极低资源场景仍有局限。更深层的局限在于：Transformer 的"全局连接"假设**所有位置两两交互都是必要的**，但真实语言中绝大多数位置间并无直接依赖（句内依赖高度局部化）。这一过度假设正是高效注意力（稀疏/线性/分块）的改进空间：它们通过限制交互范围或降低交互秩，把 $O(n^2)$ 降到 $O(n\log n)$ 甚至 $O(n)$，代价是可能损失长程信息——这是"表达力"与"效率"的根本权衡，Transformer 站在表达力一端，高效注意力则向效率一端妥协。

**意义表示。** Transformer 通过自注意力聚合全局信息，其表示隐式编码了句法与语义（第 7.5 节探测，第 29 章）。但它是 M2 层的表示学习——不显式保证 M4 指称正确（第 29 章幻觉）。注意力权重常被误读为"模型在看什么"的解释，但第 7.5 节的探测实验表明，注意力权重与可解释的"解释"往往不一致——它是计算过程的中间产物，而非语义归因。把注意力图当作"模型的解释"是一种常见的过度解读，须以探测分析等更严格的方法代替。

**与后续章节的紧密联系。** Transformer 是全书枢纽：第 21 章预训练范式在此架构上展开（BERT 用编码器、GPT 用解码器、T5 用编解码器）；第 23 章 LoRA 微调针对 Transformer 权重；第 26–30 章大模型皆基于 Transformer；第 27 章的高效架构（MoE、稀疏注意力）由其演化。第 17 章的注意力在此深化为自注意力。可以说，不理解 Transformer，就无法理解当代语言智能。具体地，式 (20-5) 的残差—归一化算子是第 23 章"冻结主干、只调低秩适配"的解剖对象；式 (20-1) 的 $\mathbf{Q}\mathbf{K}^\top$ 是第 26 章计算量核算（FLOPs）的主导项；式 (20-4) 的位置编码外推问题直接催生第 27 章的长上下文技术。下一章进入预训练范式。

第五篇（第 20–25 章）以本章为基石，将展开预训练范式的全貌：预训练目标（第 21 章）、训练（第 22 章）、微调适配（第 23 章）、上下文学习（第 24 章）、多语言（第 25 章）。

## 本章小结

本章论述注意力机制与 Transformer，是全书的 A 类核心章与架构枢纽。

我们首先介绍自注意力与缩放点积注意力（式 20-1），推导缩放因子 $\sqrt{d_k}$ 的理论依据（点积方差为 $d_k$，式 20-2），并用手算示例（例 20.1、表 20-1）展示注意力权重矩阵。接着介绍多头注意力（式 20-3，多子空间关系，例 20.2 给出 $d=512$、$h=8$ 的维度设定）与位置编码（式 20-4，注入顺序），说明它们如何增强表示。我们介绍 Transformer 的编码器（双向自注意力 + FFN）与解码器（掩码自注意力 + 交叉注意力 + FFN）堆叠，用式 (20-5)、(20-6) 把"子层 + 残差 + 层归一化"统一为算子，并分析 $O(n^2)$ 复杂度与长序列之困：式 (20-7) 给出 Transformer 与 RNN 的优劣分界（$n\lessgtr d$），例 20.6 与表 20-5 给出注意力矩阵随序列长度平方增长的数值直觉，并指出高效注意力方向。

我们还明确边界：Transformer 统一三种架构模式但有复杂度与数据依赖代价；其表示是 M2 层的，不保证 M4 指称。Transformer 作为全书枢纽，衔接第 17、21、23、26–30 章。

Transformer 为预训练提供了可扩展的架构基础。下一章进入预训练范式，讲 BERT、GPT、T5、ELECTRA 等如何通过不同预训练目标，在 Transformer 架构上学习通用语言能力。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[2]、[3]、[4]。

## 参考文献

[1] Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need. *Advances in Neural Information Processing Systems*, 2017, 30.

[2] Bahdanau D, Cho K, Bengio Y. Neural machine translation by jointly learning to align and translate. *ICLR*, 2015.

[3] Su J, Lu Y, Pan S, et al. RoFormer: Enhanced transformer with rotary position embedding. *arXiv:2104.09864*, 2021.

[4] Child R, Gray S, Radford A, Sutskever I. Generating long sequences with sparse Transformers. *arXiv:1904.10509*, 2019.

[5] Beltagy I, Peters M E, Cohan A. Longformer: The long-document transformer. *arXiv:2004.05150*, 2020.

[6] Zaheer M, Guruganesh G, Dubey K A, et al. Big Bird: Transformers for longer sequences. *Advances in Neural Information Processing Systems*, 2020, 33.

[7] Devlin J, Chang M W, Lee K, Toutanova K. BERT: Pre-training of deep bidirectional transformers for language understanding. *NAACL*, 2019.

[8] Jurafsky D, Martin J H. *Speech and Language Processing*. 3rd ed. Stanford, 2023.
