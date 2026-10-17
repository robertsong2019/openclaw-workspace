# HEARTBEAT.md - 2026-10-18 02:00 KO（第 20 纯内容日整合 + 警告消失预测兑现）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊，10-15）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=81（10-18 02:00）；10-17 全天 10 代；当前代 10-17 23:17 起 RSS 958MB@2.7h**。勿动 heap 上限（2GB 主机）。上游 issue 报告挂账置顶
- **⚠️ Gateway 取证口径（10-18 实测）**：cron 沙箱 `journalctl -u` 返回空、系统级 systemctl 同名 unit 得 NRestarts=0 是陷阱——真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- **✅ 警告消失预测兑现**：MEMORY.md 瘦身（10-17 02:02）后首个干净代（10-17 05:38 起）「MEMORY.md is N chars」零复发，39 天 1,802 次警告后首次静默。但 OOM 未缓解（根因=V8 堆，非注入）。**KO 纪律：MEMORY.md 超 ~15k 即归档瘦身**
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 27+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（10-18 02:00）：mem avail 604MB / 磁盘 69% / uptime 178d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓历史笔记 untracked**（08-24 起 6+ 篇）——下次手动窗口批量 commit

### 中优先级（详情见 10-15~10-17 daily + trending 报告）
- [ ] **hindsight vs amg 对标实验**（arXiv 2512.12818；判卷人钉环外）；**ai-memory 试用**（10-17：跨 harness 记忆总线+访问加权衰减，死信区对照）
- [ ] **Agent-Reach 试装升级**（⚠️ 连续 10 天未执行，已飞书罗嵩待排期）
- [ ] **amg 实验四连**：3-layer 渐进披露 / claude-mem 集成对比 / EvidenceLedger 工具化 / 压缩悖论三件
- [ ] **amg PPR 对照臂**（Zep LME +18.5% 参照）+ acs 双时间戳；**orca worktree fan-out 评估**（10-17，mission-control 借鉴）
- [ ] **AGENTS.md/MEMORY.md 按 ACE 改造**（bullet+计数器；瘦身已走第一步）
- [ ] MCP 安全清单+tool 哈希锁 · 睡眠期记忆蒸馏 heartbeat pass · vercel-labs/skills 精读 · context-mode 插件试装 · VoiceStudio MCP 接入 · paperclip budget→mission-control
- [ ] amg kd 手动续跑（queue 4 候选+纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；零回滚 362 天；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量）
- **gateway**：当前代 10-17 23:17 启动；RSS 958MB；下崩预计 10-18 03~05 时段（上次同型代 270min 家族）
- **KO 日历**：10-14 ✅ → 10-15 ✅ → 10-16 ❌（600s 超时）→ 10-17 ✅（瘦身 158k→8.7k）→ **10-18 ✅（本 run：预测验证+口径修正）**

## 近期活动（10-16 ~ 10-17，第 19/20 纯内容日）
- **10-16**：essay《宿主每 4.5h 死一次》22d2294 · trending rea+superpowers · 深研 ACE d6d6e66 · dashboard c5230da
- **10-17**：KO 瘦身 158k→8.7k · essay《83% 读不到的笔记》aee7540 · trending context-mode/xerj/ai-memory/orca · 深研 CUA ffce7e9+博文 5ad7d9a

## 本周关键路径
1. ✅ 内容线连续 20 日；⬜ 上游 issue 报告（置顶）
2. ⬜ README/publish 四项目 — BLOCKED on human
3. ⬜ amg next（PPR 臂/压缩悖论三件/ai-memory 对照）— 待罗嵩排期
4. ⬜ 双 cron 线索落地（Agent-Reach/vercel skills/ACE 改造/orca 模式，见中优先级）

## 上次检查
- **KO 2026-10-18 02:00（本 run）**：✅ 10-17 整合（第 20 纯内容日，零回滚 362）+ NRestarts=81 取证 + 警告消失预测验证 + journalctl 沙箱陷阱口径修正（TOOLS.md）+ HEARTBEAT 全刷新
- KO 2026-10-17 02:00：✅ MEMORY.md 大瘦身 158k→8.7k（全文归档）
- KO 2026-10-16 02:00：❌ 600s 超时被杀（10-17 修复）
