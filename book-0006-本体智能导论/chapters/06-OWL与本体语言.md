# 第 6 章　OWL 与本体语言

第 5 章的 RDFS 只能表达轻量语义，而第 4 章的描述逻辑提供了完整的公理化能力。OWL（Web Ontology Language）正是把描述逻辑带入 Web 标准的本体语言。本章先介绍 OWL 的层级 Lite/DL/Full（6.1 节），给出构造算子与公理（6.2 节），建立 OWL 与描述逻辑的对应（6.3 节），用统一案例演示疾病—药物本体建模（6.4 节），最后讨论边界（6.5 节）。本章是 A 类核心章，承接第 4 章并为第 8、9 章奠基。

## 6.1　OWL 的层级：Lite、DL、Full

**引入与动机。** OWL 需同时满足「表达力强」「推理可判定」「与 RDF 兼容」三个目标，而三者不可兼得。为此 OWL 定义了三个子语言，分别取舍[1]。

**直觉解释。** OWL Lite 最简单——只支持类层级与简单约束，适合轻量应用；OWL DL 是主力——保持描述逻辑的可判定性，支持丰富公理；OWL Full 最自由——允许任意 RDF 语义，但推理不可判定。三者像「经济舱、商务舱、头等舱」：越往上越灵活，但代价越高。

**严格定义与推导。** 给出三个子语言的界定。

**定义 6.1（OWL Lite）** OWL Lite 是 OWL DL 的受限子集，仅允许类与属性的层级、简单基数约束（0 或 1）、有限的属性特征。其推理复杂度低于 OWL DL，适合以分类为主的应用。

**定义 6.2（OWL DL）** OWL DL 是 OWL 的可判定片段，对应描述逻辑 $\mathcal{SHOIN}(\mathbf{D})$（后扩展到 $\mathcal{SROIQ}$）。它要求类、属性、个体三者分离（disjointness of vocabulary），且禁止属性被当作个体使用——这些限制保证推理可判定。

**定义 6.3（OWL Full）** OWL Full 允许 OWL 词汇与 RDF 词汇任意混合（如把 owl:Class 当作实例），表达力最强但与 RDF 语义完全一致，导致推理不可判定。

由定义 6.1—6.3 可推出子语言间的包含关系：$\text{OWL Lite}\subset\text{OWL DL}\subset\text{OWL Full}$。任何合法的 OWL Lite 本体都是合法 OWL DL 本体，任何 OWL DL 本体都是合法 OWL Full 本体；但反向不成立。这一单调包含关系意味着应用可从 Lite 起步，需要时升级到 DL，而 Full 因不可判定性通常仅用于无需自动推理的场景。

**数值算例。** 设某本体含 50 个类、20 个属性、3 个基数约束（值为 1）。若所有构造在 OWL Lite 允许范围内，则可用 Lite 推理（多项式）；若加入「$\text{药物}\sqcup\text{疾病}$」这类布尔组合类，则超出 Lite，须用 DL（ExpTime）；若再把「owl:Class 本身作为实例」用于元建模，则进入 Full，推理不可判定。三层取舍决定了同一本体可能需在不同子语言间迁移。

**技术谱系与变体。** 表 6-1 对照 OWL 三子语言。

**表 6-1　OWL 子语言对照**

| 子语言 | 表达力 | 可判定性 | 对应 DL | 适用 |
|--------|--------|---------|--------|------|
| OWL Lite | 弱 | 多项式/低 | $\mathcal{SHIF}$ | 简单分类 |
| OWL DL | 中强 | ExpTime/NExpTime | $\mathcal{SHOIN}/\mathcal{SROIQ}$ | 主流推理 |
| OWL Full | 最强 | 不可判定 | 无 | 元建模、无需推理 |

**边界与讨论。** 选择 OWL DL 还是 Full 是常见困惑。经验法则：凡需自动推理（分类、一致性检测）的应用，必须用 OWL DL；凡强调最大自由度且不需要推理的场景，可用 Full。OWL Lite 因表达力过弱，现代应用较少采用。

**承上启下。** 层级明确后，本节给出 OWL 的具体构造算子与公理。

### 6.1.1　子语言选型：表达力、复杂度与规模的量化权衡

**直觉解释。** 6.1 节指出三子语言「表达力递增、可判定性递减」，但工程选型还需考虑第三个维度——**本体规模**（类数、公理数、ABox 大小）。三子语言本质是在「表达力—复杂度—规模」三角上取不同顶点：Lite 牺牲表达力换规模，DL 取平衡，Full 牺牲可判定性换表达力。本节用统一案例量化这一权衡。

**严格定义与推导。** 设本体 $O$ 的**表达力需求**为其公理所需构造算子集 $\mathcal{O}p$（如是否需要 $\neg$、$\forall$、基数约束），**规模**为 $|C|$ 类、$|A|_\mathcal{A}$ 条 ABox 断言。子语言 $L\in\{\text{Lite},\text{DL},\text{Full}\}$ 的**可行性判据**为：

$$
L\ \text{可行}\iff \mathcal{O}p\subseteq\mathcal{O}p(L)\ \wedge\ \mathrm{time}_L(|C|,|A|_\mathcal{A})\le T_{\max}. \tag{6-1A}
$$

式 (6-1A) 中 $\mathcal{O}p(L)$ 是 $L$ 支持的构造算子集，$\mathrm{time}_L$ 是 $L$ 下推理的实测耗时，$T_{\max}$ 是应用可接受时限。$\mathcal{O}p\subseteq\mathcal{O}p(L)$ 是「表达力够」，$\mathrm{time}_L\le T_{\max}$ 是「跑得快」。两条件缺一则 $L$ 不可行——前者排除表达力不足，后者排除规模超限。

**数值算例。** 设统一案例医学本体 $|C|=60$、$|A|_\mathcal{A}=8500$，所需构造 $\mathcal{O}p=\{\sqcap,\sqsubseteq,\exists,\forall,\text{disjoint},\neg\}$（含否定与不相交）。
- **OWL Lite**：$\mathcal{O}p(\text{Lite})=\{\sqsubseteq,\text{基数 }0/1\}$，缺 $\sqcap,\exists,\forall,\neg,\text{disjoint}$，故 $\mathcal{O}p\nsubseteq\mathcal{O}p(\text{Lite})$，**不可行**（表达力不足）。
- **OWL 2 DL**：$\mathcal{O}p(\text{DL})$ 含全部所需构造，$\mathcal{O}p\subseteq\mathcal{O}p(\text{DL})$；实测 $\mathrm{time}_{DL}\approx3$ 秒（NExpTime 但 $|C|=60$ 小），$T_{\max}=10$ 秒，**可行**。
- **OWL 2 EL**：$\mathcal{O}p(\text{EL})$ 缺 $\neg,\forall$（EL 无否定与全称），$\mathcal{O}p\nsubseteq\mathcal{O}p(\text{EL})$，**不可行**——除非放弃式 (6-1) 的 disjoint 公理（disjoint 需 $\neg$ 表达）。
- **OWL 2 QL**：针对查询优化，$\mathcal{O}p(\text{QL})$ 缺 $\neg$ 与 $\sqcap$，同样不可行。

结论：该本体只能选 OWL 2 DL，或「降级」放弃否定与不相交公理改用 EL（牺牲表达力换 PTime 推理，可支撑 $|C|$ 增至 6000 的规模）。若某应用 $|C|=6000$、$T_{\max}=1$ 秒，则即使 DL 表达力够，$\mathrm{time}_{DL}$ 也超限，须降级 EL 或用 QL——此时「表达力够」让位于「规模跑得快」。

**技术谱系与变体。** 表 6-1、表 6-3 已对照三子语言与对应 DL 的复杂度。工程实践中，SNOMED CT 用 OWL 2 EL（$|C|$ 约 35 万，放弃否定与全称换 PTime），生物医学领域本体常用 OWL 2 DL（$|C|$ 数千至数万，需否定与不相交）。表 6-5 给出版本选型的决策表。

**表 6-5　OWL 子语言选型决策表**

| 需求特征 | 推荐子语言 | 理由 |
|---------|-----------|------|
| $|C|\le10^3$，需否定/不相交 | OWL 2 DL | 表达力够、规模可承受 |
| $|C|\ge10^4$，不需否定/全称 | OWL 2 EL | PTime 推理，规模大 |
| 面向数据库查询（AC0） | OWL 2 QL | 查询复杂度 AC0，可推入 RDB |
| 需元建模、不需推理 | OWL Full | 表达力最强 |

**边界与讨论。** 式 (6-1A) 的 $T_{\max}$ 是「软约束」，依赖硬件与推理机实现（第 9 章），非理论常数；而 $\mathcal{O}p\subseteq\mathcal{O}p(L)$ 是「硬约束」，由子语言定义决定，不可通过优化突破。因此选型应先用硬约束排除表达力不足的子语言，再用软约束在可行子语言中按规模择优。这一「先硬后软」的选型策略贯穿第 9 章推理机选型。

**承上启下。** 子语言选型量化后，下一节给出 OWL 的具体构造算子与公理。

## 6.2　OWL 的构造算子与公理

**引入与动机。** OWL DL 的表达力来自丰富的构造算子与公理。理解它们，才能把领域知识写成可推理的本体。

**直觉解释。** OWL 的构造算子与第 4 章的 ALC 算子一脉相承（布尔组合、量词），并增加了逆属性、属性层级、不相交性、基数约束与名义（枚举个体）等。公理则把这些概念组织成知识库。

**严格定义与推导。** OWL 的构造算子包括：布尔算子（`owl:complementOf`、`owl:unionOf`、`owl:intersectionOf`）、枚举（`owl:oneOf`）、属性限制（`owl:someValuesFrom`、`owl:allValuesFrom`、`owl:minCardinality` 等）、属性特征（`owl:inverseOf`、`owl:TransitiveProperty` 等）。公理包括类公理（`subClassOf`、`equivalentClass`、`disjointWith`）、属性公理（`subPropertyOf`、`domain`、`range`）、个体公理（`differentFrom`、`sameAs`）[2]。

**定义 6.4（OWL DL 公理的语义）** OWL DL 公理的语义由到描述逻辑的映射给出：类公理 `C subClassOf D` 映射为 $C\sqsubseteq D$；`C equivalentClass D` 映射为 $C\equiv D$；`C disjointWith D` 映射为 $C\sqcap D\sqsubseteq\bot$；`P domain C` 映射为 $\top\sqsubseteq\forall P^{-}.C$（或等价形式）；属性限制 `P someValuesFrom C` 映射为 $\exists P.C$。所有公理的语义由第 4.2 节的解释函数 $\cdot^{\mathcal{I}}$ 给出。

由定义 6.4 可推出 OWL DL 与描述逻辑的严格等价：OWL DL 本体可无损失地翻译为 $\mathcal{SROIQ}$ 知识库，反之亦然。这是 OWL DL 推理可判定性的理论依据，也是第 9 章推理机实现的基础。

**数值算例。** 设 OWL 本体含公理：`阿司匹林 equivalentClass 药物 ⊓ (∃hasSideEffect.副作用)`、`hasSideEffect domain 药物`、`hasSideEffect range 副作用`、`药物 disjointWith 疾病`。映射到 DL：$\text{阿司匹林}\equiv\text{药物}\sqcap\exists\text{hasSideEffect}.\text{副作用}$，$\top\sqsubseteq\forall\text{hasSideEffect}^{-}.\text{药物}$，$\top\sqsubseteq\forall\text{hasSideEffect}.\text{副作用}$，$\text{药物}\sqcap\text{疾病}\sqsubseteq\bot$。若本体另有断言 `hasSideEffect(阿司匹林, 恶心)` 与 `疾病(恶心)`，则由 range 公理推出 `副作用(恶心)`，再由不相交公理得 `疾病 ⊓ 副作用` 不可满足——推理机可检测出该本体的不一致性。例中本体含 4 条类/属性公理、1 条个体断言，推理发现 1 处冲突——展示了 OWL 公理的检测能力。

**技术谱系与变体。** 表 6-2 对照 OWL 构造算子的 DL 对应。

**表 6-2　OWL 构造算子与 DL 对应**

| OWL 构造 | DL 表示 | 语义级 |
|---------|--------|-------|
| `complementOf` | $\neg C$ | S3 |
| `unionOf` | $C\sqcup D$ | S3 |
| `intersectionOf` | $C\sqcap D$ | S3 |
| `someValuesFrom` | $\exists r.C$ | S3 |
| `allValuesFrom` | $\forall r.C$ | S3 |
| `min/maxCardinality` | $\ge n\,r.C$ | S3 |
| `oneOf` | $\{a_1,\dots,a_n\}$ | S3 |
| `inverseOf` | $r^-$ | S3 |

**边界与讨论。** OWL DL 的表达力虽强，但公理数量增大时推理性能下降（第 9 章）。此外，OWL 采用开放世界假设：未声明的不一致不等于一致，未声明的实例不等于不存在。"缺失即未知"是理解 OWL 推理结果的关键。

**承上启下。** 构造算子明确后，下一节严格建立 OWL 与描述逻辑的对应。

## 6.3　OWL 与描述逻辑的对应

**引入与动机。** 为何 OWL DL 推理可判定？因为它与描述逻辑 $\mathcal{SROIQ}$ 严格对应。本节给出这一对应的形式化陈述，它是 OWL 推理机（第 9 章）的理论根基。

**直觉解释。** OWL 像描述逻辑的「Web 语法外衣」：同一份知识，用 OWL 的 RDF/XML 或 Turtle 语法写成，与用 DL 符号写成，语义完全等价。推理机可把 OWL 本体翻译成 DL 知识库后调用 Tableau 算法。

**严格定义与推导。** 给出对应的形式化。

**定理 6.1（OWL DL 与 $\mathcal{SROIQ}$ 的等价性）** OWL DL 本体与 $\mathcal{SROIQ}(\mathbf{D})$ 知识库之间存在保持语义的双射：对每个 OWL DL 本体 $O$，存在 $\mathcal{SROIQ}$ 知识库 $\mathcal{K}$，使对任意查询 $q$，$O\models q$ 当且仅当 $\mathcal{K}\models q$[3]。

证明要点：OWL DL 的每个构造算子与公理都有唯一对应的 $\mathcal{SROIQ}$ 构造（定义 6.4 给出的映射），该映射保持解释与满足关系；由于映射是双射且保真，蕴含关系一致。

由定理 6.1 可推出：OWL DL 的推理复杂度等同于 $\mathcal{SROIQ}$ 的推理复杂度（NExpTime 完全），且所有 $\mathcal{SROIQ}$ 推理算法都可用于 OWL DL。这解释了为何推理机（HermiT、Pellet）内部以 DL 而非 OWL 语法工作。

**数值算例。** 某 OWL DL 本体含 120 个类、30 个对象属性、5 个数据属性、200 条公理。翻译为 $\mathcal{SROIQ}$ 知识库后，类数 120、角色数 35（30 对象+5 数据）、公理数 200 保持不变。若用 Tableau 推理机分类，需判定 $120\times119/2=7140$ 对类的包含关系；实测在标准硬件上耗时数秒——这展示了定理 6.1 的工程价值：复杂 OWL 推理可外包给成熟 DL 推理机。

**技术谱系与变体。** 表 6-3 对照 OWL 版本与对应 DL。

**表 6-3　OWL 版本与描述逻辑对应**

| OWL 版本 | 对应 DL | 推理复杂度 |
|---------|--------|-----------|
| OWL 1 DL | $\mathcal{SHOIN}(\mathbf{D})$ | NExpTime |
| OWL 2 DL | $\mathcal{SROIQ}(\mathbf{D})$ | NExpTime |
| OWL 2 EL | $\mathcal{EL}^{++}$ | PTime |
| OWL 2 QL | DL-Lite | AC0 |

**边界与讨论。** OWL 2 引入了 EL 与 QL 两个轻量 profile，分别针对大规模分类与数据库查询优化（第 9、14 章）。这再次体现「表达力—复杂度—规模」的三角权衡。

**承上启下。** 对应关系确立后，下一节用统一案例做一次完整的 OWL 建模。

## 6.4　统一案例：疾病—药物本体建模

**引入与动机。** 理论需落地。本节用统一案例展示如何把一个医学领域的需求转化为 OWL 本体。

**直觉解释。** 建模从需求出发：我们要让系统能回答「某药可治哪些病」「某病有哪些症状」「某药有哪些副作用」「某症状是否提示某病」。为回答这些问题，需要定义疾病、药物、症状、副作用四类核心概念及其关系。

**严格定义与推导。** 建模步骤：先列核心类（疾病、药物、症状、副作用、患者、医生），再定义对象属性（治疗、表现为、有副作用、开具），再写类公理与属性公理，最后添加个体断言。核心公理如下：

$$
\begin{aligned}
&\text{药物}\sqsubseteq\exists\text{治疗}.\text{疾病},\\
&\text{疾病}\sqsubseteq\exists\text{表现为}.\text{症状},\\
&\text{副作用}\sqcap\text{疾病}\sqsubseteq\bot,\\
&\text{有副作用的药物}\equiv\text{药物}\sqcap\exists\text{有副作用}.\text{副作用}.
\end{aligned} \tag{6-1}
$$

式 (6-1) 中，前两条定义概念的必要条件，第三条声明不相交性（副作用不是疾病），第四条定义复合概念。若添加个体断言 $\text{阿司匹林}:\text{药物}$、$\text{头痛}:\text{疾病}$、$\text{治疗}(\text{阿司匹林},\text{头痛})$，则可推出 $\text{可治头痛药}(\text{阿司匹林})$ 等结论（若定义了相应复合概念）。

**数值算例。** 设统一案例的 OWL 本体含：类 60 个、对象属性 25 个、数据属性 12 个、公理 180 条、个体 1200 个。按 OWL 2 DL 翻译为 $\mathcal{SROIQ}$，推理复杂度 NExpTime 但实测可控。若改用 OWL 2 EL（放弃否定与全称），推理降为 PTime，可处理更大规模——代价是无法表达式 (6-1) 的不相交公理。这一取舍在真实医学本体（如 SNOMED CT 用 OWL 2 EL）中十分典型。

**技术谱系与变体。** 表 6-4 对照本体建模的逐层产物。

**表 6-4　疾病—药物本体建模产物**

| 步骤 | 产物 | 语义级 |
|------|------|--------|
| 术语收集 | 类与属性名 | S1 |
| 层级构建 | subClassOf 公理 | S2 |
| 公理添加 | 式 (6-1) 公理 | S3 |
| 推理 | 分类与一致性 | S4 |

**边界与讨论。** 建模的难点是「公理的真实性」。例如「所有药物都有适应证」在医学上并非绝对，写死为公理会引入错误。实践中需与领域专家反复确认，并区分「定义性公理」（必然）与「常识性规则」（或然，交给规则层第 8 章）。

### 6.4.1　推理任务与推断代价

**直觉解释。** 6.4 节给出了本体公理，但「推理」具体做什么？OWL 推理机的核心任务有四：**分类**（把每个命名类归入 TBox 的层级，找出其最近父类与子类）、**一致性检测**（判断 TBox 与 ABox 是否矛盾，即 $\bot$ 是否被推出）、**实例检测**（判断某个体是否属于某命名类）、**检索**（找出某概念的所有实例）。四者共同构成「S4 推理级」的能力。

**严格定义与推导。** 设 OWL DL 本体 $O$ 翻译为 $\mathcal{SROIQ}$ 知识库 $\mathcal{K}=\langle\mathcal{T},\mathcal{A}\rangle$，定义**分类代价**：

$$
\mathrm{cost}_{\text{cls}}(O)=\binom{|C|}{2}=\frac{|C|(|C|-1)}{2}\ \text{次包含检测}. \tag{6-2A}
$$

式 (6-2A) 中 $\binom{|C|}{2}$ 是 $|C|$ 个命名类两两判定包含的对数。每次包含检测归约为一次 $\mathcal{SROIQ}$ 可满足性检测（第 4.1 节），故分类总代价为 $\binom{|C|}{2}\cdot\mathrm{cost}_{\text{sat}}$。一致性检测只需判定 $\bot$ 是否属于 $\mathcal{T}$ 的闭包，为 1 次可满足性检测；实例检测对每个个体 $a$ 判定 $\mathcal{K}\models C(a)$，代价随 $|A|_\mathcal{A}\cdot|C|$ 增长。

**数值算例。** 设统一案例 $|C|=60$、$|A|_\mathcal{A}=1200$。则 $\mathrm{cost}_{\text{cls}}=\binom{60}{2}=60\times59/2=1770$ 次包含检测。设每次 $\mathcal{SROIQ}$ 可满足性检测实测 $0.5$ ms，则分类总耗时 $\approx1770\times0.5$ ms $\approx0.89$ 秒——与 6.3 节「实测数秒」一致。若 $|C|$ 增至 600（10 倍），$\mathrm{cost}_{\text{cls}}$ 增至 $\binom{600}{2}=179700$（约 101 倍，因组合数二次增长），耗时 $\approx89$ 秒——分类代价随类数**二次增长**，这是 OWL DL 推理在大规模本体上变慢的根本原因。一致性检测始终仅 1 次可满足性检测，代价与 $|C|$ 无关，故「先查一致性、再做分类」是推理机的标准优化顺序。

**技术谱系与变体。** 四推理任务的复杂度：分类与实例检测为 NExpTime 完全（随 $|C|$、$|\mathcal{A}|$ 增长），一致性检测为 NExpTime 但常数小。第 9 章推理机（HermiT、Pellet）通过增量推理、缓存中间结果、把包含检测转化为 SAT 实例化等技术，使实测代价远低于 NExpTime 上界。表 6-5 的选型决策正基于「$|C|$ 增长时 $\mathrm{cost}_{\text{cls}}$ 二次膨胀」这一事实——规模超限时降级 EL（PTime）。

**边界与讨论。** 式 (6-2A) 假设「两两独立判定」，实际推理机用增量分类（一次推理同时确定整个层级）把 $O(|C|^2)$ 降为近 $O(|C|\cdot\log|C|)$，但理论复杂度上界不变。此外，分类结果依赖 TBox 公理的完整性——若 TBox 缺失某包含公理，分类会给出「错误但自洽」的层级（OWA 下无矛盾），这正呼应 6.5 节「公理真实性」的难点。

**承上启下。** 推理任务与代价量化后，下一节讨论 OWL 的边界。

## 6.5　边界与讨论

本章建立 OWL 本体语言的完整图景：三子语言（定义 6.1—6.3）、构造算子与公理（定义 6.4）、与描述逻辑的等价（定理 6.1）与统一案例（式 6-1）。

**语义之梯四问的回应。** OWL DL 处于语义之梯 S3 公理级，隐含开放世界与清晰语义假设，突破了 RDFS 无法表达复杂公理之限，但无法突破「可判定性约束下的表达力上限」——为保持可判定，OWL DL 禁止元建模与任意规则。这与第 3.4 节的不可判定性一脉相承。

需要强调：OWL 的「推理可判定」依赖 OWL DL 的词汇分离限制。一旦跨越到 OWL Full（如 OWL 词汇自描述），推理即不可判定。此外，OWL 缺乏封闭世界与默认推理能力，处理「除非另有说明」这类常识需规则扩展（第 8 章）或概率方法（第 18 章）。

下一章进入 SPARQL 查询，看如何检索 OWL/RDF 知识库中的知识。

> 【图 6-1　OWL 子语言层级与 DL 对应】（原图见 figures/图6-1.png）：Lite/DL/Full 三层包含关系，标注对应 DL 与复杂度
>
> ![图 6-1　OWL 子语言层级与 DL 对应](figures/图6-1.png)

## 本章小结

本章系统论述 OWL 与本体语言。我们首先介绍 OWL Lite/DL/Full 三子语言（定义 6.1—6.3）；给出构造算子与公理及其 DL 映射（定义 6.4、表 6-2）；建立 OWL DL 与 $\mathcal{SROIQ}$ 的等价（定理 6.1、表 6-3）；用统一案例演示疾病—药物本体建模（式 6-1）并讨论边界。

我们还明确边界：OWL DL 处于 S3 公理级，隐含开放世界语义，突破 RDFS 公理薄弱之限但无法突破可判定性约束下的表达力上限。这些辨析衔接第 4 章的描述逻辑、第 5 章的 RDF/RDFS、第 8 章的规则扩展，以及第 9 章的推理机。

下一章介绍 SPARQL 查询语言，把知识检索能力带入本体系统。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[2]、[3]。

## 参考文献

[1] McGuinness D L, van Harmelen F. OWL Web Ontology Language Overview. *W3C Recommendation*, 2004.

[2] Dean M, Schreiber G. OWL Web Ontology Language Reference. *W3C Recommendation*, 2004.

[3] Motik B, Parsia B, Grau B C, et al. OWL 2 Web Ontology Language: Structural Specification and Functional-Style Syntax. *W3C Recommendation*, 2009.

[4] Horrocks I, Sattler U. Ontology reasoning in the SHOQ(D) description logic. *IJCAI*, 2001: 199–204.

[5] Smith M K, Welty C, McGuinness D L. OWL Web Ontology Language Guide. *W3C Recommendation*, 2004.

[6] Golbreich C, Zhang Z, Boley H. OWL 2 web ontology language new features and rationale. *OWLED*, 2008.

[7] Grau B C, Horrocks I, Motik B, et al. OWL 2: The next step for OWL. *Journal of Web Semantics*, 2008, 6(4): 309–322.

[8] Uschold M, Gruninger M. Ontologies: Principles, methods and applications. *Knowledge Engineering Review*, 1996, 11(2): 93–136.
