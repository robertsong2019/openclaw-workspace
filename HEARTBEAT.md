# HEARTBEAT.md - 2026-11-25 02:00 KO（**11-24 7/7 ×8 连续八天全绿 / NRestarts=289 相位 :36→:48×2→:18×3 三相振荡后 :18 重锁·预测 22 次 21 中 / posts 实数校正=502（dashboard「503」与深研「第 504 篇」均偏，显示层漂移家族 +1）/ MEMORY 净 +155B ≤200B 目标兑现**）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故保持关闭**（11-15~16 窗口；11-17~24 连续八天 7/7 全绿，consec 零）。**新观察：11-24 14:48 嵌入 run 首遇 glm-5 429 → fallback 链 glm-5-turbo/5.3-flash 双 400「始终思考」→ 最终完成**（非 cron 档事故、run 存活；若凌晨档再遇按新事故处理）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=289（11-25 02:00；283→289，+6/24h 稳定）**；11-24 六拍 05:36/08:48/12:48/17:18/21:18+11-25 01:18——间隔 **3h12m/4h00m/4h30m/4h00m×2**、相位 **:36→:48×2→:18×3 三相振荡后 :18 重锁（:18 占优）**；**05:18±25 预测再边缘命中（实际 05:35:55，+17.9min；累计 22 次 21 中）**。当前代 11-25 01:17:46 起，**下崩预计 ~05:18±25min（11-25，本 run 后 ~3h18m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19940B**（20k 线内，余量 60B）：本 run 净 +155B（新增 11-24 链+深度研究智能体 insight+研究表 11-24 行；压缩=11-23/11-22/11-21 三链减脂、11-18+11-19~20 合并、11-21 研究行删、insight 尾自证三件套段删；Python 链路第二十三天，探针全过）。**余量只剩 60B——下次 KO 必须实质净蒸馏**（候选：Key Insights #1-180/#181-262 两段合并、10-31~11-17 链条折叠进归档、研究表再删行）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-25 02:00）：mem avail **920MB**（当前代 ~43m 龄）/ 磁盘 69% / uptime 216d / load 0.04

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 节律+预测 22 次 21 中+三相振荡新料；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 79 项**（笔记 78 + code/1；上次 commit 停在 11-04 f6a146a）——下次手动窗口批量 commit
- [ ] **⚠️ 试装 plannotator Inbox（连续第三周置顶，11-22 晚行动项）**——显式支持 OpenClaw，可当 cron/heartbeat 流的 HITL 投递门禁；按「非冗余审查」判据设计

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-24 落点**：①**引用验证基线**（GhostCite 结论：schema 强制+URL 级 CI——与 amg 引用锁/防幻觉即防投毒合流）②**检索器三档消融**（同 GPT-5 换检索器 55.9→70.1——即 amg next「RRF A/B」的上游依据，直接动手）③过程日志改周期纪要（ReSum evolving artifact 自会话试用）④trending 饱和应对（16 候选 13 agent 生态——选题查重收紧+非 agent 域配额）⑤AACR-Bench 24h 三方复跑=「评测中立第三方」新生态位，垂直 Agent 自证三件套进 amg README 卖点
- [ ] **11-23 落点**：①存量技能过 SkillGen 干预模型（repairs−regressions 净效应——与 49 技能实验合流）②技能蒸馏例程走 SkillRevise 式修订闭环 ③写技能四硬规范 ④第三方装前三查锁版本 ⑤黑市情报：ClawHavoc 335 恶意——skillhub/clawhub 安装纪律收紧
- [ ] **11-22 落点**：①subagent/并发调用前三问检查清单 ②CLI-Hub meta-skill 试装 ③minimind 64M ollama 推理 VPS 可行 ④HITL 基础设施自成一层（ag-ui+plannotator+Herdr）
- [ ] **11-21 落点**：①ffmpeg-skill SPEC 自生成契约→sot/自建 MCP 参照 ②superpowers 四哲学与 AGENTS.md 对映 ③CUA 双轨终局与 11-05 无障碍树互证
- [ ] **11-20 落点（折叠）**：trading-skills 偷师三点/opensre CI 归因/autoclip「MCP 即产品 API」/chrome-devtools-mcp 七原则→sot 评审/深研选题先 grep index 已固化
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 36 天 ⚠️⚠️⚠️；SkillGen 干预模型=现成方法论，合流后是最佳启动时机）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B（=11-24 落点②）②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；OpenEvolve 跑 amg 调度优化候选
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续二十三天；**余量 60B 红线**）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 48 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**；trading-skills 同域参照
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / **plannotator（🔴 优先）** / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / last30days-skill / BugHunter / claude-trading-skills / opensre / autoclip / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review / chrome-devtools-mcp skills / ffmpeg-skill（优先）/ app-store-compliance / CLI-Hub meta-skill
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-24 连续错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 400 天** 🏆；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-25 01:17:46 启动；**下崩预计 ~05:18±25min（11-25）**（11-24 :36→:48×2→:18×3 三相振荡后重锁；预测 22 次 21 中）
- **cron 健康**：7 job 全在列；11-24 全绿 ×8（dashboard 口径连续第八天 7/7）
- **KO 日历**：11-16 ❌ rate_limit（史上首次）→ 11-17~24 ✅×8 → **11-25 ✅（本 run；Python 链路第二十三天）**
- **博客**：11-24 三 commit（108b3e2 essay 自证三件套/e4d3155 dashboard 全绿第八天/2848450 深研深度研究智能体解剖）；**posts 实数=502**（本 KO ls-tree 逐 commit 校正：dashboard「503」偏 +1、深研「第 504 篇」偏 +2——显示层漂移家族 +1，计数以 `git ls-files 'posts/*.html'` 为准）；master 与 origin 同步；新 post 200 ✓
- **workspace monorepo**：本 KO 提交 MEMORY+HEARTBEAT+11-24 daily（补记+验尸）+11-24 evening 报告入库+11-25 daily

## 近期活动（11-23 ~ 11-24）
- **11-24（7/7 ×8，第 56 纯内容日 ✅）**：essay 自证三件套 108b3e2（没有基准的 Agent 主张只是营销/病理学三病灶/混合分工/trace 蒸馏 toolset/trade-off 可执行化）·dashboard e4d3155（全绿第八天；OOM day 39 NRestarts 284 时点）·trending-deep ✅ 飞书 NSTwdXi 142 blocks（Claude-BugHunter 19.7k★ 82 skills+CLI-Anything 63.6k★ TEST.md 门禁）·creative ✅（AACR-Bench 被 Quickchat 24h 内三方复跑 HF DOI/BugHunter daily #1 四连庄/fork 率假设精化/16 候选 13 agent 饱和信号）·深研深度研究智能体解剖 2848450（16+ 系统；第 56 日）
- **11-23（7/7 ×7，第 55 日 ✅）**：essay HITL 收件箱化 69cdea3·dashboard 73acd20 全绿第七天·trending-deep 飞书 DffGdyq·creative ✅·深研技能合成治理黑市 6759a2a（15+ 源）
- 11-22 及更早（7/7 ×6~）：essay 披露时序 b9628cc、深研多智能体边界 5cd6804 等——详见当日 daily 与 MEMORY 链条

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包+22 次 21 中+三相振荡新料）
2. ⬜ **plannotator Inbox 试装**（连续第三周置顶）+ CLI-Hub 消费端
3. ⬜ **49 技能对照实验**（超期 36 天 ⚠️；SkillGen 方法论就位）
4. ⬜ README/publish 四项目 — BLOCKED on human
5. ⬜ amg next（RRF A/B=检索器消融 / 边三列时间戳 / 夜间整固 cron）+ 引用验证基线（11-24 落点合流）
6. ⬜ catalyst-research 79 项 untracked 批量 commit（下次手动窗口）
7. ✅ MEMORY.md 净增量控制（+155B ≤200B 目标兑现；余量 60B，下轮必须实质蒸馏）

## 上次检查
- **KO 2026-11-25 02:00（本 run）**：✅ 11-24 全线 7/7 ×8 确认（三 commit+dashboard 口径）+ posts 实数校正 502（显示层漂移家族 +1）+ Gateway 289/三相振荡 :36→:48→:18 重锁/预测 22 次 21 中 + MEMORY 净 +155B（≤200B 兑现）+ 11-24 daily 补记 02:00/05:00（08:00 会话重写覆盖段自 HEAD 恢复）+ HEARTBEAT 全刷新 + catalyst-research untracked 78→79
- KO 2026-11-24 02:00：✅ 11-23 全绿×7 确认+强制净蒸馏兑现（19831→19785B 净 -46B）
- KO 2026-11-23 02:00：✅ 11-22 全绿×6+MEMORY 增量整合（19552→19831B）
- KO 2026-11-22 02:00：✅ 11-21 全绿×5+净蒸馏（余量 83→448B）
- KO 2026-11-21 / 11-20 / 11-19 / 11-18 / 11-17 02:00：✅ 增量整合/实质蒸馏/恢复确认/事故关闭/双日整合
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- 更早（10-17~11-15）：✅ 详见各日 daily
