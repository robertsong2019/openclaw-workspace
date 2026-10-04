# HEARTBEAT.md - October 5, 2026 (Monday) 02:00 KO — 连续第 7 纯内容日·第二个全绿日

## ⚠️ 执行环境（09-27 起；10-02 一项修复）
**cron 现为 7 条（10-01 停用 ai-neuro 后）**: KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00，全内容线。09-27 罗嵩手删 7 条开发线 cron（kd 链/开发/测试/文档），**开发节奏=罗嵩手动驱动**（kd prompt 全文在 09-27 会话可重建；amg kd 赛道 0.732/47 连不受影响，queue 手动续跑参考下方系统状态节）。
**cron timeout 全表健康（10-03 验证闭环）**: creative 600 修复一次生效；KO/essay/daily/creative=600 / deep=900 / dashboard、deep-analysis=默认。
**Tavily 新 dev key 全链路生效（10-02 首战 ✅）**: 10-04 essay 素材核实一击全中。**永久教训：gateway=systemd user service，env 真源是 `gateway.systemd.env` 而非 `.env`，改 env 必须两处同步+重启**。AnySearch MCP 已从 mcporter 消失（仅剩 tencent-docs），备援链=web_fetch 直抓。
**已知 cosmetic warning**: cron list 带 `plugins.entries.memory-tencentdb: plugin not found`（stale config，待清理，不影响执行）。

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **11272 tests**（@c596d1f C611；**banked 366/500=0.732，C565 起 47 连 keep**），990+ APIs。能力全景：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 20+ forms）+ judge 链 + provenance 指纹 + kd face 族 39+ + 五条新赛道（recency-supersession/base+delta/distinct-days/N-times/(class,day)-dedup）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph`，均实测 FREE）— 技术前置 100% 完成 (#066)，human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**
- [ ] **structured-output-toolkit: README + npm publish** — **619 tests**
- [ ] **agent-task-cli: README + npm publish** — **2052 tests**，R82 ✅（Redis list 族上半场；余 8 法 R83 候选——手动驱动）

### 中优先级（本月）
- [ ] **hindsight vs amg 对标实验（10-04 evening 头号线索）**: 论文 arXiv 2512.12818 + 公开 benchmark 站（hindsight 45.3k★，周 +14.5k）——半天可出 amg 外部坐标；同表比较须先核对判分口径是否同源（09-30 情报）
- [ ] **paperclip budget 模型 → mission-control 治理化**（96.9k★，"OpenClaw 是员工，Paperclip 是公司"；预算即权限与 treg 四级凭证阶梯同族）+ **caveman_retrieve / context-mode 沙箱 → acs 压缩策略候选**
- [ ] **AGENTS.md 两条升级（10-04 trending-deep 线索）**: ①错误升级协议补「成功→候选 skill」对称方向（ECC instincts 双向沉淀）②双轴 review（mattpocock/skills）直接搬进 AGENTS.md
- [ ] **Agent-Reach tier-0 试装**（90.3k★；YouTube/B站/雪球对本地是净增量，exec profile 已满足；能力层架构=TOOLS.md 搜索路由表代码化的现成范本）
- [x] amg MCP server — Research #043 ✅, Python MCP 16 tools；demo-orphan 已修复（09-24 473600a）
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [x] **AI×Neuro 线停用（10-01 罗嵩指令）** — cron 已移除（8→7）；#55 章鱼篇欠账悬置（空壳 doc 不再追）
- [x] **trending-deep provider 故障归档为瞬态（10-03 关闭）**: 10-01 08:00 zai 三级空响应未复发，此后连续正常（10-04 飞书 336 blocks）
- [ ] **竞品对读**：hindsight 优先（对标实验见上）+ codebase-memory-mcp（44.6k★ C，code-aware #044 直接竞品）+ ai-memory（Rust）+ TencentCloud/Octop + pi（112.3k★，agent loop 架构，README 自证与 OpenClaw 集成关系——候选下期深研）+ mattpocock/skills（275k★，可作 skills 采样库专题）

## 系统状态
- **agent-memory-graph (Python)**: **11272 tests** @C611（c596d1f fitness_week face；**banked 366/500=0.732，C565 起 47 连 keep；abs 30=18 abs+12 held；权威链 /tmp/c611/live500_c611.json**——被清以 HEAD 重跑重建 ~1200s）。**kd 链停（cron 删除）**；手动续跑 queue 参考：`gpt4_f2262a51` doctors（GT 长句 'three different doctors…'）/ `gpt4_ab202e7f` kitchen 5 items（donate→replace 语义墙）/ `bf659f65` albums GT=3 只辨识 2（Telluride 'their EP' 歧义）/ `0a995998` clothing（C607 已判偏重）/ 项目对 + pref-gate 12 行 NEEDS_JUDGE（风险高）；unbanked 剩 134。核心纪律：harness verbatim 拷贝、tsv 裸字节 append、census-first + pin census 第 4 步、队列候选先查链上 banked 态、**amg 新正则前缀 grep 前缀级冲突（_SPT_ 教训）**、**后台长 suite Tee 落盘（/tmp/c611/run_suite.py 范本）**、pytest.main() 进程内=静默 exit-0（shell env 前缀 PYTHONHASHSEED=7）、python3 -m 必 runner 脚本化（TOOLS.md）、replay 一律 cp canonical + Python 字节级替换（count==1 assert）+ diff 审计、OOM 重活串行、exec timeout ≥400s（含 git commit）。_search_cache 46+ 天脏 hunk 留工作树（备份 /tmp/amg_dirty_backup_20260924.diff，将来独立 cycle）
- **agent-context-store**: **3173 tests**（09-17 三连击）
- **agent-task-cli**: **2052 tests** — R82 ✅。坑：exec timeout ≥400s；分支是 main；set 键非 JSON-exportable
- **context-forge**: **1563 tests** / **prompt-mgr**: **480** / **amf**: **754**（09-25 merge 悬空链接修复）
- **09-27 外部五连**: olb **320** / a2at **108** / sotk **619** / pw **229** / brc **401** / dg **78**
- **tools/其他**: ctxpack 104 / ato 57 / afm 32 / project-dashboard 15 / skill-scaffolder 34 / session-archiver 90 / agent-memory-kit 33 / cqc 66 / act 51 / mcpt 41 / ai-dev-tools 93 / skill-doctor 81 / prompt-template-manager 34 / amg-mcp 128 / nano 1162 / mcx 65 / jp 59 / obs 268 / pocket-agent 80 / a2a_minimal 62 / cot 123 / wget-rust 25 / edge-agent-runtime 345 / agent-log 75 bats+32 / openclaw-mcp-server 29 / mission-control 45
- **四项目总计**: **13943**（amg 11272 + sot 619 + atc 2052）
- **全项目总计**: ~**24744** tests（09-28 后连续纯内容日零增量维持）
- **零回滚率**: amg **349天** 🏆（KO 链 08-22:299 → 10-02:347 → 10-03:348 → 10-04:349；C565-C611 47 连 keep）/ acs **207天**（口径=有产出天数）
- **工具链**: Tavily 新 dev key 全链路生效（10-02 首战、10-04 再验证）；AnySearch MCP 已从 mcporter 消失（仅剩 tencent-docs），备援=web_fetch 直抓；tencentdb stale plugin warning 待清理
- **10-04 02:00 KO cron err=「edit fail」口径伪影**: 产物齐全且已 commit（4f7e1b6），dashboard 次日已标注；本 KO 改用 Python 脚本重放编辑 MEMORY.md（TOOLS.md CJK 多块编辑规则的正常执行，非事件）

## 近期活动 (10-04 全天——连续第 7 纯内容日，内容线 6/6 全绿：第二个连续全绿日)
- **05:00 essay《最好的代码是你没写的代码》（76e2470）**: ponytail 懒惰决策阶梯——七级阶梯（代码库已有→stdlib→平台原生→已装依赖→一行→最小实现）/"规则从不是 fewest tokens"（省解空间非省 token；caveman 文风对照 token 反 +7%）/三臂 agentic 基准 -54% LOC 100% safe、YAGNI 提示词 safe 95%=把简洁理解成砍校验/基准修正史 80-94%→-54% 与本地「显示层 bug 伪装数据异常」家族同源/30 行 ladder_preflight 闸门；post 200 首查即过
- **06:00 dashboard 97c1ce6 ✅ / 07:00 daily ✅（轻量）**: err 1=10-04 02:00 KO edit-fail 口径伪影（产物齐全）；creative 2→0 恢复
- **08:00 trending-deep 飞书 XKFhdQ2VYozTX7xOPr5c93VFnFy（336 blocks）✅**: 日榜 agent harness/skills/上下文工程占 Top15 的 11 席——ECC（17-harness 适配矩阵、instincts 双向沉淀）+ Agent-Reach（能力层架构：which() 不算健康证明/tier 分层）；四条可落地线索入中优先级
- **19:00 creative ✅ 周榜「记忆与组织」接管**: hindsight 45.3k★（周 +14.5k）/ paperclip 96.9k★ / hyperframes 56.5k★（HeyGen 开源 HTML→确定性 MP4）/ Agent-Reach 90.3k★ / VoiceStudio 52.8k★ / pi 112.3k★ / cloudflare-os 10.7k★；给罗嵩三件事：hindsight 对标实验 / caveman 沙箱→acs / paperclip budget→mission-control
- **20:00 deep-exploration 54eb149《技能给同一个 Agent 带 +16 分或 0 分，差别只在谁来写》**: Agent 技能习得首覆盖——SkillsBench 策展 +16.6pp vs 自生成 0 / SkillWeaver 验证闭环 +31.8%（自由生成×执行验证×门控入库缺一归零；强→弱迁移 +54.3%）/ SkillsVote 1.68M SKILL.md 证据门控治理 / Snyk ToxicSkills 36.8% 缺陷率 91% 注入+恶意码 / DGM 20→50 瓶颈是裁判不是创造力；笔记入 catalyst-research
- **全天零 dev 增量**（计数持平第 7 日）+ 零回滚 349；本周主轴成型：「技能/记忆的治理与验证」（essay+深研+creative 三线呼应）

## 本周关键路径
1. ✅ 09-28~10-04 内容线连续七日运行（essay×7 / 深研×7 / dashboard×7 / daily×6 / creative×6 缺 10-02；AI×Neuro 10-01 停用）；**10-03+10-04 连续两日 6/6 全绿**
2. ✅ creative timeout 600 修复验证闭环；✅ Tavily 工具链修复；✅ trending-deep provider 瞬态归档；✅ cron timeout 全表健康
3. ⬜ kd 链续跑与否=罗嵩决策（手动续跑 queue 见系统状态节；或重建 cron——prompt 在 09-27 会话）
4. ⬜ README(agent-memory-graph) → npm publish + amg PyPI 人工三步 + npm 命名决策 — **BLOCKED on human action**
5. ⬜ hindsight vs amg 对标实验（半天可出坐标）+ 竞品对读（pi/Octop 新入）
6. ⬜ amg next（09-30 深研产出）：nightly consolidation + AgentSleep 四指标评测——待罗嵩排期或手动 kd 窗口
7. ⬜ 10-04 双 cron 线索落地：AGENTS.md 双轴 review +「成功→候选 skill」对称方向 / Agent-Reach tier-0 试装 / paperclip budget→mission-control

## 上次检查
- **Knowledge org: 2026-10-05 02:00** — Integrated 10-04 全天（连续第 7 纯内容日·第二个连续全绿日：essay 76e2470 最好的代码是你没写的代码 ponytail 懒惰决策阶梯 / 深研 54eb149 技能习得 SkillsBench 首覆盖 / dashboard 97c1ce6 / 飞书 336 blocks ECC+Agent-Reach / creative 周榜记忆与组织接管 / 零回滚 349）。MEMORY：10-04 新节+Active Theme+测试快照 10-05+**09-28~30 Current Focus 归档至 memory/archive-2026-09-28-30.md**（瘦身）；HEARTBEAT 全刷新（10-04 线索入中优先级）；10-04 daily 补录 06:00/07:00+KO 小结
- **Knowledge org: 2026-10-04 02:00** — Integrated 10-03 全天（连续第 6 纯内容日，内容线 6/6 全绿=7-cron 体制首个全绿日：essay 2a83a7b 零个工人无效配置四死法 + 深研 f01975c Context Rot 首覆盖 + dashboard 032291c + 飞书 161 blocks + creative ✅ timeout 600 修复验证闭环 + evening Harness 层总爆发；零回滚 348）。MEMORY：10-03 新节+Active Theme+测试快照 10-04；HEARTBEAT 全刷新（creative 验证项关闭）；10-03 daily 补录 06:00/07:00
- **Knowledge org: 2026-10-03 02:00** — Integrated 10-02 全天（连续第 5 纯内容日 5/6：essay 2430953 状态谎言五图鉴 / 深研 a7b5b9a 扩散 LLM 首覆盖 / dashboard 4bc2a39 / daily OpenShell 加速翻倍 / deep 飞书 229 blocks；❌ 19:00 creative 真实失败=timeout 300 同 ai-neuro 病，KO 现场修复 300→600 待 10-03 验证；provider 瞬态归档；零回滚 347）
- **Knowledge org: 2026-10-02 02:00** — Integrated 10-01 全天（连续第 4 纯内容日 6/7；❌ 08:00 trending-deep provider 级联空响应=真实缺口入档；AI×Neuro cron 停用 8→7；Tavily 新 key 三段修复闭环 KO /proc 实测生效）
- **Knowledge org: 2026-10-01 11:15** — 罗嵩两条指令落地：Tavily key 更新 + ai-neuroscience-research 停用，cron 8→7
