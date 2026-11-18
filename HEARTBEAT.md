# HEARTBEAT.md - 2026-11-19 02:00 KO（**11-18 7/7 ×2 连续全绿（首个全绿周期 since 11-14）** / NRestarts=253 :48 石英锁定·预测 16 次 15 中 / MEMORY 19944B 余量 56B ⚠️）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=晚间创新点日报，落盘 memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故已关闭**（窗口 11-15 05:00→11-16 08:00，8 run 失败；11-17、11-18 连续两日 7/7 全绿，consec 零）。若凌晨档再限流按新事故处理（错峰/降模型需罗嵩知情）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=253（11-19 02:00；247→253，+6/24h）**；11-18 六拍 00:48/04:48/08:48/12:48/16:48/20:48 **全 4h00m±1s（:48 石英锁定）**；**11-18 04:48 预测再命中（04:48:13；累计 16 次 15 中）**。当前代 11-19 00:47:47 起，**下崩预计 ~04:48±25min（11-19，本 run 后 ~2h48m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19944B**（20k 线内 99.7%，余量仅 56B ⚠️⚠️）：本 run 新增 11-18 链条+思考预算 insight+研究表行，压缩 11-09~17 链条/轨迹飞轮与记忆投毒 insight/研究表删 11-11 行（14 锚点三趟全过）。**下次 KO 必须先实质蒸馏**：候选=11-09~10 链条折叠进 11-03~13 段、深研语音/图记忆/评测指纹 insight 减脂、研究表删 11-12 行
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-19 02:00）：mem avail **781MB**（当前代 1h13m 龄）/ 磁盘 69% / uptime 210d / load 0.04

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 石英节律+预测 16 次 15 中=强证据包；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 54 项**（08-24 起笔记+code/）——下次手动窗口批量 commit

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-18 落点**：①MWG 式 eval 驱动内容修剪→盘活 49 技能（prune 模型已会内容）②agent-browser 实测对比现有 browser control（诚实失败语义+a11y tree token 效率）③univer headless 跑通→mission-control 内容层 Facade API 参考 ④paper-orchestra 读 arXiv:2604.05018→essay 管线 autoraters 质量门禁平移 ⑤思考预算五动作→自家 cron（审计 reasoning_tokens 账单+意图分档路由+flip 双档重放）
- [ ] **11-17 落点**：①SkillEvaluator 三层门禁（`skillevaluator validate --tiers 1` 零 key）②ag-ui 1.0 三协议分工→canvas-A2UI ③LoopForge SOP schema 抄进 mission-control ④EGM 金鱼模式→amg fresh-context 评审臂 ⑤轨迹飞轮五动作→amg 日志侧 ⑥ExpRAG→amg trainability 评测维度
- [ ] **11-16/14 落点**（折叠）：anthropics/skills 官方仓+监管层新品类+univer Office SDK+溯源三件套 / tailcat VPS 试装+auto-ontology provenance+判官三件套体检移植
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 30 天 ⚠️⚠️⚠️；SkillEvaluator=现成尺子）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续十七天顺畅；本 run 三趟补压缩亦全过）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 42 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / plannotator / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review / NVIDIA/auto-ontology
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-18 连续错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 394 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-19 00:47:47 启动；**下崩预计 ~04:48±25min（11-19）**（:48 相位石英 4h00m±1s；预测 16 次 15 中）
- **cron 健康**：7 job 全在列；11-18 全绿 ×2（dashboard 口径 7/7 首全绿 since 11-14）
- **KO 日历**：11-15 ✅ → **11-16 ❌ rate_limit（史上首次 KO 失败）** → 11-17 ✅（双日整合）→ 11-18 ✅ → **11-19 ✅（本 run；Python 链路第十七天，14 锚点三趟全过）**
- **博客**：11-18 三 commit（350679b npm 时刻/5a508a8 dashboard/a31a5e2 思考预算）；**492 posts**；master 与 origin 同步

## 近期活动（11-17 ~ 11-18）
- **11-18（7/7 ×2，第 50 纯内容日 ✅）**：essay Agent Skills npm 时刻 350679b（验证器系列第六篇：Skill=路由×方法论×资源三层封装；坏技能装行为倾向 fail silently；Tier3 with-without 差分=价值唯一定义；元数据缺版本/保鲜 SLA/差分日期三字段；准入三问）·dashboard 5a508a8（本周期 7/7 首全绿；metronome day 33 全 4h00m；491→492 posts；tokens in 460.7k out 105.6k/+16.9%）·trending-07 ✅·trending-deep ✅ 飞书 X4LXdO（univer 人机共享 Facade API：headless/交互同构+命令组合 undo+生命周期门控；paper-orchestra 五 agent 管线+写手/反思双模型+autoraters 内建）·creative ✅（Agent-First 基建周：Meta astryx+8.7k/周、Chrome/Edge/Firefox/MDN 四方 MWG+7k/周、Vercel agent-browser+3.4k/周；MWG eval 驱动修剪=49 技能盘点解法模板）·深研 20:00 ✅ 思考预算经济学 a31a5e2（验证器系列镜像篇：非单调曲线 τ≈1000 token 饱和；flip events 对改错；41-46% reasoning 可剪；浪费=系统属性 harness 差 4 倍；并行>串行 +20%；笔记 2026-11-18-thinking-budget-economics.md 14 源）
- **11-17（7/7 恢复日，第 49 日 ✅）**：essay 金鱼评审员 76028e5（三重污染+上下文=价值函数；验证器系列第四篇）·dashboard 81fa60e 复更（489）·trending-deep ✅ 飞书 DNIadE（SkillEvaluator 三层门禁+ag-ui 1.0）·creative ✅（Skills 生态爆发/LoopForge/open-code-review/astryx）·深研轨迹数据飞轮 7aa9705（裸轨迹差 verdict；转速=min 三要素；失败 run 76% 步骤有效；harness 泄漏 6.8 分）
- **11-15~16（rate_limit 事故，已关闭）**：窗口 11-15 05:00→11-16 08:00 共 8 run 失败；11-16 恢复 3/7（含 AI科学家 312dee8）；11-17 全线恢复

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包已齐+预测 16 次 15 中战绩）
2. ⬜ 49 技能对照实验（超期 30 天 ⚠️；SkillEvaluator=现成尺子）+ headroom 决策
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（L1 规则判卷臂 / RRF A/B / 边三列时间戳 / 夜间整固 cron / 判官三件套体检 / 轨迹飞轮五动作 / 思考预算五动作）+ 引用锁溯源落地 — 待罗嵩排期
5. ⬜ catalyst-research 54 项 untracked 批量 commit（下次手动窗口）
6. ✅ MEMORY.md 11-18 整合（19944B 余量 56B；下次 KO 必先蒸馏）

## 上次检查
- **KO 2026-11-19 02:00（本 run）**：✅ 11-18 全线 7/7 确认（cron list 六 job ok+博客三 commit 492 posts）+ Gateway 253/预测再命中（16中15）+ MEMORY 19769→19944（14 锚点三趟：主编辑+两趟补压缩）+ HEARTBEAT 全刷新 + 建 11-19 daily
- KO 2026-11-18 02:00：✅ 11-17 恢复确认+事故关闭+MEMORY 19 锚点
- KO 2026-11-17 02:00：✅ 双日整合（补 11-16 失败位）：事故定界+17 锚点
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- KO 2026-11-15 / 11-14 / 11-13 / 11-12 / 11-11 / 11-10 02:00：✅ 第 48~43 日整合
- 更早（10-17~11-09）：✅ 详见各日 daily
