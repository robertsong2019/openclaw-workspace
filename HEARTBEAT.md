# HEARTBEAT.md - 2026-11-23 02:00 KO（**11-22 7/7 ×6 连续六天全绿 / NRestarts=277 两拍漂移+两次 :48→:18 相位跳变·预测 20 次 19 中 / MEMORY 增量整合 19831B 余量 169B**）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故已关闭**（11-15~16 窗口 8 run 失败；11-17~22 连续六天 7/7 全绿，consec 零）。若凌晨档再限流按新事故处理（错峰/降模型需罗嵩知情）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=277（11-23 02:00；271→277，+6/24h）**；11-22 七拍 01:18/05:35/08:48/12:48/16:48/20:48+11-23 01:18——间隔 **4h17m/3h12m/4h00m×3/4h30m 两拍漂移**、**两次 :48→:18 相位跳变**（13:18 首例后 20:48→01:18 再现，:48↔:18 双相稳态）；**05:18±25 预测命中（实际 05:35；累计 20 次 19 中）**。当前代 11-23 01:17:47 起，**下崩预计 ~05:18±25min（11-23，本 run 后 ~3h18m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19831B**（20k 线内，余量 169B）：本 run 增量整合（19552→19831，净 +279B 兑现 ≤400B 承诺；新增 11-22 链+披露时序/多智能体边界两 insight+研究表 11-22 行；压缩=11-19~20 链合并、做梦/CLM/图算法/常驻税/CUA/reward-hacking 六 insight 减脂、研究表删 11-17/11-18 行；Python 链路第二十一天，15 锚点全过）。**下次 KO 目标：净增量 ≤300B 或再蒸馏**（候选：11-17~18 链合并进 11-19~20、思考预算/轨迹飞轮 insight 减脂）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-23 02:00）：mem avail **829MB**（当前代 43m 龄）/ 磁盘 69% / uptime 214d / load 0.04

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 节律+预测 20 次 19 中+两次相位跳变双相稳态新证据；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 77 项**（笔记 76 + code/1；内部仓上次 commit 停在 11-04 f6a146a）——下次手动窗口批量 commit
- [ ] **⚠️ 试装 plannotator Inbox（本周最高优先级，11-22 晚行动项）**——显式支持 OpenClaw，可当 cron/heartbeat 流的 HITL 投递门禁；按「非冗余审查」判据设计（与多智能体三问合流）

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-22 落点**：①subagent/并发调用前三问检查清单（共享只读/上下文自足/固定判据合成——多智能体边界结论落地）②CLI-Hub meta-skill 本周试装（cli-hub list 消费端；VPS 公共 pip/npm CLI 可装、桌面后端类内存受限）③minimind 64M ollama 推理 VPS 可行（fp16 ~128MB）④astryx「对 AI 更容易=对人也更容易」=agent-ready 基建三例链第三例 ⑤HITL 基础设施自成一层（ag-ui 协议+plannotator 产品+Herdr TUI）
- [ ] **11-21 落点**：①ffmpeg-skill：SPEC 自生成契约（argparse 单源派生 input_schema+CI 防漂移）→sot/自建 MCP 返回设计参照 ②superpowers 四哲学与 AGENTS.md Karpathy 原则对映→对照笔记 ③CUA 双轨终局与 11-05 无障碍树互证
- [ ] **11-20 落点（折叠）**：trading-skills 偷师三点/opensre CI 归因/autoclip=「MCP 即产品 API」/chrome-devtools-mcp 七原则→sot 评审/**深研选题先 grep index 已固化**
- [ ] **11-17~19 落点（折叠）**：SkillEvaluator 门禁/ag-ui 1.0→canvas-A2UI/last30days 三点/BugHunter 包管理范本/做梦五动作（失效墓碑+夜间整固+nx.pagerank 试点）
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 34 天 ⚠️⚠️⚠️；SkillEvaluator=现成尺子）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron（与做梦五动作②同源）
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续二十一天顺畅）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 46 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）；trading-skills 同域参照
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / **plannotator（🔴 优先）** / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / last30days-skill / BugHunter / claude-trading-skills / opensre / autoclip / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review（delegation 零 key）/ chrome-devtools-mcp skills / ffmpeg-skill（优先，与 video-frames 同域）/ app-store-compliance（hook 模式参考）/ CLI-Hub meta-skill
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-22 连续错开 ✅；深研 index grep 规则执行中）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 398 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-23 01:17:47 启动；**下崩预计 ~05:18±25min（11-23）**（11-22 两拍漂移后 :18 相位；预测 20 次 19 中）
- **cron 健康**：7 job 全在列；11-22 全绿 ×6（dashboard 口径连续第六天 7/7）
- **KO 日历**：11-16 ❌ rate_limit（史上首次）→ 11-17~22 ✅×6 → **11-23 ✅（本 run；Python 链路第二十一天）**
- **博客**：11-22 三 commit（b9628cc essay 披露时序/61d54ba dashboard 全绿第六天/5cd6804 深研多智能体边界）；**498 html posts**（+2）；master 与 origin 同步；两新 post 200 ✓ index 引用 ×4 ✓
- **posts 口径注**：html-only=498 为准（git tracked≈500 含 2 .bak）——dashboard 06:00 报的 497→499 系其自身快照口径，以 ls 实数为准
- **workspace monorepo**：本 KO 已补 push（此前 11-22 05:00/08:00 两 commit 未推，现全同步）

## 近期活动（11-21 ~ 11-22）
- **11-22（7/7 ×6，第 54 纯内容日 ✅）**：essay 披露时序 b9628cc（披露时序=定价机制/SPEC 投影永不漂移实测/最小稳定索引三纪律/决策矩阵）·dashboard 61d54ba（全绿第六天；metronome day 37 相位切换+两拍漂移）·trending-deep ✅ 飞书 F3aIdl（CLI-Anything 62.1k★ HARNESS.md 方法论+CLI-Hub；minimind 68.1k★ 64M MoE 3090 可训）·creative ✅（plannotator 14.3k★ Inbox 异步 HITL **显式支持 OpenClaw**；astryx 32k★ Meta agent-first 设计系统）·深研多智能体边界 5cd6804（耦合度唯一先验/MAST/Self-MoA/侵蚀效应/动手三问；12+ 源）
- **11-21（7/7 ×5，第 53 日 ✅）**：essay MCP 常驻税 e04532a·dashboard d4bd2c0·trending-deep 飞书 DLSVdF（CLI-Anything+superpowers）·creative ✅（ffmpeg-skill SPEC 契约/app-store-compliance）·深研 CUA 长任务悬崖 214770e（20 源）
- 11-20 及更早（7/7 ×3~4）：essay 大纲即合同/环境即接口、深研图算法+记忆做梦等——详见当日 daily 与 MEMORY 链条

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包已齐+20 次 19 中+双相稳态新料）
2. ⬜ **plannotator Inbox 试装**（11-22 行动项合流：HITL 门禁+非冗余审查判据）+ CLI-Hub 消费端
3. ⬜ 49 技能对照实验（超期 34 天 ⚠️）+ headroom 决策
4. ⬜ README/publish 四项目 — BLOCKED on human
5. ⬜ amg next（RRF A/B / 边三列时间戳 / 夜间整固 cron / 判官三件套体检）+ 引用锁溯源落地 — 待罗嵩排期
6. ⬜ catalyst-research 77 项 untracked 批量 commit（下次手动窗口）
7. ✅ MEMORY.md 11-23 增量整合（19552→19831B，净 +279B ≤400B 承诺兑现）

## 上次检查
- **KO 2026-11-23 02:00（本 run）**：✅ 11-22 全线 7/7 确认（cron 七 job+博客三 commit 498 posts+两新 post 200）+ Gateway 277/两拍漂移+双相位跳变+预测 20 次 19 中 + MEMORY 增量整合 + HEARTBEAT 全刷新 + 建 11-23 daily + 11-22 daily 补 06:00/07:00 条目 + workspace 补 push
- KO 2026-11-22 02:00：✅ 11-21 全绿×5 确认+MEMORY 净蒸馏兑现（19917→19552B 余量 83→448B）
- KO 2026-11-21 / 11-20 / 11-19 / 11-18 / 11-17 02:00：✅ 增量整合/实质蒸馏/恢复确认/事故关闭/双日整合
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- KO 2026-11-15 ~ 11-10 02:00：✅ 第 48~43 日整合
- 更早（10-17~11-09）：✅ 详见各日 daily
