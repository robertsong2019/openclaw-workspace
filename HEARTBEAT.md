# HEARTBEAT.md - 2026-11-24 02:00 KO（**11-23 7/7 ×7 连续七天全绿 / NRestarts=283 相位 :18→:36 往返一跳后重锁·预测 21 次 20 中 / MEMORY 强制净蒸馏兑现 19785B 余量 215B**）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故已关闭**（11-15~16 窗口 8 run 失败；11-17~23 连续七天 7/7 全绿，consec 零）。若凌晨档再限流按新事故处理（错峰/降模型需罗嵩知情）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=283（11-24 02:00；277→283，+6/24h 稳定）**；11-23 六拍 01:18/05:36/09:18/13:18/17:18/21:18+11-24 01:18——间隔 **4h18m/3h41m/4h00m×4**、相位 :18→:36 往返一跳后 :18 重锁（双相稳态持续）；**05:18±25 预测边缘命中（实际 05:36:44，+18.7min；累计 21 次 20 中）**。当前代 11-24 01:17:47 起，**下崩预计 ~05:18±25min（11-24，本 run 后 ~3h18m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19785B**（20k 线内，余量 215B）：本 run **强制净蒸馏兑现**（19831→19785，净 -46B；新增 11-23 链+HITL 收件箱化/技能合成治理两 insight+研究表 11-23 行；压缩=11-09~14 六链合并、11-17~22 五链减脂、11-03/11-06/10-22~25 三 insight 减脂、研究表删 11-19/11-20 行；Python 链路第二十二天，6+2 探针全过）。**下次 KO 目标：净增量 ≤200B 或再蒸馏**（候选：Key Insights #1-262 两段再蒸馏、归档索引行合并）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-24 02:00）：mem avail **925MB**（当前代 ~43m 龄）/ 磁盘 69% / uptime 216d / load 0.00

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 节律+预测 21 次 20 中+相位双相稳态证据；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 78 项**（笔记 77 + code/1；内部仓上次 commit 停在 11-04 f6a146a）——下次手动窗口批量 commit
- [ ] **⚠️ 试装 plannotator Inbox（本周最高优先级，11-22 晚行动项）**——显式支持 OpenClaw，可当 cron/heartbeat 流的 HITL 投递门禁；按「非冗余审查」判据设计（与多智能体三问合流）

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-23 落点**：①**存量技能过 SkillGen 干预模型**（repairs−regressions 净效应计算——与 49 技能超期实验合流，方法论已就位）②技能蒸馏例程走 SkillRevise 式修订闭环（执行锚定+失败反馈+最优版保留，不做静态总结）③写技能四硬规范（description what+when / ≤3 模块 / 代码进 scripts 输出进上下文 / 长参考拆文件）④第三方装前三查锁版本（scripts 网络调用清单/NL 注入迹象/frontmatter 预授权）⑤黑市情报：ClawHavoc 335 恶意+22-26% 漏洞——skillhub/clawhub 安装纪律收紧
- [ ] **11-22 落点**：①subagent/并发调用前三问检查清单（共享只读/上下文自足/固定判据合成——多智能体边界结论落地）②CLI-Hub meta-skill 本周试装（cli-hub list 消费端）③minimind 64M ollama 推理 VPS 可行（fp16 ~128MB）④HITL 基础设施自成一层（ag-ui 协议+plannotator 产品+Herdr TUI）
- [ ] **11-21 落点**：①ffmpeg-skill：SPEC 自生成契约（argparse 单源派生 input_schema+CI 防漂移）→sot/自建 MCP 返回设计参照 ②superpowers 四哲学与 AGENTS.md Karpathy 原则对映→对照笔记 ③CUA 双轨终局与 11-05 无障碍树互证
- [ ] **11-20 落点（折叠）**：trading-skills 偷师三点/opensre CI 归因/autoclip=「MCP 即产品 API」/chrome-devtools-mcp 七原则→sot 评审/**深研选题先 grep index 已固化**
- [ ] **11-17~19 落点（折叠）**：SkillEvaluator 门禁/ag-ui 1.0→canvas-A2UI/last30days 三点/BugHunter 包管理范本/做梦五动作（失效墓碑+夜间整固+nx.pagerank 试点）
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 35 天 ⚠️⚠️⚠️；**SkillGen 干预模型=现成方法论**，与 11-23 落点①合流后是最佳启动时机）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron（与做梦五动作②同源）
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续二十二天顺畅）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 47 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）；trading-skills 同域参照
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / **plannotator（🔴 优先）** / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / last30days-skill / BugHunter / claude-trading-skills / opensre / autoclip / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review（delegation 零 key）/ chrome-devtools-mcp skills / ffmpeg-skill（优先，与 video-frames 同域）/ app-store-compliance（hook 模式参考）/ CLI-Hub meta-skill
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-23 连续错开 ✅；深研 index grep 规则执行中）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 399 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-24 01:17:47 启动；**下崩预计 ~05:18±25min（11-24）**（11-23 :18→:36 往返一跳后 :18 重锁；预测 21 次 20 中）
- **cron 健康**：7 job 全在列；11-23 全绿 ×7（dashboard 口径连续第七天 7/7）
- **KO 日历**：11-16 ❌ rate_limit（史上首次）→ 11-17~23 ✅×7 → **11-24 ✅（本 run；Python 链路第二十二天）**
- **博客**：11-23 三 commit（69cdea3 essay HITL 收件箱化/73acd20 dashboard 全绿第七天/6759a2a 深研技能合成治理黑市）；**500 html posts**（+2）；master 与 origin 同步；两新 post 200 ✓
- **workspace monorepo**：本 KO 提交 MEMORY+HEARTBEAT+11-23 daily（补记 06:00/07:00/20:00）+11-23 evening 报告+11-24 daily

## 近期活动（11-22 ~ 11-23）
- **11-23（7/7 ×7，第 55 纯内容日 ✅）**：essay HITL 收件箱化 69cdea3（同步审批三死结/revision 漂移/四验收）·dashboard 73acd20（全绿第七天；metronome day 38 相位往返一跳）·trending-deep ✅ 飞书 DffGdyq（cursor/plugins 18.4k★+Claude-BugHunter 83 skills 漏洞挖掘包）·creative ✅（alibaba/open-code-review AACR-Bench 回归/univer v1.6 两连版/plannotator README 确认 Inbox 支持 OpenClaw）·深研技能合成治理黑市 6759a2a（SkillsBench 会消费≠会编写/SkillWeaver 练车闭环/SkillGen 干预模型/SkillRevise 36→62/ClawHavoc 黑市三重攻击面；15+ 源）
- **11-22（7/7 ×6，第 54 日 ✅）**：essay 披露时序 b9628cc·dashboard 61d54ba·trending-deep 飞书 F3aIdl（CLI-Anything+minimind）·creative ✅（plannotator Inbox HITL+astryx）·深研多智能体边界 5cd6804（12+ 源）
- 11-21 及更早（7/7 ×5）：essay MCP 常驻税、深研 CUA 长任务悬崖 214770e 等——详见当日 daily 与 MEMORY 链条

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包已齐+21 次 20 中+双相稳态新料）
2. ⬜ **plannotator Inbox 试装**（11-22 行动项合流：HITL 门禁+非冗余审查判据）+ CLI-Hub 消费端
3. ⬜ **49 技能对照实验**（超期 35 天 ⚠️；SkillGen 干预模型方法论就位=最佳启动时机）
4. ⬜ README/publish 四项目 — BLOCKED on human
5. ⬜ amg next（RRF A/B / 边三列时间戳 / 夜间整固 cron）+ 引用锁溯源落地 — 待罗嵩排期
6. ⬜ catalyst-research 78 项 untracked 批量 commit（下次手动窗口）
7. ✅ MEMORY.md 11-24 强制净蒸馏兑现（19831→19785B，净 -46B；余量 215B）

## 上次检查
- **KO 2026-11-24 02:00（本 run）**：✅ 11-23 全线 7/7 确认（cron 七 job+博客三 commit 500 posts+两新 post 200）+ Gateway 283/:18→:36 往返一跳重锁/预测 21 次 20 中 + MEMORY 强制净蒸馏 + HEARTBEAT 全刷新 + 建 11-24 daily + 11-23 daily 补 06:00/07:00/20:00 三条
- KO 2026-11-23 02:00：✅ 11-22 全绿×6 确认+MEMORY 增量整合（19552→19831B）
- KO 2026-11-22 02:00：✅ 11-21 全绿×5+净蒸馏兑现（余量 83→448B）
- KO 2026-11-21 / 11-20 / 11-19 / 11-18 / 11-17 02:00：✅ 增量整合/实质蒸馏/恢复确认/事故关闭/双日整合
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- KO 2026-11-15 ~ 11-10 02:00：✅ 第 48~43 日整合
- 更早（10-17~11-09）：✅ 详见各日 daily
