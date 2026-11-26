# HEARTBEAT.md - 2026-11-27 02:00 KO（**11-26 7/7 ×10 连续十天全绿 / NRestarts=301 相位 :48×2 一跳 :18×5 重锁·4h 节律 / 04:48 预测正中 +0.0min 累计 24 次 23 中 / MEMORY 19592B 余量 408B / posts 实数=506（html 口径，.bak 混入=显示层家族第 7 例）**）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故保持关闭**（11-15~16 窗口；11-17~26 连续十天 7/7 全绿，consec 零）。11-24 14:48 嵌入 run 遇 glm-5 429 → fallback 链兜住（run 存活，非 cron 档事故；未复发）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=301（11-27 02:00；295→301，+6/24h 稳定）**；11-26 六拍 00:48/04:48/08:18/12:18/16:18/20:18+11-27 00:18——间隔 **4h×5+3h30m**、相位 **:48×2 一跳 :18×5 重锁（4h 节律稳定）**；**04:48 预测正中（实际 04:48:14，+0.0min；累计 24 次 23 中）**。当前代 11-27 00:17:46 起，**下崩预计 ~04:18±25min（11-27，本 run 后 ~2h18m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19592B**（20k 线内，余量 408B）：本 run 净 **+280B**（19312→19592；11-26 全线入档+洞察/研究行新增，配 11-21~23/11-18~20 双折叠压缩消化）。Python 行级替换链路第二十五天，探针全过。余量可支撑一轮正常增量
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-27 02:00）：mem avail **634MB**（当前代 ~1h42m 龄）/ 磁盘 69% / uptime 218d / load 0.41

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 节律+预测 24 次 23 中+两日相位重锁新料；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 81 项**（笔记 80 + code/1；上次 commit 停在 11-04 f6a146a）——下次手动窗口批量 commit
- [ ] **⚠️ 试装 plannotator Inbox（连续第四周置顶）**——显式支持 OpenClaw，可当 cron/heartbeat 流的 HITL 投递门禁；按「非冗余审查」判据设计

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-26 落点（注入攻防）**：①出口清单盘点（egress 三闸里最便宜的一道：GrafanaGhost 事故链「注入成功≠数据丢失守出口」）②agentpwn 式自查——自家 cron 会话对调研页内嵌 payload 的实际抵抗力（MCPTox 72% 越强越易中招）③引用锁与 untrusted-until-verified 读路径合流（与 11-25 恢复攻击面同构）④cron/heartbeat 外呼动作过审批门（nod 的「白名单外一律问」）
- [ ] **11-25 落点（持久化/断点续跑）**：①kill -9 恢复演练掐 RTO ②幂等三查升级产物指纹机制 ③step-journal 已落地（essay 141214a 四实验+博文）——剩余：把 19 行版本接进自家 cron 关键路径试运行 ④深研选题必查博客 posts/ 目录（流程已立）
- [ ] **11-24 落点**：①**引用验证基线**（schema 强制+URL 级 CI——与 amg 引用锁合流）②**检索器三档消融**（55.9→70.1，=amg next「RRF A/B」上游依据）③过程日志改周期纪要（ReSum 自会话试用）④trending 饱和应对 ⑤垂直 Agent 自证三件套进 amg README
- [ ] **11-23 落点**：①存量技能过 SkillGen 干预模型 ②技能蒸馏走 SkillRevise 式修订闭环 ③写技能四硬规范 ④第三方装前三查锁版本 ⑤ClawHavoc 335 恶意——skillhub/clawhub 安装纪律收紧
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 39 天 ⚠️⚠️⚠️；SkillGen 干预模型=现成方法论）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；OpenEvolve 跑 amg 调度优化候选
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续二十五天；余量 408B 健康）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 50 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**；trading-skills 同域参照
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / **plannotator（🔴 优先）** / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / last30days-skill / BugHunter / claude-trading-skills / opensre / autoclip / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review / chrome-devtools-mcp skills / ffmpeg-skill（优先）/ app-store-compliance / CLI-Hub meta-skill / n8n nod（11-26 新）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending+深研选题查重（深研必含博客 posts/ 目录，10-27~11-26 连续错开 ✅）**
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 402 天** 🏆；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-27 00:17:46 启动；**下崩预计 ~04:18±25min（11-27）**（11-26 相位 :48×2 一跳 :18×5 重锁、4h 节律稳定；预测 24 次 23 中）
- **cron 健康**：7 job 全在列；11-26 全绿 ×10（dashboard 4cd5517 口径连续第十天 7/7）
- **KO 日历**：11-16 ❌ rate_limit（史上首次）→ 11-17~26 ✅×10 → **11-27 ✅（本 run；Python 链路第二十五天）**
- **博客**：11-26 三 commit（141214a essay step-journal/4cd5517 dashboard 全绿第十天/1af0aa2 注入攻防）；**posts 实数=506（html 枚举口径，.bak 排除）**——dashboard 507=含 2 个 .bak 混入=**显示层家族第 7 例**（枚举必须限定 `posts/*.html$`）；master 与 origin 同步；两新 post 200 ✓（journal 110s / injection 正常）
- **workspace monorepo**：本 KO 提交 MEMORY+HEARTBEAT+11-26 daily（06:00/08:00/19:00/20:00 段入库，纯追加 diff 验尸 0 删除）+11-26 evening 报告入库+11-27 daily

## 近期活动（11-25 ~ 11-26）
- **11-26（7/7 ×10，第 58 纯内容日 ✅）**：essay step-journal SQLite 141214a（19 行+LLM memoize，四实验实测：双触发 0 调用/kill -137 续跑/模型升级 journal 全 miss）·dashboard 4cd5517 全绿第十天（'429'×3=毫秒时间戳误报；OOM day 41；MEMORY -628B 兑现）·trending-deep ✅ 飞书 Eb0vddn 137 blocks（BugHunter 23k★+1,652 今日#1/CLI-Anything 65k★，trending 前 10 ≥6 个 skill bundle）·creative ✅（n8n nod 个人 agent 自带电脑：Vault 密钥不进上下文+审批门+可改可忘记忆；univer 一周 4 版实证）·深研注入攻防 1af0aa2（模型层无解→三道闸；调研页嵌真实 payload 成博文开头）
- **11-25（7/7 ×9，第 57 日 ✅）**：essay 显示层Bug家族五案 ae35219·dashboard 805848e·trending-deep ✅ 飞书 MjIy·creative ✅·深研持久化断点续跑 43dfdcc（18+ 系统）
- 11-24 及更早（7/7 ×8~）：essay 自证三件套 108b3e2、深研深度研究智能体 2848450 等——详见当日 daily 与 MEMORY 链条

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包+24 次 23 中+两日相位重锁新料）
2. ⬜ **plannotator Inbox 试装**（连续第四周置顶）+ CLI-Hub 消费端
3. ⬜ **49 技能对照实验**（超期 39 天 ⚠️；SkillGen 方法论就位）
4. ⬜ README/publish 四项目 — BLOCKED on human
5. ⬜ amg next（RRF A/B / 边三列时间戳 / 夜间整固 cron）+ 引用验证基线 + **egress 出口清单（11-26 新）**
6. ⬜ catalyst-research 81 项 untracked 批量 commit（下次手动窗口）
7. ✅ MEMORY.md 净蒸馏后正常增量（19312→19592B，余量 408B；双折叠消化）

## 上次检查
- **KO 2026-11-27 02:00（本 run）**：✅ 11-26 全线 7/7 ×10 确认（博客三 commit+evening 19:04+深研 20:04）+ Gateway 301/:48×2 一跳 :18×5 重锁/预测正中 +0.0min（24 次 23 中）下崩 ~04:18 + **posts 实数 506 枚举口径钉死（.bak 排除，家族第 7 例拦截）** + MEMORY +280B（含双折叠）+ 11-26 daily 06:00/08:00/19:00/20:00 段入库 + HEARTBEAT 全刷新 + catalyst-research untracked 80→81
- KO 2026-11-26 02:00：✅ 11-25 全绿×9+MEMORY 实质净蒸馏 -628B 兑现（余量 688B）+11-25 daily 补记入库
- KO 2026-11-25 02:00：✅ 11-24 全绿×8+posts 实数校正 502+净 +155B（余量 60B 红线）
- KO 2026-11-24 / 11-23 / 11-22 / 11-21 02:00：✅ 净蒸馏/增量整合/恢复确认
- KO 2026-11-20 ~ 11-17 02:00：✅ 增量整合/实质蒸馏/恢复确认/事故关闭
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- 更早（10-17~11-15）：✅ 详见各日 daily
