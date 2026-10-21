# HEARTBEAT.md - 2026-10-22 02:00 KO（第 24 纯内容日整合 + OOM NRestarts=102）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=102（10-22 02:00）**；10-21 全天 5 代 textbook（04:18/08:48/13:18/17:48/22:18，270min×4 精确无漂移；**04:18 KO 预测命中精确到秒=三连中，dashboard 08:48 亦中，节拍器化 4 日**）；当前代 10-21 22:17 起，**下崩预计 10-22 ~02:47**。勿动 heap 上限（2GB 主机）。对策候选 headroom 未装三理由已论证（10-20 essay），若装须先过 eval-gap 20 题配对实验
- **⚠️ Gateway 取证口径**：cron 沙箱 `journalctl -u` 返回空、系统级 systemctl 同名 unit 得 NRestarts=0 是陷阱——真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- **✅ 注入层手术五日验证**：截断警告 10-18 起持续归零（dashboard 10-21 口径 day 4）；OOM 独立（根因=V8 堆，非注入）。**KO 纪律：MEMORY.md 超 ~15k bytes 即归档/修剪**（当前 15.5k bytes ✅ 本次已修剪：kd queue/研究表压缩，10-17/10-18 逐日条目下沉归档）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 27+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（10-22 02:00）：mem avail **489MB ⚠️**（连续两日 <500MB，与 gateway 代际 RSS 增长相关）/ 磁盘 69% / uptime 182d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；270min 节拍器化 4 日、预测三连命中精确到秒是强证据；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓历史笔记 untracked**（08-24 起 6+ 篇）——下次手动窗口批量 commit

### 中优先级（详情见 10-20~10-21 daily + trending 报告）
- [ ] **49 技能 eval-gap 对照实验**（10-19 essay 承诺"排下周"=本周；API 封装类先写 20 道判分题再决定去留）
- [ ] **20 题归档召回基线**（10-18 essay：dreaming/压缩改动必须过 recall eval 的量尺）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（10-19 深研 next：metaproductivity 台账最小版）
- [ ] **headroom `wrap openclaw` 实测**（10-21 trending 官方支持再确认；仍须先过 20 题配对）/ **context-mode 本机试装**（单项目先试 ctx_execute，对照 context-forge）/ skills add security-audit 审计 workspace / SmartCrusher 方差判据→context-forge
- [ ] **hindsight vs amg 对标实验**（arXiv 2512.12818）；**ai-memory 试用**（跨 harness 记忆总线，死信区对照）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval（10-21：现实结果反哺=评测锚定现实）
- [ ] **Agent-Reach 试装升级**（⚠️ 连续 14 天未执行，已飞书罗嵩待排期）
- [ ] **amg 实验四连**：3-layer 渐进披露 / claude-mem 集成对比 / EvidenceLedger 工具化 / 压缩悖论三件
- [ ] **amg PPR 对照臂**（Zep LME +18.5% 参照）+ acs 双时间戳；**orca worktree fan-out 评估**（mission-control 借鉴）
- [ ] **AGENTS.md/MEMORY.md 按 ACE 改造**（bullet+计数器；瘦身已走第一步）
- [ ] **研究 cron 加停搜判据**（R1-Searcher++ 式自检省 30% 检索）
- [ ] **trending 选题查重**（晨间 trending 前先 grep 近 2 日报告的深挖对象；10-20 08:00 曾复选）
- [ ] MCP 安全清单+tool 哈希锁 · vercel-labs/skills 精读 · VoiceStudio MCP 接入 · paperclip budget→mission-control
- [ ] amg kd 手动续跑（queue 4 候选+纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 366 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量）
- **gateway**：当前代 10-21 22:17 启动；**下崩预计 10-22 ~02:47**（270min 家族）
- **KO 日历**：10-20 ✅（3cc354f 第 22 日）→ 10-21 ✅（0453798 第 23 日）→ **10-22 ✅（本 run：第 24 日整合）**
- **博客**：2 posts/24h（b6a12f1 orca + 55153ba 单租户），master 与 origin 同步

## 近期活动（10-20 ~ 10-21，第 23/24 纯内容日）
- **10-21**：essay×2——晨《97k 星的 Agent 编排器，只做两件笨事》b6a12f1（orca 终端接入层+PTY 三纪律+worktree fan-out）+ 晚《2026 年最火的 AI Agent，都只服务一个人》55153ba（单租户 Agent OS 品类独立，深研笔记 13 系统对照）· trending 飞书 TpTVdtO1（security-audit-skill 34.1k★+headroom 官方 wrap openclaw）· creative：ai-job-search 62k★/VoiceStudio 79.6k★/context-mode 31.5k★ 显式支持 OpenClaw gateway；**rea 周净增首次减速** · dashboard 7/7 day 2
- **10-20**：essay《省 40% 的 token 账单却 3.3 倍》20cc992 · trending ZuHqd7rY（ai-memory×orca 复选）· creative ponytail/security-audit/graphify（OpenClaw 3 天被 4 项目点名）· 深研 MAST 40323e7 · dashboard 7/7 恢复

## 本周关键路径
1. ✅ 内容线连续 24 日；⬜ 上游 issue 报告（置顶，节拍器化 4 日+预测三连中证据已足）
2. ⬜ 49 技能对照实验（essay 承诺本周）+ headroom 决策（装前过 20 题配对）
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（PPR 臂/20 题召回基线/ai-memory 对照）— 待罗嵩排期

## 上次检查
- **KO 2026-10-22 02:00（本 run）**：✅ 10-21 整合（第 24 纯内容日，零回滚 366）+ NRestarts=102 取证（五代 textbook，04:18 预测三连中）+ MEMORY 增 10-21 条目/单租户+良性记忆安全债+对抗式审查洞察/研究表增行+修剪回 15.5k + HEARTBEAT 全刷新
- KO 2026-10-21 02:00：✅ 第 23 日整合 + NRestarts=97 + daily 补录 + MEMORY 15.0k
- KO 2026-10-20 02:00：✅ 第 22 日整合 + NRestarts=92（五代节律）
- KO 2026-10-19 / 10-18 / 10-17：✅ NRestarts=86 / 警告消失预测验证 / MEMORY 大瘦身 158k→8.7k
