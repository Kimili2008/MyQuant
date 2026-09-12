# 20-Day Oxford Quant-First Sprint

> 使用这份清单替代 30 天版本。原则：先保证基础、一个可复现量化项目、一个衍生品项目和一份可讲清楚的 stock pitch；所有 optional 内容都暂时跳过。

## 每日节奏

- [ ] 3h 数学 / 概率 / timed questions
- [ ] 2h Python /
- [ ] pandas / coding exercises
- [ ] 2h 金融基础 / 期权 / 估值
- [ ] 4h 当天项目交付
- [ ] 1h 英文表达、market journal 或面试复盘

如果当天项目卡住，不要牺牲睡眠去补 12 小时；优先完成当天的最小交付物。

## Day 1–3：笔试基础与环境

### Day 1

- [ ] Oxford Probability：conditional probability、expectation、variance
- [ ] 完成 20 道概率 / Bayes / expectation 题
- [ ] pandas：读取价格数据、处理日期、计算 daily return
- [ ] 读懂两个项目 README 和测试文件
- [ ] 产出：一页公式笔记 + 150 词英文 `Why quantitative finance?`

### Day 2

- [ ] Oxford Probability：distributions、independence、CLT intuition
- [ ] 完成 20 道 timed probability / estimation 题
- [ ] pandas：rolling mean、rolling volatility、groupby、缺失值
- [ ] 产出：一个计算 volatility、Sharpe、max drawdown 的 notebook 或脚本

### Day 3

- [ ] MIT 18.642：returns、portfolio、risk、no-arbitrage 基础
- [ ] 完成 15 道金融题：payoff、put-call parity、bond yield、EV/equity value
- [ ] 90 分钟混合 mock；逐题写错因
- [ ] 产出：个人错题表和 finance formula sheet

## Day 4–10：旗舰 ETF Momentum 项目

### Day 4

- [ ] 阅读 `momentum_research/README.md` 和 `src/data.py`
- [ ] 自己解释 12–1 signal、rebalancing、transaction cost
- [ ] 下载或读取缓存数据并画出 3 只 ETF 的价格 / return 图
- [ ] 产出：数据字典和研究问题说明

### Day 5

- [ ] 阅读并逐函数解释 `src/strategy.py`
- [ ] 手算一个调仓日的 signal 和权重
- [ ] 运行现有单元测试
- [ ] 产出：一页 execution-timing 说明

### Day 6

- [ ] 自己实现或重写 baseline equal-weight portfolio
- [ ] 检查每个调仓日权重是否合计为 1
- [ ] 产出：baseline metrics 和一张 wealth curve

### Day 7

- [ ] 实现 / 验证 12–1 momentum
- [ ] 检查最近 21 个交易日没有进入 signal
- [ ] 增加一个 look-ahead bias 单元测试
- [ ] 产出：signal timing 测试结果

### Day 8

- [ ] 实现 inverse-volatility weighting 和 turnover
- [ ] 加入 10 bps one-way trading cost
- [ ] 产出：四种策略的 metrics.csv

### Day 9

- [ ] 运行 research period 与 out-of-sample period 对比
- [ ] 随机抽查三个 rebalance dates
- [ ] 写出至少五个 bias / limitation
- [ ] 产出：2 页研究结果草稿

### Day 10

- [ ] 完成 momentum report 初稿和 6–8 页 deck 初稿
- [ ] 用英文录音讲 5 分钟：question、method、result、limitation
- [ ] 产出：可复现项目版本 1

## Day 11–14：Option Pricing & Hedging Lab

### Day 11

- [ ] Hull / MIT 18.642：European option payoff、Black–Scholes assumptions
- [ ] 逐行阅读 `option_lab/src/option_models.py`
- [ ] 产出：解释 d1、d2、delta、gamma、vega、theta 的笔记

### Day 12

- [ ] 验证 Black–Scholes call / put 和 put-call parity
- [ ] 比较 analytical Greeks 与 finite-difference Greeks
- [ ] 产出：定价与 Greeks 图表

### Day 13

- [ ] 验证 Monte Carlo convergence 和 standard error
- [ ] 改变 spot、volatility、maturity，解释结果变化
- [ ] 产出：MC convergence 图和误差解释

### Day 14

- [ ] 运行 daily / weekly delta hedging
- [ ] 比较 volatility misspecification 或 jump risk 下的 P&L
- [ ] 完成测试和 README
- [ ] 产出：2–3 页 technical note + 3 分钟英文解释

## Day 15–17：AMAT Fundamental Stock Pitch

### Day 15

- [ ] 阅读 AMAT FY2025 10-K 与最新 quarterly release
- [ ] 写 business map：客户、半导体流程、竞争对手、收入分部
- [ ] 产出：一页事实表，区分 fact / inference / assumption

### Day 16

- [ ] 完成 thesis、三个 catalysts、三个 disconfirming risks
- [ ] 建立最小 DCF / comparable framework；不强行编造 price target
- [ ] 产出：2 页英文 memo

### Day 17

- [ ] 完成 6–8 页 stock-pitch deck
- [ ] 5 分钟讲清：view、evidence、valuation question、risks
- [ ] 产出：可接受追问的 pitch 版本 1

## Day 18–20：申请资产与模拟面试

### Day 18

- [ ] 用真实个人信息完成一页英文 CV
- [ ] 只保留你能讲两分钟的项目 bullet
- [ ] 整理 GitHub README、tests、reports、deck links
- [ ] 产出：CV v1 + clean repository

### Day 19

- [ ] 完成一套 60 分钟 quant / coding / finance mixed mock
- [ ] 准备 8 个行为问题：Why quant、Why OAF、Why CapitOx、market view、failure、teamwork
- [ ] 进行一次 30 分钟模拟面试并录音
- [ ] 产出：错题复盘 + 英文回答稿

### Day 20

- [ ] 在新环境从 README 重新运行两个项目
- [ ] 进行最终 5 分钟 momentum pitch 和 5 分钟 AMAT pitch
- [ ] 检查申请追踪表和社团招新页面
- [ ] 产出：CV、GitHub、两份 PDF、两份 deck 和最终申请材料包

## 20 天验收标准

- [ ] 能解释 momentum 项目的 signal timing、cost、out-of-sample 和五个 limitations
- [ ] 能解释 Black–Scholes 的假设、Greeks 和 delta-hedging P&L
- [ ] 能在 5 分钟内完成 AMAT pitch，并明确区分事实和推断
- [ ] 能在 60 分钟内完成一套混合 mock，并复盘错误
- [ ] CV 一页、项目链接可打开、所有项目 bullet 都真实且可追问

## 直接跳过的内容

- [ ] 不在这 20 天内系统学习深度学习交易、强化学习、复杂 C++ 模板或完整 LBO
- [ ] 不为了增加项目数量再开第三个量化策略
- [ ] 不把 backtest 的历史 Sharpe 写成未来收益承诺
