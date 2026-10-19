# HEARTBEAT.md - 2026-10-20 02:00 KO（第 22 纯内容日整合 + OOM NRestarts=92）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=92（10-20 02:00）**；10-19 全天 5 代（02:18/07:18/11:48/16:18/20:48，270min×4+300min×1；02:18 与 KO 预测精确命中）；当前代 10-20 01:17 起，**下崩预计 ~05:48**。勿动 heap 上限（2GB 主机）。**新对策候选（10-19 发现）：headroom README 明列 `wrap openclaw`——先 doctor+savings 实测，按 eval-gap 判据验收**
- **⚠️ Gateway 取证口径**：cron 沙箱 `journalctl -u` 返回空、系统级 systemctl 同名 unit 得 NRestarts=0 是陷阱——真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- **✅ 注入层手术三日验证**：截断警告 10-18/10-19 持续归零；OOM 独立（根因=V8 堆，非注入）。**KO 纪律：MEMORY.md 超 ~15k 即归档瘦身**（当前 10.4k chars / 14.9k bytes ✅）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 27+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（10-20 02:00）：mem avail 878MB / 磁盘 68% / uptime 180d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；270min 节拍器化已连续 2 日是强证据；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓历史笔记 untracked**（08-24 起 6+ 篇）——下次手动窗口批量 commit

### 中优先级（详情见 10-18~10-19 daily + trending 报告）
- [ ] **headroom doctor+savings 实测**（`wrap openclaw` 官方支持；OOM/token 双痛点对准）
- [ ] **49 技能 eval-gap 对照实验**（10-19 essay 承诺排下周；API 封装类先写 20 道判分题再决定去留）
- [ ] **20 题归档召回基线**（10-18 essay：dreaming/压缩改动必须过 recall eval 的量尺）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（10-19 深研 next：metaproductivity 台账最小版）
- [ ] **hindsight vs amg 对标实验**（arXiv 2512.12818）；**ai-memory 试用**（跨 harness 记忆总线，死信区对照）
- [ ] **Agent-Reach 试装升级**（⚠️ 连续 12 天未执行，已飞书罗嵩待排期）
- [ ] **amg 实验四连**：3-layer 渐进披露 / claude-mem 集成对比 / EvidenceLedger 工具化 / 压缩悖论三件
- [ ] **amg PPR 对照臂**（Zep LME +18.5% 参照）+ acs 双时间戳；**orca worktree fan-out 评估**（mission-control 借鉴）
- [ ] **AGENTS.md/MEMORY.md 按 ACE 改造**（bullet+计数器；瘦身已走第一步）
- [ ] **研究 cron 加停搜判据**（R1-Searcher++ 式自检省 30% 检索）
- [ ] MCP 安全清单+tool 哈希锁 · vercel-labs/skills 精读 · context-mode 插件试装 · VoiceStudio MCP 接入 · paperclip budget→mission-control
- [ ] amg kd 手动续跑（queue 4 候选+纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；零回滚 364 天；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量）
- **gateway**：当前代 10-20 01:17 启动；**下崩预计 10-20 ~05:48**（270min 家族）
- **KO 日历**：10-17 ✅（瘦身 158k→8.7k）→ 10-18 ✅ → 10-19 ⚠️（dashboard 标 error 230s 但实质完成 cf165c6）→ **10-20 ✅（本 run：第 22 日整合）**

## 近期活动（10-18 ~ 10-19，第 21/22 纯内容日）
- **10-18**：essay《访问加权衰减两次翻车》a7a1f1d（提及≠访问）· trending 飞书 ai-memory/xerj 深挖 · creative android/skills Google 官方入场 · 深研 Deep Research RL 06dd90e · dashboard 7/7 day 2
- **10-19**：essay《Google 官方给 Agent 写技能》3cbb060（eval-gap 判据+49 技能自查）· trending 飞书 TUW4d5aD（ai-memory×orca）· creative rea 329k★ 集群+headroom 点名 openclaw · 深研 Self-Evolving Agents 612affa · dashboard 6/7（全绿 streak 终结 day 3）

## 本周关键路径
1. ✅ 内容线连续 22 日；⬜ 上游 issue 报告（置顶，节拍器化×2 日证据已足）
2. ⬜ headroom 实测（OOM 对策候选）+ 49 技能对照实验（essay 承诺）
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（PPR 臂/20 题召回基线/ai-memory 对照）— 待罗嵩排期

## 上次检查
- **KO 2026-10-20 02:00（本 run）**：✅ 10-19 整合（第 22 纯内容日，零回滚 364）+ NRestarts=92 取证（10-19 五代节拍）+ MEMORY 补 10-19/压缩 10-16 链（10.4k chars）+ HEARTBEAT 全刷新
- KO 2026-10-19 02:00：✅ 第 21 日整合+daily 补录 2 条 + NRestarts=86 取证（dashboard 后标 error 230s，实质完成）
- KO 2026-10-18 02:00：✅ 警告消失预测验证 + journalctl 沙箱陷阱口径修正（TOOLS.md）
- KO 2026-10-17 02:00：✅ MEMORY.md 大瘦身 158k→8.7k（全文归档）
