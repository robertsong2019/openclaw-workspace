# HEARTBEAT.md - 2026-10-29 02:00 KO（第 31 纯内容日整合：10-28 7/7 全绿收口 / NRestarts=138 前四拍分秒不差=八连中 / 品味管线+审批疲劳双 essay）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **✅ rate_limit 事故双日收口**：10-26 四连灭（08:00 自愈）→ 10-27 晨线恢复 → **10-28 7/7 全绿**（dashboard 8b4bfa3 首次 7/7，day 12）。cron lastRunStatus 全部 ok / consecutiveErrors=0
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=138（10-29 02:00；132→138 +6 恰合六代）**；10-28 六代 02:18/06:48/11:18/15:48/20:39/（+10-29）00:48——**前四拍与预测分秒不差（八连中）**，后两拍漂移（间隔 291/248min，270min 家族内波动）；当前代 10-29 00:47 起，**下崩预计 ~05:17**（五代节拍 ~05:17/09:47/14:17/18:47/23:17）。勿动 heap 上限（2GB 主机）。headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零（dashboard 链续至 day 12）；OOM 独立（根因=V8 堆，非注入）
- **✅ KO 纪律达成**：MEMORY.md 17.2k→**15.0k**（10-22~24 逐日下放归档 + 10-07~21 洞察早期批压缩 + 索引块压缩 + 重复规则回指 TOOLS.md）；已回 15k 线内，下次 KO 常规维护即可
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（10-29 02:00）：mem avail **847MB**（当前代 1h 龄，优于昨日 409MB）/ 磁盘 69% / uptime ~192d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；270min **八连中** + 10-26/27 活动耦合对照=最强证据包；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 54 项**（08-24 起笔记+code/，比此前记录的「6+ 篇」大得多）——下次手动窗口批量 commit

### 中优先级（详情见 10-28 daily + trending 报告）
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 10 天 ⚠️⚠️⚠️；API 封装类先写 20 道判分题再决定去留）
- [ ] **20 题归档召回基线**（dreaming/压缩改动必须过 recall eval 的量尺）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（metaproductivity 台账最小版）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit 审计 workspace
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 21 天未执行）+ skill 安装流程接 SkillSpector 扫描
- [ ] **hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service 待排期**
- [ ] **graphify 试装评估 + huashu-design 3.0 装用实测**（10-27）；**jakubkrehel/skills interface-review 试装**（10-28，8.9k★ PR 门禁）；**SPEC.md 图谱模式评估**（thinkrail/openbot 信号）
- [ ] **amg×Agentic RL 接口**（LME exact judge 作 verifier 接 RL 循环）；DeepTutor 索引血缘并入图谱记忆评估（10-28）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **amg 实验四连**：3-layer 渐进披露 / claude-mem 集成对比 / EvidenceLedger 工具化 / 压缩悖论三件
- [ ] **amg PPR 对照臂**（注意 10-27 研究结论：别拿 leaderboard 做决策，优先独立复测）+ acs 双时间戳（valid_at 两列最小实现）
- [ ] **TTT 后续**（LoRA<1%+20 条信息增益邻居）；**Governance Decay 后续**（宪法存活测试进 KO 自检 / KV-cache ≥70% 阈值进仪表盘）；**Agentic Commerce 后续**（预算三档对照）
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27/10-28 essay 均已执行错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 373 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 10-29 00:47 启动；**下崩预计 ~05:17**（270min 家族；五代节拍 ~05:17/09:47/14:17/18:47/23:17）
- **KO 日历**：10-26 ✗（rate_limit）→ 10-27 ✅（补两日）→ 10-28 ✅ → **10-29 ✅（本 run）**
- **博客**：10-28 双 essay + dashboard（ad81313 品味管线 + 8758e5f 审批疲劳 + 8b4bfa3 day 12），master 与 origin 同步

## 近期活动（10-27 ~ 10-28）
- **10-28（第 31 日，7/7 全绿）**：essay 反AI slop 品味管线 ad81313（AI 味=分布坍缩；品味三能力 agent 全缺；判断前置成工序；60 行账本实测）· dashboard 8b4bfa3（rate_limit 后首次 7/7，day 12）· creative：jakubkrehel/skills（interface-review）/macro/DeepTutor 47k★/thinkrail 持续高位——skills 三层分化完成；ECC 290k★（AgentShield 供应链 SAST，与 10-27 博文互证）· 晚深研+essay《第 41 次点击「允许」》8758e5f（18 源；监督不可能三角；判断搬进配置；⚠️ commit message $ 展开瑕疵）
- **10-27**：晨线全恢复 · essay Skill 供应链 76da252 + 图谱记忆 e5da563 · creative：thinkrail 22× 跳变/openbot/huashu-design 3.0 · dashboard e2228d2 补跑 day 11

## 本周关键路径
1. ✅ 内容线连续 31 纯内容日（10-26 中断后 10-27 恢复、10-28 7/7 全绿）；⬜ 上游 issue 报告（置顶，八连中+活动耦合证据已足）
2. ⬜ 49 技能对照实验（超期 10 天 ⚠️）+ headroom 决策（装前过 20 题配对）
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（PPR 臂/20 题召回基线/exact judge 接 RL 循环）— 待罗嵩排期
5. ⬜ catalyst-research 54 项 untracked 批量 commit（下次手动窗口）

## 上次检查
- **KO 2026-10-29 02:00（本 run）**：✅ 第 31 日整合 + NRestarts=138（+6 恰六代；前四拍分秒不差=八连中）+ 10-28 7/7 全绿收口 + MEMORY 17.2k→15.0k（大力度归档：15 处字节级替换 + 6 处修剪零失配）+ 10-28 daily 补记 06:00/07:00 + HEARTBEAT 全刷新
- KO 2026-10-28 02:00：✅ 第 30 日整合 + NRestarts=132（+5；03:48 命中=七连中）+ MEMORY 16.1k→17.2k（⚠️ 越 15k 线挂账本次执行）
- KO 2026-10-27 02:00：✅ 补两日整合（10-25 晚+10-26 全天）
- KO 2026-10-26 02:00：✗ rate_limit 未跑（晨线四连灭之一）
- 更早（10-17~10-25）：✅ 详见各日 daily
