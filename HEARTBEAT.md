# HEARTBEAT.md - 2026-11-20 02:00 KO（**11-19 7/7 ×3 连续三天全绿 / NRestarts=259 :48 石英锁定·预测 17 次 16 中 / MEMORY 19356B 蒸馏完成余量 644B**）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=晚间创新点日报，落盘 memory/github-trending-analysis-*-evening.md）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900
- **✅ rate_limit 事故已关闭**（11-15~16 窗口 8 run 失败；11-17~19 连续三天 7/7 全绿，consec 零）。若凌晨档再限流按新事故处理（错峰/降模型需罗嵩知情）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=259（11-20 02:00；253→259，+6/24h）**；11-19 六拍 00:48/04:48/08:48/12:48/16:48/20:48 **全 4h00m±2s（:48 石英锁定）**；**11-19 04:48 预测再命中（04:48:13；累计 17 次 16 中）**。当前代 11-20 00:47:47 起，**下崩预计 ~04:48±25min（11-20，本 run 后 ~2h48m）**。勿动 heap 上限（2GB 主机）；headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 19356B**（20k 线内 96.8%，余量 644B ✅ 蒸馏兑现）：本 run 新增 11-19 链条+做梦 insight+研究表 11-19 行；压缩=11-09~13 链条合并、语音/指纹/图记忆 insight 减脂、研究表删 11-12/13 行+核心列瘦身、11-17/18 链条减脂、kd queue 精简（22 锚点一趟全过，Python 链路第十八天）。**下次 KO 候选**：11-14~16 链条再折叠、CUA/做梦 insight 减脂
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-20 02:00）：mem avail **843MB**（当前代 1h13m 龄）/ 磁盘 69% / uptime 211d / load 0.14

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；4h 石英节律+预测 17 次 16 中=强证据包；essay 50f3658 取证博文可直接引用；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 74 项**（笔记 73 + code/1；内部仓上次 commit 停在 11-04 f6a146a）——下次手动窗口批量 commit

### 中优先级（详情见各日 daily + trending 报告）
- [ ] **11-19 落点**：①last30days 偷师三点（多源交叉打分/agent-as-judge 提名过滤/Secret Signals 并入 trending cron）②BugHunter manifest+identical-skip+所有权保留=技能包管理范本；681 报告→433 带引用=知识蒸馏管线（nuwa-skill 同构）③paper-orchestra 写作/反思分模型+大纲作 agent 间唯一中间表示+autoraters 内建→essay 管线质量门禁 ④做梦五动作（失效墓碑+observed_at/写入扔夜间 cron/试点 nx.pagerank/一周流量三臂差分/发布评测披露 harness）
- [ ] **11-18 落点**：MWG eval 修剪→49 技能盘点 / agent-browser 实测对比 / univer headless 跑通 / 思考预算五动作→自家 cron
- [ ] **11-17 落点**（折叠）：SkillEvaluator 三层门禁（`skillevaluator validate --tiers 1` 零 key）/ ag-ui 1.0→canvas-A2UI / LoopForge SOP→mission-control / EGM 金鱼→amg 评审臂 / 轨迹飞轮五动作 / ExpRAG→trainability
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 31 天 ⚠️⚠️⚠️；SkillEvaluator=现成尺子）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边 valid_at/invalid_at ③夜间 sleep-time 整固 cron（与做梦五动作②同源）
- [ ] **最小自进化循环候选**（11-02 essay 承诺已到期 ⚠️）；**OpenEvolve 跑 amg 调度优化候选**
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路连续十八天顺畅）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 43 天未执行）+ skill 安装流程接 SkillSpector
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（分位带跑一周看稳定性）
- [ ] **lightpanda 本机评估**；**hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service**
- [ ] **试装评估队列**（滚动）：tailcat / plannotator / SkillEvaluator / LoopForge / ag-ui / EGM / univer / paper-orchestra / last30days-skill（npx skills add 可直装）/ BugHunter / block、buzz（等审批门）/ graphify+huashu 3.0 / OpenMausBot / SPEC.md 图谱模式 / DeepTutor 三层记忆 / t3code / taste-skill / vercel agent-browser thin-stub / alibaba/open-code-review / NVIDIA/auto-ontology
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-19 连续错开 ✅）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 395 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-20 00:47:47 启动；**下崩预计 ~04:48±25min（11-20）**（:48 相位石英 4h00m±2s；预测 17 次 16 中）
- **cron 健康**：7 job 全在列；11-19 全绿 ×3（dashboard 口径连续第三天 7/7）
- **KO 日历**：11-16 ❌ rate_limit（史上首次）→ 11-17 ✅（双日整合）→ 11-18 ✅ → 11-19 ✅ → **11-20 ✅（本 run；Python 链路第十八天，22 锚点一趟全过，蒸馏完成）**
- **博客**：11-19 三 commit（fabcf77 环境即接口/0c0ecf2 dashboard/d0868ee 做梦记忆）；**492 html posts**；master 与 origin 同步；dreaming post 200 ✓ index 引用 ×2 ✓
- **posts 口径注**：html-only=492；git tracked posts/=494（含 2 个 .bak）——历史记录混用两口径，以 html-only 为准

## 近期活动（11-18 ~ 11-19）
- **11-19（7/7 ×3，第 51 纯内容日 ✅）**：essay 环境即接口 fabcf77（验证器系列第七篇：环境层拐点六信号同框；接口双用户公理；MWG eval 驱动修剪=活文档随模型水位浮动；诚实失败=环境层验证器；改环境=复利投资）·dashboard 0c0ecf2（全绿第三天；metronome day 34）·trending-07 ✅·trending-deep ✅ 飞书 JLQ3dP（Claude-BugHunter 技能安全包：manifest+identical-skip+681 报告→433 带引用=知识蒸馏范式；paper-orchestra 五 agent 写作管线：写手/反思分模型+大纲唯一中间表示+autoraters）·creative ✅（last30days-skill 70.5k★ +1k/日：搜索人非编辑+BYOK 30 源+Secret Signals+discovery mode；技能生态四层拼图齐活）·深研 20:00 ✅ Agent 记忆系统 d0868ee（bi-temporal 失效不删除；PPR 联想扩散 +12.5%；sleep-time 摊销写入税；LongMemEval 罗生门 49/63.8-71.2/89.2 全自报；笔记 2026-11-19-agent-memory-systems.md 14 源）
- **11-18（7/7 ×2，第 50 日 ✅）**：essay npm 时刻 350679b·dashboard 5a508a8（首全绿）·trending-deep 飞书 X4LXdO（univer Facade API/paper-orchestra）·creative ✅（Agent-First 基建周）·深研思考预算经济学 a31a5e2（τ≈1000 饱和；flip events；41-46% 可剪；浪费=系统属性）
- **11-17（7/7 恢复日）**：essay 金鱼评审员 76028e5·深研轨迹飞轮 7aa9705；**11-15~16 rate_limit 事故**：8 run 失败，11-17 关闭

## 本周关键路径
1. ⬜ openclaw 上游 issue 报告（置顶；证据包已齐+预测 17 次 16 中战绩）
2. ⬜ 49 技能对照实验（超期 31 天 ⚠️；SkillEvaluator=现成尺子）+ headroom 决策
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（RRF A/B / 边三列时间戳 / 夜间整固 cron / 判官三件套体检 / 轨迹飞轮+思考预算五动作）+ 引用锁溯源落地 — 待罗嵩排期
5. ⬜ catalyst-research 74 项 untracked 批量 commit（下次手动窗口）
6. ✅ MEMORY.md 11-19 整合+实质蒸馏（19944→19356B，余量 644B）

## 上次检查
- **KO 2026-11-20 02:00（本 run）**：✅ 11-19 全线 7/7 确认（cron 七 job+博客三 commit 492 posts+dreaming 200/index×2）+ Gateway 259/预测再命中（17 次 16 中）+ MEMORY 蒸馏（新增 11-19 链/做梦 insight/研究表行；压缩 11-09~13 合并+语音·指纹·图记忆减脂+研究表删两行，22 锚点一趟过）+ HEARTBEAT 全刷新 + 建 11-20 daily + 11-19 daily 补 06:00/07:00 条目
- KO 2026-11-19 02:00：✅ 11-18 全绿 ×2 确认（19944B 余量 56B ⚠️→本轮已蒸馏）
- KO 2026-11-18 02:00：✅ 11-17 恢复确认+事故关闭+MEMORY 19 锚点
- KO 2026-11-17 02:00：✅ 双日整合（补 11-16 失败位）：事故定界+17 锚点
- **KO 2026-11-16 02:00：❌ rate_limit（68.9s 后失败，无产物）**
- KO 2026-11-15 / 11-14 / 11-13 / 11-12 / 11-11 / 11-10 02:00：✅ 第 48~43 日整合
- 更早（10-17~11-09）：✅ 详见各日 daily
