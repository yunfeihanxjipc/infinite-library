# 第 15 章　波动率与条件异方差模型

前面四章的模型，无论指数平滑、ARIMA 还是状态空间，预测的几乎都是**条件均值**：给定历史，下一期的负荷最可能是多少。但均值只是分布的一个侧面。对电网调度而言，"预测误差通常多大、极端日会偏离多少"往往比点预测本身更决定备用容量；对金融风险管理而言，波动率就是被直接交易与监管的对象。本章把建模对象从**一阶矩**转向**二阶矩**，系统建立条件异方差模型，并把它放回全书"概率预测"的框架中理解。

这一转向有清晰的历史节点。Engle 于 1982 年研究英国通胀时提出 ARCH，第一次让"方差随时间变化"成为可建模、可估计的对象[1]；Bollerslev 于 1986 年加入方差自身的滞后项，得到参数更节约的 GARCH[2]；此后 Nelson 的 EGARCH[4]、Glosten 等的 GJR-GARCH[5]、Zakoian 的 TGARCH[6] 处理"坏消息比好消息更抬升波动"的杠杆效应，Engle 等人把波动率引入均值方程得到 GARCH-M[7]。Engle 因 ARCH 获 2003 年诺贝尔经济学奖，标志这一框架成为计量经济学的基石。平行地，Taylor 等发展的随机波动率（SV）模型[8] 把方差本身设为不可观测的随机过程，与第 13 章状态空间语言天然相通。

在全书理论主线里，本章代表 L1 统计可预测性在**二阶矩**上的延伸：一阶矩（均值）可能已近白噪声、毫无线性可预测性，但**平方残差仍显著自相关**——这意味着"波动的大小"可预测，即使"波动的方向"不可预测。它突破了第 12 章 ARIMA"常方差"这一硬假设（回顾 12.6 节边界之二），却无法突破"仅建模条件方差、不刻画分布形状与外部冲击"的边界。按本书统一的编写原则，恰当评分规则、CRPS 等概率预测工具已在第 2 章定义、第 24 章系统展开，本章只聚焦方差模型本身；状态空间的完整推导在第 13 章，SV 一节只作交叉引用。全章沿用统一案例：对第 12 章某市级电网 ARIMA 模型的**残差**建模——这些残差在均值上已近似白噪声，却在盛夏高温日、节假日前后呈现明显的波动聚集。

本章结构：15.1 节从波动率的典型事实引出 ARCH；15.2 节推导 GARCH(1,1) 的平稳性与无条件方差；15.3 节处理非对称变体；15.4 节讲估计、诊断与多步波动率预测；15.5 节讨论随机波动率、VaR/ES 与边界。

## 15.1　波动率的典型事实与 ARCH 模型

对资产收益或预测残差作平方、取绝对值后观察自相关，会反复看到三组**典型事实**（stylized facts）：① **波动聚集**（volatility clustering）——大波动后倾向跟随大波动，小波动后跟随小波动；② **厚尾**——极端值出现频率远高于正态分布预测；③ **杠杆效应**——负向冲击（坏消息）比同等幅度的正向冲击引发更大波动。常方差模型（第 12 章）无法解释任何一条：它假设 $\mathrm{Var}(\varepsilon_t)=\sigma^2$ 恒定。

**定义 15.1（ARCH($q$) 模型）** 设均值方程已充分提取信息，残差 $\varepsilon_t$ 满足

$$
\varepsilon_t = \sigma_t z_t,\quad z_t\sim \mathrm{iid}(0,1),\qquad
\sigma_t^2 = \omega + \sum_{i=1}^{q}\alpha_i\,\varepsilon_{t-i}^2, \tag{15-1}
$$

其中 $\omega>0,\ \alpha_i\ge0$，且 $\sigma_t^2$ 与 $z_t$ 独立。称 $\{\varepsilon_t\}$ 为 $q$ 阶自回归条件异方差过程。

式 (15-1) 的直觉极简：**用过去的"冲击平方"预测现在的方差**。一个大的 $|\varepsilon_{t-1}|$ 会通过 $\alpha_1\varepsilon_{t-1}^2$ 抬高 $\sigma_t^2$，于是下一期更可能出现大波动——波动聚集被直接写进方程。注意 $\varepsilon_t$ 本身仍是不可预测的零均值白噪声（因 $z_t$ 独立），可预测的是它的**幅度**。这正是本章开头"方向不可预测、大小可预测"的数学表达。

**例 15.1（统一案例：残差平方的自相关）** 取第 12 章 $\text{ARIMA}(1,1,1)(0,1,1)_7$ 拟合负荷后的残差 $\hat\varepsilon_t$，作 Ljung–Box 检验：残差本身 $Q(12)$ 的 $p=0.42$（已无均值相关），但**残差平方** $\hat\varepsilon_t^2$ 的 $Q(12)$ 的 $p=0.003$，强烈自相关。这就是 ARCH 效应的标准诊断[1]：均值已被榨干，方差里还剩可提取的结构。若忽略它，第 12 章给出的预测区间会因常方差假设而"在平静期过宽、在剧烈期过窄"，覆盖率失真——第 38 章的区间校准检验正是为此而设。对这样的残差，一个 ARCH(1) 拟合得 $\hat\omega=0.018,\hat\alpha_1=0.34$，说明约三分之一的上期冲击平方会传导到本期方差。

ARCH($q$) 的平稳性要求 $\sum_i\alpha_i<1$，此时无条件方差为 $\omega/(1-\sum\alpha_i)$。它的主要缺陷是**参数不经济**：要捕捉持续很久的波动记忆，往往需要很大的 $q$（如 $q=20$ 以上），既难估计又易违反非负约束。这直接催生了 GARCH。

## 15.2　GARCH 模型、平稳性与无条件方差

Bollerslev 的关键一步[2] 是在式 (15-1) 中加入**方差自身的滞后**，用少量参数获得长记忆。

**定义 15.2（GARCH($p,q$) 模型）**

$$
\sigma_t^2 = \omega + \sum_{i=1}^{q}\alpha_i\,\varepsilon_{t-i}^2 + \sum_{j=1}^{p}\beta_j\,\sigma_{t-j}^2, \qquad \omega>0,\ \alpha_i,\beta_j\ge0. \tag{15-2}
$$

最常用的是 GARCH(1,1)：$\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2$。它等价于一个关于 $\varepsilon_t^2$ 的 ARMA：$\varepsilon_t^2=\omega+(\alpha+\beta)\varepsilon_{t-1}^2+w_t-\beta w_{t-1}$（其中 $w_t=\varepsilon_t^2-\sigma_t^2$ 为鞅差），故 GARCH(1,1) 可视为"平方残差的 ARMA(1,1)"——这解释了它为何用一个 $\alpha$、一个 $\beta$ 就能刻画 ARCH($\infty$) 的长记忆[2]。

**定理 15.1（GARCH(1,1) 的平稳性与无条件方差）** 若 $\alpha+\beta<1$，则 $\varepsilon_t$ 协方差平稳，且

$$
\bar\sigma^2=\mathbb{E}[\sigma_t^2]=\frac{\omega}{1-\alpha-\beta}. \tag{15-3}
$$

**推导。** 把 $\varepsilon_{t-1}^2=\sigma_{t-1}^2 z_{t-1}^2$ 代入式 (15-2) 并取条件期望，利用 $\mathbb E[z_{t-1}^2]=1$：

$$
\mathbb E[\sigma_t^2]=\omega+\alpha\,\mathbb E[\varepsilon_{t-1}^2]+\beta\,\mathbb E[\sigma_{t-1}^2]=\omega+(\alpha+\beta)\mathbb E[\sigma_{t-1}^2].
$$

这是关于 $v_t=\mathbb E[\sigma_t^2]$ 的一阶线性递推 $v_t=\omega+(\alpha+\beta)v_{t-1}$，收敛当且仅当 $|\alpha+\beta|<1$，稳态解 $v^*=\omega+(\alpha+\beta)v^*$ 即式 (15-3)。$\gamma=\alpha+\beta$ 称**持续性**（persistence）：越接近 1，冲击消退越慢。当 $\gamma=1$ 时为 **IGARCH**（单整 GARCH），冲击永久不衰，$\bar\sigma^2$ 不存在；$\gamma>1$ 则方差爆炸、非平稳。

四阶矩存在还需更强条件。Bollerslev[3] 证明当 $z_t\sim N(0,1)$ 且 $(\alpha+\beta)^2+2\alpha^2<1$ 时，$\varepsilon_t$ 的峰度为

$$
\kappa_\varepsilon = 3\,\frac{1-(\alpha+\beta)^2}{1-(\alpha+\beta)^2-2\alpha^2} > 3, \tag{15-4}
$$

即 GARCH 即使在正态新息下也能产生**厚尾**——典型事实②被内生地解释，而无须假设 $z_t$ 本身厚尾。这是 GARCH 相对常方差正态模型最漂亮的性质之一。

**例 15.2（统一案例：GARCH(1,1) 的稳态与半衰期）** 对负荷残差拟合 GARCH(1,1) 得 $\hat\omega=0.05,\hat\alpha=0.10,\hat\beta=0.85$（$\gamma=0.95$）。由式 (15-3)，无条件方差 $\bar\sigma^2=0.05/(1-0.95)=1.00$，即长期日均波动为 1 个单位。持续性 0.95 对应的**半衰期**为 $\ln(0.5)/\ln(\gamma)\approx(-0.693)/(-0.0513)\approx13.5$ 期，即一次冲击约需两周才衰减一半，与盛夏高温过程的时间尺度相符。由式 (15-4)，$(\alpha+\beta)^2+2\alpha^2=0.9025+0.02=0.9225<1$，四阶矩存在，$\kappa_\varepsilon=3(1-0.9025)/(1-0.9225)=3\times0.0975/0.0775\approx3.77>3$，厚尾成立。再看逐期递推：设 $\sigma_1^2=\bar\sigma^2=1$，某日出现大残差 $\varepsilon_1^2=2.0$，则 $\sigma_2^2=0.05+0.10\times2.0+0.85\times1.0=1.10$；若次日 $\varepsilon_2^2=1.1$，$\sigma_3^2=0.05+0.11+0.85\times1.10=1.095$——方差被冲击抬高后缓慢回落，正是波动聚集。图 15-1 展示这一递推与残差序列。

> 【图 15-1　GARCH 波动率与波动聚集】（原图见 `figures/图15-1.png`）：上图绘制一段模拟/实际残差序列（大幅波动成簇出现），下图叠加对应的条件标准差 $\sigma_t$ 曲线与无条件波动水平线，标注一次大冲击后的指数衰减。

![图 15-1　GARCH 波动率与波动聚集](figures/图15-1.png)

## 15.3　非对称变体：杠杆效应与灵活形式

标准 GARCH 中 $\sigma_t^2$ 只依赖 $\varepsilon_{t-1}^2$，故同等幅度的正、负冲击对波动影响相同，无法刻画典型事实③的**杠杆效应**。为此发展出一批非对称变体。

**EGARCH**（Nelson, 1991[4]）对**对数方差**建模，天然保证 $\sigma_t^2>0$、无需非负参数约束：

$$
\ln\sigma_t^2 = \omega + \beta\ln\sigma_{t-1}^2 + \theta\,\frac{\varepsilon_{t-1}}{\sigma_{t-1}} + \xi\left(\left|\frac{\varepsilon_{t-1}}{\sigma_{t-1}}\right|-\mathbb E|z|\right). \tag{15-5}
$$

其中 $\xi$ 捕捉幅度效应，$\theta$ 捕捉符号效应：若 $\theta<0$，负冲击（$\varepsilon_{t-1}<0$）比对等正冲击更抬升方差，即杠杆效应。

**GJR-GARCH**（Glosten 等, 1993[5]）用示性函数直接给负冲击加一项：

$$
\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\lambda\,\mathbf 1\{\varepsilon_{t-1}<0\}\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2, \tag{15-6}
$$

$\lambda>0$ 时坏消息的有效系数为 $\alpha+\lambda$、好消息为 $\alpha$。其平稳条件为 $\alpha+\beta+\lambda/2<1$（对对称新息）。**TGARCH**[6] 用阈值形式对 $|\varepsilon_{t-1}|$ 而非 $\varepsilon_{t-1}^2$ 建模，思路相近。此外 **GARCH-M**[7] 把 $\sigma_t$ 或 $\ln\sigma_t^2$ 放进均值方程，刻画"风险越高、要求回报越高"；**FIGARCH**[13] 用分数差分刻画波动的长记忆；**APARCH** 则把幂次与杠杆统一为一个灵活族。表 15-1 汇总。

**表 15-1　GARCH 主要变体对照**

| 模型 | 建模对象 | 关键新增项 | 针对的典型事实 | 出处 |
|------|----------|------------|----------------|------|
| GARCH(1,1) | $\sigma_t^2$ | $\beta\sigma_{t-1}^2$ | 波动聚集、长记忆 | [2] |
| EGARCH | $\ln\sigma_t^2$ | 符号项 $\theta z_{t-1}$ | 杠杆、无需非负约束 | [4] |
| GJR-GARCH | $\sigma_t^2$ | $\lambda\mathbf 1\{\varepsilon<0\}\varepsilon^2$ | 杠杆 | [5] |
| TGARCH | $\sigma_t$ | 阈值绝对值 | 杠杆、稳健 | [6] |
| GARCH-M | 均值方程 | $\delta\sigma_t$ | 风险—收益权衡 | [7] |
| IGARCH | $\sigma_t^2$ | $\alpha+\beta=1$ | 冲击永久持续 | [2] |
| FIGARCH | $\sigma_t^2$ | 分数差分 $(1-B)^d$ | 波动长记忆 | [13] |

**例 15.3（负荷残差里也存在"非对称"）** 直觉上杠杆效应是金融现象，但负荷残差同样有非对称：气温骤升带来的**正向**残差（负荷远高于预测）比同等幅度的负向残差更抬升后续波动，因为高温往往持续数日、伴随空调负荷的累计不确定。对统一案例拟合 GJR-GARCH 得 $\hat\lambda=-0.06$（负值、方向与股市相反），似然比检验相对标准 GARCH 显著（$p=0.02$）。这个例子说明：**非对称的方向由领域机制决定，不应照搬金融先验**；模型形式（15-5）(15-6) 是通用的，杠杆项的符号与大小须由数据估计。

## 15.4　估计、诊断与多步波动率预测

GARCH 族通常用**准极大似然（QMLE）**估计[9]：即便 $z_t$ 并非正态，在高斯似然下最大化仍可得到一致渐近正态的估计量（Bollerslev–Wooldridge 稳健标准误修正）。均值方程与方差方程联合的对数似然为

$$
\log L=-\frac12\sum_{t=1}^{T}\Big(\log 2\pi+\log\sigma_t^2+\frac{\varepsilon_t^2}{\sigma_t^2}\Big), \tag{15-7}
$$

其中 $\sigma_t^2$ 由式 (15-2) 从初值递推，$\varepsilon_t$ 来自均值方程（如第 12 章 ARIMA）。若拒绝正态假设，可改用 Student-$t$ 或 GED 分布[3] 以更好拟合厚尾。

**诊断**与第 12 章同构但对象不同：对标准化残差 $\hat z_t=\hat\varepsilon_t/\hat\sigma_t$ 作 Ljung–Box 检验（应无均值相关），对 $\hat z_t^2$ 作 Ljung–Box 与 ARCH-LM 检验（应无剩余异方差）；若 $\hat z_t^2$ 仍自相关，说明阶数不足或需非对称项。这一步与 12.5 节"残差须为白噪声"遥相呼应，只是把"榨干信息"从一阶推进到二阶。

**多步波动率预测**由递推取期望得到。由 $\sigma_{t+1}^2=\omega+\alpha\varepsilon_t^2+\beta\sigma_t^2$ 与 $\mathbb E_t[\varepsilon_{t+1}^2]=\sigma_{t+1}^2$，可证 $h$ 步预测

$$
\mathbb E_t[\sigma_{t+h}^2]=\bar\sigma^2+(\alpha+\beta)^{h-1}\big(\sigma_{t+1}^2-\bar\sigma^2\big), \tag{15-8}
$$

即波动率预测以几何速率 $\gamma=\alpha+\beta$ 从当前 $\sigma_{t+1}^2$ **指数回归长期均值** $\bar\sigma^2$。这与第 12 章式 (12-13) 均值预测趋于无条件均值完全平行，也再次印证第 4 章"可预测信息随时域耗散"：$\gamma$ 越接近 1，波动可预测的时域越长。对 IGARCH（$\gamma=1$），预测恒为 $\sigma_{t+1}^2$、不回归，须格外谨慎。

**例 15.4（统一案例：波动率预测与区间）** 沿用 $\omega=0.05,\alpha=0.10,\beta=0.85,\bar\sigma^2=1$，设今日 $\sigma_{t+1}^2=1.10$（受昨日大残差抬升）。由式 (15-8)，$\mathbb E_t[\sigma_{t+2}^2]=1+0.95\times0.10=1.095$，$\mathbb E_t[\sigma_{t+8}^2]=1+0.95^7\times0.10\approx1+0.0698=1.070$，逐步回落到 1。于是明日负荷的 95% 预测区间为 $\hat y\pm1.96\sqrt{1.10}\approx\hat y\pm2.06$，而按常方差 $\sigma^2=1$ 会给出 $\pm1.96$——在波动期低估约 5%。对极端日的风险准备而言，这一修正正是 GARCH 的工程价值。

## 15.5　随机波动率、风险度量与适用边界

GARCH 把 $\sigma_t^2$ 设为**过去观测的确定性函数**。另一条思路是把它设为**不可观测的随机过程**，即**随机波动率（SV）模型**[8]：

$$
\varepsilon_t = e^{h_t/2} z_t,\qquad h_{t+1}=\mu+\phi(h_t-\mu)+\eta_t,\quad \eta_t\sim N(0,\sigma_\eta^2). \tag{15-9}
$$

式 (15-9) 是一个非线性状态空间模型（$h_t$ 为隐状态），与第 13 章的语言直接相通；但它对观测非高斯、似然无闭式解（需对 $h_{1:T}$ 高维积分），估计须用 MCMC、粒子滤波[13.5 节]或重要性采样。SV 的优势是更灵活、对新息分布假设更弱，代价是计算重。金融高频数据还可用**已实现波动率**（realized volatility，由日内平方收益和构造）作为 $\sigma_t^2$ 的近似可直接观测代理[10]，把隐状态问题化为观测建模——这是与第 5 章重采样、第 25 章不规则采样相关的另一条路。

波动率预测最直接的落地是**风险度量**。设收益 $r_{t+1}=\mu+\varepsilon_{t+1}$，$\varepsilon_{t+1}=\sigma_{t+1}z_{t+1}$，则在正态新息下置信水平 $1-\alpha$ 的**风险价值**与**期望损失**为

$$
\mathrm{VaR}_\alpha=-\mu+\sigma_{t+1}\,z_{1-\alpha},\qquad
\mathrm{ES}_\alpha=-\mu+\sigma_{t+1}\,\frac{\phi(z_{1-\alpha})}{\alpha}, \tag{15-10}
$$

其中 $z_{1-\alpha}$ 为正态分位数、$\phi$ 为标准正态密度；ES（Expected Shortfall / CVaR）度量"突破 VaR 后平均损失多大"，是比 VaR 更审慎的一致性风险度量[11]。

**例 15.5（从波动率到风险数字）** 设某日 $\sigma_{t+1}=0.02$（2% 日波动）、$\mu=0$、$\alpha=0.01$（99% 置信），$z_{0.99}=2.326$。由式 (15-10)，$\mathrm{VaR}_{0.01}=2.326\times0.02=4.65\%$，$\mathrm{ES}_{0.01}=0.02\times\phi(2.326)/0.01\approx0.02\times0.0267/0.01=5.34\%$。可见 ES 比 VaR 高约 15%，捕捉了厚尾情形下的尾部平均损失。对电网而言，把 $\sigma_{t+1}$ 换成负荷预测误差的条件标准差，同法即可给出"备用容量应覆盖到多少分位"——这与第 14 章的层次调和、第 32 章的调度决策连成一条从二阶矩到决策的完整链。

**边界与讨论。** GARCH 族的优势是：以极少参数刻画波动聚集、厚尾与杠杆，给出可解释的持续性与半衰期，有成熟 QMLE 与诊断体系，是金融风险管理的工业标准。其边界有四：其一，**只建模条件方差**，对偏度、峰度的时变、跳跃与极端事件仍不充分，须结合第 24 章的概率生成模型与第 38 章的极值/共形方法；其二，**新息分布假设**影响 VaR/ES 精度，厚尾下须用 $t$/GED 或历史模拟；其三，**参数非负与平稳约束**较繁琐，EGARCH/SV 可缓解但估计更复杂；其四，**单变量、线性方差结构**，多变量波动（DCC、BEKK 等多元 GARCH）与第 10 章的协整、第 23 章的图依赖相关，本书不展开。还须提醒：GARCH 描述的是"波动可预测"，绝非"收益可预测"——方向仍是零均值白噪声，任何声称用 GARCH 预测价格方向的用法都是误读，这与第 4 章"相关性不等于可预测性、更不等于因果性"的清醒态度一致。

下一章转向另一条贯穿全书的主线：第 16 章把参数本身也视为随机变量，用贝叶斯范式统一结构时间序列的不确定性量化，并为第 24 章的深度概率预测铺路。

## 本章小结

本章把建模对象从条件均值推进到条件方差，建立了完整的条件异方差框架。15.1 节从波动聚集、厚尾、杠杆三组典型事实出发，用 ARCH($q$) (15-1) 说明"方向不可预测、幅度可预测"，并以统一案例残差平方的 Ljung–Box 检验（$p=0.003$）给出 ARCH 效应的标准诊断。15.2 节严格推导 GARCH(1,1)：由 $v_t=\omega+(\alpha+\beta)v_{t-1}$ 得平稳条件 $\alpha+\beta<1$ 与无条件方差 $\omega/(1-\alpha-\beta)$ (15-3)，由四阶矩条件得内生厚尾峰度 (15-4)，并以 $\gamma=0.95$ 的算例展示半衰期 13.5 期与冲击后的波动递推。

15.3 节用 EGARCH (15-5)、GJR-GARCH (15-6) 等刻画杠杆效应，表 15-1 汇总七类变体；例 15.3 提醒非对称方向由领域机制决定，负荷残差的"正向冲击更抬升波动"与股市相反。15.4 节给出 QMLE 似然 (15-7)、标准化残差诊断与多步波动预测 $\bar\sigma^2+\gamma^{h-1}(\sigma_{t+1}^2-\bar\sigma^2)$ (15-8)，证明波动预测指数回归长期均值，与第 12 章均值预测趋于无条件均值完全平行。15.5 节以 SV 状态空间视角交叉引用第 13 章，并由式 (15-10) 把波动率落到 VaR/ES，例 15.5 给出完整风险数字。

从理论主线看，本章是 L1 统计可预测性在二阶矩的延伸，突破了第 12 章 ARIMA 的常方差假设；其隐含线性方差结构与新息分布假设，则是它无法突破的边界。本章与全书：第 2、24 章提供概率评分与生成模型，第 12 章提供均值方程与残差，第 13 章提供 SV 的状态空间语言，第 35 章计量经济学视角给出学科定位，第 38 章提供区间校准与共形覆盖，第 39 章给出金融与能源专题应用。理解 GARCH，读者便掌握了"在均值已被榨干之后，如何从方差里继续提取可预测结构"这一重要能力。


从四问看，本章的 GARCH 利用 L1（统计）：假设方差随时间聚集、新息条件异方差；它突破了「均值已被榨干后无结构可挖」的盲区，仍受「分布假设与杠杆效应建模」的边界约束。

**进一步阅读**　本章建议延伸阅读的文献：[12]。

## 参考文献

[1] Engle R F. Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 1982, 50(4): 987–1007.

[2] Bollerslev T. Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 1986, 31(3): 307–327.

[3] Bollerslev T. A conditionally heteroskedastic time series model for speculative prices and rates of return. *The Review of Economics and Statistics*, 1987, 69(3): 542–547.

[4] Nelson D B. Conditional heteroskedasticity in asset returns: A new approach. *Econometrica*, 1991, 59(2): 347–370.

[5] Glosten L R, Jagannathan R, Runkle D E. On the relation between the expected value and the volatility of the nominal excess return on stocks. *The Journal of Finance*, 1993, 48(5): 1779–1801.

[6] Zakoian J M. Threshold heteroskedastic models. *Journal of Economic Dynamics and Control*, 1994, 18(5): 931–955.

[7] Engle R F, Lilien D M, Robins R P. Estimating time varying risk premia in the term structure: The ARCH-M model. *Econometrica*, 1987, 55(2): 391–407.

[8] Taylor S J. *Modelling Financial Time Series*. 2nd ed. Singapore: World Scientific, 2008.

[9] Bollerslev T, Wooldridge J M. Quasi-maximum likelihood estimation and inference in dynamic models with time-varying covariances. *Econometric Reviews*, 1992, 11(2): 143–172.

[10] Andersen T G, Bollerslev T, Diebold F X, Labys P. Modeling and forecasting realized volatility. *Econometrica*, 2003, 71(2): 579–625.

[11] Jorion P. *Value at Risk: The New Benchmark for Managing Financial Risk*. 3rd ed. New York: McGraw-Hill, 2006.

[12] Tsay R S. *Analysis of Financial Time Series*. 3rd ed. Hoboken: Wiley, 2010.

[13] Baillie R T, Bollerslev T, Mikkelsen H O. Fractionally integrated generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 1996, 74(1): 3–30.
