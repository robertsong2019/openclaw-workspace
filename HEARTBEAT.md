# HEARTBEAT.md - September 28, 2026 (Monday) — 02:00 KO update

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

## 近期活动 (09-27 全天 crons——cron 缩编前最后一个完整日)
- **03:00 project-testing 双 keep +19**: olb 307→**320** + a2at 102→**108**；⚠️ write 覆盖事故（`ls|head` 截断误判→覆盖 26 pins→staged diff 验尸自救）→新规：**write 前 `git ls-files` 验存在性**
- **04:00 docs C606-C611 六连追平（df77623）**: README badge 11272 + TUTORIAL §5.57-§5.62 + 原则 23 条；⚠️ edit 工具标点归一化第 2 例（多块编辑触发全文件全角→半角）→新规：**CJK 密集文件多块编辑走 Python 字节级重放**
- **05:00 essay《工具说成功，diff 说不是》（6835207）**: 双事故成文；index.html 插入自我实践 Python 锚点替换
- **06:00 dashboard 26a20e5 + AI×Neuro 投递修复**: 84707ade 54 连败根因=delivery 缺 `to`→已补，当晚验证 ✅
- **08:00 trending 深析（飞书 ZUEodl3ohoAzXQxndRfc83rEn9c）**: hindsight（LongMemEval SOTA=amg 外部参照系）+ paperclip（87k★）
- **19:00 creative**: treg「OpenRouter for agent tools」头条；Octop（腾讯 OpenClaw 竞品）新面孔；Tavily 432→curl 抓取
- **20:00 deep-exploration**: Agent 记忆图结构化（12 系统调研；博文 e305827；next actions 连 amg：PPR 检索臂/双时戳/建图成本实测）
- **21:00 code-lab 四连 keep +32**: sotk 619 / pw 229 / brc 401 / dg 78（新形态×2：shift N 静默退出 / split 先删后产零块）
- **21:55 罗嵩删 cron ×7（15→8）**: 夜间 kd + 晚间自动开发 + 晨间测试/文档全停（见顶部）
- **22:30 AI×Neuro #55 鸣禽学歌（XSmLdH8gmoeFguxrI5kcsThGn1）**: RLHF 生物原型；Tavily 耗尽→web_fetch 全程替代成功；投递修复验证 ✅；选题池 #54 起自创

## 本周关键路径
1. ✅ 09-27 内容线全绿（essay/dashboard/trending×2/creative/深研/AI×Neuro #55）
2. ⬜ kd 链续跑与否=罗嵩决策（手动续跑：queue 见系统状态节；或重建 cron——prompt 在 09-27 会话 cron list 输出）
3. ⬜ README(agent-memory-graph) → npm publish + amg PyPI 人工三步 + npm 命名决策 — **BLOCKED on human action**
4. ⬜ doc 队列（手动，如 kd 续跑则 C612+ 追平）；counting 形态学四分法（枚举/自述总数/仲裁/算术）可作 TUTORIAL §5 小结
5. ⬜ 竞品对读（hindsight 优先）

## 上次检查
- **Knowledge org: 2026-09-28 02:00** — Integrated 09-27 全天（cron 缩编 15→8；03:00 双项目 +19（olb 320/a2at 108）+write 覆盖事故新规；04:00 docs C606-C611 追平+edit 标点归一化第 2 例新规；essay 6835207；AI×Neuro 投递修复当晚验证；code-lab 四连 sotk 619/pw 229/brc 401/dg 78；#55 鸣禽学歌。MEMORY：CF 09-28 新节+旧节归档（archive-2026-09-26-27.md）+Active Theme 343/09-27 段+Pre-08-15 长弧线归档+测试表全刷（13943/~24744）+Quick Reference 刷新；HEARTBEAT 全刷含执行环境变化节；123KB→120KB）
- **Knowledge org: 2026-09-27 02:00** — kd 三连 0.732/47 连；code-lab 四连；atc R82 2052；AI×Neuro #52 收口；_SPT_/Tee/pin census/pytest.main 四教训入库
- **Knowledge org: 2026-09-26 02:00** — C606-C608 三连 0.726；amf 754；doc 原则 22 条
- **Knowledge org: 2026-09-25 02:00** — C603-C605 三连 0.720；prompt-mgr 480

## ⚠️ 已知问题
- **cron 健康**: 剩余 8 条内容线 09-27 全绿（#55 投递修复验证 ✅）；已删 7 条开发线——如需重建 kd/测试/文档 cron，prompt 全文在 09-27 会话 cron list 输出
- **memory_graph.py _search_cache +24 行脏 hunk（e04d222d）**: 46 天未提交——留工作树，备份 /tmp/amg_dirty_backup_20260924.diff，将来独立 cycle；另有 temporal_test_data.json / test_optimization.py / test_status.log 三个 untracked 杂物（挂账未清）
- **MEMORY.md size**: 123KB → **120KB**（09-28 KO：CF 旧节+Pre-08-15 长弧线已移 archive-2026-09-26-27.md，新节抵消部分）；下轮候选=近期研究一览表精简 + Deep Research 节只留 #074+ 活跃项
- **Tavily 配额**: 09-25/26/27 三连晚 432 超额；备援链已验证：AnySearch（TOOLS.md 路由）→ web_fetch（#55 全程成功：Google News RSS/arXiv API/DuckDuckGo；NCBI eutils 被封 IP）
- **experiments.tsv**: amg C410+ 条目在项目仓内，workspace tsv 记外部项目（C601 起 kd 行 workspace 短格式）；tsv HEAD 含 NUL 字节（历史遗留，修需专项 Python 行级手术）
- **npm publish blocked**: 四项目 13943 tests ready；README human review + amg npm 命名（#068 human-blocked）
- **Competitive pressure**: hindsight 26.9K★（LongMemEval SOTA，最直接对标）/ TencentCloud/Octop（OpenClaw 同类新面孔）/ codebase-memory-mcp 44.6k★ / hermes-agent 242k★ / ECC 264k★。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + counting 20+ forms + kd face 族 39+ + 五条新赛道
- **AI×Neuro Topic Pool**: #55 已交付（#54 起选题池自创）；候选：计算精神病学 / 噪声与随机共振 / 鸦科会聚智能
- **相邻 cron CPU 竞争**: 2GB 内存下 OOM 风险——重活串行；exec timeout ≥400s（含 git commit 带 hook）
- **atc / mission-control 分支是 main**（写死记忆）
