# HEARTBEAT.md - September 30, 2026 (Wednesday) — 02:00 KO update

## ⚠️ 执行环境变化（09-27 21:55 起）
**cron 15→8（罗嵩手动删 7 条）**：已删 00:00 kd-2 / 01:00 kd-3 / 21:00 code-lab-evening / 22:00 tool-development-evening / 23:00 key-development-1 / 03:00 project-testing-morning / 04:00 documentation-morning。夜间 kd 链、晚间自动开发、晨间测试/文档线全部停摆，**开发节奏转罗嵩手动驱动**（kd prompt 全文在 09-27 会话 cron list 输出中可随时重建；amg kd 赛道 0.732/47 连不受影响，可手动续跑）。剩余 8 cron 全为内容线：02:00 KO / 05:00 essay / 06:00 dashboard / 07:00+08:00 trending / 19:00 creative / 20:00 deep-exploration / 22:30 AI×Neuro

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **11272 tests**（@c596d1f C611；**banked 366/500=0.732，C565 起 47 连 keep（0.600→0.732）**），990+ APIs。能力全景：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 20+ forms）+ judge 链 + provenance 指纹 + kd face 族 39+ + 五条新赛道（recency-supersession/base+delta/distinct-days/N-times/(class,day)-dedup）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph`，均实测 FREE）— 技术前置 100% 完成 (#066)，human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**
- [ ] **structured-output-toolkit: README + npm publish** — **619 tests**
- [ ] **agent-task-cli: README + npm publish** — **2052 tests**，R82 ✅（Redis list 族上半场；余 8 法 R83 候选——cron 已删，手动驱动）

### 中优先级（本月）
- [x] amg MCP server — Research #043 ✅, Python MCP 16 tools；demo-orphan 已修复（09-24 473600a）
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] **AI×Neuro #55 章鱼篇补做** — 09-28 空壳 doc W8JJdfbtxolwVTx7WricKF8qndh 待某期补做或重发（#56 已用防超时流程正常闭环，流程法已验证）
- [ ] **竞品对读**：hindsight 优先（40.8k★，LongMemEval SOTA，amg 最直接对标；09-29 essay 94f7b16 已深拆其 observation/mental-model 机制——benchmarks.hindsight.vectorize.io=amg 分数外部参照系）+ codebase-memory-mcp（44.6k★ C，code-aware #044 直接竞品）+ ai-memory（Rust 同赛道）+ TencentCloud/Octop + paperclip（92.5k★ goal ancestry/预算硬停→mission-control 借鉴）

## 系统状态
- **agent-memory-graph (Python)**: **11272 tests** @C611（c596d1f fitness_week face；**banked 366/500=0.732，C565 起 47 连 keep；abs 30=18 abs+12 held；权威链 /tmp/c611/live500_c611.json**——被清以 HEAD 重跑重建 ~1200s）。**夜间 kd 链已停（cron 删除）**；kd queue 手动续跑参考：`gpt4_f2262a51` doctors（GT 长句 'three different doctors…'，clinic 噪声重，需 _cnt_numval 长句数值抽取验证）/ `gpt4_ab202e7f` kitchen 5 items（donate→replace 语义墙，设计偏重）/ `bf659f65` albums GT=3 只辨识 2（Telluride 'their EP' 歧义）/ `0a995998` clothing（C607 已判偏重）/ 项目对 + pref-gate 12 行 NEEDS_JUDGE（风险高）；unbanked 剩 134。核心纪律：harness verbatim 拷贝、tsv 裸字节 append（历史空行勿动）、census-first + **pin census 第 4 步**、队列候选先查链上 banked 态、**amg 新正则前缀 grep 前缀级冲突（_SPT_ 教训）**、**后台长 suite Tee 落盘（isatty()=False，/tmp/c611/run_suite.py 范本）**、pytest.main() 进程内=静默 exit-0（shell env 前缀 PYTHONHASHSEED=7）、python3 -m 必 runner 脚本化（TOOLS.md）、replay 一律 cp canonical + Python 字节级替换（count==1 assert）+ diff 审计、OOM 重活串行、exec timeout ≥400s（含 git commit）。_search_cache 46+ 天脏 hunk 留工作树（备份 /tmp/amg_dirty_backup_20260924.diff，将来独立 cycle）
- **agent-context-store**: **3173 tests**（09-17 三连击）
- **agent-task-cli**: **2052 tests** — R82 ✅。坑：exec timeout ≥400s；分支是 main；set 键非 JSON-exportable
- **context-forge**: **1563 tests** / **prompt-mgr**: **480** / **amf**: **754**（09-25 merge 悬空链接修复）
- **09-27 外部五连**: olb **320**（7c89fa2 rate-limit/throttle NaN 配置校验）/ a2at **108**（9dd93b6 trust-engine-v2 六纯函数守卫）/ sotk **619**（b3b0391 TemperatureSchedule）/ pw **229**（78f8ed8 literal_eval 沙箱逃逸）/ brc **401**（964d8bc split 先删后产零块守卫）/ dg **78**（e3da058 shift 越界静默退出）
- **tools/其他**: ctxpack 104 / ato 57 / afm 32 / project-dashboard 15 / skill-scaffolder 34 / session-archiver 90 / agent-memory-kit 33 / cqc 66 / act 51 / mcpt 41 / ai-dev-tools 93 / skill-doctor 81 / prompt-template-manager 34 / amg-mcp 128 / nano 1162 / mcx 65 / jp 59 / obs 268 / pocket-agent 80 / a2a_minimal 62 / cot 123 / wget-rust 25 / edge-agent-runtime 345 / agent-log 75 bats+32 / openclaw-mcp-server 29 / mission-control 45
- **四项目总计**: **13943**（amg 11272 + sot 619 + atc 2052）
- **全项目总计**: ~**24744** tests（09-29 连续纯内容日零增量维持；09-28 +51 口径）
- **零回滚率**: amg **344天** 🏆（KO 链 08-22:299 → 09-28:343 → 09-29:344；C565-C611 47 连 keep）/ acs **207天**（口径=有产出天数）
- **工具链**: ⚠️ Tavily 本月配额耗尽（432）——10-01 重置；月初前内容线搜索走 AnySearch(mcporter)+web_fetch 备援链（09-29 全天验证通畅）

## 近期活动 (09-29 全天——连续第 2 纯内容日，8/8 全绿)
- **05:00 essay《RAG 记得住，学不会》（94f7b16）**: hindsight 40.8k★ 深拆——observation 修正不覆盖/mental model 物化视图/recall≠learn；与 amg 同卷 LongMemEval 直接对照；staged 验尸 163 纯新增 0 删除
- **07:00/08:00 trending 双发**: 09-29 晚报（NVIDIA/OpenShell 头条=agent 运行时+策略形式化验证、openrig 同域、PageIndex 回榜、VoiceStudio 4 周 3 倍）；09-28 晚报缺失（幂等三查中记录）
- **19:00 creative**: 与 trending 同题晚报（buzz 落榜解除深析 flag）
- **20:00 deep-exploration（ebbd578）**: 《测试全绿，代码没修》Agent RL 奖励作弊全景——METR o3 30.4%/GPT-5 76% 可拨 92%↔1%/RHB 23×/Bergen 57-96% 激活探针；14 源笔记入 catalyst-research
- **22:30 AI×Neuro #56 裂脑人解释器 ✅**: doc KQ9Fd9BlionnVsxPOtlcWfwFnbd（59 blocks write+verify 一次过）+飞书投递 ✅——**防超时流程四招验证有效**（选题认领先行/搜索少而准/本地底稿先行/write+verify 一次过），未触 300s；遗留 #55 章鱼篇待补
- **全天零 dev 增量**（kd/测试/文档 cron 已删）+ 罗嵩无直接对话——连续第 2 个「无人类交互日」

## 本周关键路径
1. ✅ 09-28+09-29 内容线连续两日 8/8 全绿（essay×2 / 深研×2 / trending×4 / creative×2 / AI×Neuro #56 ✅）
2. ✅ AI×Neuro 超时问题以流程法解决（未动 timeoutSeconds；后续如再触发 300s 截杀才考虑加时）
3. ⬜ AI×Neuro #55 章鱼篇补做（空壳 doc W8JJdfbtxolwVTx7WricKF8qndh）
4. ⬜ kd 链续跑与否=罗嵩决策（手动续跑：queue 见系统状态节；或重建 cron——prompt 在 09-27 会话 cron list 输出）
5. ⬜ README(agent-memory-graph) → npm publish + amg PyPI 人工三步 + npm 命名决策 — **BLOCKED on human action**
6. ⬜ 竞品对读（hindsight 优先；09-29 essay 已完成其机制层深拆，余 benchmark 对照）
7. ⬜ Tavily 配额 10-01 重置后恢复默认搜索路由

## 上次检查
- **Knowledge org: 2026-09-30 02:00** — Integrated 09-29 全天（连续第 2 纯内容日 8/8 全绿：essay 94f7b16 hindsight《RAG 记得住学不会》+ 深研 ebbd578 奖励作弊全景 + AI×Neuro #56 ✅ 防超时流程四招验证无超时闭环——#55 章鱼仍欠；零 dev 增量计数全面持平；Tavily 月配额耗尽全程 AnySearch 备援；git ls-files echo 陷阱入册）。MEMORY：CF 09-29 新节+修复重复头行+Active Theme 09-29 段+零回滚 344；HEARTBEAT 全刷新
- **Knowledge org: 2026-09-29 02:00** — Integrated 09-28 全天（缩编后首个完整日：内容线 8/8 跑满、零 dev 增量计数不变；essay a5d3c98/深研 ec7902f OSWorld 两副面孔/trending OYAXdQNb/creative；⚠️ AI×Neuro #55 章鱼 300s 超时第 56 连 error——doc 空壳未写完+投递未达，选题表补行+topics 文件入库+修复方向入档）
- **Knowledge org: 2026-09-28 02:00** — Integrated 09-27 全天（cron 缩编 15→8；外部五连 +51；write 覆盖事故新规；docs C606-C611 追平+edit 标点归一化第 2 例新规；AI×Neuro 投递修复；code-lab 四连）
- **Knowledge org: 2026-09-27 02:00** — kd 三连 0.732/47 连；code-lab 四连；atc R82 2052；AI×Neuro #52 收口；_SPT_/Tee/pin census/pytest.main 四教训入库
