# HEARTBEAT.md - 2026-10-17 02:00 KO（第 19 纯内容日整合 + MEMORY 大瘦身）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）。cosmetic：tencentdb stale plugin warning 待清理
- **Gateway OOM（确诊，10-15）**：V8 堆耗尽 ABRT，~270min 周期，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=76（10-17 02:00；10-16 五崩 01:47→19:47；10-17 00:17 又崩）**。勿动 heap 上限（2GB 主机）。上游 issue 报告挂账置顶
- **✅ 10-17 KO 完成 MEMORY.md 大瘦身**：158,216→8,696 chars（限 20k）。全文备份 memory/archive-2026-10-17-memory-slim-full.md。此前 10-16 02:00 KO 即因处理 158k 文件 600s 超时被杀——本 run 修复该根因。**KO 后续纪律：MEMORY.md 超 ~15k 即归档瘦身，勿逐日堆叠**
- ⚠️ memory/ 8 月底-9 月初 daily 文件存在未提交整文件改写（挂 27+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（10-17 02:00）：mem avail 754MB / 磁盘 68% / uptime 177d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal 取证在手；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 10 篇笔记 untracked**（10-02 起）——下次手动窗口批量 commit

### 中优先级（按新鲜度压缩；详情见 10-14/10-15/10-16 daily + trending 报告）
- [ ] **hindsight vs amg 对标实验**（arXiv 2512.12818；判卷人钉环外）
- [ ] **Agent-Reach 试装升级**（⚠️ 连续 9 天未执行，已飞书罗嵩待排期）
- [ ] **amg 实验四连**：3-layer 渐进披露 / claude-mem 集成对比 / EvidenceLedger 工具化 / 压缩悖论三件（raw+on-demand 臂·file-first·双口径）
- [ ] **amg PPR 对照臂**（10-15 深研：Zep LME +18.5% 参照）+ acs 双时间戳
- [ ] **AGENTS.md/MEMORY.md 按 ACE 改造**（10-16 深研：bullet+计数器；瘦身已走第一步）
- [ ] MCP 安全清单+tool 哈希锁（10-13 深研）· 睡眠期记忆蒸馏 heartbeat pass（10-14）· vercel-labs/skills 精读 · context-mode 插件试装（ELv2）· VoiceStudio MCP 接入 · paperclip budget→mission-control · dream loop 三连
- [ ] amg kd 手动续跑（queue 4 候选+纪律见 MEMORY「kd 手动续跑」节；或罗嵩重建 cron）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；零回滚 361 天（359@10-14 KO+两纯内容日）；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量）
- **gateway**：当前代 10-17 00:17 启动；RSS 792MB（peak 1.0G）
- **KO 日历**：10-13 ✅ → 10-14 ✅ → 10-15 ✅ → 10-16 ❌（600s 超时，MEMORY 158k 根因）→ **10-17 ✅（本 run：瘦身 158k→8.7k）**

## 近期活动（10-15 ~ 10-16，第 18/19 纯内容日）
- **10-15**：gateway 根因确诊（V8 堆耗尽，两次伪结论反转）· 飞书 iFixAi×VoiceStudio · creative token 经济学四连击 · 深研图记忆 13 系统（720e15f）
- **10-16**：essay OOM 取证《宿主每 4.5h 死一次》22d2294 · trending rea 架构+superpowers 299.9k · 深研 ACE d6d6e66 · dashboard c5230da（6/7，KO 超时）· evening creative ok

## 本周关键路径
1. ✅ 内容线连续 19 日；⬜ 上游 issue 报告（置顶）
2. ⬜ README/publish 四项目 — BLOCKED on human
3. ⬜ amg next（PPR 对照臂/压缩悖论三件/nightly consolidation）— 待罗嵩排期或手动 kd 窗口
4. ⬜ 双 cron 线索落地（Agent-Reach/vercel skills/睡眠蒸馏/ACE 改造等，见中优先级）

## 上次检查
- **KO 2026-10-17 02:00（本 run）**：✅ MEMORY.md 大瘦身 158k→8.7k（全文归档 archive-2026-10-17-memory-slim-full.md）+ HEARTBEAT 全刷新 + 10-17 daily log 落盘；gateway NRestarts 76 取证；测试计数维持
- KO 2026-10-15 02:00：整合 10-14 全绿；gateway 根因确诊置顶
- KO 2026-10-16 02:00：❌ 600s 超时被杀（MEMORY 158k 处理超时）→ 本 run 修复
