# HEARTBEAT.md - 2026-11-03 02:00 KO（第 36 纯内容日整合：11-02 6/7 绿·KO edit 工具失败但实质完成 / NRestarts=166 / 全绿纪录止步 5 天）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **11-02 记 6/7 绿**：KO run 的 Edit MEMORY.md 工具在 CJK 密集文件上多块编辑连续失败（cron 记 failed）但实质完成（HEARTBEAT 全刷新+MEMORY 已更新，唯漏 commit）；其余 6 条全 ok。**10-28~11-01 连续五天 7/7 全绿止步**；dashboard 链 day 17（74f64ca）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=166（11-03 02:00；160→166）**；11-02 六拍 CST 00:18/04:18/08:18/12:48/17:18/21:18——间隔 240/240/270/270/240min 均值 252min（4h~4h30 带稳定）；昨日预测 04:36±25 → 实际 04:18（−18min，连续两天命中）。当前代 11-03 01:17 起，**下崩预计 ~05:32±25min**。勿动 heap 上限（2GB 主机）。headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零（dashboard 链续至 day 17）；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 18.5k**（20k 线内 92%；本 run：增 11-02 条目+睡眠记忆洞察、OOM 更至 166/下崩 05:32、零回滚 377→378、研究表增 11-02 删 10-22；全部走 Python 行级替换，0 edit 工具调用）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-03 02:00）：mem avail **791MB**（当前代 0.7h 龄）/ 磁盘 68% / uptime ~195d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；252min 节拍族+取证三层全瞎=最强证据包；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 54 项**（08-24 起笔记+code/）——下次手动窗口批量 commit

### 中优先级（详情见 11-02 daily + trending 报告）
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 15 天 ⚠️⚠️⚠️；API 封装类先写 20 道判分题再决定去留）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边加 valid_at/invalid_at（bi-temporal 最小实现）③夜间 sleep-time 整固 cron（11-02 晚研再证：先攻时间排序/知识更新分项；daily→MEMORY.md，升级 heartbeat）
- [ ] **最小自进化循环候选**（11-01 深研落点+11-02 essay 承诺「一个月后见分晓」）：50 题+评估器+git 存档，可挂 cron；**OpenEvolve 跑 amg 调度优化候选**（喂真问题，机器可验证域）
- [ ] **20 题归档召回基线**（dreaming/压缩改动必须过 recall eval 的量尺）；**amg×Agentic RL 接口**（LME exact judge 作 verifier 接 RL 循环）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（metaproductivity 台账最小版；本 run 已验证 Python 行级替换链路顺畅——上次 edit 失败教训的解法生效）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit 审计 workspace（cloudflare security-audit-skill 53.3k★ 可沙箱跑自有项目）
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 26 天未执行）+ skill 安装流程接 SkillSpector 扫描
- [ ] **11-02 trending deep 两落点**：①claude-mem 实装 OpenClaw gateway 周观察对照 amg ②Kronos-mini + akshare 日频预测 skill 原型
- [ ] **11-02 creative 候选**：agent-desktop（Vercel OS 无障碍树 CUA，对比 vision-based）/ paperclip（"OpenClaw 是员工，Paperclip 是公司"，管理层抽象互补性最强）
- [ ] **hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service 待排期**
- [ ] **试装评估队列**：graphify+huashu-design 3.0（10-27）/ jakubkrehel skills interface-review（10-28）/ OpenMausBot（10-29）/ SPEC.md 图谱模式（10-30）/ DeepTutor 三层记忆（10-30）/ expo/skills 三渠道（10-31）/ t3code 对标（11-01）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **amg 实验三连**：3-layer 渐进披露 / EvidenceLedger 工具化 / 压缩悖论三件；**amg PPR 对照臂**（别拿 leaderboard 做决策）
- [ ] **TTT 后续**（LoRA<1%+20 条信息增益邻居）；**Governance Decay 后续**（宪法存活测试进 KO 自检 / KV-cache ≥70% 阈值进仪表盘）；**Agentic Commerce 后续**（预算三档对照）
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-02 连续错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 378 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-03 01:17 启动；**下崩预计 ~05:32±25min**（间隔族 240~270min 均值 252；预测连续两天命中）
- **KO 日历**：10-30 ✅ → 10-31 ✅ → 11-01 ✅ → 11-02 ⚠️（edit 工具失败/实质完成）→ **11-03 ✅（本 run，Python 编辑全通过）**
- **博客**：11-02 三 commit（essay 最小自进化循环 f1808bb + dashboard 74f64ca + 晚研《Agent 的睡眠》5d759b5）；461 posts；master 与 origin 同步

## 近期活动（11-01 ~ 11-02）
- **11-02（第 36 日，6/7 绿）**：essay《最小自进化循环》f1808bb（50 题+评估器+git 存档；裁判物理隔离）· dashboard 74f64ca（day 17；第 161 杀；全绿止步 5 天）· trending deep：claude-mem 1526★/日+Kronos 金融 K 线模型（飞书 ✅）· creative：agent-desktop（Vercel 无障碍树 CUA）/paperclip（公司管理层抽象）/mattpocock skills · 晚深研《Agent 的睡眠》5d759b5（Google SLEEP/Letta/MemOS/HippoRAG 2；瓶颈检索→整理；记忆=第三扩展轴；进权重=审计权转移；LoCoMo/BEAM 基准危机）
- **11-01（第 35 日，7/7 全绿连续 5 天）**：essay《12,924 次工具调用的考古》e2ec6d9（read 三连 3066 次=记忆税/规则留频率指纹）· dashboard 086abce（day 16）· trending deep：claude-mem 107.8K★+Orkas 双显式支持 OpenClaw · creative：skills 垂直品类化/t3code/Game-Studios · 晚深研《改自己代码的 Agent》09a84f4（五条铁律；DGM node114 作弊案/AlphaEvolve 48 mults/SICA 零梯度 17→53）

## 本周关键路径
1. ✅ 内容线连续 36 纯内容日（10-28~11-01 五天 7/7 后 11-02 一条 edit 失误，看本周能否重开全绿）；⬜ 上游 issue 报告（置顶，252min 节拍族+取证全瞎三层证据已足）
2. ⬜ 49 技能对照实验（超期 15 天 ⚠️）+ headroom 决策（装前过 20 题配对）
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（RRF A/B / 边 valid_at / 夜间整固 cron / 20 题召回基线 / 最小自进化循环 / OpenEvolve 喂 amg）— 待罗嵩排期
5. ⬜ catalyst-research 54 项 untracked 批量 commit（下次手动窗口）

## 上次检查
- **KO 2026-11-03 02:00（本 run）**：✅ 第 36 日整合（11-02 6/7 收口：KO edit 失败定因+教训固化）+ NRestarts=166（+6 恰六拍；252min 均值；预测连续两天命中）+ MEMORY 7 处 Python 替换全通过（18.5k）+ HEARTBEAT 全刷新（eval-gap 15 天、Agent-Reach 26 天、新增 11-02 双落点四候选）
- KO 2026-11-02 02:00：⚠️ 6/7——Edit MEMORY.md 工具在 CJK 密集文件多块编辑连续失败（实质完成：HEARTBEAT/MEMORY 已更新但未 commit）；NRestarts=160（+6）
- KO 2026-11-01 02:00：✅ 第 34 日整合 + NRestarts=154（+5 恰五拍）+ MEMORY 常规维护（17.3k）
- KO 2026-10-31 02:00：✅ 第 33 日整合 + NRestarts=149（+6 恰六拍）+ MEMORY 常规维护（16.5k）
- KO 2026-10-30 02:00：✅ 第 32 日整合 + NRestarts=143 + MEMORY 常规维护（15.9k）
- 更早（10-17~10-29）：✅ 详见各日 daily
