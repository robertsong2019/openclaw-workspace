# HEARTBEAT.md - 2026-11-18 02:00 KO（**11-17 全线恢复 7/7，rate_limit 事故关闭** / NRestarts=247 :48 相位石英锁定·04:48 预测命中到秒 15中14 / MEMORY 19769B 余量~230B）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=晚间创新点日报，落盘 memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故已关闭**（窗口定界 11-15 05:00→11-16 08:00，8 run 失败，全绿 ×7 终止）：11-17 七任务全部成功（05:00 essay 76028e5 / 06:00 dashboard 81fa60e / **07:00 trending cron 实证 ok delivered** / 08:00 deep 飞书 DNIadE / 19:00 creative / 20:00 deep 7aa9705 / 02:00 KO）——consec 全清零，**恢复日 7/7 streak ×1**。若凌晨档再限流按新事故处理（错峰/降模型需罗嵩知情）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=247（11-18 02:00；241→247，+6/24h）**；11-17 六拍 04:48/08:48/12:48/16:48/20:48/11-18 00:47:46 **全 4h00m±1s（:48 相位石英锁定）**；**昨日 04:48 下崩预测命中到秒（04:48:14；预测累计 15 次 14 中）**。当前代 11-18 00:47:46 起，**下崩预计 ~04:48±25min（11-18，本 run 后 ~2h48m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则；essay 50f3658 取证博文）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19769B**（20k 线内 98.8%；+69B 净增——新增 11-17 链条+insight+研究行，压缩 11-11~13 折叠/11-15~16 减脂/研究表删 11-09、10 行/头部去重/11-14 减脂；19 锚点全过。下次 KO 若逼近 19.9k 可再折 11-09~10 链条+深研语音/图记忆 insight 减脂）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-18 02:00）：mem avail **899MB**（当前代 1h13m 龄）/ 磁盘 69% / uptime ~209d / load 0.08

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 石英节律+预测 15 次 14 中（最新命中到秒）=强证据包；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 54 项**（08-24 起笔记+code/）——下次手动窗口批量 commit

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-17 落点**：①NVIDIA SkillEvaluator 三层门禁=技能评测现成尺子（`skillevaluator validate --tiers 1` 零 key，对 49 技能实验直接可用）②ag-ui 1.0（31 事件 8 族）+ MCP/A2A/AG-UI 三协议分工→mission-control/canvas-A2UI 关联 ③LoopForge SOP schema 抄进 mission-control ④EGM 金鱼模式→amg fresh-context 评审臂候选 ⑤轨迹飞轮五动作（六件套 schema+判据单列+失败 mask+export 格式+沙箱自造经验）→amg 日志侧 ⑥ExpRAG organization/utilization 框架→amg trainability 评测维度
- [ ] **11-16 落点**：①anthropics/skills 官方仓+SkillEvaluator ②人机监管层新品类（plannotator/LoopForge/ag-ui）③univer Office SDK→amg MCP 分发参考 ④AI 科学家溯源三件套→amg provenance 叙事
- [ ] **11-14 落点**：①tailcat VPS 试装 ②plannotator 官方 openclaw-plugin 试用 ③auto-ontology provenance→amg 答案来源验证 ④amg 试点 L1 规则判卷臂 ⑤判官三件套体检（swap/padding/self-pref）移植自家 cron
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 29 天 ⚠️⚠️⚠️；SkillEvaluator=现成尺子）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路已连续十六天顺畅；今晨锚点 #4 一次未中→diff_check 定位后命中，链路自愈验证）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 41 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / plannotator / SkillEvaluator / LoopForge / ag-ui / EGM / univer / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review / NVIDIA/auto-ontology
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-17 连续错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 393 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-18 00:47:46 启动；**下崩预计 ~04:48±25min（11-18）**（:48 相位石英 4h00m±1s；预测 15 次 14 中）
- **cron 健康**：7 job 全在列且 11-17 全绿；rate_limit 监控项关闭（一次性事故定界完成）
- **KO 日历**：11-14 ✅ → 11-15 ✅ → **11-16 ❌ rate_limit（史上首次 KO 失败）** → 11-17 ✅（双日整合补位）→ **11-18 ✅（本 run；Python 链路第十六天，19 锚点全过）**
- **博客**：11-17 三 commit（76028e5 金鱼评审员/81fa60e dashboard/7aa9705 轨迹飞轮）；dashboard 489 posts（06:00 口径）+晚间 1 篇→~490；master 与 origin 同步

## 近期活动（11-16 ~ 11-17）
- **11-17（7/7，恢复日 ✅ 第 49 纯内容日）**：essay 金鱼评审员 76028e5（EGM 大象起草金鱼零历史评审；共享上下文三重污染=锚定/共享幻觉/沉没成本继承；上下文=价值函数；验证器系列第四篇）·dashboard 81fa60e 断档 3 天后复更（489 posts；tokens in 467k/+29.6% out 90k/-20.6%；MEMORY 水位预警）·trending-07 ✅ univer 报（delivered）·trending-deep ✅ 飞书 DNIadE（NVIDIA SkillEvaluator 三层门禁：Tier1 静态/Tier2 语义去重/Tier3 with-without 实测+ag-ui 1.0 三协议分工）·creative ✅（Skills 生态爆发：anthropics/skills 5.7k/周+skills.sh 目录；delivery 层大厂同周交卷：LoopForge SOP+人工门禁/alibaba open-code-review precision-first 兼容 OpenClaw 的 plannotator；astryx 周榜之王「agent-ready 同一份参考」）·深研 20:00 ✅ 轨迹数据飞轮 7aa9705（验证器系列第五篇：裸轨迹差一个 verdict；转速=min(验证带宽,任务多样性,重放保真度)；失败 run 76% 步骤有效；harness 泄漏 6.8 分；ExpRAG 混合学习；笔记 2026-11-17-agent-trajectory-data-flywheel.md 20+ 源；Top3 已告知罗嵩）
- **11-16（3/7，恢复日）**：trending-deep 08:00 ✅·creative 19:00 ✅·深研 20:00 ✅《论文不等于发现》312dee8（25k runs 68% 忽略证据/底座占 41.4% 方差/插值器非外推器；笔记 2026-11-16-ai-scientist-verification-gap.md）；❌ KO/essay/dashboard/trending-07（rate_limit）
- **11-15（0/7，事故日）**：5 内容 job 全 rate_limit，零产物零 commit；仅 02:00 KO ✅

## 本周关键路径
1. ✅ rate_limit 事故关闭（11-17 全线恢复 7/7）；⬜ 上游 issue 报告（置顶；证据包已齐+命中到秒战绩）
2. ⬜ 49 技能对照实验（超期 29 天 ⚠️；SkillEvaluator=现成尺子）+ headroom 决策
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（L1 规则判卷臂 / RRF A/B / 边三列时间戳 / 夜间整固 cron / 判官三件套体检 / 轨迹飞轮五动作）+ 引用锁溯源落地 — 待罗嵩排期
5. ⬜ catalyst-research 54 项 untracked 批量 commit（下次手动窗口）
6. ✅ MEMORY.md 整合+再压缩（19769B，余量 ~230B；下次逼近 19.9k 可折 11-09~10 链条）

## 上次检查
- **KO 2026-11-18 02:00（本 run）**：✅ 11-17 全线恢复确认（cron runs 实证 07:00 ok；事故关闭）+ MEMORY 19700→19769（19 锚点；11-11~13 折叠+去重）+ HEARTBEAT 全刷新 + Gateway 预测命中到秒（15中14）+ 建 11-18 daily
- KO 2026-11-17 02:00：✅ 双日整合（补 11-16 KO 失败位）：rate_limit 事故定界 + 恢复确认 + MEMORY 压缩 17 锚点
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- KO 2026-11-15 / 11-14 / 11-13 / 11-12 / 11-11 / 11-10 02:00：✅ 第 48/47/46/45/44/43 日整合
- 更早（10-17~11-09）：✅ 详见各日 daily
