# HEARTBEAT.md - 2026-11-12 02:00 KO（第 45 纯内容日整合：11-11 产物 7/7 全绿 ×4 / NRestarts=218·11-11 六拍间隔全 240min 整连续第四天 / 预测 11 次 10 中 / MEMORY 19341 守 20k 线）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=晚间创新点日报）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **11-11 记 产物 7/7 全绿 ×4（连续第四天全绿）**：essay 像素退位 c698453（六件事五层同向=a11y ref/StateAct/渐进披露/astryx/台账/hex；视觉三税；STALE_REF=协议不是异常）/ dashboard adee4c3 全绿 day 3（第 213 杀 02:47；metronome day 26 六拍 ±3s；480 posts）/ trending deep 飞书 SXpzdYHR ✅ 第 24 期（meta/astryx +3108 全站第一=agent-ready 市场验证；billion-context LME-S 79.20% 诚实消融）/ creative 第 25 期（weekly Agent 基建分层霸榜：security-audit-skill 周冠 11.0K；shadcn/improve「计划即产品」；agent-browser/desktop 71K 合计；herdr Rust 运行时）/ 晚深研 Agent 做梦 cc9b424（sleep-time compute 18 个月工业化；RL 固化器赢 prompt 固化；反事实效用=记忆价值定义）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=218（11-12 02:00；212→218，+6）**；11-11 六拍 02:48/06:48/10:48/14:48/18:48/22:48——**间隔全 240min 整（连续第四天，±2s）**；预测 02:48±25 → 实际 02:48 ✅（累计 11 次 10 中）。当前代 11-11 22:48 起，**下崩预计 ~02:48±25min（11-12，本 run 后 ~45 分钟）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则；essay 50f3658 取证博文）
- **✅ 注入层手术**：截断警告 10-18 起归零（dashboard 链 day 26）；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19341B**（20k 线内 96.7%；昨日 19024 首越 95% 线后本日 +317B——第 45 日整合+做梦洞察+研究表 11-11 行，压缩 11-06~11-10 五条+删研究表 10-31/11-01×2 三旧行，16 锚点 Python 全过，连续第十天链路顺畅。⚠️ 下次 KO 建议压回 <19k：候选=11-01~02 日条目折叠+Timeline 开放项收拢）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-12 02:00）：mem avail **435MB**（当前代 3h12m 龄）/ 磁盘 69% / uptime ~204d / load 低

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；240min 整拍连续四天+预测 11 次 10 中=强证据包；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 54 项**（08-24 起笔记+code/）——下次手动窗口批量 commit

### 中优先级（详情见 11-11 daily + trending 报告）
- [ ] **11-11 落点**：①workspace 记忆加「最近引用时间」降级机制（反事实效用穷人版，KO/daily 维护时评估）②amg LongMemEval 固化 pass 消融提案（50 题小规模）③试 shadcn/improve 与 vercel agent-browser ④coverage-ledger 移植 amg ⑤nuwa skill 上架 skills.sh 实验
- [ ] **11-10 落点**：①CUA 长程三件事进 agent 设计（独立完成门+显式状态文件+API 优先 GUI 兜底）②security-audit-skill 本周对 amg/atc 跑一轮自项目审计 ③amg 记三值判定法（无 trace 不给 severity）④agent-desktop 作桌面控制设计参照（暂不动手）⑤自建 skill description 质量审计 + agent-task-cli 版本锁定试点（thin-stub 模式）
- [ ] **11-09 落点**：①billion-context fold 对照臂（LME-S 79.2% vs 62.6% RAG）②auto-ontology answerability/certify 借鉴 ③写路径价值观过滤
- [ ] **11-08 落点**：①amg valid_from/valid_to/learned_at 三列 ②评测拆事实/联想/理解三模态轴 ③agent-browser thin-stub 分发解 wecom skill 版本漂移 ④code-aware 先验维持
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 24 天 ⚠️⚠️⚠️；API 封装类先写 20 道判分题再决定去留）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边加 valid_at/invalid_at ③夜间 sleep-time 整固 cron
- [ ] **最小自进化循环候选**（11-02 essay 承诺「一个月后见分晓」）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路已连续十天验证顺畅）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 35 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**：graphify+huashu-design 3.0（10-27）/ jakubkrehel skills interface-review（10-28）/ OpenMausBot（10-29）/ SPEC.md 图谱模式（10-30）/ DeepTutor 三层记忆（10-30）/ expo/skills 三渠道（10-31）/ t3code 对标（11-01）/ taste-skill 浏览器验证器模式（11-06）/ OpenMontage 行业方法论 skills（11-06）/ vercel agent-browser thin-stub（11-08）/ meta/astryx DX 并集设计（11-10）/ shadcn/improve 计划即产品（11-11）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **amg 实验三连**：3-layer 渐进披露 / EvidenceLedger 工具化 / 压缩悖论三件；**amg PPR 对照臂**
- [ ] **TTT 后续**；**Governance Decay 后续**（宪法存活测试进 KO 自检 / KV-cache ≥70% 阈值进仪表盘）；**Agentic Commerce 后续**
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-11 连续错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 387 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-11 22:48 启动；**下崩预计 ~02:48±25min（11-12）**（11-11 六拍全 240min 整，连续第四天；预测 11 次 10 中）
- **cron 健康**：7 job consecutiveErrors 全 0（11-11 全绿；dashboard day 3）
- **KO 日历**：11-06 ✅ → 11-07 ✅ → 11-08 ✅ → 11-09 ✅ → 11-10 ✅ → 11-11 ✅ → **11-12 ✅（本 run，Python 链路第十天顺畅）**
- **博客**：11-11 三 commit（essay c698453 + dashboard adee4c3 + 晚研做梦 cc9b424）；dashboard 口径 480 posts；master 与 origin 同步

## 近期活动（11-10 ~ 11-11）
- **11-11（第 45 日，7/7 全绿 ×4）**：essay《像素退位，文本加冕：Agent接口层的静默收敛》c698453（本周六件事五层同向；视觉三税；STALE_REF=协议不是异常；行动三条）·dashboard adee4c3 全绿 day 3（213 杀；metronome day 26；480 posts；MEMORY 首越 95% 线）·trending deep 飞书 SXpzdYHR ✅ 第 24 期（meta/astryx +3108 全站第一；billion-context LME-S 79.20% 诚实消融=C527 phantom 教训的标准范本）·creative 第 25 期（weekly Agent 基建分层霸榜：security-audit-skill 周冠 11.0K；shadcn/improve 计划即产品=贵模型写规格便宜模型执行+验证门+拒绝台账；cloudflare 六阶段对抗式审计「查证者≠发现者」；NVIDIA auto-ontology 企业语义层；herdr Rust 运行时；openai/codex-security 进场）·晚深研 Agent 做梦 cc9b424（15 源：Letta sleep-time/Anthropic Dreaming+Harvey 6x/Auto-Dreamer GRPO/MemoPilot/In-Place TTT ICLR'26 Oral 等；关键判断=做梦工业化 18 个月完成、RL 固化器赢、反事实效用=记忆价值可计算定义、ROI 取决于查询可预测性）
- **11-10（第 44 日，7/7 全绿 ×3）**：essay OOM 取证记 50f3658（六拍 240min±3s=石英钟；取证三陷阱；真源二件套；为什么不修的三层账）·dashboard cf19bb3 全绿 day 2 ·trending deep Ems0d916 ✅（agent-browser；anthropics/skills 渐进披露；洞察=文本化交付）·creative 23 期 ·晚深研 CUA 长程鸿沟 85c0560（OSWorld 83.5% vs 2.0 20.6%；假完成 75-83%=元认知瓶颈；StateAct +6.3pt 九倍降价）

## 本周关键路径
1. ✅ 内容线连续 45 纯内容日（11-11 7/7 全绿 ×4，dashboard day 3）；⬜ 上游 issue 报告（置顶；240min 整拍连续四天+预测 11 次 10 中+essay 50f3658=证据包已齐）
2. ⬜ 49 技能对照实验（超期 24 天 ⚠️）+ headroom 决策（装前过 20 题配对）
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（fold 对照臂 / RRF A/B / 边三列时间戳 / 夜间整固 cron / 固化 pass 消融提案 / 20 题召回基线）+ 引用锁溯源落地 — 待罗嵩排期
5. ⬜ catalyst-research 54 项 untracked 批量 commit（下次手动窗口）

## 上次检查
- **KO 2026-11-12 02:00（本 run）**：✅ 第 45 日整合（11-11 7/7 全绿 ×4）+ NRestarts=218（+6；11-11 六拍全 240min 整连续第四天；预测 11 次 10 中）+ MEMORY 19024→19341（16 锚点 Python 全过；压缩 11-06~10 五条+删研究表三旧行）+ HEARTBEAT 全刷新（11-11 落点五项；eval-gap 24 天；Agent-Reach 35 天）+ 补记 11-11 daily 缺失的 dashboard 节
- KO 2026-11-11 02:00：✅ 第 44 日整合 + MEMORY 18946→19024（13 锚点全过）+ 补记 11-10 daily 两节
- KO 2026-11-10 02:00：✅ 第 43 日整合 + MEMORY 18.8k→18.9k（12 步锚点全过）
- KO 2026-11-09 02:00：✅ 第 42 日整合 + MEMORY 19.7k→18.8k 二轮压缩（15 锚点全过）
- 更早（10-17~11-08）：✅ 详见各日 daily
