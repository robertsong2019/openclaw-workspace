# HEARTBEAT.md - 2026-10-31 02:00 KO（第 33 纯内容日整合：10-30 7/7 全绿连续 3 天 / NRestarts=149 六拍漂移回摆 / 记忆整固 essay）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **✅ 连续 3 天 7/7 全绿**（10-28、10-29、10-30）：cron lastRunStatus 全 ok / consecutiveErrors=0；dashboard 链 day 14（6517bb8）。rate_limit 事故彻底收口
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=149（10-31 02:00；143→149 +6 恰合六拍）**；10-30 六拍 CST 03:48/07:48/11:48/16:18/20:36/10-31 00:48——间隔 240/240/270/258/252min 均值 252min，**漂移回摆、收窄至 4h~4h30m**；昨日五代预测仅首拍命中（其后系统性早 30~72min）。当前代 10-31 00:48 起，**下崩预计 ~04:55±25min**（漂移期预测精度降级）。勿动 heap 上限（2GB 主机）。headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零（dashboard 链续至 day 14）；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 16.5k**（20k 线内 82%；本 run 常规维护：增 10-30 条目/下放 10-26/27 细节/增记忆整固洞察+研究表行）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（10-31 02:00）：mem avail **851MB**（当前代 1.2h 龄）/ 磁盘 68% / uptime ~194d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；250min 节拍族+取证三层全瞎=最强证据包；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 54 项**（08-24 起笔记+code/）——下次手动窗口批量 commit

### 中优先级（详情见 10-30 daily + trending 报告）
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 12 天 ⚠️⚠️⚠️；API 封装类先写 20 道判分题再决定去留）
- [ ] **amg next 三件（10-30 深研落点，直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边加 valid_at/invalid_at（bi-temporal 最小实现）③夜间 sleep-time 整固 cron（daily→MEMORY.md，升级 heartbeat）
- [ ] **20 题归档召回基线**（dreaming/压缩改动必须过 recall eval 的量尺）；**amg×Agentic RL 接口**（LME exact judge 作 verifier 接 RL 循环）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（metaproductivity 台账最小版）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit 审计 workspace（10-30 creative：cloudflare security-audit-skill 53.3k★ 可沙箱跑自有项目）
- [ ] **博客加 llms.txt 吃 Agent Readiness 红利**（10-30 creative 建议；claude-seo 24.2k★ GEO/AEO）
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 23 天未执行）+ skill 安装流程接 SkillSpector 扫描
- [ ] **hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service 待排期**
- [ ] **graphify 试装评估 + huashu-design 3.0 装用实测**（10-27）；**jakubkrehel/skills interface-review 试装**（10-28，8.9k★ PR 门禁）；**OpenMausBot 试装评估**（10-29，陪伴 agent×VM×审批闭环）；**SPEC.md 图谱模式评估**（thinkrail/openbot 信号）；**DeepTutor 三层记忆/claude-mem 六钩子**消化（10-30 trending，均指向 agent 记忆基础设施化）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **amg 实验四连**：3-layer 渐进披露 / claude-mem 集成对比（104k★）/ EvidenceLedger 工具化 / 压缩悖论三件
- [ ] **amg PPR 对照臂**（注意 10-27 研究结论：别拿 leaderboard 做决策，优先独立复测）
- [ ] **TTT 后续**（LoRA<1%+20 条信息增益邻居）；**Governance Decay 后续**（宪法存活测试进 KO 自检 / KV-cache ≥70% 阈值进仪表盘）；**Agentic Commerce 后续**（预算三档对照）
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~10-30 连续错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 375 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 10-31 00:48 启动；**下崩预计 ~04:55±25min**（间隔族 240~270min；漂移回摆期，预测精度降级）
- **KO 日历**：10-27 ✅（补两日）→ 10-28 ✅ → 10-29 ✅ → 10-30 ✅ → **10-31 ✅（本 run）**
- **博客**：10-30 essay 组织架构即配置 79315a9 + 记忆整固 3c5a36d + dashboard 6517bb8（day 14），master 与 origin 同步

## 近期活动（10-29 ~ 10-30）
- **10-30（第 33 日，7/7 全绿连续 3 天）**：essay《在 GitHub 上下载一家公司》79315a9（组织设计层；60 行 org-lint 埋 5 组织病全命中可接 CI）· dashboard 6517bb8（day 14；六拍 240~270min）· trending deep：DeepTutor+claude-mem 双记忆基建（飞书文档验证 ✅）· creative：security-audit-skill 53.3k★/mattpocock skills 破 30 万星/给罗嵩 3 项（security-audit 沙箱、llms.txt、TradingAgents 金融场景）· 晚深研+essay《让 Agent 睡个觉》3c5a36d（记忆整固三共识；amg 落点 RRF/valid_at/夜间整固）
- **10-29（第 32 日）**：essay《270 分钟节拍器》ce0ba71（OOM 取证三层全瞎+crash-only 三件套）· dashboard day 13 · creative：OpenMausBot/Claude-Code-Game-Studios/双破 10 万星 · 晚深研+essay《把对错外包给公证员》18f704a（LLM-Modulo；LTL 监控>LLM judge 13.33% vs 86.67%）

## 本周关键路径
1. ✅ 内容线连续 33 纯内容日（10-28/29/30 连续 7/7）；⬜ 上游 issue 报告（置顶，250min 节拍族+取证全瞎三层证据已足）
2. ⬜ 49 技能对照实验（超期 12 天 ⚠️）+ headroom 决策（装前过 20 题配对）
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（RRF A/B / 边 valid_at / 夜间整固 cron / PPR 臂 / 20 题召回基线）— 待罗嵩排期
5. ⬜ catalyst-research 54 项 untracked 批量 commit（下次手动窗口）

## 上次检查
- **KO 2026-10-31 02:00（本 run）**：✅ 第 33 日整合（10-30 全 7/7 收口）+ NRestarts=149（+6 恰六拍；漂移回摆 240~270min）+ MEMORY 增 10-30 条目/下放 10-26/27/增记忆整固洞察+研究表行（16.5k）+ HEARTBEAT 全刷新
- KO 2026-10-30 02:00：✅ 第 32 日整合 + NRestarts=143（八连中终结漂移扩大）+ MEMORY 常规维护（15.9k）
- KO 2026-10-29 02:00：✅ 第 31 日整合 + NRestarts=138 八连中 + MEMORY 17.2k→15.0k 大力度归档 + error-patterns 首记 $ 展开
- KO 2026-10-28 02:00：✅ 第 30 日整合（MEMORY 16.1k→17.2k 越线挂账）；10-27：✅ 补两日；10-26：✗ rate_limit
- 更早（10-17~10-25）：✅ 详见各日 daily
