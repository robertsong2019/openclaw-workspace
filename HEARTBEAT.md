# HEARTBEAT.md - 2026-10-24 02:00 KO（第 26 纯内容日整合 + OOM NRestarts=113 / 270min 平均精确保持）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）。**10-23 全线 err=0（KO consecutiveErrors 清零确认 ✅，Python 字节级替换方案生效）**
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=113（10-24 02:00）**；10-23 五代 01:48/06:34/10:48/15:18/19:48+10-24 00:18——五间隔合计恰 1350min=**平均 270.0 整**（286/254/270/270/270；06:18 预测实际 06:34 +16min 近中，精确命中 streak 止于四连中，后三隔 270 整锁回）；当前代 10-24 00:17 起，**下崩预计 10-24 ~04:48**。勿动 heap 上限（2GB 主机）。headroom 候选须先过 eval-gap 20 题配对实验
- **⚠️ Gateway 取证口径**：cron 沙箱 `journalctl -u` 返回空、系统级 systemctl 同名 unit 得 NRestarts=0 是陷阱——真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- **✅ 注入层手术七日验证**：截断警告 10-18 起持续归零（dashboard 10-23 口径 day 6）；OOM 独立（根因=V8 堆，非注入）。**KO 纪律：MEMORY.md 超 ~15k bytes 即归档/修剪**（本次 15.9k：已增 10-23 全天条目+2 洞察+研究行，10-21 压缩、10-20 下沉、研究表删 10-14/15/16 行、kd 纪律与 Timeline 收拢）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 27+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（10-24 02:00）：mem avail **736MB**（当前代年轻态）/ 磁盘 68% / uptime ~184d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；270min 平均 6 日节拍是强证据；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓历史笔记 untracked**（08-24 起 6+ 篇）——下次手动窗口批量 commit

### 中优先级（详情见 10-22~10-23 daily + trending 报告）
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 5 天 ⚠️⚠️；API 封装类先写 20 道判分题再决定去留）
- [ ] **20 题归档召回基线**（10-18 essay：dreaming/压缩改动必须过 recall eval 的量尺；**10-23 Governance Decay 深研再度强化此判据**）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（10-19 深研 next：metaproductivity 台账最小版）
- [ ] **headroom `wrap openclaw` 实测**（官方支持三确认；仍须先过 20 题配对）/ **context-mode 本机试装**（单项目先试 ctx_execute，对照 context-forge）/ skills add security-audit 审计 workspace
- [ ] **hindsight vs amg 对标实验**（arXiv 2512.12818）；**ai-memory 已精读（10-23 essay 全量核实）→ 落地三件抄进 agent-memory-service 待排期**（交接协议/markdown 事实源/访问强化老化）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval（现实结果反哺=评测锚定现实）
- [ ] **Agent-Reach 试装升级**（⚠️ 连续 16 天未执行，已飞书罗嵩待排期）
- [ ] **amg 实验四连**：3-layer 渐进披露 / claude-mem 集成对比 / EvidenceLedger 工具化 / 压缩悖论三件（**10-23 深研给足弹药：11 组对照什么都不做三线全胜**）
- [ ] **amg PPR 对照臂**（Zep LME +18.5% 参照）+ acs 双时间戳；**orca worktree fan-out 评估**（mission-control 借鉴）
- [ ] **TTT 后续**（10-22 深研）：LoRA<1%+20 条信息增益邻居=最便宜实验；审计同文档反复进上下文的租金
- [ ] **Governance Decay 后续**（10-23 深研）：宪法存活测试进 KO 自检 / KV-cache 命中率进仪表盘（≥70% 阈值）/ 高危校验进 hook / recitation 防漂移
- [ ] **AGENTS.md/MEMORY.md 按 ACE 改造**（bullet+计数器；瘦身已走三步）
- [ ] **研究 cron 加停搜判据**（R1-Searcher++ 式自检省 30% 检索）
- [ ] **trending 选题查重**（晨间 trending 前先 grep 近 2 日报告的深挖对象）
- [ ] MCP 安全清单+tool 哈希锁 · vercel-labs/skills 精读 · VoiceStudio MCP 接入 · paperclip budget→mission-control · **OpenShell 小范围试点**（本机 cron agent 沙箱化现实需求，10-23 creative）
- [ ] amg kd 手动续跑（queue 4 候选+纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 368 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 10-24 00:17 启动；**下崩预计 10-24 ~04:48**（270min 家族）
- **KO 日历**：10-22 ✅ 产物全落但 cron 判 error（CJK edit 失配，consecutiveErrors=1）→ 10-23 ✅ 全 Python 字节级替换 → **10-24 ✅（本 run：第 26 日整合，同方案零失配，daily 补录 4 条晚线）**
- **博客**：2 posts/24h（9a42c88 handoff 分布式协议 + 6645077 Governance Decay），master 与 origin 同步

## 近期活动（10-22 ~ 10-23，第 25/26 纯内容日）
- **10-23**：晨 essay《换 Agent 不用重新解释：把会话交接做成分布式协议》9a42c88（三不可靠三对策/CAS ended_at/offer-not-claim/markdown 事实源）· 晚深研+essay《Agent 的宪法是在哪一轮消失的》6645077（Governance Decay 0→59%/什么都不做三线全胜/KV-cache 命中率第一指标/四层栈）· creative：NVIDIA OpenShell 18.2k★（形式化验证治理）/Claude-Red 8k★（攻击侧 skill）/VoxCPM2 40k★；rakazo 列 OpenClaw 为直接竞品 · dashboard 6/7（自身 running 良性口径）
- **10-22**：essay《Agent 不能给自己批作业》18a0946（对抗式审查三分离+四眼）· 深研+essay《读完就忘，读完就学》f08d67e（TTT 上下文即 RAM）· creative：CLI-Anything/ai-memory/android/skills · dashboard 6/7（KO 判 error 实为 edit 失配）

## 本周关键路径
1. ✅ 内容线连续 26 日；⬜ 上游 issue 报告（置顶，270min 平均 6 日证据已足）
2. ⬜ 49 技能对照实验（超期 5 天 ⚠️）+ headroom 决策（装前过 20 题配对）
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（PPR 臂/20 题召回基线/ai-memory 三件抄排期）— 待罗嵩排期

## 上次检查
- **KO 2026-10-24 02:00（本 run）**：✅ 10-23 整合（第 26 纯内容日，零回滚 368）+ NRestarts=113（五隔平均恰 270.0；06:18 预测 +16min 近中，下崩预计 ~04:48）+ MEMORY 增 10-23 条目/Handoff+Governance Decay 两洞察/研究表增行（10-21 压缩 10-20 下沉，15.9k）+ HEARTBEAT 全刷新 + daily 补录 dashboard/trending/creative/deep 四条
- KO 2026-10-23 02:00：✅ 第 25 日整合 + NRestarts=108 + KO 改全 Python 字节级替换
- KO 2026-10-22 02:00：✅ 第 24 日整合（cron 判 error，产物全落）+ NRestarts=102
- KO 2026-10-21 / 10-20 / 10-19 / 10-18 / 10-17：✅ 详见各日 daily
