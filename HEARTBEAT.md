# HEARTBEAT.md - 2026-11-26 02:00 KO（**11-25 7/7 ×9 连续九天全绿 / NRestarts=295 相位 :48×5 重锁·4h 节律回归 / 05:18 预测正中 +0.2min 累计 23 次 22 中 / MEMORY 实质净蒸馏 -628B 兑现余量 688B / posts 实数=504**）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故保持关闭**（11-15~16 窗口；11-17~25 连续九天 7/7 全绿，consec 零）。11-24 14:48 嵌入 run 遇 glm-5 429 → fallback 链兜住（run 存活，非 cron 档事故；未复发）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=295（11-26 02:00；289→295，+6/24h 稳定）**；11-25 六拍 01:18/05:18/08:48/12:48/16:48/20:48+11-26 00:48——间隔 **4h00m×5+3h30m**、相位 **:18 后 :48×5 重锁（4h 节律回归稳定，对照 11-24 三相振荡已收敛）**；**05:18 预测正中（实际 05:18:13，+0.2min；累计 23 次 22 中）**。当前代 11-26 00:47:47 起，**下崩预计 ~04:48±25min（11-26，本 run 后 ~2h48m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19312B**（20k 线内，余量 688B）：本 run 净 **-628B**（红线兑现：pass1 新增 11-25 内容 +212B 超线 → pass2 同族双研合并七组 -840B 拉回）。Python 行级替换链路第二十四天，探针全过。余量恢复后下轮可正常增量
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-26 02:00）：mem avail **836MB**（当前代 ~72m 龄）/ 磁盘 69% / uptime 217d / load 0.40

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 节律+预测 23 次 22 中+三相振荡收敛新料；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 80 项**（笔记 79 + code/1；上次 commit 停在 11-04 f6a146a）——下次手动窗口批量 commit
- [ ] **⚠️ 试装 plannotator Inbox（连续第四周置顶，11-22 晚行动项）**——显式支持 OpenClaw，可当 cron/heartbeat 流的 HITL 投递门禁；按「非冗余审查」判据设计

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-25 落点（持久化/断点续跑）**：①kill -9 恢复演练掐 RTO ②幂等三查升级产物指纹机制（display-layer 案的反伪影第五条同向）③50 行 SQLite step-journal 实验（LLM 调用 memoize）④深研选题必查博客 posts/ 目录（本轮已补入流程：10 月 durable-execution-agents 撞题教训）
- [ ] **11-24 落点**：①**引用验证基线**（GhostCite 结论：schema 强制+URL 级 CI——与 amg 引用锁/防幻觉即防投毒合流）②**检索器三档消融**（同 GPT-5 换检索器 55.9→70.1——即 amg next「RRF A/B」的上游依据，直接动手）③过程日志改周期纪要（ReSum evolving artifact 自会话试用）④trending 饱和应对（选题查重收紧+非 agent 域配额）⑤垂直 Agent 自证三件套进 amg README 卖点
- [ ] **11-23 落点**：①存量技能过 SkillGen 干预模型（repairs−regressions 净效应）②技能蒸馏例程走 SkillRevise 式修订闭环 ③写技能四硬规范 ④第三方装前三查锁版本 ⑤ClawHavoc 335 恶意——skillhub/clawhub 安装纪律收紧
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 38 天 ⚠️⚠️⚠️；SkillGen 干预模型=现成方法论，合流后是最佳启动时机）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B（=11-24 落点②）②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；OpenEvolve 跑 amg 调度优化候选
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续二十四天；余量 688B 恢复健康）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 49 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**；trading-skills 同域参照
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / **plannotator（🔴 优先）** / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / last30days-skill / BugHunter / claude-trading-skills / opensre / autoclip / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review / chrome-devtools-mcp skills / ffmpeg-skill（优先）/ app-store-compliance / CLI-Hub meta-skill
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending+深研选题查重（深研必含博客 posts/ 目录，10-27~11-25 连续错开 ✅）**
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 401 天** 🏆；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-26 00:47:47 启动；**下崩预计 ~04:48±25min（11-26）**（11-25 相位 :48×5 重锁、4h 节律回归；预测 23 次 22 中）
- **cron 健康**：7 job 全在列；11-25 全绿 ×9（dashboard 805848e 口径连续第九天 7/7）
- **KO 日历**：11-16 ❌ rate_limit（史上首次）→ 11-17~25 ✅×9 → **11-26 ✅（本 run；Python 链路第二十四天）**
- **博客**：11-25 三 commit（ae35219 essay 显示层Bug家族/805848e dashboard 全绿第九天/43dfdcc 深研持久化断点续跑）；**posts 实数=504**（git ls-files 口径；11-26 KO ls-files 复核）；master 与 origin 同步；两新 post 200 ✓
- **workspace monorepo**：本 KO 提交 MEMORY+HEARTBEAT+11-25 daily（补记 06:00+入库 08:00/20:00 段）+11-25 evening 报告入库+11-26 daily

## 近期活动（11-24 ~ 11-25）
- **11-25（7/7 ×9，第 57 纯内容日 ✅）**：essay 显示层Bug家族五案 ae35219（分母/tie-break/双臂不同源/stale-base/计数漂移，反伪影五条+三示例实测）·dashboard 805848e（全绿第九天；OOM day 40 NRestarts 290；posts 口径自修正 501）·trending-deep ✅ 飞书 MjIy 162 blocks（Claude-BugHunter 21.4k★+1,826/CLI-Anything 64.7k★ 7-phase+CLI-Hub）·creative ✅（Agent Skills 生态工业化 16 席 10 基建）·深研持久化断点续跑 43dfdcc（18+ 系统：Temporal/Restate/DBOS/LangGraph/AgentRewind/Chronicle/Concordia/GhostServe）
- **11-24（7/7 ×8，第 56 日 ✅）**：essay 自证三件套 108b3e2·dashboard e4d3155 全绿第八天·trending-deep ✅ 飞书 NSTwdXi 142 blocks·creative ✅（AACR-Bench 24h 三方复跑）·深研深度研究智能体解剖 2848450（16+ 系统）
- 11-23 及更早（7/7 ×7~）：essay HITL 收件箱化 69cdea3、深研技能合成治理黑市 6759a2a 等——详见当日 daily 与 MEMORY 链条

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包+23 次 22 中+4h 节律回归新料）
2. ⬜ **plannotator Inbox 试装**（连续第四周置顶）+ CLI-Hub 消费端
3. ⬜ **49 技能对照实验**（超期 38 天 ⚠️；SkillGen 方法论就位）
4. ⬜ README/publish 四项目 — BLOCKED on human
5. ⬜ amg next（RRF A/B=检索器消融 / 边三列时间戳 / 夜间整固 cron）+ 引用验证基线（11-24 落点合流）
6. ⬜ catalyst-research 80 项 untracked 批量 commit（下次手动窗口）
7. ✅ MEMORY.md 实质净蒸馏（-628B 红线兑现；余量 60B→688B 恢复健康）

## 上次检查
- **KO 2026-11-26 02:00（本 run）**：✅ 11-25 全线 7/7 ×9 确认（三 commit+evening 19:04）+ Gateway 295/:48×5 重锁/预测正中 +0.2min（23 次 22 中）+ **MEMORY 实质净蒸馏 -628B 兑现**（pass2 同族双研合并七组）+ 11-25 daily 补记 06:00（+08:00/20:00 段入库）+ HEARTBEAT 全刷新 + catalyst-research untracked 79→80
- KO 2026-11-25 02:00：✅ 11-24 全绿×8 确认+posts 实数校正 502（显示层漂移 +1）+净 +155B≤200B 兑现（余量 60B 红线）
- KO 2026-11-24 02:00：✅ 11-23 全绿×7+强制净蒸馏兑现（19831→19785B 净 -46B）
- KO 2026-11-23 / 11-22 / 11-21 02:00：✅ 增量整合/净蒸馏/恢复确认
- KO 2026-11-20 / 11-19 / 11-18 / 11-17 02:00：✅ 增量整合/实质蒸馏/恢复确认/事故关闭
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- 更早（10-17~11-15）：✅ 详见各日 daily
