# 第 12 章　ARMA/ARIMA/SARIMA 与 Box–Jenkins 方法学

如果说指数平滑代表的是"递推式"预测哲学——用一个不断修正的水平直接外推，那么 Box–Jenkins 方法学代表的是"建模式"预测哲学：先把序列视为某个随机过程的实现，识别其相关结构，估计一个能解释该结构的模型，经严格诊断确认残差已无可用信息后，再由模型演绎出预测。二者并非优劣之分，而是两种截然不同的知识态度。第 11 章的 ETS 在第 13 章将被证明是状态空间模型的特例；本章要建立的 ARIMA 家族，则是这条"建模"路线最成熟、也最经得起统计检验的典范，至今仍是任何新预测方法必须对比的经典基准。

这条脉络有清晰的历史纵深。Yule 于 1927 年用自回归解释太阳黑子周期，把"序列由自身滞后值加扰动生成"形式化[1]；Slutsky 与 Wold 分别用移动平均的滑动作解释经济周期，Wold 更在 1938 年证明任何平稳过程都可分解为确定性成分与不可预测新息的线性组合[2]——这一 **Wold 分解**正是第 2 章 2.6 节"创新表示"的理论源头，也是本章全部模型的存在性依据。Box 与 Jenkins 于 1970 年的专著[3] 把识别、估计、诊断、预测整合为可操作的迭代流程，并推广到非平稳（差分）与季节（乘积）情形，从此 ARIMA 成为时间序列的通用语言。

在全书的理论主线里，ARIMA 是 **L1 统计可预测性**最完整的表达：它把"可预测"精确定义为"当前值与历史线性相关"，用自相关函数（第 3 章）度量这种相关，并以白噪声残差作为"信息已被榨干"的判据。它隐含四个可检验的假设：线性、平稳（差分后）、新息不相关且常方差、单变量。它突破了指数平滑"只凭近期惯性、无统计推断"的局限，给出了参数显著性、模型诊断与预测区间；却无法突破线性与常方差的理论边界——一旦存在非线性依赖、多变量传导或波动聚集，就须分别让位于第 18 章起的深度模型、第 10 章的 VAR 与第 15 章的 GARCH。遵循全书「基础理论只讲一次」的编写原则，多元 VAR/VECM/Granger 已在第 10 章唯一讲授，本章只处理单变量，并在 ARIMAX 中说明外生变量的引入方式；状态空间的统一推导留给第 13 章。全章沿用统一案例：某市级电网经日历校正后的日均负荷序列。

本章结构：12.1 节用差分把非平稳序列化为平稳；12.2、12.3 节分别严格推导 AR 与 MA 模型及其对偶性质；12.4 节组合为 ARMA/ARIMA/SARIMA；12.5 节完整展开 Box–Jenkins 四步方法学，含 AIC 家族与 Ljung–Box 检验的推导，并给出贯穿全章的完整建模算例；12.6 节处理多步预测、ARIMAX 与适用边界。

## 12.1　差分算子与非平稳性的处理

ARMA 理论只适用于弱平稳序列（第 2 章定义 2.3），而现实序列多含趋势与季节。Box–Jenkins 的第一招是用**差分**把非平稳转化为平稳，再对差分后的序列建模，最后把差分"积回"（integration）还原为原尺度预测。

**定义 12.1（差分与后移算子）** 定义后移算子 $B$ 满足 $B^k y_t = y_{t-k}$，一阶差分算子 $\nabla = 1-B$，即 $\nabla y_t = y_t - y_{t-1}$；$d$ 阶差分 $\nabla^d$，季节差分 $\nabla_s = 1-B^s$。若序列经 $d$ 阶差分后平稳，称其 $d$ 阶单整，记作 $y_t\sim I(d)$。

把差分纳入模型便得 **ARIMA$(p,d,q)$** 的一般形式：

$$
\phi(B)\,\nabla^d y_t = \theta(B)\,\varepsilon_t, \qquad \varepsilon_t\sim\mathrm{WN}(0,\sigma^2), \tag{12-1}
$$

其中 $\phi(B)=1-\phi_1 B-\cdots-\phi_p B^p$、$\theta(B)=1+\theta_1 B+\cdots+\theta_q B^q$ 分别为自回归与移动平均多项式。式 (12-1) 的含义是：对 $\nabla^d y_t$ 拟合一个平稳可逆的 ARMA$(p,q)$。

差分阶数 $d$ 的选取须以单位根检验（第 3 章 ADF/PP/KPSS[11]）为依据，而非凭肉眼。**过度差分**是常见误用：对已平稳序列再作差分，会人为引入一个单位根的 MA 项，使模型不可逆、预测方差虚高。例如对白噪声 $y_t=\varepsilon_t$ 作一阶差分得 $\nabla y_t=\varepsilon_t-\varepsilon_{t-1}$，这是一个 $\theta=-1$ 的 MA(1)，恰落在可逆性边界上（12.3 节）。因此原则是"取使序列平稳的最小 $d$"，通常 $d\le2$。

**例 12.1（统一案例：负荷序列的差分诊断）** 对两年日均负荷 $L_t$（单位 GW）作 ADF 检验，原始序列 $\tau=-1.9$（不能拒绝单位根），一阶差分后 $\tau=-8.7$（强烈拒绝），故 $d=1$。但一阶差分序列的 ACF 在滞后 7、14、21 处仍有显著峰值，提示残留周季节；再作季节差分 $\nabla_7$ 后季节峰消失。于是候选模型含 $\nabla\nabla_7$，即 $d=1,D=1,s=7$。若忽略季节差分直接拟合 ARIMA，残差将保留周期性自相关，Ljung–Box 检验必然报警。这个例子说明：**差分诊断必须与 ACF 形态（12.5 节）配合**，把趋势与季节逐一剥离干净，模型才谈得上"榨干了信息"。

差分还确定了长期预测的行为：$d=0$ 的平稳 ARMA 预测趋于均值，$d=1$ 趋于线性趋势（漂移项存在时），$d=2$ 趋于二次曲线。这与第 4 章"预测时域有限"并不矛盾——差分模型外推的是确定性多项式趋势，其误差方差仍随 $h$ 增长，只是形式上不衰减。

## 12.2　自回归模型：平稳条件与 Yule–Walker 方程

自回归（autoregression, AR）的思想最直观：当前值是近期若干值的线性组合加一个不可预测的新息。先从 AR(1) 把全部核心推导做透，再推广到 AR($p$)。

**定义 12.2（AR($p$) 模型）** 若

$$
y_t = c + \phi_1 y_{t-1} + \cdots + \phi_p y_{t-p} + \varepsilon_t, \qquad \varepsilon_t\sim\mathrm{WN}(0,\sigma^2), \tag{12-2}
$$

且 $\varepsilon_t$ 与 $y_{t-1},y_{t-2},\dots$ 不相关，则称 $\{y_t\}$ 为 $p$ 阶自回归过程。用算子写作 $\phi(B)y_t=c+\varepsilon_t$。

**平稳条件。** 以 AR(1)（$y_t=\phi y_{t-1}+\varepsilon_t$，暂设 $c=0$）为例，反复向前代入得

$$
y_t = \varepsilon_t + \phi\varepsilon_{t-1} + \phi^2\varepsilon_{t-2}+\cdots = \sum_{j\ge0}\phi^j\varepsilon_{t-j}. \tag{12-3}
$$

该无穷级数均方收敛当且仅当 $|\phi|<1$；等价地，特征方程 $\phi(z)=1-\phi z=0$ 的根 $z=1/\phi$ 落在单位圆外。一般 AR($p$) 的平稳条件是 $\phi(z)=0$ 的所有根模大于 1（单位圆外）。当 $|\phi|\ge1$ 时，式 (12-3) 发散，序列非平稳——$\phi=1$ 即随机游走（第 2 章）。这个"根在单位圆外"的判据将在第 10 章推广为 VAR 的稳定性条件、在第 12.5 节推广为可逆性判据，是全书的通用工具。

**ACF 与 Yule–Walker。** 设过程已中心化（$\mu=0$）。把式 (12-2) 两边同乘 $y_{t-k}$ 再取期望，利用 $\mathbb{E}[\varepsilon_t y_{t-k}]=0$（$k\ge1$），得**Yule–Walker 方程**

$$
\gamma_k = \phi_1\gamma_{k-1}+\cdots+\phi_p\gamma_{k-p},\quad k\ge1; \qquad
\gamma_0 = \sum_{j=1}^{p}\phi_j\gamma_j + \sigma^2. \tag{12-4}
$$

除以 $\gamma_0$ 得自相关的递推 $\rho_k=\sum_j\phi_j\rho_{k-j}$。对 AR(1)，$\rho_k=\phi\rho_{k-1}$，故 $\rho_k=\phi^k$——**ACF 呈指数（或阻尼振荡）衰减，即"拖尾"**。方差由 $\gamma_0=\phi\gamma_1+\sigma^2=\phi^2\gamma_0+\sigma^2$ 解得

$$
\gamma_0 = \frac{\sigma^2}{1-\phi^2}. \tag{12-5}
$$

式 (12-5) 也说明 $|\phi|\to1$ 时方差爆炸，再次印证平稳边界。AR($p$) 的另一个识别特征是**偏自相关函数（PACF）在 $p$ 阶后截尾**：PACF 度量"剔除中间滞后影响后，$y_t$ 与 $y_{t-k}$ 的净相关"，对 AR($p$) 在 $k>p$ 处理论为零。ACF 拖尾、PACF 截尾，是 12.5 节识别 AR 阶数的依据。

**例 12.2（AR(1) 与 AR(2) 的数值推导）**　(a) 设 $\phi=0.8$、$\sigma^2=1$，则 $\rho_k=0.8^k$：$\rho_1=0.80,\rho_2=0.64,\rho_3=0.512,\rho_4=0.410$，拖尾；由式 (12-5)，$\gamma_0=1/(1-0.64)=2.78$。(b) 设 AR(2) 的样本 ACF 为 $\hat\rho_1=0.6,\hat\rho_2=0.4$。由 Yule–Walker 前两式 $\rho_1=\phi_1+\phi_2\rho_1$、$\rho_2=\phi_1\rho_1+\phi_2$，代入解得 $\phi_1\approx0.44,\ \phi_2\approx0.27$。再验 $\rho_3=\phi_1\rho_2+\phi_2\rho_1\approx0.44\times0.4+0.27\times0.6\approx0.34$，与样本相符，说明 AR(2) 定阶合理。这类"由 ACF 反解参数"的矩估计正是第 2 章 2.5 节 MoM 的具体化。

## 12.3　移动平均模型与可逆性

若说 AR 用"过去的观测"解释现在，移动平均（MA）则用"过去的预测误差（新息）"解释现在。它不是平滑技巧，而是 Wold 分解[2] 中有限阶新息和的直接实现。

**定义 12.3（MA($q$) 模型）** 若

$$
y_t = \mu + \varepsilon_t + \theta_1\varepsilon_{t-1}+\cdots+\theta_q\varepsilon_{t-q} = \mu + \theta(B)\varepsilon_t, \tag{12-6}
$$

则称为 $q$ 阶移动平均过程。

MA 的自相关可显式算出。以 MA(1)（$y_t=\varepsilon_t+\theta\varepsilon_{t-1}$）为例：$\gamma_0=(1+\theta^2)\sigma^2$，$\gamma_1=\theta\sigma^2$，而 $k\ge2$ 时 $\gamma_k=0$。故

$$
\rho_1 = \frac{\theta}{1+\theta^2}, \qquad \rho_k=0\ (k\ge2). \tag{12-7}
$$

即 **MA($q$) 的 ACF 在 $q$ 阶后截尾**——与 AR 的 ACF 拖尾恰成对偶；相应地 MA 的 PACF 拖尾，AR 的 PACF 截尾。这一漂亮的**对偶性**是 12.5 节模型识别的基石，汇总于表 12-1。

**可逆性。** MA 模型要能从观测反解出新息（用于似然计算与预测），须满足**可逆性条件**：$\theta(z)=0$ 的根在单位圆外。对 MA(1) 即 $|\theta|<1$。此时把式 (12-6) 反演为 AR($\infty$)：

$$
\varepsilon_t = \theta(B)^{-1} y_t = \sum_{j\ge0}(-\theta)^j y_{t-j},
$$

这是几何收敛的级数，故当前新息可由全部历史观测表示。可逆性还有辨识上的必要性：$(\theta,\sigma^2)$ 与 $(1/\theta,\theta^2\sigma^2)$ 给出完全相同的 ACF（因 $\rho_1=\theta/(1+\theta^2)$ 在 $\theta\leftrightarrow1/\theta$ 下不变），若不加 $|\theta|<1$ 约束，参数不唯一。**平稳性管 AR、可逆性管 MA**，二者共同保证 ARMA 模型可辨识、可估计。

**例 12.3（MA(1) 的 ACF 与不可逆反例）**　设 $\theta=0.5$、$\sigma^2=1$，由式 (12-7) 得 $\rho_1=0.5/1.25=0.4$，$\rho_2=\rho_3=\cdots=0$，$\gamma_0=1.25$。若数据实际是 $\theta=2$（不可逆），其 $\rho_1=2/5=0.4$ 与 $\theta=0.5$ 完全相同，但 $\gamma_0=5$ 而非 1.25；模型若不加可逆约束，会在两个等价解间摇摆。实践中取 $|\theta|<1$ 的那个，把另一支排除。这个对偶反例说明：**ACF 只定到二阶矩，辨识必须靠可逆性等结构约定**。

| 模型 | ACF | PACF |
|------|-----|------|
| AR($p$) | 拖尾（指数/振荡衰减） | $p$ 阶后截尾 |
| MA($q$) | $q$ 阶后截尾 | 拖尾 |
| ARMA($p,q$) | 拖尾 | 拖尾 |

**表 12-1　ARMA 族的模型识别规则（含 ARMA 混合情形）**

## 12.4　ARMA、ARIMA 与乘积季节模型

把 AR 与 MA 组合即得 **ARMA($p,q$)**：

$$
\phi(B)y_t = \theta(B)\varepsilon_t, \tag{12-8}
$$

其平稳性由 $\phi(z)$ 的根、可逆性由 $\theta(z)$ 的根共同决定（均在单位圆外，且两多项式无公共根）。由 Wold 分解，任何平稳可逆 ARMA 都有 $\mathrm{MA}(\infty)$ 表示 $y_t=\sum_{j\ge0}\psi_j\varepsilon_{t-j}$，其中 $\psi_j$ 由 $\psi(B)=\theta(B)/\phi(B)$ 展开得到——这正是第 2 章 2.6 节"创新表示 $y_t=\sum\psi_j\varepsilon_{t-j}$"的具体实现，也是 12.6 节多步预测误差方差的出发点。

将式 (12-8) 中的 $y_t$ 换为 $\nabla^d y_t$ 即得 12.1 节的 ARIMA$(p,d,q)$。对含季节的序列，Box–Jenkins 引入**乘积季节 ARIMA**，记作 $(p,d,q)\times(P,D,Q)_s$：

$$
\phi(B)\Phi(B^s)\,\nabla^d\nabla_s^D\, y_t = \theta(B)\Theta(B^s)\,\varepsilon_t, \tag{12-9}
$$

其中 $\Phi,\Theta$ 是季节自回归/移动平均多项式，$\nabla_s^D$ 是 $D$ 阶季节差分。乘积结构用很少的参数同时刻画"相邻时刻的短程相关"与"相隔一季的长程相关"，是参数效率的典范。

**例 12.4（统一案例：负荷的乘积季节模型）**　结合 12.1 节的差分诊断（$d=1,D=1,s=7$），对残差 ACF/PACF 的观察给出：非季节部分 PACF 在 1 阶截尾、ACF 拖尾（提示 $p=1$），季节部分在滞后 7 处 ACF 有单峰（提示 $Q=1$）。于是选定 $\text{ARIMA}(1,1,1)(0,1,1)_7$，展开后 $\phi(B)=1-\phi_1 B$、$\Theta(B^7)=1+\Theta_1 B^7$ 等共 3 个待估参数。这个俗称"航空模型"（源自 Box–Jenkins 对航空旅客数据的经典拟合[3]）的结构，用极少参数同时捕捉了日间惯性、周季节与缓慢趋势，是工业负荷基线中最常见的选择之一。

## 12.5　Box–Jenkins 四步方法学与信息准则

Box–Jenkins 的真正贡献不在某个公式，而在把建模变成**可迭代、可证伪**的四步循环[3][4]：① 识别（identification）→ ② 估计（estimation）→ ③ 诊断检验（diagnostic checking）→ ④ 预测（forecasting）；若诊断不通过，回到 ① 修正阶数。图 12-1 给出这一循环。下面逐步展开，其中 AIC 家族与 Ljung–Box 的推导是本节重点。

**第一步：识别。** 用 12.1 节的差分确定 $d,D$，再用样本 ACF/PACF 按表 12-1 定 $p,q,P,Q$。实践中阶数往往不唯一，故识别只给出一小组候选，交由信息准则裁决。

**第二步：估计。** 常用**条件最小二乘**或**精确极大似然**。后者利用第 2 章式 (2-11) 的预测误差分解，把似然写为逐期一步预测密度之积；对高斯 ARMA，一步预测误差及方差可由第 13 章卡尔曼滤波递推高效算出，故似然可精确求值。估计后须检查 $\phi(z),\theta(z)$ 的根是否满足平稳可逆，不满足则剔除该候选。

**第三步：诊断检验。** 核心是检验残差 $\hat\varepsilon_t$ 是否已为白噪声。Box–Pierce 统计量 $Q^*=T\sum_{k=1}^{K}\hat\rho_k^2$ 在小样本下偏差较大，Ljung 与 Box[10] 提出修正

$$
Q = T(T+2)\sum_{k=1}^{K}\frac{\hat\rho_k^2(\hat{\boldsymbol\varepsilon})}{T-k} \;\stackrel{\text{近似}}{\sim}\; \chi^2_{K-p-q}, \tag{12-10}
$$

其中自由度为 $K$ 减去已估的 ARMA 参数个数（每估一个参数损失一个自由度）。若 $Q$ 的 $p$ 值过小，说明残差仍含可提取的线性相关，模型欠拟合，须返回识别步增阶。常配合残差 ARCH 检验（指向第 15 章）与正态性检验。

**第四步：模型选择——AIC 家族的由来。** 当多个候选都通过诊断，用信息准则权衡拟合优度与复杂度。Akaike[7] 从 **Kullback–Leibler 散度**出发：设真实密度为 $g$、模型为 $f_\theta$，使 $\mathrm{KL}(g\|f_{\hat\theta})$ 期望最小的渐近无偏估计是 $-2\log\hat L + 2k$（$k$ 为参数个数），即

$$
\mathrm{AIC} = -2\log\hat L + 2k. \tag{12-11}
$$

$2k$ 是过拟合惩罚。小样本下 AIC 倾向选过多参数，Hurvich–Tsai[8] 给出**小样本修正**

$$
\mathrm{AICc} = \mathrm{AIC} + \frac{2k(k+1)}{T-k-1}, \tag{12-12}
$$

当 $T$ 小时附加项显著，$T\to\infty$ 时退化为 AIC；预测场景优先用 AICc。Schwarz[9] 从贝叶斯后验出发给出 $\mathrm{BIC}=-2\log\hat L+k\ln T$，惩罚更重、具有模型选择一致性（真实模型在候选内时依概率选出它），但预测误差未必最小。三者取舍：以预测为目标用 AICc，以"识别真实阶数"为目标用 BIC。

**表 12-2　统一案例：候选模型的 AICc 与诊断对照**

| 候选模型 | $k$ | $\log\hat L$ | AICc | Ljung–Box $Q(12)$ 的 $p$ 值 | 结论 |
|----------|-----|--------------|------|------------------------------|------|
| ARIMA$(1,1,0)(0,1,0)_7$ | 2 | −812.4 | 1628.9 | 0.01 | 残差相关，弃 |
| ARIMA$(1,1,1)(0,1,1)_7$ | 4 | −788.1 | **1584.4** | 0.42 | 通过，最优 |
| ARIMA$(2,1,1)(0,1,1)_7$ | 5 | −787.6 | 1585.5 | 0.45 | 通过但 AICc 略高 |
| ARIMA$(1,1,2)(0,1,1)_7$ | 5 | −787.9 | 1586.1 | 0.39 | 通过但略高 |

**例 12.5（统一案例：完整的四步建模）**　对 12.1 节的两年日均负荷（训练集 640 天、测试集 90 天），执行四步：① 识别——ADF 定 $d=1,D=1$，ACF/PACF 提示 $p\le2,q\le2,Q=1$，得 8 个候选；② 估计——对每个候选作精确 MLE，剔除 2 个根不在单位圆外的；③ 诊断——计算残差 Ljung–Box $Q(12)$，其中 $\text{ARIMA}(1,1,0)(0,1,0)_7$ 的 $p=0.01$ 被淘汰，其余通过；④ 选择——按式 (12-12) 算 AICc，得表 12-2，$\text{ARIMA}(1,1,1)(0,1,1)_7$ 以 1584.4 最小，其参数估计 $\hat\phi_1=0.63,\hat\theta_1=0.41,\hat\Theta_1=-0.72$，残差方差 $\hat\sigma^2=0.031$。在 90 天测试集上，该模型 MASE=0.58，优于 11.1 节季节朴素基准的 0.71，也优于 11.5 节 ETS(M,A,M) 的 0.61——说明在含强线性季节的负荷序列上，ARIMA 对相关结构的精细刻画确有收益。整个流程可复现、可证伪，正是 Box–Jenkins 相对"试参数"式调参的本质优势。

> 【图 12-1　Box–Jenkins 四步循环】（原图见 `figures/图12-1.png`）：环形流程图——识别（定 $d,D,p,q,P,Q$）→ 估计（精确 MLE，检查平稳可逆）→ 诊断（残差 Ljung–Box、ARCH、正态性）→ 若通过则预测，否则沿回边返回识别；标注各步使用的统计量与判据。深蓝主色、圆角矩形、学术白底。

![图 12-1　Box–Jenkins 四步循环](figures/图12-1.png)

## 12.6　多步预测、ARIMAX 与适用边界

模型通过诊断后即可用于预测。由 12.4 节的 $\mathrm{MA}(\infty)$ 表示 $y_t=\sum_{j\ge0}\psi_j\varepsilon_{t-j}$，在 $T$ 时刻作 $h$ 步预测时，未来新息 $\varepsilon_{T+1},\dots,\varepsilon_{T+h}$ 的期望为零，故

$$
\hat y_{T+h\mid T} = \sum_{j\ge h}\psi_j\,\varepsilon_{T+h-j}, \qquad
e_{T+h}=\sum_{j=0}^{h-1}\psi_j\varepsilon_{T+h-j}, \tag{12-13}
$$

其中 $e_{T+h}$ 是 $h$ 步预测误差，其方差

$$
\mathrm{Var}(e_{T+h}) = \sigma^2\sum_{j=0}^{h-1}\psi_j^2. \tag{12-14}
$$

式 (12-14) 是 11.6 节 ETS 预测方差在 ARMA 框架下的对应物：随 $h$ 增大单调不减，且当 $h\to\infty$ 时 $\sum_{j\ge0}\psi_j^2\sigma^2=\gamma_0$（过程无条件方差），即**长程预测退化为无条件均值**（$d>0$ 时为趋势外推），再次印证第 4 章"可预测信息随步长耗散"的结论。多步预测有两条实现路线：把一步预测递归代入（递归策略）与对每个 $h$ 单独建模（直接策略），二者的偏差—方差权衡将在第 14 章结合多元预测系统讨论。

**ARIMAX 与动态回归。** 单变量 ARIMA 只用自己的历史，而负荷显然受气温驱动。引入外生变量 $x_t$ 有两种方式：其一是**回归 + ARMA 误差**（$y_t=\boldsymbol\beta^\top\mathbf x_t+n_t$，$n_t$ 服从 ARMA），把外生效应作为均值、相关结构留给误差，统计解释最干净；其二是 **ARIMAX**（把 $\mathbf x_t$ 直接塞进式 (12-1) 右侧），实现简单但系数含义被差分与滞后算子纠缠。须警惕**伪回归**：若 $x_t$ 与 $y_t$ 都含趋势，回归可能显著却无真实关系，应检验残差平稳或用协整（第 10 章）。统一案例中，把制冷度日数（CDD）作为 $x_t$ 加入回归 + ARMA 误差，测试集 MASE 由 0.58 降至 0.49，验证了第 10 章例 10.1 指出的"气温领先负荷"所带来的增量可预测性。

**边界与讨论。** ARIMA 的优势是理论严密、参数少、可解释、自带预测区间与诊断，且在小样本上往往优于深度模型。其硬边界有四：其一，**线性**——无法刻画阈值、饱和等非线性，须让位第 18 章起；其二，**常方差**——金融、电价等波动聚集序列须用第 15 章 GARCH 或第 24 章概率模型；其三，**单变量、低维**——多变量系统须用第 10 章 VAR、第 14 章调和或第 23 章图模型；其四，**结构稳定**——遇变点（第 9 章）或概念漂移（第 25、40 章），固定参数的 ARIMA 会持续失准，须滚动重估或在线学习。此外，长程预测退化与多步误差累积（第 14 章）意味着 ARIMA 更适合短程。理解这些边界，才能把它放在正确的位置：它是**线性单变量短程预测的黄金基准**，也是第 13 章状态空间统一视角的一个特例。

## 本章小结

本章系统建立了 ARIMA 家族与 Box–Jenkins 方法学，把预测从"递推外推"提升为"基于随机过程的统计建模"。起点是差分：后移算子 $\nabla^d$ 把 $I(d)$ 序列化为平稳，ADF 检验与 ACF 形态共同确定最小差分阶数，过度差分会引入不可逆的 MA 单位根（12.1 节）。核心推导在 12.2、12.3 节：AR(1) 的 $\mathrm{MA}(\infty)$ 展开 (12-3) 给出平稳条件 $|\phi|<1$ 与方差 $\sigma^2/(1-\phi^2)$，Yule–Walker 方程 (12-4) 推出 ACF 拖尾、PACF 截尾；MA(1) 则给出 ACF 一阶截尾与可逆性条件 $|\theta|<1$，二者形成漂亮的识别对偶（表 12-1）。组合为 ARMA/ARIMA/乘积季节模型 (12-9) 后，用极少参数同时刻画短程惯性与季节长程相关。

全章的方法学核心是 12.5 节的四步循环：识别靠 ACF/PACF，估计靠预测误差分解下的精确 MLE，诊断靠 Ljung–Box $Q$ 统计量 (12-10) 及其自由度修正，选择靠从 KL 散度导出的 AIC (12-11) 与小样本修正 AICc (12-12)。统一案例的完整算例（例 12.5）展示了这套流程如何把"试参数"变成可复现、可证伪的统计决策，并以 MASE=0.58 稳定超过第 11 章的基准与 ETS。12.6 节由 $\mathrm{MA}(\infty)$ 表示导出 $h$ 步预测方差 $\sigma^2\sum_{j<h}\psi_j^2$，证明长程预测退化为无条件均值，与第 4 章可预测性边界首尾呼应。

从理论主线看，ARIMA 是 L1 统计可预测性最完整的实现：它把可预测性定义为线性相关结构，以白噪声残差为"信息榨干"的判据，隐含线性、平稳、常方差、单变量四假设。它突破了指数平滑缺乏统计推断的局限，却无法突破非线性、异方差与多变量传导的边界。本章与全书：第 10 章 VAR 是它的多元推广（已唯一讲授）；第 13 章状态空间模型将证明 ARIMA 与 ETS 同为统一框架的特例；第 15 章处理它无能为力的波动聚集；第 14 章把递归与直接多步策略系统化；第 38 章把 Ljung–Box、AICc 与滚动回测纳入实验规范。掌握 ARIMA，等于掌握了"如何用统计证伪的方式，诚实地判断一条序列里还剩多少可提取的规律"。


从四问看，本章的 ARIMA 利用 L1（统计）：假设经差分后平稳、残差为白噪声；它突破了朴素外推、给出可诊断的建模范式，仍受「线性与平稳假设」的边界约束，无法跨越信息论下界（第 4 章）。

**进一步阅读**　本章建议延伸阅读的文献：[5]、[6]、[12]、[13]、[14]、[15]、[16]。

## 参考文献

[1] Yule G U. On a method of investigating periodicities in disturbed series, with special reference to Wolfer's sunspot numbers. *Philosophical Transactions of the Royal Society A*, 1927, 226: 267–298.

[2] Wold H. *A Study in the Analysis of Stationary Time Series*. 2nd ed. Stockholm: Almqvist & Wiksell, 1938.

[3] Box G E P, Jenkins G M. *Time Series Analysis: Forecasting and Control*. San Francisco: Holden-Day, 1970.

[4] Box G E P, Jenkins G M, Reinsel G C, Ljung G M. *Time Series Analysis: Forecasting and Control*. 5th ed. Hoboken: Wiley, 2015.

[5] Brockwell P J, Davis R A. *Introduction to Time Series and Forecasting*. 2nd ed. New York: Springer, 2002.

[6] Hamilton J D. *Time Series Analysis*. Princeton: Princeton University Press, 1994.

[7] Akaike H. A new look at the statistical model identification. *IEEE Transactions on Automatic Control*, 1974, 19(6): 716–723.

[8] Hurvich C M, Tsai C L. Regression and time series model selection in small samples. *Biometrika*, 1989, 76(2): 297–307.

[9] Schwarz G. Estimating the dimension of a model. *The Annals of Statistics*, 1978, 6(2): 461–464.

[10] Ljung G M, Box G E P. On a measure of lack of fit in time series models. *Biometrika*, 1978, 65(2): 297–303.

[11] Dickey D A, Fuller W A. Distribution of the estimators for autoregressive time series with a unit root. *Journal of the American Statistical Association*, 1979, 74(366): 427–431.

[12] Hyndman R J, Athanasopoulos G. *Forecasting: Principles and Practice*. 3rd ed. Melbourne: OTexts, 2021.

[13] Shumway R H, Stoffer D S. *Time Series Analysis and Its Applications: With R Examples*. 4th ed. New York: Springer, 2017.

[14] Chatfield C. *The Analysis of Time Series: An Introduction*. 6th ed. London: Chapman & Hall/CRC, 2003.

[15] Makridakis S, Hibon M. The M3-Competition: Results, conclusions and implications. *International Journal of Forecasting*, 2000, 16(4): 451–476.

[16] Tsay R S. *Analysis of Financial Time Series*. 3rd ed. Hoboken: Wiley, 2010.
