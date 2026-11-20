# HEARTBEAT.md - 2026-11-21 02:00 KO（**11-20 7/7 ×4 连续四天全绿 / NRestarts=265 :48 石英锁定·预测 18 次 17 中 / MEMORY 19917B 增量整合后余量 83B**）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=晚间创新点日报，落盘 memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故已关闭**（11-15~16 窗口 8 run 失败；11-17~20 连续四天 7/7 全绿，consec 零）。若凌晨档再限流按新事故处理（错峰/降模型需罗嵩知情）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=265（11-21 02:00；259→265，+6/24h）**；11-20 六拍 00:48/04:48/08:48/12:48/16:48/20:48 **全 4h00m±2s（:48 石英锁定）**；**11-20 04:48 预测再命中（04:48:14；累计 18 次 17 中）**。当前代 11-21 00:47:47 起，**下崩预计 ~04:48±25min（11-21，本 run 后 ~2h48m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19917B**（20k 线内 99.6%，余量 83B ⚠️ 已紧）：本 run 新增 11-20 链条+图推理 insight+研究表 11-20 行（删 11-14 行）；压缩=11-15~16 折叠进 11-17、11-14 链条减脂、CUA/做梦/CLM insight 减脂（Python 链路第十九天，13+5 锚点两轮全过）。**下次 KO 必蒸馏**：11-03~09 链条合并、验证器/轨迹飞轮 insight 减脂、研究表只留 5 行
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-21 02:00）：mem avail **837MB**（当前代 1h13m 龄）/ 磁盘 69% / uptime 212d / load 0.04

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 石英节律+预测 18 次 17 中=强证据包；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 75 项**（笔记 74 + code/1；内部仓上次 commit 停在 11-04 f6a146a）——下次手动窗口批量 commit

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-20 落点**：①trading-skills 偷师三点（workflow manifest+strict validator 多技能编排→finance-news-pro 升级；纪律门禁输出「姿态+置信度」非结论；skills-index canonical 索引防文档漂移）②opensre「修 CI」空档位：CI-caused vs code-caused 分离+cron 失败自动归因 headless JSON 可嵌自家管线 ③autoclip 桌面应用 MCP 化=「MCP 即产品 API」信号 ④chrome-devtools-mcp 七原则（reference over value/token-optimized）→sot 与自建 MCP 返回设计评审 ⑤**深研选题先 grep 博客 index 覆盖**（已执行并固化为规则：skill 主题已 14 篇险撞车）
- [ ] **11-19 落点**：①last30days 偷师三点（多源交叉打分/agent-as-judge 提名过滤/Secret Signals 并入 trending cron）②BugHunter manifest+identical-skip+所有权保留=技能包管理范本 ③paper-orchestra 写作/反思分模型+大纲唯一中间表示+autoraters→essay 管线质量门禁 ④做梦五动作（失效墓碑+observed_at/写入扔夜间 cron/试点 nx.pagerank/一周流量三臂差分/发布评测披露 harness）
- [ ] **11-17~18 落点**（折叠）：SkillEvaluator 三层门禁/ag-ui 1.0→canvas-A2UI/LoopForge SOP→mission-control/轨迹飞轮五动作/MWG eval 修剪→49 技能盘点/思考预算五动作
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 32 天 ⚠️⚠️⚠️；SkillEvaluator=现成尺子）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron（与做梦五动作②同源）
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续十九天顺畅）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 44 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）；trading-skills 同域参照 11-20 落点①
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / plannotator / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / last30days-skill / BugHunter / claude-trading-skills / opensre / autoclip / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review（delegation 零 key）/ chrome-devtools-mcp skills
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-20 连续错开 ✅；深研新增 index grep 规则 11-20 起）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 396 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-21 00:47:47 启动；**下崩预计 ~04:48±25min（11-21）**（:48 相位石英 4h00m±2s；预测 18 次 17 中）
- **cron 健康**：7 job 全在列；11-20 全绿 ×4（dashboard 口径连续第四天 7/7）
- **KO 日历**：11-16 ❌ rate_limit（史上首次）→ 11-17 ✅ → 11-18 ✅ → 11-19 ✅ → 11-20 ✅ → **11-21 ✅（本 run；Python 链路第十九天，13+5 锚点两轮全过）**
- **博客**：11-20 三 commit（5e1eb2e essay 大纲即合同/f3febbf dashboard 全绿第四天/733b064 深研图推理）；**494 html posts**；master 与 origin 同步；两新 post 200 ✓ index 引用各 ×2 ✓
- **posts 口径注**：html-only=494；git tracked posts/=496（含 2 个 .bak）——历史记录混用两口径，以 html-only 为准

## 近期活动（11-19 ~ 11-20）
- **11-20（7/7 ×4，第 52 纯内容日 ✅）**：essay 大纲即合同 5e1eb2e（验证器系列第八篇：大纲=agent 间唯一合同 IDL/服务/私有实现之喻；写作反思分模型=被告不自任法官；autoraters 同仓同版本=citation_f1 回归测试；本文自身即大纲即合同试点）·dashboard f3febbf（全绿第四天；metronome day 35）·trending-deep ✅ 飞书 GoZg（open-code-review 确定性工程×agent 混合 token 1/9；chrome-devtools-mcp 63 工具+七原则 reference-over-value；skill 品类前 25 占 8）·creative ✅（claude-trading-skills 7.3k★ 金融垂直包：workflow manifest+strict 校验+纪律门禁+每笔交易 postmortem；opensre 修 CI 空档；autoclip 桌面 MCP 化；firecrawl 改口径 agent 知识基础设施）·深研 20:00 ✅ LLM 图算法求解器 733b064（GraphArena NP-large 全员<10%；GCoder 代码范式 +16.42%；不熟≠会 8B 追平；介质不匹配 CoT 反噬；笔记 11 源；⚠️ 选题教训：先 grep index 避开 14 篇 skill 文撞车）
- **11-19（7/7 ×3，第 51 日 ✅）**：essay 环境即接口 fabcf77·dashboard 0c0ecf2（全绿第三天）·trending-deep 飞书 JLQ3dP（BugHunter/paper-orchestra）·creative ✅（last30days-skill 70.5k★）·深研做梦记忆 d0868ee（bi-temporal/PPR/sleep-time/LME 罗生门）
- **11-18（7/7 ×2，第 50 日 ✅）**：essay npm 时刻 350679b·dashboard 5a508a8（首全绿）·trending-deep 飞书 X4LXdO·深研思考预算经济学 a31a5e2（11-17 恢复日详见当日 daily）

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包已齐+预测 18 次 17 中战绩）
2. ⬜ 49 技能对照实验（超期 32 天 ⚠️；SkillEvaluator=现成尺子）+ headroom 决策
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（RRF A/B / 边三列时间戳 / 夜间整固 cron / 判官三件套体检 / 轨迹飞轮+思考预算五动作）+ 引用锁溯源落地 — 待罗嵩排期
5. ⬜ catalyst-research 75 项 untracked 批量 commit（下次手动窗口）
6. ✅ MEMORY.md 11-20 整合（19356→19917B，余量 83B；下次 KO 必蒸馏）

## 上次检查
- **KO 2026-11-21 02:00（本 run）**：✅ 11-20 全线 7/7 确认（cron 七 job+博客三 commit 494 posts+两新 post 200/index×2）+ Gateway 265/预测再命中（18 次 17 中）+ MEMORY 整合（新增 11-20 链/图推理 insight/研究表行；折叠 11-15~16+减脂五处，13+5 锚点两轮过）+ HEARTBEAT 全刷新 + 建 11-21 daily + 11-20 daily 补 06:00/07:00/08:00/19:00 条目
- KO 2026-11-20 02:00：✅ 11-19 全绿 ×3 确认+MEMORY 实质蒸馏（19944→19356B）
- KO 2026-11-19 / 11-18 / 11-17 02:00：✅ 恢复确认/事故关闭/双日整合
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- KO 2026-11-15 / 11-14 / 11-13 / 11-12 / 11-11 / 11-10 02:00：✅ 第 48~43 日整合
- 更早（10-17~11-09）：✅ 详见各日 daily
