# HEARTBEAT.md - 2026-11-05 02:00 KO（第 38 纯内容日整合：11-04 7/7 全绿×2 / NRestarts=177·预测四连中 / MEMORY 压缩 19.5k→18.0k）

## ⚠️ 执行环境
- **cron 7 条（10-01 起）**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00（产出=晚间创新点日报）/ deep-exploration 20:00。开发线已删=罗嵩手动驱动。timeout：KO/essay/daily/creative=600 / deep=900（健康）
- **11-04 记 7/7 全绿 ×2**（11-03 起连续两天）：essay 确定性验证器 c34c6ce / dashboard 0fdf3a6 day 19 / trending 双场（deep 飞书 VJ9NdRSMJo9 ✅+晚间场）/ creative=晚间场（skills 成 GitHub 最大品类：superpowers 312K 四大厂收编）/ 晚深研写路径 RL 革命 12d05ee（daily 20:00 段由 KO 11-05 补账）
- **Tavily dev key 生效**；env 真源=`gateway.systemd.env` 非 `.env`。AnySearch MCP 已消失（备援 web_fetch）
- **Gateway OOM（确诊）**：V8 堆耗尽 ABRT，systemd 5s 自愈，危害=长会话上下文丢失非产物。**NRestarts=177（11-05 02:00；172→177）**；11-04 六拍 CST 02:36/06:36/10:18/14:48/19:18/23:18——间隔 240/222/270/270/240min 均值 248min（4h~4h30 带稳定）；预测 02:29±25 → 实际 02:36（+7min，**四连中**）。当前代 11-04 23:17 起，**下崩预计 ~03:30±25min（11-05）**。勿动 heap 上限（2GB 主机）。headroom 候选须先过 20 题配对
- **⚠️ Gateway 取证口径**：真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`（详见 TOOLS.md 永久规则）
- **✅ 注入层手术**：截断警告 10-18 起归零（dashboard 链续至 day 19）；OOM 独立（根因=V8 堆，非注入）
- **MEMORY.md 18.0k**（20k 线内 89.9%；本 run 大压缩：10-22~11-03 洞察精炼 ~2.1k + 增 11-04 条目/洞察/研究行 + 删 10-24 研究行；全走 Python 行级替换，0 edit 工具调用，连续第三天链路顺畅）
- ⚠️ memory/ 8 月底-9 月初 daily 存在未提交整文件改写（挂 30+ 天），处理前逐文件 diff 验尸，勿盲目 commit
- 主机（11-05 02:00）：mem avail **510MB**（当前代 2.7h 龄）/ 磁盘 69% / uptime ~196d

## 待办任务

### 🔴 最高优先级
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal+文件日志取证在手；248min 节拍族+取证三层全瞎=最强证据包；先搜 known issue）
- [ ] **amg: README + PyPI/npm publish** — 11272 tests / 0.732 banked / 47 连 keep；PyPI 人工三步 + npm 命名决策（human-blocked）
- [ ] acs 3173 / sot 619 / atc 2052：README + publish（human-blocked）
- [ ] **catalyst-research 仓 untracked 54 项**（08-24 起笔记+code/）——下次手动窗口批量 commit

### 中优先级（详情见 11-04 daily + trending 报告）
- [ ] **49 技能 eval-gap 对照实验**（essay 承诺超期 17 天 ⚠️⚠️⚠️；API 封装类先写 20 道判分题再决定去留）
- [ ] **11-03 Skills 生态 next actions**：①本地技能库 drift 园丁体检脚本（只进不出→检索稀释检测）②skill description 审计 ③第三方技能安装 checklist（无签名无沙箱=装前逐字读）
- [ ] **11-04 trending 落点**：①agent-desktop 的 JSON envelope/retry 错误协议移植 agent-task-cli（无障碍树语义路线领跑 computer use）②worktrunk 模式（worktree 按分支并行寻址，缓解多 clone/并行会话血泪史）③Scrapling（agent 数据采集层，有官方 OpenClaw skill）
- [ ] **amg next 三件（直接可动手）**：①检索 BM25+实体 RRF 融合 A/B ②图谱边加 valid_at/invalid_at（bi-temporal 最小实现）③夜间 sleep-time 整固 cron（daily→MEMORY.md，升级 heartbeat）；**写路径 RL 读法**（11-04 晚研）：确定性代码管骨架+轻量管线管常规写入+学习策略管取舍边界=amg 架构印证
- [ ] **最小自进化循环候选**（11-02 essay 承诺「一个月后见分晓」）：50 题+评估器+git 存档，可挂 cron；**OpenEvolve 跑 amg 调度优化候选**（机器可验证域）
- [ ] **20 题归档召回基线**；**amg×Agentic RL 接口**（LME exact judge 作 verifier 接 RL 循环）
- [ ] **MEMORY/TOOLS 结构性编辑配前后探针**（Python 行级替换链路已连续三天验证顺畅）
- [ ] **headroom `wrap openclaw` 实测**（先过 20 题配对）/ **context-mode 本机试装** / skills add security-audit 审计 workspace
- [ ] **待罗嵩决策（10-26 creative）**：装 Agent-Reach（建议小号；⚠️ 连续 28 天未执行）+ skill 安装流程接 SkillSpector 扫描
- [ ] **Kronos-mini + akshare 日频预测 skill 原型**（11-02 trending 落点+11-03 essay 承诺：分位带跑一周看稳定性）
- [ ] **claude-mem 实装 OpenClaw gateway 周观察对照 amg**（11-02 落点；官方支持 OpenClaw、111K 总星）
- [ ] **lightpanda 本机评估**（Zig 无渲染浏览器 123MB/5s，2C/2GB 替代 headless Chrome 候选）
- [ ] **hindsight vs amg 对标实验**；**ai-memory 落地三件抄进 agent-memory-service 待排期**
- [ ] **试装评估队列**：graphify+huashu-design 3.0（10-27）/ jakubkrehel skills interface-review（10-28）/ OpenMausBot（10-29）/ SPEC.md 图谱模式（10-30）/ DeepTutor 三层记忆（10-30）/ expo/skills 三渠道（10-31）/ t3code 对标（11-01）
- [ ] **ai-job-search /outcome 模式移植**到 agent-task-cli eval
- [ ] **amg 实验三连**：3-layer 渐进披露 / EvidenceLedger 工具化 / 压缩悖论三件；**amg PPR 对照臂**
- [ ] **TTT 后续**；**Governance Decay 后续**（宪法存活测试进 KO 自检 / KV-cache ≥70% 阈值进仪表盘）；**Agentic Commerce 后续**（预算三档对照）
- [ ] **研究 cron 加停搜判据**；**trending 选题查重**（10-27~11-04 连续错开 ✅；11-04 教训：worktrunk +77→+438 反弹，退潮判断需确认期）
- [ ] MCP 安全清单+tool 哈希锁 · **OpenShell 小范围试点**
- [ ] amg kd 手动续跑（候选 4 + 纪律见 MEMORY「kd 手动续跑」节）

## 系统状态
- **amg**: 11272 tests @C611；banked 366/500=0.732（47 连 keep）；**零回滚 380 天**；权威链 /tmp/c611
- **主力**：acs 3173 / atc 2052 / sot 619 / context-forge 1563 / nano 1162 / 全项目 ~24744（09-29 起零增量，纯内容日）
- **gateway**：当前代 11-04 23:17 启动（port 34526）；**下崩预计 ~03:30±25min（11-05）**（间隔族 222~270min 均值 248；预测四连中）
- **KO 日历**：11-02 ⚠️（edit 工具失败/实质完成）→ 11-03 ✅ → 11-04 ✅（Python 链路第二天顺畅）→ **11-05 ✅（本 run，Python 链路第三天顺畅+大压缩+daily 20:00 补账）**
- **博客**：11-04 三 commit（essay 确定性验证器 c34c6ce + dashboard 0fdf3a6 + 晚研写路径 RL 12d05ee）；dashboard 口径 464 posts；master 与 origin 同步

## 近期活动（11-03 ~ 11-04）
- **11-04（第 38 日，7/7 全绿 ×2）**：essay《生成交给模型，验收交给代码》c34c6ce（验证不对称性：否决特定坏答案比生成好答案便宜数量级；三态判定 confirmed/needs_validation/rejected；coverage ledger 增量审计；needs_validation 禁 severity=掐断幻觉传染）· dashboard 0fdf3a6（day 19；第 172 杀 02:36；MEMORY 97% 水位预警→本 run 压缩化解）· trending deep：agent-desktop 12.7k★（无障碍树+disposition.retry）+worktrunk（wt merge/APFS CoW/hash_port）· creative=晚间场：superpowers 312K 四大厂 marketplace 收编+anthropics skills 187K 上 weekly——skills 成 GitHub 最大品类；Scrapling 95.6k★；worktrunk 反弹修正昨日退潮判断 · 晚深研《记忆不是存出来的，是学出来的》12d05ee（Mem-α 写记忆=可泛化技能 13 倍泛化；Memory-r1 四原语；Memento 案例>梯度；memory drift 冷水）
- **11-03（第 37 日，7/7 全绿重开）**：essay《把 K 线变成语言》fd573c3（BSQ 层级双子 tokenizer/分位带=免费波动率）· dashboard 4d56910（day 18）· trending deep claude-mem 106.7k★+lightpanda（Zig 无渲染浏览器）· creative=晚间场（cloudflare security-audit-skill/impeccable/本地主权栈三件套）· 晚深研《别让你的 Agent 长成 npm》14a674b（SkillsBench +16.6pp vs 自写 -1.3pp；Library Drift；ToxicSkills 91%）

## 本周关键路径
1. ✅ 内容线连续 38 纯内容日（11-03 起连续 7/7 ×2）；⬜ 上游 issue 报告（置顶，248min 节拍族+预测四连中=证据包又厚一层）
2. ⬜ 49 技能对照实验（超期 17 天 ⚠️）+ headroom 决策（装前过 20 题配对）
3. ⬜ README/publish 四项目 — BLOCKED on human
4. ⬜ amg next（RRF A/B / 边 valid_at / 夜间整固 cron / 20 题召回基线 / 最小自进化循环）— 待罗嵩排期
5. ⬜ catalyst-research 54 项 untracked 批量 commit（下次手动窗口）

## 上次检查
- **KO 2026-11-05 02:00（本 run）**：✅ 第 38 日整合（11-04 7/7 收口+daily 20:00 补账）+ NRestarts=177（+5；248min 均值；预测四连中）+ MEMORY 大压缩 19.5k→18.0k（10-22~11-03 洞察精炼，20 锚点全过）+ HEARTBEAT 全刷新（eval-gap 17 天、Agent-Reach 28 天、新增 11-04 落点三候选）
- KO 2026-11-04 02:00：✅ 第 37 日整合（11-03 7/7 收口+daily 补账）+ NRestarts=171（+5；预测三连中）+ MEMORY 9 处 Python 替换全通过（19.0k）
- KO 2026-11-03 02:00：✅ 第 36 日整合（11-02 6/7 收口）+ NRestarts=166（+6）+ MEMORY 7 处 Python 替换全通过（18.5k）
- KO 2026-11-02 02:00：⚠️ 6/7——Edit MEMORY.md 工具 CJK 多块失败（实质完成未 commit）；NRestarts=160
- 更早（10-17~11-01）：✅ 详见各日 daily
