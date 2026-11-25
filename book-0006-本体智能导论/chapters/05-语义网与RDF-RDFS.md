# 第 5 章　语义网与 RDF/RDFS

第 4 章建立的描述逻辑是语义网推理的理论内核。本章把概念落到 Web 数据模型上：介绍语义网愿景与资源描述框架（5.1 节）、RDF 数据模型与三元组（5.2 节）、RDFS 轻量模式（5.3 节）、命名图与数据集（5.4 节），最后讨论边界（5.5 节）。本章核心问题是：如何为 Web 上的海量数据提供机器可处理的语义，使知识层（$L_2$）大规模落地。

## 5.1　语义网愿景与资源描述框架

**引入与动机。** 今天的 Web 主要由人类阅读：网页是人看的，机器只知抓取字符串。语义网（semantic web）愿景主张：让 Web 上的数据带有机器可理解的语义，使程序能自动推理与互操作[1]。RDF 是这一愿景的基石。

**直觉解释。** 若把 Web 看作一个巨大的图书馆，传统网页是「给人看的书」，语义网则给每本书贴上机器能读的标签：这本书讲什么、作者是谁、与哪些书相关。这些标签用统一格式写成，程序可自动汇总与推理。

**严格定义与推导。** 语义网分层架构由 Berners-Lee 提出：底层为 Unicode 与 URI，其上为 XML 与 RDF，再上为 RDFS、OWL、SPARQL、规则与证明层[2]。

$$\langle x,\text{type},d\rangle\in\mathrm{cl}(G)\ \text{若}\ \langle x,\text{type},c\rangle\in G\wedge\langle c,\text{subClassOf},d\rangle\in G.\tag{5-1}$$

**定义 5.1（资源描述框架 RDF）** RDF 是一种基于三元组的数据模型，用于描述网络资源。一个 RDF 三元组（triple）形如 $(s,p,o)$，其中 $s$ 为主语（subject，资源）、$p$ 为谓词（predicate，属性）、$o$ 为客体（object，资源或字面量）。三元组集合构成 RDF 图。

由定义 5.1 可推出 RDF 与描述逻辑的对应：三元组 $(s,p,o)$ 对应 ABox 断言 $p(s,o)$；RDFS/OWL 类声明对应 TBox 公理。RDF 图是有标注的有向图，节点为资源或字面量，边为属性——这把第 4 章的 DL 概念落到图结构上。

**数值算例。** 设一个 RDF 数据集描述医学知识：$\langle\text{阿司匹林},\text{类型},\text{药物}\rangle$、$\langle\text{阿司匹林},\text{治疗},\text{头痛}\rangle$、$\langle\text{头痛},\text{类型},\text{症状}\rangle$。共 $|V|=3$ 个资源节点（阿司匹林、药物、头痛、症状中字面量除外共 4 个 URI 节点），$|E|=3$ 条边。若再添加 1000 种药物、每种平均 5 条三元组，则三元组总数增至 $3+1000\times5=5003$——RDF 的图模型可自然扩展到大规模知识层。

**技术谱系与变体。** 表 5-1 对照语义网各层技术。

**表 5-1　语义网技术栈**

| 层次 | 技术 | 作用 |
|------|------|------|
| 标识 | URI / IRI | 资源的全局唯一标识 |
| 语法 | Turtle / RDF/XML | 三元组的序列化格式 |
| 数据模型 | RDF | 三元组与图 |
| 模式 | RDFS | 类、属性与轻量蕴含 |
| 本体 | OWL | 丰富公理与推理 |
| 查询 | SPARQL | 图模式查询 |
| 规则 | SWRL / RIF | 自定义推理规则 |

**边界与讨论。** RDF 只提供数据模型而非推理能力；语义的严格化由 RDFS 与 OWL 完成。把 RDF 等同于「语义网」是常见误解——RDF 是语法与数据层，语义在更高层。

**承上启下。** 愿景确立后，本节深入 RDF 数据模型与三元组细节。

## 5.2　RDF 数据模型与三元组

**引入与动机。** RDF 的简洁性（只有三元组）既是优点也是限制。理解其数据模型，才能理解为何说「RDF 把知识表示为图」以及蕴含如何发生。

**直觉解释。** 每个三元组是一句「主—谓—宾」的简单陈述，如「阿司匹林 治疗 头痛」。大量三元组连成图，节点共享即产生关联。这种「关系优先」的表示，与关系数据库的「表优先」形成对比，更适合稀疏、多变的领域知识。

**严格定义与推导。** 给出 RDF 的形式定义。

**定义 5.2（RDF 图）** 设 $U$ 为 URI 集合、$L$ 为字面量集合、$B$ 为空白节点集合。RDF 项集 $T=U\cup L\cup B$。一个 RDF 三元组是 $(s,p,o)\in(U\cup B)\times U\times T$。RDF 图是三元组的有限集合 $G\subset T\times U\times T$。

字面量可带语言标签或数据类型（如 `"阿司匹林"@zh`、`"37.5"^^xsd:decimal`）。空白节点表示存在但无需命名的个体，用于描述复合结构。

**定义 5.3（RDF 蕴含）** RDF 图 $G_1$ 蕴含 $G_2$（$G_1\models G_2$），若每个使 $G_1$ 为真的解释也使 $G_2$ 为真。RDF 有一组形式化蕴含规则（RDF entailment regimes）[3]，例如从 $(s,\text{type},p)$ 不能推出更多，但 RDFS 规则可推出类与属性层级。

由定义 5.3 可推出 RDF 图上的蕴含闭包概念：给定规则集 $R$，图 $G$ 关于 $R$ 的闭包是应用 $R$ 中规则可推出的所有三元组的集合，记作 $\mathrm{cl}_R(G)$。蕴含判定即检查目标三元组是否在闭包中。

**数值算例。** 设 $G=\{\langle a,\text{type},A\rangle,\ \langle A,\text{subClassOf},B\rangle\}$，RDFS 规则包括：若 $(x,\text{type},y)$ 且 $(y,\text{subClassOf},z)$ 则 $(x,\text{type},z)$。应用规则得 $\langle a,\text{type},B\rangle$，故 $\mathrm{cl}(G)=G\cup\{\langle a,\text{type},B\rangle\}$，共 3 条三元组。若再添 $\langle B,\text{subClassOf},C\rangle$，则闭包增至 5 条（新增 $\langle a,\text{type},C\rangle$ 与 $\langle B,\text{subClassOf},C\rangle$ 本身已计）——展示了 RDFS 规则的传递扩张。

**技术谱系与变体。** 表 5-2 对照 RDF 序列化格式。

**表 5-2　RDF 序列化格式对照**

| 格式 | 特点 | 适用 |
|------|------|------|
| Turtle | 紧凑、可读 | 人工编写与教学 |
| RDF/XML | XML 语法 | 早期标准、工具兼容 |
| N-Triples | 每行一个三元组 | 大规模数据流 |
| JSON-LD | JSON 兼容 | Web 应用 |

**边界与讨论。** RDF 的开放世界语义与关系数据库不同：三元组缺失不等于否定。例如图中没有「阿司匹林 治疗 癌症」不意味着「阿司匹林不治疗癌症」——这与第 4.2 节的 OWA 一致。

### 5.2.1　Turtle 序列化与空白节点展开

**直觉解释。** 定义 5.2 给出的三元组是「抽象语法」，但人写 RDF 时用的是具体语法（Turtle、RDF/XML、N-Triples）。Turtle 允许用 `@prefix` 缩写 URI、用 `;` 串联同主语的谓词、用 `[]` 内联空白节点，从而把图写得紧凑。理解序列化与抽象语法的关系，才能正确解析与生成 RDF 数据。

**严格定义与推导。** 一个 Turtle 片段与 RDF 图之间存在确定的**序列化展开**（parse）映射 $\pi$：

$$
\pi:\text{Turtle}\to\mathcal{P}(\mathcal{T}\times\mathcal{U}\times\mathcal{T}),\qquad
\texttt{a:aspirin a:Drug ; a:treats a:headache .}\ \mapsto\ \{\langle\texttt{a:aspirin},\texttt{a:Drug}\rangle,\ \langle\texttt{a:aspirin},\texttt{a:treats},\texttt{a:headache}\rangle\}. \tag{5-1A}
$$

式 (5-1A) 中，前缀 `a:Drug` 由 `@prefix a: <http://ex.org/drug#>` 展开为完整 IRI；内联空白节点 `[]` 在展开时生成唯一标识符（如 `_:b0`）。展开是「语法不唯一、图唯一」的标准化基础：不同 Turtle 片段若表达同一三元组集，则展开后相同。

**数值算例。** 设统一案例的医学片段，用 Turtle 写作：

```
@prefix a: <http://ex.org/drug#> .
a:aspirin a:Drug ; a:treats a:headache .
a:headache a:Symptom .
```

展开为三元组：$\langle\texttt{a:aspirin},\texttt{a:Drug}\rangle$、$\langle\texttt{a:aspirin},\texttt{a:treats},\texttt{a:headache}\rangle$、$\langle\texttt{a:headache},\texttt{a:Symptom}\rangle$，共 3 条。注意 `a:aspirin a:Drug ; a:treats a:headache .` 一行展开为 2 条三元组（`;` 串联同主语），这正是 Turtle 的紧凑性来源。若改为内联空白节点 `a:aspirin a:hasSideEffect [ a:name "nausea" ] .`，则展开为 2 条三元组 $\langle\texttt{a:aspirin},\texttt{a:hasSideEffect},\_:b0\rangle$、$\langle\_:b0,\texttt{a:name},\texttt{"nausea"}\rangle$——空白节点 `_:b0` 在展开时产生，使「有副作用」这一复合结构无需给副作用单独命名。

**技术谱系与变体。** 各序列化格式的「展开粒度」不同：N-Triples 每条三元组一行（无缩写，最接近抽象语法）、Turtle 支持前缀与 `;`/`,` 串联、RDF/XML 用 XML 元素表达（一个元素可含多个属性）、JSON-LD 用 JSON 对象表达（支持上下文压缩）。表 5-2 已对照。工程上，大规模数据流常用 N-Triples（行式、易并行解析），人工编写与教学用 Turtle（可读），Web 应用用 JSON-LD（与 JSON 生态兼容）。

**边界与讨论。** 空白节点是 RDF 序列化与抽象语法的关键衔接点：它让「不命名中间对象」成为可能，但也带来「跨图空白节点身份」问题——不同图各自的 `_:b0` 可能指不同对象，跨图查询时不可直接合并（第 5.4 节命名图）。此外，字面量类型（`"37.5"^^xsd:decimal`）在展开时保留类型信息，但不同格式对字面量类型标注的支持程度不一（JSON-LD 用 `@type` 标注），这是序列化间非无损转换的根源之一。

**承上启下。** 序列化展开明确后，下一节介绍赋予 RDF 图语义的 RDFS 模式语言。

## 5.3　RDFS 与轻量模式

**引入与动机。** 纯 RDF 三元组没有类型、层级与域/值域约束，机器无法从「阿司匹林 治疗 头痛」推出「阿司匹林是一种干预」。RDFS（RDF Schema）提供轻量模式语言，补齐这些语义。

**直觉解释。** RDFS 像给 RDF 图加一层「类型系统」：声明哪些是类、类之间如何继承、属性适用于什么类型的主语与宾语。有了它，机器可做简单的蕴含推理——这是从 S1 词汇级到 S2 概念级的跃迁。

**严格定义与推导。** RDFS 引入核心词汇：`rdf:type`（实例归属）、`rdfs:subClassOf`（子类）、`rdfs:subPropertyOf`（子属性）、`rdfs:domain`（定义域）、`rdfs:range`（值域）。其语义由一组蕴含规则定义[4]。

**定义 5.4（RDFS 蕴含规则）** 关键规则包括：(a) 若 $(c,\text{subClassOf},d)$ 且 $(x,\text{type},c)$，则 $(x,\text{type},d)$；(b) 若 $(c,\text{subClassOf},d)$ 且 $(d,\text{subClassOf},e)$，则 $(c,\text{subClassOf},e)$；(c) 若 $(p,\text{domain},c)$ 且 $(x,p,y)$，则 $(x,\text{type},c)$；(d) 若 $(p,\text{range},c)$ 且 $(x,p,y)$，则 $(y,\text{type},c)$；(e) 若 $(p,\text{subPropertyOf},q)$ 且 $(x,p,y)$，则 $(x,q,y)$。

由定义 5.4 可推出：RDFS 的蕴含是单调的——规则只添加三元组不删除。这与第 3.2 节 DL 的单调性一致。RDFS 推理的复杂度为 NP 完全（对数据复杂度为多项式），远低于 OWL DL——这是「轻量模式」的含义。

**数值算例。** 设 RDFS 图含：$\langle\text{药物},\text{subClassOf},\text{干预}\rangle$、$\langle\text{治疗},\text{domain},\text{药物}\rangle$、$\langle\text{治疗},\text{range},\text{疾病}\rangle$、$\langle\text{阿司匹林},\text{治疗},\text{头痛}\rangle$。应用规则 (c) 推出 $\langle\text{阿司匹林},\text{type},\text{药物}\rangle$；再由规则 (a) 推出 $\langle\text{阿司匹林},\text{type},\text{干预}\rangle$；应用规则 (d) 推出 $\langle\text{头痛},\text{type},\text{疾病}\rangle$。原始 4 条三元组，闭包增至 7 条——3 条新事实由 RDFS 语义自动推出，展示了轻量模式的推理价值。

**技术谱系与变体。** 表 5-3 对照 RDFS 与 OWL 的表达力。

**表 5-3　RDFS 与 OWL 表达力对照**

| 能力 | RDFS | OWL DL |
|------|------|--------|
| 类层级 | 有 | 有 |
| 域/值域 | 有 | 有 |
| 布尔组合类 | 无 | 有 |
| 基数约束 | 无 | 有 |
| 不相交性 | 无 | 有 |
| 推理复杂度 | NP | ExpTime/NExpTime |

**边界与讨论。** RDFS 表达力有限：无法表达「药物与疾病不相交」或「某类至少有 2 个实例」。这些需 OWL（第 6 章）。RDFS 的价值在于简单高效，适合大规模、推理需求轻的场景。

### 5.3.1　RDFS 蕴含闭包的不动点计算与复杂度

**直觉解释。** 5.3 节给出 RDFS 的单步蕴含规则，但实际推理是反复应用规则直到「不再产生新三元组」。这一反复应用的过程可用不动点（fixpoint）刻画：从初始图 $G_0$ 出发，每轮应用所有规则得到 $G_{i+1}$，直到 $G_{i+1}=G_i$ 收敛。理解不动点计算，才能估计 RDFS 推理的规模膨胀与终止性。

**严格定义与推导。** 设 RDFS 规则集 $\mathcal{R}$，定义闭包迭代序列 $G_0=G$、$G_{i+1}=G_i\cup\mathrm{Derive}(G_i)$，其中 $\mathrm{Derive}(G_i)$ 是 $G_i$ 上应用 $\mathcal{R}$ 新推出的三元组。若存在 $n$ 使 $G_n=G_{n+1}$，则 $G^* = G_n$ 是 $G$ 关于 $\mathcal{R}$ 的**蕴含闭包**（不动点）。闭包规模膨胀比定义为：

$$
\lambda(G)=\frac{|G^*|}{|G|}\ge1. \tag{5-2A}
$$

式 (5-2A) 中 $\lambda$ 度量推理使三元组数膨胀的倍数。RDFS 规则（定义 5.4 的 (a)–(e)）是单调的（只加不删），故序列 $G_0\subseteq G_1\subseteq\cdots$ 单调递增；又因三元组集有限（URI 与字面量有限），序列必在某轮达到不动点，故 RDFS 闭包**有限步收敛**。但 $\lambda$ 可能很大——若类层级很深（$A_1\sqsubseteq A_2\sqsubseteq\cdots\sqsubseteq A_n$），一条 $(x,\text{type},A_1)$ 经规则 (a) 可推出 $n$ 条 $(x,\text{type},A_i)$。

**数值算例。** 设初始图 $G$ 含 $\langle\text{阿司匹林},\text{type},\text{药物}\rangle$、$\langle\text{药物},\text{subClassOf},\text{干预}\rangle$、$\langle\text{干预},\text{subClassOf},\text{实体}\rangle$、$\langle\text{治疗},\text{domain},\text{药物}\rangle$、$\langle\text{治疗},\text{range},\text{疾病}\rangle$、$\langle\text{阿司匹林},\text{治疗},\text{头痛}\rangle$，共 $|G|=6$。
- $G_1$（第 1 轮）：规则 (a) 推 $\langle\text{药物},\text{subClassOf},\text{实体}\rangle$、$\langle\text{阿司匹林},\text{type},\text{干预}\rangle$；规则 (c) 推 $\langle\text{阿司匹林},\text{type},\text{药物}\rangle$（已有）；规则 (d) 推 $\langle\text{头痛},\text{type},\text{疾病}\rangle$。新增 3 条，$|G_1|=9$。
- $G_2$（第 2 轮）：规则 (a) 推 $\langle\text{阿司匹林},\text{type},\text{实体}\rangle$（由 $\text{阿司匹林}:\text{干预}$ 与 $\text{干预}\sqsubseteq\text{实体}$）。新增 1 条，$|G_2|=10$。
- $G_3=G_2$，不动点，$G^*=G_2$。

故 $\lambda=10/6\approx1.667$，经 2 轮收敛。若类层级深度增至 $n=10$（$\text{药物}\sqsubseteq A_2\sqsubseteq\cdots\sqsubseteq A_{10}$），则 $\langle\text{阿司匹林},\text{type},\text{药物}\rangle$ 将推出 9 条新类声明，$\lambda$ 随 $n$ 线性增长——这解释了为何深层类层级会放大 RDFS 闭包规模，也是大规模本体推理（第 14 章）需优化类层级深度的原因。

**技术谱系与变体。** RDFS 闭包的不动点计算复杂度：对数据（ABox 式三元组）固定时，推理为多项式；对数据规模计，RDFS 蕴含判定为 NP 完全（第 5.3 节表 5-3）。这与 OWL DL 的 ExpTime/NExpTime 复杂度形成对照——RDFS 的「轻量」正体现在闭包计算的多项式性。第 7 章 SPARQL 查询若开启 RDFS 语义，则每次查询隐式执行一次闭包计算（或依赖预计算闭包），开销取决于 $\lambda$。

**边界与讨论。** 不动点收敛依赖「三元组集有限」，若 URI 空间无界（如动态生成 IRI），闭包可能不终止——这是 RDFS 在动态数据源上的边界。此外，$\lambda$ 线性膨胀假设层级为链式；若层级为分叉（一个父类多个子类），膨胀更复杂但仍是多项式。工程上，预计算 RDFS 闭包并缓存是常见优化（第 14 章），代价是存储膨胀 $\lambda$ 倍。

**承上启下。** 闭包计算给出 RDFS 推理的可量化模型，下一节讨论多图共存的命名图与数据集。

## 5.4　命名图与数据集

**引入与动机。** 真实应用中，RDF 数据来自多个来源：一个图存医学本体，一个图谱存临床事实，一个存用户标注。若混在一起，来源信息丢失且可能产生冲突。命名图（named graph）解决这一问题。

**直觉解释。** 命名图像给每张 RDF 图贴标签「这是 A 来源的」「这是 B 来源的」。数据集由多个命名图构成，查询时可指定在哪个图中查，也可跨图查询——这为知识融合（第 12 章）与联邦查询（第 7 章）奠定基础。

**严格定义与推导。** 给出 RDF 数据集的形式定义。

**定义 5.5（RDF 数据集）** RDF 数据集是一个集合 $\{(g_i,G_i)\}$，其中 $g_i$ 为命名图的 IRI，$G_i$ 为 RDF 图；另有一个默认图 $G_0$（无名）。数据集的合流式（merge）为 $\bigcup_i G_i$，用于不区分来源的查询[5]。

由定义 5.5 可推出：命名图保留来源语义，而合并丢失来源。例如图 $g_1$ 含「阿司匹林 治疗 头痛」，图 $g_2$ 含「阿司匹林 治疗 发热」，合并后无法区分哪个来源主张哪条事实。若要做「可信来源优先」的融合（第 12、13 章），必须保留命名图结构。

**数值算例。** 设数据集含 3 个命名图：$g_1$（医学本体）含 180 条三元组、$g_2$（临床事实）含 8500 条、$g_3$（用户标注）含 300 条。数据集总三元组数为 $180+8500+300=8980$（各图可能有重复 URI，但三元组按图独立计数）。若对 $g_1$ 做 RDFS 闭包推理得 250 条，对 $g_2$ 不做推理，则跨图查询「所有药物」时需从 $g_1$ 的 250 条类声明中提取——命名图使推理范围可控。

**技术谱系与变体。** 表 5-4 对照命名图相关技术。

**表 5-4　命名图与数据集技术**

| 技术 | 作用 | 相关章节 |
|------|------|---------|
| 命名图 | 保留来源与上下文 | 5, 7, 12 |
| RDF 数据集 | 多图容器 | 5, 7 |
| 具名查询图 | SPARQL 跨图查询 | 7 |
| 链接数据 | Web 上分布的数据集 | 34 |

**边界与讨论。** 命名图是 RDF 数据模型的扩展，不同三元组库对 SPARQL 具名图的支持有差异（第 7 章）。此外，命名图间的语义关系（如「$g_2$ 与 $g_1$ 矛盾」）需额外机制刻画，超出 RDF 标准。

**承上启下。** 数据模型与模式语言已备，下一节讨论 RDF/RDFS 的边界。

## 5.5　边界与讨论

本章建立语义网的数据基础：RDF 三元组模型（定义 5.1、5.2）、RDFS 蕴含规则（定义 5.4）、命名图数据集（定义 5.5）。这些内容处于知识层（$L_2$）并把概念层（$L_1$）的术语标准化。

**语义之梯四问的回应。** RDF/RDFS 处于语义之梯 S1—S2：RDF 三元组是 S1 词汇级的图化，RDFS 类层级与域/值域是 S2 概念级；它隐含「开放世界、三元组语义」假设，突破了传统 Web 数据无结构之限，但无法突破「公理与强推理之限」——这正是 OWL（第 6 章）要补的。

需要强调：RDF 的「图」与知识图谱的「图」概念相通但粒度不同。RDF 图是形式语义对象，知识图谱是工程上对大规模 RDF/属性图的统称（第 11、14 章）。第 16 章的嵌入推理以知识图谱为对象，但其三元组语义源于本章。

下一章进入 OWL 与本体语言，看 S3 公理级语义如何在 Web 标准中落地。

> 【图 5-1　RDF 三元组图模型】（原图见 figures/图5-1.png）：节点为主语客体、边为谓词，标注 RDFS 蕴含扩张
>
> ![图 5-1　RDF 三元组图模型](figures/图5-1.png)

## 本章小结

本章系统论述语义网与 RDF/RDFS。我们首先介绍语义网愿景与 RDF 三元组模型（定义 5.1、5.2）；给出 RDFS 蕴含规则（定义 5.4）与轻量推理算例；讨论命名图与数据集（定义 5.5）；用四张表对照语义网技术栈、序列化格式、RDFS 与 OWL 表达力。

我们还明确边界：RDF/RDFS 处于 S1—S2 级，隐含开放世界与三元组语义，突破 Web 数据无结构之限但无法突破公理与强推理之限。这些辨析衔接第 4 章的描述逻辑、第 6 章的 OWL、第 7 章的 SPARQL，以及第 12、34 章的融合与链接数据。

下一章介绍 OWL 与本体语言，把描述逻辑的公理化能力带入 Web 标准。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[3]、[4]。

## 参考文献

[1] Berners-Lee T, Hendler J, Lassila O. The semantic web. *Scientific American*, 2001, 284(5): 34–43.

[2] Berners-Lee T. Semantic Web — W3C Design Issues. W3C, 1998.

[3] Klyne G, Carroll J J. Resource Description Framework (RDF): Concepts and Abstract Syntax. *W3C Recommendation*, 2004.

[4] Brickley D, Guus S. RDF Vocabulary Description Language 1.0: RDF Schema. *W3C Recommendation*, 2004.

[5] Carroll J J, Bizer C, Hayes P J, Stickler P. Named graphs. *Journal of Web Semantics*, 2005, 3(4): 247–267.

[6] Beckett D. RDF/XML Syntax Specification (Revised). *W3C Recommendation*, 2004.

[7] wood D, Lanthaler M, Cáceres C P. JSON-LD 1.0: A JSON-based Serialization for Linked Data. *W3C Recommendation*, 2014.

[8] Prud'hommeaux E, Seaborne A. SPARQL Query Language for RDF. *W3C Recommendation*, 2008.
