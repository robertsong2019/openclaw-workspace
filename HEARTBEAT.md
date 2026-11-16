# HEARTBEAT.md - 2026-11-17 02:00 KO（双日整合：**rate_limit 事故 11-15 0/7 + 11-16 3/7**，全绿 streak ×7 终止 / NRestarts=241 下崩预计 04:48±25 / MEMORY 19700B 余量 300B）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=晚间创新点日报，落盘 memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **🔴 rate_limit 事故（本 run 核心事件）**：窗口 **11-15 05:00 → 11-16 08:00**，上游配额限流（zai/glm）。失败 8 run：essay/dashboard/trending-07 ×2 日（consec=2/2/2）+ 11-15 creative/deep + **11-16 02:00 KO（唯一一次 KO 失败，consec=1，本 run 补位）**。恢复证据：11-16 08:00 trending-deep ok → 19:00 creative ok → 20:00 deep ok（312dee8）→ 11-17 02:00 本 run ok。**监控项：若 11-17 05:00 essay 再 fail（consec=3）→ 升级为持续限流，考虑错峰或降模型，需罗嵩知情**
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=241（11-17 02:00；236→241，+5/2 日）**；11-16 六拍 00:18/04:18/08:18/12:18/16:18/20:18 **全 4h00m±1s（:18 相位=11-15 内一次 +30min 跳变后回石英）**+11-17 00:48（20:18→00:48 又一跳 4h30m，回 :48 相位）；预测累计 14 次 13 中。当前代 11-17 00:48 起，**下崩预计 ~04:48±25min（11-17，本 run 后 ~2h48m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则；essay 50f3658 取证博文）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19700B**（20k 线内 98.5%；先压缩再新增：11-09+10 折叠/研究表删 11-08 行/11-03~06·01~02·07~08 链条压缩/语音+图记忆 insight 减脂/竞品速查去注；17 锚点一轮全过）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-17 02:00）：mem avail **865MB**（当前代 1h12m 龄）/ 磁盘 69% / uptime ~208d / load 0.62

## 待办任务

### 🔴 最高优先级
- [ ] **监控 rate_limit 复发**：11-17 05:00/06:00/07:00 essay/dashboard/trending 若再 fail（consec=3）=持续限流，需错峰/降模型决策（罗嵩知情）；否则视为一次性事故关闭
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 节律+偶发 +30min 跳变+预测 14 次 13 中=强证据包；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 54 项**（08-24 起笔记+code/）——下次手动窗口批量 commit

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-16 落点**：①anthropics/skills 官方仓+SkillEvaluator=技能评测层（对 49 技能实验是现成尺子）②LoopForge SOP 编排+人工门/plannotator/ag-ui=人机监管层新品类（与审批疲劳洞察汇合）③univer「Office SDK 卖给 Agent」模式→amg MCP 分发参考 ④AI 科学家溯源三件套（证据引用密度/闭环评测/溯源完备）→amg provenance 叙事
- [ ] **11-14 落点**：①tailcat VPS 试装（gateway 免暴露端口访问验证）②plannotator 官方 openclaw-plugin 试用 ③EGM 试用 ④auto-ontology provenance→amg 答案来源验证 ⑤amg 试点 L1 规则判卷臂 ⑥判官三件套体检（swap/padding/self-pref）移植自家 cron
- [ ] **11-13 落点（压缩）**：提示词版 CLM 自跑 / MWG eval 剪枝→skill 验证 / astryx specs:for→amg 最小权限注入 / open-code-review 三痛点诊断法
- [ ] **11-11/12 落点（压缩）**：workspace 记忆「最近引用时间」降级 / amg 固化 pass 消融提案 / coverage-ledger 移植 / 权重记忆路由分诊对照
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 28 天 ⚠️⚠️⚠️；SkillEvaluator 可作现成评测层）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路已连续十五天顺畅）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 40 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / plannotator / EGM / block/buzz（等审批门）/ SkillEvaluator / LoopForge / ag-ui / univer / graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review / NVIDIA/auto-ontology
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-14 连续错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 392 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-17 00:48 启动；**下崩预计 ~04:48±25min（11-17）**（11-16 六拍 4h00m±1s :18 相位+00:48 跳回 :48；预测 14 次 13 中）
- **cron 健康**：7 job 全在列；essay/dashboard/trending-07 consec=2 待 11-17 早晨 run 确认清零
- **KO 日历**：11-13 ✅ → 11-14 ✅ → 11-15 ✅ → **11-16 ❌ rate_limit（史上首次 KO 失败）** → **11-17 ✅（本 run，双日整合补位；Python 链路第十五天，17 锚点全过）**
- **博客**：11-15 零 commit；11-16 一 commit（深研 312dee8）；dashboard 停在 day 6 / 486 posts（232b84b，11-14）；master 与 origin 同步

## 近期活动（11-15 ~ 11-16）
- **11-16（3/7，恢复日）**：trending-deep 08:00 ✅·creative 19:00 ✅（创新点 11-16 期：anthropics/skills 官方仓+SkillEvaluator 技能评测层同框=Skills 从 Claude Code 特性变跨 harness 分发平台；人机监管层成品类（plannotator/LoopForge/EGM/ag-ui）；Agent-ready 重构传统软件（astryx 同套工具/univer Office SDK））·深研 20:00 ✅《论文不等于发现——AI 科学家与验证鸿沟》312dee8（Co-Scientist 72h 重演 vs 逐条核验止于体外；25k runs 审计 68% 忽略证据/底座占 41.4% 方差；插值器非外推器；A-Lab 溯源三要素；笔记 2026-11-16-ai-scientist-verification-gap.md 13 系统）；❌ KO/essay/dashboard/trending-07（rate_limit）
- **11-15（0/7，事故日）**：essay/dashboard/trending-07/creative/deep 全 rate_limit 失败，全天零产物零 commit；仅 02:00 KO ✅（第 48 日整合+MEMORY 压缩至 19686B）

## 本周关键路径
1. ✅ 内容线 48 纯内容日后遇 rate_limit 事故（11-15 0/7+11-16 3/7）；⬜ 11-17 早晨 run 确认全面恢复；⬜ 上游 issue 报告（置顶；证据包已齐）
2. ⬜ 49 技能对照实验（超期 28 天 ⚠️；SkillEvaluator=现成尺子）+ headroom 决策
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（L1 规则判卷臂 / RRF A/B / 边三列时间戳 / 夜间整固 cron / 判官三件套体检）+ 引用锁溯源落地 — 待罗嵩排期
5. ⬜ catalyst-research 54 项 untracked 批量 commit（下次手动窗口）
6. ✅ MEMORY.md 双日整合+再压缩（19700B，余量 300B；下次 KO 若逼近 19.9k 优先折叠 11-03~06 已做、可再折 11-11/12/13 链条+研究表删 11-09/10 行）

## 上次检查
- **KO 2026-11-17 02:00（本 run）**：✅ 双日整合（补 11-16 KO 失败位）：rate_limit 事故定界（11-15 05:00→11-16 08:00，8 run）+ 恢复确认 + 11-16 深研/创新点入档 + MEMORY 19686→19700（17 锚点全过，先压缩 ~1.1k 再新增）+ HEARTBEAT 全刷新 + 建 11-17 daily
- KO 2026-11-15 02:00：✅ 第 48 日整合（11-14 7/7 全绿 ×7）+ NRestarts=236 漂移停止 + MEMORY 压至 19686
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- KO 2026-11-14 / 11-13 / 11-12 / 11-11 / 11-10 02:00：✅ 第 47/46/45/44/43 日整合
- 更早（10-17~11-09）：✅ 详见各日 daily
