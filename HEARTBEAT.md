# HEARTBEAT.md - 2026-11-22 02:00 KO（**11-21 7/7 ×5 连续五天全绿 / NRestarts=271 相位跳变 :48→:18 后重锁·预测 19 次 18 中 / MEMORY 净蒸馏兑现 19552B 余量 448B**）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故已关闭**（11-15~16 窗口 8 run 失败；11-17~21 连续五天 7/7 全绿，consec 零）。若凌晨档再限流按新事故处理（错峰/降模型需罗嵩知情）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=271（11-22 02:00；265→271，+6/24h）**；11-21 七拍 00:48/04:48/08:48/**13:18**/17:18/21:18 + 11-22 01:18——**13:18 首现 4h30m 相位跳变（:48→:18），随后以 :18 重锁 4h00m±1s**；**04:48 预测再命中（04:48:14；累计 19 次 18 中）**。当前代 11-22 01:17:47 起，**下崩预计 ~05:18±25min（11-22，本 run 后 ~3h18m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19552B**（20k 线内，余量 448B）：本 run **净蒸馏兑现承诺**（19917→19552，新增 11-21 链+常驻税/CUA 两 insight+研究表行；压缩=11-01~08 三链合一、11-09~19 五链减脂、验证器/科学发现/轨迹/思考预算/做梦/CLM/CUA11-10 七 insight 减脂、研究表仍 5 行；Python 链路第二十天，锚点全过）。**下次 KO 目标：净增量 ≤400B 或再蒸馏**（候选：11-19~20 链合并、做梦/习得 CLM insight 再减脂）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-22 02:00）：mem avail **809MB**（当前代 43m 龄）/ 磁盘 69% / uptime 213d / load 0.19

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 节律+预测 19 次 18 中+13:18 相位跳变新证据；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 76 项**（笔记 75 + code/1；内部仓上次 commit 停在 11-04 f6a146a）——下次手动窗口批量 commit

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-21 落点**：①ffmpeg-skill：SPEC 自生成契约（argparse 单源派生 input_schema+CI 防漂移）→sot/自建 MCP 返回设计参照；MCP 默认广告 12/42=工具面税第三方实证 ②CLI-Anything --help 按需披露 vs MCP schema 常驻税=上下文财政系列续篇候选 ③superpowers 四哲学与 AGENTS.md Karpathy 原则逐条对映→对照笔记 ④CLI-Hub meta-skill（ClawHub）入试装队列 ⑤CUA 双轨终局（关键路径 MCP/API、长尾像素）与 11-05 无障碍树互证
- [ ] **11-20 落点**：①trading-skills 偷师三点（workflow manifest→finance-news-pro；纪律门禁输出「姿态+置信度」；skills-index canonical 索引）②opensre「修 CI」空档位：CI-caused vs code-caused 分离+cron 失败自动归因 ③autoclip=「MCP 即产品 API」信号 ④chrome-devtools-mcp 七原则→sot 返回设计评审 ⑤**深研选题先 grep 博客 index 覆盖**（已固化）
- [ ] **11-19 落点（折叠）**：last30days 三点/BugHunter 包管理范本/paper-orchestra 质量门禁/做梦五动作（失效墓碑+夜间整固+nx.pagerank 试点）
- [ ] **11-17~18 落点（折叠）**：SkillEvaluator 门禁/ag-ui 1.0→canvas-A2UI/轨迹飞轮五动作/MWG 修剪→49 技能盘点/思考预算五动作
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 33 天 ⚠️⚠️⚠️；SkillEvaluator=现成尺子）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron（与做梦五动作②同源）
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续二十天顺畅）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 45 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）；trading-skills 同域参照
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / plannotator / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / last30days-skill / BugHunter / claude-trading-skills / opensre / autoclip / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review（delegation 零 key）/ chrome-devtools-mcp skills / ffmpeg-skill（优先，与 video-frames 同域）/ app-store-compliance（hook 模式参考）/ CLI-Hub meta-skill（11-21 晨析）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-21 连续错开 ✅；深研 index grep 规则执行中）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 397 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-22 01:17:47 启动；**下崩预计 ~05:18±25min（11-22）**（13:18 相位跳变后 :18 重锁 4h00m±1s；预测 19 次 18 中）
- **cron 健康**：7 job 全在列；11-21 全绿 ×5（dashboard 口径连续第五天 7/7）
- **KO 日历**：11-16 ❌ rate_limit（史上首次）→ 11-17 ✅ → 11-18 ✅ → 11-19 ✅ → 11-20 ✅ → 11-21 ✅ → **11-22 ✅（本 run；Python 链路第二十天）**
- **博客**：11-21 三 commit（e04532a essay MCP 常驻税/d4bd2c0 dashboard 全绿第五天/214770e 深研 CUA 悬崖）；**496 html posts**；master 与 origin 同步；两新 post 200 ✓ index 引用 ✓
- **posts 口径注**：html-only=496；git tracked=498（含 2 .bak）——历史记录混用两口径，以 html-only 为准

## 近期活动（11-20 ~ 11-21）
- **11-21（7/7 ×5，第 53 纯内容日 ✅）**：essay MCP 常驻税 e04532a（上下文财政：58 工具 55K token 常驻/三重伤害/供给侧三原则/defer_loading 85%/中转税）·dashboard d4bd2c0（全绿第五天；metronome day 36）·trending-deep ✅ 飞书 DLSVdF（CLI-Anything 61.4k★ 七阶段生成器+~80 harness+CLI-Hub；superpowers 322.8k★ 15 技能 SDLC+bootstrap 注入+drill eval）·creative ✅（ffmpeg-skill 9k★ SPEC 自生成契约+12/42 按需披露；app-store-compliance 117 拒审模式+PreToolUse hook）·深研 CUA 长任务悬崖 214770e（OSWorld 断层/状态维持/思考税/攻击面/双轨终局；20 源）
- **11-20（7/7 ×4，第 52 日 ✅）**：essay 大纲即合同 5e1eb2e·dashboard f3febbf·trending-deep 飞书 GoZg（open-code-review/chrome-devtools-mcp）·creative ✅（trading-skills/opensre/autoclip）·深研图算法求解器 733b064（NP-large<10%/GCoder+16.42%/选题先 grep 教训）
- 11-19 及更早（7/7 ×3~）：essay 环境即接口/深研记忆做梦等——详见当日 daily 与 MEMORY 链条

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包已齐+19 次 18 中+相位跳变新料）
2. ⬜ 49 技能对照实验（超期 33 天 ⚠️；SkillEvaluator=现成尺子）+ headroom 决策
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（RRF A/B / 边三列时间戳 / 夜间整固 cron / 判官三件套体检 / 轨迹+思考预算五动作）+ 引用锁溯源落地 — 待罗嵩排期
5. ⬜ catalyst-research 76 项 untracked 批量 commit（下次手动窗口）
6. ✅ MEMORY.md 11-22 净蒸馏兑现（19917→19552B，余量 83→448B）

## 上次检查
- **KO 2026-11-22 02:00（本 run）**：✅ 11-21 全线 7/7 确认（cron 七 job+博客三 commit 496 posts+两新 post 200）+ Gateway 271/相位跳变观测+预测 19 次 18 中 + MEMORY 净蒸馏 + HEARTBEAT 全刷新 + 建 11-22 daily + 11-21 daily 补 06:00/07:00 条目并去重
- KO 2026-11-21 02:00：✅ 11-20 全绿 ×4 确认+MEMORY 增量整合（19356→19917B；余量 83B 警告→本 run 兑现蒸馏）
- KO 2026-11-20 / 11-19 / 11-18 / 11-17 02:00：✅ 实质蒸馏/恢复确认/事故关闭/双日整合
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- KO 2026-11-15 ~ 11-10 02:00：✅ 第 48~43 日整合
- 更早（10-17~11-09）：✅ 详见各日 daily
