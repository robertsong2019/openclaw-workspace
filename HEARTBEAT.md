# HEARTBEAT.md - October 4, 2026 (Sunday) 02:00 KO — 内容线首个全绿日（6/6）

## ⚠️ 执行环境（09-27 起；10-02 一项修复）
**cron 现为 7 条（10-01 停用 ai-neuro 后）**: KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00，全内容线。09-27 罗嵩手删 7 条开发线 cron（kd 链/开发/测试/文档），**开发节奏=罗嵩手动驱动**（kd prompt 全文在 09-27 会话可重建；amg kd 赛道 0.732/47 连不受影响，queue 手动续跑参考下方系统状态节）。
**creative timeout 600 修复验证闭环 ✅（10-03）**: 10-02 KO 现场修复（300→600）后，10-03 19:00 creative 正常落地（19:05 出报告）——一次生效，ai-neuro 型隐患全部排除。**cron timeout 现全表健康**（KO/essay/daily/creative=600 / deep=900 / dashboard、deep-analysis=默认）。
**Tavily 新 dev key 全链路生效（10-02 首战 ✅）**: 10-02 essay 两搜全中。**永久教训：gateway=systemd user service，env 真源是 `gateway.systemd.env` 而非 `.env`，改 env 必须两处同步+重启**。AnySearch MCP 已从 mcporter 消失（仅剩 tencent-docs），备援链=web_fetch 直抓。
**已知 cosmetic warning**: cron list 带 `plugins.entries.memory-tencentdb: plugin not found`（stale config，待清理，不影响执行）。

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **11272 tests**（@c596d1f C611；**banked 366/500=0.732，C565 起 47 连 keep**），990+ APIs。能力全景：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 20+ forms）+ judge 链 + provenance 指纹 + kd face 族 39+ + 五条新赛道（recency-supersession/base+delta/distinct-days/N-times/(class,day)-dedup）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph`，均实测 FREE）— 技术前置 100% 完成 (#066)，human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**
- [ ] **structured-output-toolkit: README + npm publish** — **619 tests**
- [ ] **agent-task-cli: README + npm publish** — **2052 tests**，R82 ✅（Redis list 族上半场；余 8 法 R83 候选——手动驱动）

### 中优先级（本月）
- [x] amg MCP server — Research #043 ✅, Python MCP 16 tools；demo-orphan 已修复（09-24 473600a）
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [x] **AI×Neuro 线停用（10-01 罗嵩指令）** — cron 已移除（8→7）；#55 章鱼篇欠账悬置（空壳 doc 不再追）
- [x] **trending-deep provider 故障归档为瞬态（10-03 关闭）**: 10-01 08:00 zai 三级空响应未复发，10-02 08:00 飞书 229 blocks 正常产出
- [ ] **竞品对读**：hindsight 优先（40.8k★，LongMemEval SOTA；09-29 essay 94f7b16 已深拆机制，余 benchmark 对照——benchmarks.hindsight.vectorize.io=amg 外部参照系）+ codebase-memory-mcp（44.6k★ C，code-aware #044 直接竞品）+ ai-memory（Rust）+ TencentCloud/Octop + paperclip（92.5k★ 预算硬停→mission-control 借鉴）。**NVIDIA OpenShell 加速翻倍（11.1k→13.98k，+2,503/日全榜最陡）值得关注其 memory/沙箱路线与 amg 的关系**
- [x] ✅ **10-03 19:00 creative 验证通过**（10-04 KO 关闭）: timeout 600 修复后 19:05 正常落地 trending-evening 报告，无需再查

## 系统状态
- **agent-memory-graph (Python)**: **11272 tests** @C611（c596d1f fitness_week face；**banked 366/500=0.732，C565 起 47 连 keep；abs 30=18 abs+12 held；权威链 /tmp/c611/live500_c611.json**——被清以 HEAD 重跑重建 ~1200s）。**kd 链停（cron 删除）**；手动续跑 queue 参考：`gpt4_f2262a51` doctors（GT 长句 'three different doctors…'）/ `gpt4_ab202e7f` kitchen 5 items（donate→replace 语义墙）/ `bf659f65` albums GT=3 只辨识 2（Telluride 'their EP' 歧义）/ `0a995998` clothing（C607 已判偏重）/ 项目对 + pref-gate 12 行 NEEDS_JUDGE（风险高）；unbanked 剩 134。核心纪律：harness verbatim 拷贝、tsv 裸字节 append、census-first + pin census 第 4 步、队列候选先查链上 banked 态、**amg 新正则前缀 grep 前缀级冲突（_SPT_ 教训）**、**后台长 suite Tee 落盘（/tmp/c611/run_suite.py 范本）**、pytest.main() 进程内=静默 exit-0（shell env 前缀 PYTHONHASHSEED=7）、python3 -m 必 runner 脚本化（TOOLS.md）、replay 一律 cp canonical + Python 字节级替换（count==1 assert）+ diff 审计、OOM 重活串行、exec timeout ≥400s（含 git commit）。_search_cache 46+ 天脏 hunk 留工作树（备份 /tmp/amg_dirty_backup_20260924.diff，将来独立 cycle）
- **agent-context-store**: **3173 tests**（09-17 三连击）
- **agent-task-cli**: **2052 tests** — R82 ✅。坑：exec timeout ≥400s；分支是 main；set 键非 JSON-exportable
- **context-forge**: **1563 tests** / **prompt-mgr**: **480** / **amf**: **754**（09-25 merge 悬空链接修复）
- **09-27 外部五连**: olb **320** / a2at **108** / sotk **619** / pw **229** / brc **401** / dg **78**
- **tools/其他**: ctxpack 104 / ato 57 / afm 32 / project-dashboard 15 / skill-scaffolder 34 / session-archiver 90 / agent-memory-kit 33 / cqc 66 / act 51 / mcpt 41 / ai-dev-tools 93 / skill-doctor 81 / prompt-template-manager 34 / amg-mcp 128 / nano 1162 / mcx 65 / jp 59 / obs 268 / pocket-agent 80 / a2a_minimal 62 / cot 123 / wget-rust 25 / edge-agent-runtime 345 / agent-log 75 bats+32 / openclaw-mcp-server 29 / mission-control 45
- **四项目总计**: **13943**（amg 11272 + sot 619 + atc 2052）
- **全项目总计**: ~**24744** tests（09-28 后连续纯内容日零增量维持）
- **零回滚率**: amg **348天** 🏆（KO 链 08-22:299 → 10-01:346 → 10-02:347 → 10-03:348；C565-C611 47 连 keep）/ acs **207天**（口径=有产出天数）
- **工具链**: Tavily 新 dev key 全链路生效（10-02 首战两搜全中）；AnySearch MCP 已从 mcporter 消失（仅剩 tencent-docs），备援=web_fetch 直抓；tencentdb stale plugin warning 待清理

## 近期活动 (10-03 全天——连续第 6 纯内容日，内容线 6/6 全绿：7-cron 体制首个全绿日)
- **05:00 essay《零个工人，提前完工》（2a83a7b）**: 无效配置四种静默死法（concurrency:0 圆满假象 / throttle limit:0 永假死锁 / maxAttempts:0 throw undefined / withTimeout 吞错误）——langgraph-bridge C1-C4 真实 bug + K8s/Headlamp 锚点 + AI 代码偏爱此路四因 + 构造期爆炸防线；与 10-02 状态谎言构成上下篇（汇报层骗局/执行层骗局）；post 200 首查即过
- **06:00 dashboard 032291c ✅ / 07:00 daily ✅**: err 2→1（trending-deep 恢复）；内存 575MB 回升、磁盘 68% 持平
- **08:00 trending-deep 飞书 XOpsdYOPYoFpM9xjOXFcOdFPnse（161 blocks）✅**: context-mode 25k★（沙箱/FTS5+BM25 会话连续性/Think in Code/路由风格解耦）+ openrig 4.3k★（scenario 测试可搬 mission-control）
- **19:00 creative ✅ timeout 600 修复验证闭环**: 19:05 落地 evening 报告——主旋律 Harness 层总爆发（日榜 12 席 5 席 skills/harness + 2 席 token 经济学；superpowers 294.7k/mattpocock 275k/ECC 271.7k 十万俱乐部成常态）；给罗嵩三线索：双轴 review / Mental Models 摊销式记忆博文 / Octop（腾讯 OpenClaw 同类品 6.5k★）
- **20:00 deep-exploration《窗口还空着一半，模型已经开始忘了》（f01975c）**: Context Rot 首覆盖 15+ 源——Chroma 18 模型（几千 token 起持续滑坡非窗口满才崩）/NoLiMa 11/12 跌破一半/RULER 有效上下文差 99% 是任务函数/注意力是黄油非硬盘/缓存反转 do-nothing 三项全胜/治理衰减（约束最先死，第 40 轮愉快违反第 2 轮规矩）/RLM agent-as-retriever 检索钟摆第三摆；笔记 12KB 入 catalyst-research
- **全天零 dev 增量**（计数持平第 6 日）+ 零回滚 348

## 本周关键路径
1. ✅ 09-28~10-03 内容线连续六日运行（essay×6 / 深研×6 / dashboard×6 / daily×5 / creative×5 缺 1；AI×Neuro 10-01 停用）；**10-03 内容线 6/6 全绿（7-cron 体制首个全绿日）**
2. ✅ creative timeout 600 修复验证闭环（10-03 19:05 落地）；✅ Tavily 工具链修复（10-02 首战验证）；✅ trending-deep provider 瞬态归档；✅ cron timeout 全表健康
3. ⬜ kd 链续跑与否=罗嵩决策（手动续跑 queue 见系统状态节；或重建 cron——prompt 在 09-27 会话）
4. ⬜ README(agent-memory-graph) → npm publish + amg PyPI 人工三步 + npm 命名决策 — **BLOCKED on human action**
5. ⬜ 竞品对读（hindsight 优先；OpenShell 路线观察；Octop 新入=腾讯 OpenClaw 同类品对照）
6. ⬜ amg next（09-30 深研产出）：nightly consolidation + AgentSleep 四指标评测——待罗嵩排期或手动 kd 窗口
7. ⬜ 素材候选：hindsight Mental Models 摊销式记忆（10-03 evening 线索）可作 essay/深研选题

## 上次检查
- **Knowledge org: 2026-10-04 02:00** — Integrated 10-03 全天（连续第 6 纯内容日，内容线 6/6 全绿=7-cron 体制首个全绿日：essay 2a83a7b 零个工人 / 深研 f01975c Context Rot 首覆盖 / dashboard 032291c / 飞书 161 blocks / **creative ✅ timeout 600 修复验证闭环** / evening Harness 层总爆发；零回滚 348）。MEMORY：10-03 新节+Active Theme+测试快照 10-04；HEARTBEAT 全刷新（creative 验证项关闭）；10-03 daily 补录 06:00/07:00
- **Knowledge org: 2026-10-03 02:00** — Integrated 10-02 全天（连续第 5 纯内容日 5/6：essay 2430953 状态谎言五图鉴 / 深研 a7b5b9a 扩散 LLM 首覆盖 / dashboard 4bc2a39 / daily OpenShell 加速翻倍 / deep 飞书 229 blocks；❌ 19:00 creative 真实失败=timeout 300 同 ai-neuro 病，KO 现场修复 300→600 待 10-03 验证；provider 瞬态归档；零回滚 347）。MEMORY：10-02 新节+测试快照 10-03；HEARTBEAT 全刷新；10-02 daily 补录 06:00/07:00/19:00
- **Knowledge org: 2026-10-02 02:00** — Integrated 10-01 全天（连续第 4 纯内容日 6/7；❌ 08:00 trending-deep provider 级联空响应=真实缺口入档；AI×Neuro cron 停用 8→7；Tavily 新 key 三段修复闭环 KO /proc 实测生效）
- **Knowledge org: 2026-10-01 11:15** — 罗嵩两条指令落地：Tavily key 更新 + ai-neuroscience-research 停用，cron 8→7
- **Knowledge org: 2026-10-01 02:00** — Integrated 09-30 全天（连续第 3 纯内容日 8/8 全执行；零回滚 345）
- **Knowledge org: 2026-09-30 02:00** — Integrated 09-29 全天（连续第 2 纯内容日 8/8 全绿；零回滚 344；git ls-files echo 陷阱入册）
