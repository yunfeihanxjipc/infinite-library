# 第 12 章　Dreamer 系列：基于模型的强化学习

第 11 章的 PlaNet 在潜在空间中在线规划，但每一决策步都要运行 CEM 搜索，计算昂贵。本章介绍 Dreamer 系列[1][2][3]——它用 RSSM 学到的潜在动力学**生成想象轨迹**，在想象中训练「演员—评论家」（actor–critic）策略，把规划的成本分摊到一次性的策略学习中。Dreamer 是基于模型强化学习（MBRL）的高峰：部署时只需一次策略前向传播即可输出动作，却在样本效率与最终性能上都能媲美甚至超越无模型方法。

本章先阐述从在线规划到想象训练的范式转变（12.1 节），再推导潜在想象与 $\lambda$-return、演员—评论家更新（12.2 节），用数值算例展示回报估计与策略梯度（12.3 节），梳理 V2/V3 的改进技术（12.4 节），分析样本效率与七要素覆盖（12.5 节），最后讨论边界并收束（12.6 节）。

## 12.1　动机：从规划时计算到训练时计算

PlaNet 的在线 CEM 规划有一个根本的不对称：模型训练时花费大量计算，但**每次决策又重新花一遍规划计算**。能否把这些规划计算「提取」成一个策略，以后直接查表式地输出动作？Dreamer 的回答是肯定的。

关键转变如下：不再在每一步用 CEM 现搜动作序列，而是在潜在空间中**想象**出多条 $H$ 步轨迹——从真实状态出发，用当前策略 $\pi_\phi(a_t\mid z_t)$ 采样动作、用 RSSM 转移滚动出未来状态与奖励——然后用这些想象轨迹训练一个价值网络（评论家）与一个策略网络（演员）。训练完成后，部署时直接由策略输出动作，无需任何在线搜索。这把「规划时计算」转成了「训练时计算」：推理极快，代价是训练阶段要生成大量想象数据。

**直觉解释。** PlaNet 像一位每走一步都要重新推演全局的棋手；Dreamer 则像一位先在脑海里把成千上万盘棋下完、把经验内化成直觉的棋手——后者对局时落子如飞。想象轨迹就是「脑海中对局」，演员—评论家就是内化出的「棋感」。

## 12.2　潜在想象与演员—评论家

**想象轨迹的生成。** 从重放缓冲中采样真实状态 $s_t=(h_t,z_t)$，用策略采样动作 $a_t\sim\pi_\phi(\cdot\mid s_t)$，再用 RSSM 的转移 $h_{\tau+1}=\mathrm{GRU}(h_\tau,z_\tau,a_\tau)$、$z_{\tau+1}\sim p_\psi(z_{\tau+1}\mid h_{\tau+1})$ 滚动，得到想象序列

$$
\hat s_t,\hat a_t,\hat r_{t+1},\hat s_{t+1},\hat a_{t+1},\dots,\hat r_{t+H},\hat s_{t+H}. \tag{12-1}
$$

注意在想象步里只用先验 $p_\psi(z\mid h)$，没有真实观测——这正是第 11 章 RSSM「可想象」性质的用武之地。奖励由模型预测 $\hat r_{\tau}\sim p_\theta(r_\tau\mid h_\tau,z_\tau)$。

**$\lambda$-return 回报估计。** 评论家要估计每个想象状态的价值。Dreamer 使用 $\lambda$-return——TD（$\lambda$）在想象轨迹上的截断形式，在偏差与方差间折中：

$$
R_t^{\lambda}=(1-\lambda)\sum_{n=1}^{H-1}\lambda^{n-1}V_n+\lambda^{H-1}V_H,\qquad V_n=\sum_{k=n}^{H}\gamma^{k-n}\hat r_k+\gamma^{H-n+1}V_\psi(\hat s_H). \tag{12-2}
$$

这里 $V_n$ 是从第 $n$ 步到轨迹末尾的折扣奖励与引导价值之和；$V_\psi(\hat s_H)$ 是价值网络对轨迹末端的估计（bootstrap）。$\lambda=1$ 时退化为完整蒙特卡洛回报（低偏差高方差），$\lambda=0$ 时为一步 TD（高偏差低方差），取中间值折中。原工作常用 $\lambda=0.95$、$H=15$。

**演员—评论家更新。** 评论家（价值网络）$V_\psi$ 用回归拟合 $\lambda$-return，最小化

$$
\mathcal{L}_V=\mathbb{E}_{\hat s_t}\Big[\big(V_\psi(\hat s_t)-\mathrm{sg}(R_t^{\lambda})\big)^2\Big], \tag{12-3}
$$

其中 $\mathrm{sg}$ 为 stop-gradient。演员（策略网络）$\pi_\phi$ 则最大化价值。难点在于动作是采样得到的，梯度无法穿过采样。Dreamer 用**重参数化**把策略写成 $a_t=\tanh\!\big(\mu_\phi(s_t)+\sigma_\phi(s_t)\odot\epsilon\big)$、$\epsilon\sim\mathcal{N}(0,\mathbf{I})$，使梯度可从价值经动作回传到 $\phi$（DreamerV2 进一步用离散类别采样 + straight-through 梯度）。演员目标为

$$
\mathcal{L}_\pi=-\mathbb{E}_{\hat s_t,\epsilon}\big[R_t^{\lambda}\big], \tag{12-4}
$$

即沿「让想象回报变大」的方向更新策略。价值梯度 $\nabla_{s}V_\psi$ 通过可微的 RSSM 一路回传到策略，形成「世界模型引导的策略改进」。

> 【图 12-1　Dreamer 系列架构】（原图见 figures/图12-1.png）：RSSM 学潜在动力学 → 生成想象轨迹 → $\lambda$-return 估计 → 训练评论家 $V_\psi$ 与演员 $\pi_\phi$，策略动作回流到 RSSM 形成闭环。
>
> ![图 12-1　Dreamer 系列架构](figures/图12-1.png)

### 12.2A　想象轨迹的逐步数值：一次 rollout 如何喂饱两个网络

例 12.1 给了 $\lambda$-return 的算例，这里把「从真实状态出发、用策略 + RSSM 滚出想象序列」这条流水线展开成逐步数字，看清演员与评论家各拿到什么。

**设定（数值）。** 从重放缓冲采一个真实状态 $(h_t,z_t)$，策略 $\pi_\phi$ 在 $s_t$ 处采样 $a_t=0.3$（设 $\mu_\phi=0.3,\sigma_\phi=0.1,\epsilon=0$ 取均值动作），RSSM 用先验 $p_\psi$ 与 GRU 向前滚动，视野 $H=4$、$\gamma=0.99$。

**逐步滚动。**

| $\tau$ | $a_\tau$（策略采样） | $\hat z_\tau$（先验采样，示意） | $\hat r_\tau$（模型奖励） | $\hat s_\tau=(h_\tau,z_\tau)$ |
|--------|------------------|------------------------------|----------------------|---------------------------|
| $t$   | $0.30$ | $(0.60,-0.10)$ | $1.0$ | 真实状态（锚点） |
| $t+1$ | $0.28$ | $(0.55,-0.05)$ | $1.0$ | 先验生成 |
| $t+2$ | $0.31$ | $(0.58, 0.02)$ | $2.0$ | 先验生成 |
| $t+3$ | $0.25$ | $(0.45,-0.08)$ | $5.0$ | 先验生成 |

每一步：演员给出 $a_\tau$，RSSM 的 GRU 用 $a_\tau$ 更新 $h_{\tau+1}$、先验采样 $\hat z_{\tau+1}$，解码器/奖励头从 $(h_{\tau+1},\hat z_{\tau+1})$ 出 $\hat r_{\tau+1}$。**注意全程没有真实观测**——这正是 11.2A 节「想象模式」（式 11-4）的直接应用，也是 RSSM「可想象」性质的用武之地。

**两个网络各拿到什么。** 这条 $H=4$ 的想象轨迹，评论家拿到 $\{(\hat s_\tau,\ \text{目标}=\lambda\text{-return})\}_{\tau=t}^{t+H-1}$ 四个训练对，用式 (12-3) 回归；演员拿到同一批 $\hat s_\tau$ 与对应的 $\hat r$，用式 (12-4) 沿增大回报方向更新 $\mu_\phi,\sigma_\phi$。**关键点**：两个网络的训练数据全部来自模型（RSSM）而非真实环境——真实状态 $(h_t,z_t)$ 只是「起点锚点」，其余 $H-1$ 步全是想象。这就是「用计算换数据」的微观机制：每采 1 个真实状态，可展开 $H=4$ 步（实际训练中常 $H=15$）的想象经验，数据利用率被放大了 $H$ 倍。而 12.3 例 12.2 报告的「样本效率高 10 倍」，本质是 $H$（想象长度）与「真实帧数 / 无模型所需帧数」两个倍数的乘积——模型越准、$H$ 越长，放大倍数越大，直到被模型误差累积（12.6 节）封顶。

## 12.3　带数值的算例：回报估计与策略更新

**例 12.1（$\lambda$-return 的逐步数值）** 设想象视野 $H=4$，折扣 $\gamma=0.99$，$\lambda=0.95$，价值网络对末端估计 $V_\psi(\hat s_4)=10$，模型预测的即时奖励为 $\hat r_1=1,\hat r_2=1,\hat r_3=2,\hat r_4=5$。先算各 $V_n$：

$V_4=\hat r_4+\gamma^0 V_\psi(\hat s_4)=5+10=15$；
$V_3=\hat r_3+\gamma\hat r_4+\gamma V_\psi(\hat s_4)=2+0.99\times5+0.99\times10=2+4.95+9.9=16.85$；
$V_2=1+0.99\times2+0.99^2\times5+0.99^2\times10\approx1+1.98+4.90+9.80=17.68$；
$V_1=1+0.99\times1+0.99^2\times2+0.99^3\times5+0.99^3\times10\approx1+0.99+1.96+4.85+9.71=18.51$。

再算 $R_1^{\lambda}=(1-\lambda)V_1+\lambda(1-\lambda)V_2+\lambda^2(1-\lambda)V_3+\lambda^3 V_4$。代入 $\lambda=0.95$：$0.05\times18.51+0.95\times0.05\times17.68+0.95^2\times0.05\times16.85+0.95^3\times15\approx0.926+0.840+0.760+12.857=15.38$。评论家把 $V_\psi(\hat s_1)$ 往 15.38 回归；演员则沿增大该回报的方向调整 $\mu_\phi,\sigma_\phi$。

**例 12.2（Atari 上的样本效率）** DreamerV2 直接从像素学习，在 55 个 Atari 游戏上达到人类水平中位数；相比无模型方法（如 IQN）需要约 1 亿帧环境交互，DreamerV2 在约 1000 万帧（1/10 数据量）即达到相当表现。原因正如本节所述：世界模型让智能体在想象中「练习」了大量经验——每一帧真实数据可支撑几百步想象 rollout，相当于把数据利用率放大了几十倍。

> 【图 12-2　MBRL 样本效率对比】（原图见 figures/图12-2.png）：横轴环境交互帧数、纵轴人类归一化得分，Dreamer 曲线在远少于无模型方法的帧数下达到高分。
>
> ![图 12-2　MBRL 样本效率对比](figures/图12-2.png)

### 12.3A　重参数化策略梯度的数值：世界模型如何「引导」策略改进

例 12.1 展示了评论家的回归，这里把演员的「沿增大回报方向更新」算成具体梯度，看清世界模型（RSSM）如何把梯度「引导」回策略。设 1 维动作、策略 $a_t=\tanh(\mu_\phi(s_t)+\sigma_\phi(s_t)\epsilon)$、$\epsilon=0$（取均值动作），评论家价值 $V_\psi$，RSSM 可微。

**设定（数值）。** $\mu_\phi=0.3,\sigma_\phi=0.1$，故 $a=\tanh(0.3)\approx0.291$。在想象状态 $\hat s_t$ 处，$\lambda$-return 目标 $R_t^\lambda=15.38$（例 12.1），评论家当前估计 $V_\psi(\hat s_t)=14.0$，故价值残差 $R_t^\lambda-V_\psi\approx1.38$（策略把回报「抬高」了）。设 $\partial V_\psi/\partial a\big|_{\hat s_t}=+0.8$（动作越大、价值越高——合理：更用力的动作带来更多奖励）。

**链式梯度。** 由 $\mathcal{L}_\pi=-\mathbb{E}[R_t^\lambda]$，重参数化下

$$
\frac{\partial \mathcal{L}_\pi}{\partial \mu_\phi}=-\frac{\partial V_\psi}{\partial a}\cdot\frac{\partial a}{\partial \mu_\phi}=-0.8\times\big(1-a^2\big)=-0.8\times(1-0.291^2)=-0.8\times0.915\approx-0.73. \tag{12-5}
$$

$\partial a/\partial\mu_\phi=1-\tanh^2(\mu)=1-a^2\approx0.915$（$\tanh$ 的导数）。负号说明 $\mu_\phi$ 应**增大**（梯度下降方向），把动作推得更用力、回报更高。$\sigma_\phi$ 的梯度类似地经 $\epsilon$ 回传，此处 $\epsilon=0$ 故 $\partial a/\partial\sigma_\phi=\epsilon(1-a^2)=0$，本步不动方差。

**世界模型的「引导」作用。** 注意 $\partial V_\psi/\partial a$ 来自评论家，而评论家本身是在 RSSM 生成的想象轨迹上训练（12.2A）——**梯度能一路回传到 RSSM 是因为整个想象链可微**。若用离散采样（无重参数化），$\partial a/\partial\mu_\phi$ 无法解析求出，只能用 REINFORCE 的高方差估计；DreamerV2 进一步用离散类别 + straight-through 来兼顾表达力与梯度。这个 $-0.73$ 的梯度把「世界模型（RSSM 给出未来）→ 评论家（估计未来价值）→ 策略（朝高价值方向走）」串成一条可微链——这正是第 12.1 节「世界模型引导的策略改进」的数值体现，也是 Dreamer 能在像素输入下高效学习的关键：**想象轨迹让策略梯度有了「来自模型的未来信息」**，而非只靠真实环境的稀疏奖励。

## 12.4　DreamerV2 / V3 的关键改进

Dreamer 系列三篇论文构成一个清晰的递进（表 12-1）。

**表 12-1　Dreamer 系列演进**

| 版本 | 核心改进 | 关键收益 |
|------|---------|---------|
| DreamerV1[1] | RSSM + 想象 + $\lambda$-return | 像素输入下样本效率突破 |
| DreamerV2[2] | 离散类别潜在 + KL 平衡 | Atari 达人类水平 |
| DreamerV3[3] | symlog 归一化 + 鲁棒超参 + 免费比特 | 单一超参跨域稳健 |

**DreamerV2——离散潜在。** 把连续高斯潜在换成 32 个类别变量（每个取 32 类），用 straight-through 梯度训练。离散潜在表达力更强（能表示多峰、组合结构），且天然适配 Atari 等离散域。同时改进 KL 平衡（每个类别的 KL 独立设最小阈值，即「免费比特」），防止表示塌缩（第 13 章详述）。

**DreamerV3——鲁棒性工程。** 三项关键创新：① **symlog 变换**——对奖励、价值等尺度差异巨大的量做 $\mathrm{symlog}(x)=\mathrm{sign}(x)\ln(1+|x|)$ 变换后训练，再 symexp 还原，使同一套超参能适配从 ±1 的小奖励到上千的大奖励；② **两层价值归一化**——价值与回报都做归一化以稳定训练；③ **固定超参**——不再针对每个任务调参，在 150+ 任务（Atari、DMC、Minecraft 等）上用同一组超参取得稳健表现。DreamerV3 还展示了在 Minecraft 中从零「挖钻石」这一长程任务上的能力，是长视野世界模型驱动的标志性成果。

### 12.4A　symlog 的数值：同一组超参为何能跨量级稳健

DreamerV3 的「固定超参跨 150+ 任务」靠的核心是 symlog 变换把「尺度」从优化问题里剥离。一个数值算例能看清。设某任务奖励量级 $\approx\pm1$（如 DMC 的连续控制），另一任务奖励量级 $\approx\pm1000$（如某些 Atari 或 Minecraft 的长程回报）。若直接训练，价值网络的输出尺度、损失权重、学习率必须随任务调整——这是 DreamerV1/V2 需要逐任务调参的根源。

**symlog 的压缩效应。** $\mathrm{symlog}(x)=\mathrm{sign}(x)\ln(1+|x|)$ 把不同量级压到相近区间：$\mathrm{symlog}(1)=\ln2\approx0.69$、$\mathrm{symlog}(10)\approx2.40$、$\mathrm{symlog}(100)\approx4.61$、$\mathrm{symlog}(1000)\approx6.91$。注意从 $1\to1000$（$1000$ 倍）只变成 $0.69\to6.91$（约 $10$ 倍），而对负值 $\mathrm{symlog}(-1000)=-6.91$。于是无论原始奖励是 $\pm1$ 还是 $\pm1000$，变换后的价值都落在 $\approx\pm7$ 的窄区间内，**价值网络的参数尺度、损失大小、学习率可以共用一套**——symlog 把「任务间的尺度差异」压掉了 $90\%$。训练完成后再用 $\mathrm{symexp}(x)=\mathrm{sign}(x)(e^{|x|}-1)$ 还原回原尺度做决策。

**数值验证。** 取 $x\in\{1,10,100,1000\}$，$\mathrm{symlog}$ 后 $\approx\{0.69,2.40,4.61,6.91\}$，值域宽度 $6.22$；若不变换，值域宽度 $999$——**symlog 把值域压窄了约 $160$ 倍**。这就是「同一组超参能跨量级稳健」的定量解释：网络只需拟合 $\approx\pm7$ 的窄带，而非随任务漂移 $\pm1$ 到 $\pm1000$。这个技巧与第 12.5 节「样本效率」相互支撑——V3 的固定超参降低了每个新任务的调参成本，使「像素输入 + 想象训练」的范式能规模化到 150+ 任务而不崩。

**技术谱系位置。** Dreamer 继承 PlaNet 的 RSSM 表示（第 11、13 章），与 MuZero[5] 同属「潜在空间规划/学习」路线，但 Dreamer 用想象轨迹训练显式策略，而 MuZero 用 MCTS 在线规划。二者代表了「训练时计算」与「规划时计算」的两种取舍。

## 12.5　样本效率、七要素与定位

**七要素覆盖。** Dreamer 具备全部七要素，是「完整世界模型」的代表（表 12-2）：RSSM 的 $h_t,z_t$ 给出状态表示（E1）与随机性（E4），GRU + 先验给出转移（E2），解码器给出观测生成（E3），动作条件化的转移（E5），奖励模型（E6），以及想象中训练的演员—评论家策略（E7）。

**表 12-2　Dreamer 与 PlaNet 对照**

| 方面 | PlaNet | Dreamer |
|------|--------|---------|
| 决策方式 | 在线 CEM 规划 | 学到的策略网络 |
| 想象用途 | 规划时生成候选 | 训练时生成经验 |
| 推理成本 | 高（每步搜索） | 低（一次前向） |
| 训练成本 | 中 | 高（大量想象 rollout） |
| 扩展性 | 中 | 强（V3 跨域稳健） |

**为什么样本效率高？** 真实交互只用于学世界模型（少量数据即可），策略改进几乎全在想象中完成（数据可无限生成）。这是一种「用计算换数据」的策略：在世界模型足够准的前提下，计算便宜、数据昂贵，则用想象计算替代真实交互。

## 12.6　边界与讨论

Dreamer 的局限集中在「模型误差」这一根本软肋。① **策略利用模型偏差**：策略在想象中会发现并利用模型的漏洞（在自己「做梦」的虚假状态里拿高分），部署到真实环境即失效——这被称为策略利用/模型利用（第 24 章）。② **长视野误差累积**：想象轨迹越长，$H$ 步滚动的复合误差越大，$\lambda$-return 基于失真未来估计，价值与策略被带偏（第 33 章）。③ **依赖足够真实的学模数据**：若真实交互不足以覆盖关键情形，模型本身就不准，想象越练越错。

缓解方向包括：模型集成（用多个模型的分歧度量不确定性）、对环境扰动鲁棒的训练、限制想象视野、以及显式建模认知不确定性（第 24 章）。这些局限并不否定 Dreamer 的价值，而是划定了「基于模型学习」的适用边界：世界模型必须是足够忠实的模拟器，想象训练才有意义。这些辨析衔接第 9—13、24、25、33、36 章。

## 本章小结

本章介绍 Dreamer 系列——用想象轨迹训练演员—评论家策略的基于模型强化学习。

我们首先给出动机：把 PlaNet 的「规划时计算」前移为「训练时计算」，换取极低的推理成本（12.1 节）。接着推导想象轨迹生成（式 12-1）与 $\lambda$-return（式 12-2）、评论家回归损失（式 12-3）与演员重参数化策略梯度（式 12-4），并用逐步数值算例展示回报估计（例 12.1），用 Atari 案例说明样本效率（例 12.2）（12.3 节）。随后梳理 V1→V2（离散潜在）→V3（symlog 与鲁棒超参）的改进（表 12-1），确认 Dreamer 覆盖全部七要素（表 12-2）。

新增的三处数值把 Dreamer 的机制算到了可验证的量级：12.2A 节把一次想象 rollout 展开成逐步表格（$H=4$，$a$、$\hat z$、$\hat r$ 逐步滚动），说明真实状态只是「起点锚点」、其余 $H-1$ 步全是想象，把「每 1 个真实状态放大 $H$ 倍经验」的微观机制与例 12.2 的「样本效率高 10 倍」连成一条账；12.3A 节用重参数化链式梯度（式 12-5）算出 $\partial\mathcal{L}_\pi/\partial\mu_\phi\approx-0.73$，揭示「世界模型（RSSM）→ 评论家 → 策略」是一条可微链，想象轨迹给策略梯度提供了「来自模型的未来信息」，这正是「世界模型引导的策略改进」的数值体现；12.4A 节用 symlog 的数值（$\mathrm{symlog}(1)=0.69$ 到 $\mathrm{symlog}(1000)=6.91$，值域压窄约 $160$ 倍）解释 V3 固定超参为何能跨 $\pm1$ 到 $\pm1000$ 量级稳健——symlog 把任务间尺度差异压掉了 $90\%$。

我们还明确边界：策略利用模型偏差、长视野误差累积、依赖真实学模数据。这些辨析衔接第 9—13、24、25、33、36 章。

下一章回到表征本身，深入剖析 RSSM 为何要分为确定性与随机两部分，以及其可辨识性问题。

**进一步阅读**　本章建议延伸阅读的文献：[1]、[2]、[3]。

## 参考文献

[1] Hafner D, Lillicrap T, Ba J, Norouzi M. Dream to control: Learning behaviors by latent imagination. *ICLR*, 2020.

[2] Hafner D, Lillicrap T, Ba J, Norouzi M. Mastering Atari with discrete world models. *ICLR*, 2021.

[3] Hafner D, Pasukonis J, Ba J, et al. Mastering diverse domains through world models. *Nature*, 2023, 615: 58–64.

[4] Sutton R S, Barto A G. *Reinforcement Learning: An Introduction*. 2nd ed. MIT Press, 2018.

[5] Schrittwieser J, Antonoglou I, Hubert T, et al. Mastering Atari, Go, chess and shogi by planning with a learned model. *Nature*, 2020, 588: 604–609.

[6] Levine S, Kumar A, Tucker G, Fu J. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. *arXiv:2005.01643*, 2020.

[7] Janner M, Fu J, Zhang M, Levine S. When to trust your model: Model-based policy optimization. *NeurIPS*, 2019.

[8] Kuramochi T, Han W D. Learning action-conditioned world models for exploration. *NeurIPS Workshop*, 2020.
