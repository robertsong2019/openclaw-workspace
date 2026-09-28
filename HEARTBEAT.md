# HEARTBEAT.md - September 29, 2026 (Tuesday) — 02:00 KO update

## ⚠️ 执行环境变化（09-27 21:55 起）
**cron 15→8（罗嵩手动删 7 条）**：已删 00:00 kd-2 / 01:00 kd-3 / 21:00 code-lab-evening / 22:00 tool-development-evening / 23:00 key-development-1 / 03:00 project-testing-morning / 04:00 documentation-morning。夜间 kd 链、晚间自动开发、晨间测试/文档线全部停摆，**开发节奏转罗嵩手动驱动**（kd prompt 全文在 09-27 会话 cron list 输出中可随时重建；amg kd 赛道 0.732/47 连不受影响，可手动续跑）。剩余 8 cron 全为内容线：02:00 KO / 05:00 essay / 06:00 dashboard / 07:00+08:00 trending / 19:00 creative / 20:00 deep-exploration / 22:30 AI×Neuro

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **11272 tests**（@c596d1f C611；**banked 366/500=0.732，C565 起 47 连 keep（0.600→0.732）**），990+ APIs。能力全景：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 20+ forms）+ judge 链 + provenance 指纹 + kd face 族 39+ + 五条新赛道（recency-supersession/base+delta/distinct-days/N-times/(class,day)-dedup）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph`，均实测 FREE）— 技术前置 100% 完成 (#066)，human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**
- [ ] **structured-output-toolkit: README + npm publish** — **619 tests**（09-27 晚 607→619 TemperatureSchedule NaN 校验）
- [ ] **agent-task-cli: README + npm publish** — **2052 tests**，R82 ✅（Redis list 族上半场；余 8 法 R83 候选——cron 已删，手动驱动）

### 中优先级（本月）
- [x] amg MCP server — Research #043 ✅, Python MCP 16 tools；demo-orphan 已修复（09-24 473600a）
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] **竞品对读**：hindsight 优先（26.9K★，LongMemEval SOTA，amg 最直接对标；09-27 深析已入飞书 ZUEodl3ohoAzXQxndRfc83rEn9c——benchmarks.hindsight.vectorize.io=amg 分数外部参照系）+ codebase-memory-mcp（44.6k★ C，code-aware #044 直接竞品）+ ai-memory（Rust 同赛道）+ TencentCloud/Octop（09-27 新面孔，OpenClaw 同类竞品）+ paperclip（87k★ goal ancestry/预算硬停→mission-control 借鉴）

## 系统状态
- **agent-memory-graph (Python)**: **11272 tests** @C611（c596d1f fitness_week face；**banked 366/500=0.732，C565 起 47 连 keep；abs 30=18 abs+12 held；权威链 /tmp/c611/live500_c611.json**——被清以 HEAD 重跑重建 ~1200s）。**夜间 kd 链已停（cron 删除）**；kd queue 手动续跑参考：`gpt4_f2262a51` doctors（GT 长句 'three different doctors…'，clinic 噪声重，需 _cnt_numval 长句数值抽取验证）/ `gpt4_ab202e7f` kitchen 5 items（donate→replace 语义墙，设计偏重）/ `bf659f65` albums GT=3 只辨识 2（Telluride 'their EP' 歧义）/ `0a995998` clothing（C607 已判偏重）/ 项目对 + pref-gate 12 行 NEEDS_JUDGE（风险高）；unbanked 剩 134。核心纪律：harness verbatim 拷贝、tsv 裸字节 append（历史空行勿动）、census-first + **pin census 第 4 步**、队列候选先查链上 banked 态、**amg 新正则前缀 grep 前缀级冲突（_SPT_ 教训）**、**后台长 suite Tee 落盘（isatty()=False，/tmp/c611/run_suite.py 范本）**、pytest.main() 进程内=静默 exit-0（shell env 前缀 PYTHONHASHSEED=7）、python3 -m 必 runner 脚本化（TOOLS.md）、replay 一律 cp canonical + Python 字节级替换（count==1 assert）+ diff 审计、OOM 重活串行、exec timeout ≥400s（含 git commit）。_search_cache 46+ 天脏 hunk 留工作树（备份 /tmp/amg_dirty_backup_20260924.diff，将来独立 cycle）
- **agent-context-store**: **3173 tests**（09-17 三连击）
- **agent-task-cli**: **2052 tests** — R82 ✅。坑：exec timeout ≥400s；分支是 main；set 键非 JSON-exportable
- **context-forge**: **1563 tests** / **prompt-mgr**: **480** / **amf**: **754**（09-25 merge 悬空链接修复）
- **09-27 外部五连**: olb **320**（7c89fa2 rate-limit/throttle NaN 配置校验）/ a2at **108**（9dd93b6 trust-engine-v2 六纯函数守卫）——03:00 双 keep +19；sotk **619**（b3b0391 TemperatureSchedule）/ pw **229**（78f8ed8 literal_eval 沙箱逃逸+while 死功能复活）/ brc **401**（964d8bc split 先删后产零块守卫）/ dg **78**（e3da058 shift 越界静默退出）——21:00 四连 +32
- **tools/其他**: ctxpack 104 / ato 57 / afm 32 / project-dashboard 15 / skill-scaffolder 34 / session-archiver 90 / agent-memory-kit 33 / cqc 66 / act 51 / mcpt 41 / ai-dev-tools 93 / skill-doctor 81 / prompt-template-manager 34 / amg-mcp 128 / nano 1162 / mcx 65 / jp 59 / obs 268 / pocket-agent 80 / a2a_minimal 62 / cot 123 / wget-rust 25 / edge-agent-runtime 345 / agent-log 75 bats+32 / openclaw-mcp-server 29 / mission-control 45
- **四项目总计**: **13943**（amg 11272 + sot 619 + atc 2052）
- **全项目总计**: ~**24744** tests（09-28 KO 口径：+51=olb +13/a2at +6/sotk +12/pw +6/brc +10/dg +4）
- **零回滚率**: amg **343天** 🏆（KO 链 08-22:299 → 09-27:342 → 09-28:343；C565-C611 47 连 keep）/ acs **207天**（口径=有产出天数）

## 近期活动 (09-28 全天 crons——缩编后首个完整内容日，零开发增量)
- **05:00 essay《MCP 统一了协议，没统一经济学》（a5d3c98）**: treg 四级凭证阶梯+凭证服务端注入+「预算即权限」；staged 验尸 165 纯新增 0 删除
- **06:00 dashboard（b7ca21b）**: 8 cron 口径；sessions 52/20-24h；标记 AI×Neuro「55 consecutive errors」（实为 300s 超时计数，09-27 doc 实交付 ✅）
- **07:00+08:00 trending 双发**: daily 9 项目 7 AI（paperclip 89,712★/hindsight 37,177★ 霸榜）；深析飞书 OYAXdQNb（双星与 09-27 同题深挖）
- **19:00 creative**: hindsight v0.10.1 常规版本节奏分析（常规产出）
- **20:00 deep-exploration（ec7902f）**: OSWorld 1.0 85% vs 2.0 20.6% 鸿沟博文——失败归因=行政老练度非 GUI 技能；部署门槛=可验证性非模型分
- **22:30 AI×Neuro ⚠️ 第 56 连 error**: 章鱼的分布式智能（表内 #55）——300s 超时截杀：doc W8JJdfbtxolw 空壳（write 未落盘，实测 revision 1）+ 无最终回复→投递未发生；选题表缺行已由 09-29 KO 补记（topics 文件首次入库）；修复=timeoutSeconds ≥480 或先发简版
- **全天零 dev 增量**（kd/测试/文档 cron 已删）+ 罗嵩无直接对话（主会话仅心跳）——首个「无人类交互日」

## 本周关键路径
1. ✅ 09-28 内容线 7/8 绿（essay a5d3c98/深研 ec7902f OSWorld/trending×2/creative/dashboard）；❌ AI×Neuro 22:30 300s 超时（doc 空壳未投递）待修
2. ⬜ kd 链续跑与否=罗嵩决策（手动续跑：queue 见系统状态节；或重建 cron——prompt 在 09-27 会话 cron list 输出）
3. ⬜ README(agent-memory-graph) → npm publish + amg PyPI 人工三步 + npm 命名决策 — **BLOCKED on human action**
4. ⬜ doc 队列（手动，如 kd 续跑则 C612+ 追平）；counting 形态学四分法（枚举/自述总数/仲裁/算术）可作 TUTORIAL §5 小结
5. ⬜ 竞品对读（hindsight 优先）

## 上次检查
- **Knowledge org: 2026-09-29 02:00** — Integrated 09-28 全天（缩编后首个完整日：内容线 8/8 跑满、零 dev 增量计数不变；essay a5d3c98/深研 ec7902f OSWorld 两副面孔/trending OYAXdQNb/creative；⚠️ AI×Neuro #55 章鱼 300s 超时第 56 连 error——doc 空壳未写完+投递未达，选题表补行+topics 文件入库+修复方向入档）。MEMORY：CF 09-28 节新增+Active Theme 09-28 段（120→123KB）；HEARTBEAT：近期活动/关键路径/已知问题/cron 健康全刷新
- **Knowledge org: 2026-09-28 02:00** — Integrated 09-27 全天（cron 缩编 15→8；03:00 双项目 +19（olb 320/a2at 108）+write 覆盖事故新规；04:00 docs C606-C611 追平+edit 标点归一化第 2 例新规；essay 6835207；AI×Neuro 投递修复当晚验证；code-lab 四连 sotk 619/pw 229/brc 401/dg 78；#55 鸣禽学歌。MEMORY：CF 09-28 新节+旧节归档（archive-2026-09-26-27.md）+Active Theme 343/09-27 段+Pre-08-15 长弧线归档+测试表全刷（13943/~24744）+Quick Reference 刷新；HEARTBEAT 全刷含执行环境变化节；123KB→120KB）
- **Knowledge org: 2026-09-27 02:00** — kd 三连 0.732/47 连；code-lab 四连；atc R82 2052；AI×Neuro #52 收口；_SPT_/Tee/pin census/pytest.main 四教训入库
- **Knowledge org: 2026-09-26 02:00** — C606-C608 三连 0.726；amf 754；doc 原则 22 条
- **Knowledge org: 2026-09-25 02:00** — C603-C605 三连 0.720；prompt-mgr 480

## ⚠️ 已知问题
- **cron 健康**: 8 条内容线 09-28 跑满：7 ok + **AI×Neuro 连续 error（09-27=55 连/09-28=56 连，均为 300s timeoutSeconds 截杀；09-27 doc 实交付 ✅ 但 09-28 doc W8JJdfbtxolw 空壳+投递未达）——待修：调 timeoutSeconds ≥480 或流程改先发简版再补写**；已删 7 条开发线——如需重建 kd/测试/文档 cron，prompt 全文在 09-27 会话 cron list 输出
- **memory_graph.py _search_cache +24 行脏 hunk（e04d222d）**: 46 天未提交——留工作树，备份 /tmp/amg_dirty_backup_20260924.diff，将来独立 cycle；另有 temporal_test_data.json / test_optimization.py / test_status.log 三个 untracked 杂物（挂账未清）
- **MEMORY.md size**: 120KB → **123KB**（09-29 KO：+09-28/09-29 CF 新节+Active Theme 09-28 段，无归档抵消）；下轮强烈建议执行瘦身：近期研究一览表精简 + Deep Research 节只留 #074+ 活跃项 + Timeline 旧节再归档
- **Tavily 配额**: 09-25/26/27 三连晚 432 超额；备援链已验证：AnySearch（TOOLS.md 路由）→ web_fetch（#55 全程成功：Google News RSS/arXiv API/DuckDuckGo；NCBI eutils 被封 IP）
- **experiments.tsv**: amg C410+ 条目在项目仓内，workspace tsv 记外部项目（C601 起 kd 行 workspace 短格式）；tsv HEAD 含 NUL 字节（历史遗留，修需专项 Python 行级手术）
- **npm publish blocked**: 四项目 13943 tests ready；README human review + amg npm 命名（#068 human-blocked）
- **Competitive pressure**: hindsight 26.9K★（LongMemEval SOTA，最直接对标）/ TencentCloud/Octop（OpenClaw 同类新面孔）/ codebase-memory-mcp 44.6k★ / hermes-agent 242k★ / ECC 264k★。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + counting 20+ forms + kd face 族 39+ + 五条新赛道
- **AI×Neuro Topic Pool**: #55 已交付（#54 起选题池自创）；候选：计算精神病学 / 噪声与随机共振 / 鸦科会聚智能
- **相邻 cron CPU 竞争**: 2GB 内存下 OOM 风险——重活串行；exec timeout ≥400s（含 git commit 带 hook）
- **atc / mission-control 分支是 main**（写死记忆）
