# HEARTBEAT.md - October 2, 2026 (Friday) 02:00 KO — Tavily 新 key 生效 + AI×Neuro 停用后首个完整日

## ⚠️ 执行环境变化（09-27 起；10-01 两项落地）
**cron 现为 7 条（10-01 11:12 罗嵩指令停用 ai-neuroscience-research）**: 剩余 KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00，全内容线。09-27 罗嵩已手删 7 条开发线 cron（kd 链/开发/测试/文档），**开发节奏=罗嵩手动驱动**（kd prompt 全文在 09-27 会话可重建；amg kd 赛道 0.732/47 连不受影响，queue 手动续跑参考下方系统状态节）。
**Tavily 新 dev key 已全链路生效（10-01 三段修复闭环）**: `.env` + `gateway.systemd.env` 双文件均已更新，gateway 10-02 01:17 重启后 KO 实测 `/proc/PID/environ` 含 tvly-dev ✅。**永久教训：gateway=systemd user service，env 真源是 `gateway.systemd.env` 而非 `.env`，改 env 必须两处同步+重启**。旧 key 月配额 10-01 未自然重置（KO 预测落空）。AnySearch MCP 已从 mcporter 消失（仅剩 tencent-docs），备援链=web_fetch 直抓（Science 403，Nature 可试）。
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
- [x] **AI×Neuro 线停用（10-01 罗嵩指令）** — cron 已移除（8→7）；#55 章鱼篇欠账悬置（空壳 doc W8JJdfbtxolwVTx7WricKF8qndh 不再追）；若将来重启须 timeoutSeconds≥900 或先发简版再补写
- [ ] **竞品对读**：hindsight 优先（40.8k★，LongMemEval SOTA，amg 最直接对标；09-29 essay 94f7b16 已深拆其机制——benchmarks.hindsight.vectorize.io=amg 分数外部参照系）+ codebase-memory-mcp（44.6k★ C，code-aware #044 直接竞品）+ ai-memory（Rust 同赛道）+ TencentCloud/Octop + paperclip（92.5k★ goal ancestry/预算硬停→mission-control 借鉴）
- [ ] **trending-deep provider 故障观察（10-01 08:00 ❌）**: zai 三级模型（5.3-flash→5-turbo→5）级联空响应，~1min 即死 0 token（session 899c0281 取证）。10-02 08:00 若复发→先查 provider 健康再查任务管线；若恢复→一次即可归档为瞬态

## 系统状态
- **agent-memory-graph (Python)**: **11272 tests** @C611（c596d1f fitness_week face；**banked 366/500=0.732，C565 起 47 连 keep；abs 30=18 abs+12 held；权威链 /tmp/c611/live500_c611.json**——被清以 HEAD 重跑重建 ~1200s）。**kd 链停（cron 删除）**；手动续跑 queue 参考：`gpt4_f2262a51` doctors（GT 长句 'three different doctors…'）/ `gpt4_ab202e7f` kitchen 5 items（donate→replace 语义墙）/ `bf659f65` albums GT=3 只辨识 2（Telluride 'their EP' 歧义）/ `0a995998` clothing（C607 已判偏重）/ 项目对 + pref-gate 12 行 NEEDS_JUDGE（风险高）；unbanked 剩 134。核心纪律：harness verbatim 拷贝、tsv 裸字节 append、census-first + pin census 第 4 步、队列候选先查链上 banked 态、**amg 新正则前缀 grep 前缀级冲突（_SPT_ 教训）**、**后台长 suite Tee 落盘（/tmp/c611/run_suite.py 范本）**、pytest.main() 进程内=静默 exit-0（shell env 前缀 PYTHONHASHSEED=7）、python3 -m 必 runner 脚本化（TOOLS.md）、replay 一律 cp canonical + Python 字节级替换（count==1 assert）+ diff 审计、OOM 重活串行、exec timeout ≥400s（含 git commit）。_search_cache 46+ 天脏 hunk 留工作树（备份 /tmp/amg_dirty_backup_20260924.diff，将来独立 cycle）
- **agent-context-store**: **3173 tests**（09-17 三连击）
- **agent-task-cli**: **2052 tests** — R82 ✅。坑：exec timeout ≥400s；分支是 main；set 键非 JSON-exportable
- **context-forge**: **1563 tests** / **prompt-mgr**: **480** / **amf**: **754**（09-25 merge 悬空链接修复）
- **09-27 外部五连**: olb **320** / a2at **108** / sotk **619** / pw **229** / brc **401** / dg **78**
- **tools/其他**: ctxpack 104 / ato 57 / afm 32 / project-dashboard 15 / skill-scaffolder 34 / session-archiver 90 / agent-memory-kit 33 / cqc 66 / act 51 / mcpt 41 / ai-dev-tools 93 / skill-doctor 81 / prompt-template-manager 34 / amg-mcp 128 / nano 1162 / mcx 65 / jp 59 / obs 268 / pocket-agent 80 / a2a_minimal 62 / cot 123 / wget-rust 25 / edge-agent-runtime 345 / agent-log 75 bats+32 / openclaw-mcp-server 29 / mission-control 45
- **四项目总计**: **13943**（amg 11272 + sot 619 + atc 2052）
- **全项目总计**: ~**24744** tests（09-28 后连续纯内容日零增量维持）
- **零回滚率**: amg **346天** 🏆（KO 链 08-22:299 → 09-29:344 → 09-30:345 → 10-01:346；C565-C611 47 连 keep）/ acs **207天**（口径=有产出天数）
- **工具链**: **Tavily 新 dev key 全链路生效**（.env + gateway.systemd.env 双更新，gateway 10-02 01:17 重启，KO /proc 实测 ✅）；AnySearch MCP 已从 mcporter 消失（仅剩 tencent-docs），备援=web_fetch 直抓；tencentdb stale plugin warning 待清理

## 近期活动 (10-01 全天——连续第 4 纯内容日，内容线 6/7)
- **05:00 essay《给大脑上户口》（70c0085）**: AI×Neuro #57 素材落成博客——HCA v1.0 300万核×88区 / PsychAD 630万核×1494人×8病×65亚型 / scGPT+Geneformer；冷水段=逻辑回归守门+留捐献者防泄漏；post 200 首查即过
- **06:00 dashboard 3fbcd55 ✅ / 07:00 daily ✅**: daily 亮点 VoiceStudio **破 50k**（50,355 +3,481/日）+ OpenShell 12,536
- **08:00 trending-deep ❌（真实缺口）**: zai 三级模型级联空响应（0 token，~1min 死）——10-01 无深度 trending 报告；待 10-02 观察是否瞬态
- **10:53+11:12 罗嵩两指令**: Tavily key 更新（10:53）→ ai-neuro 停用（11:12，cron 8→7，#55 悬置）
- **19:00 creative ✅（计数 error=完工后截杀伪影，报告 19:04 实际落地）**: 延续日——OpenShell 真加速（v0.1.2 驱动 11.1k→13.6k 全榜最陡）/ MoneyPrinterTurbo 回潮 / orca 稳态疑似终结 / 平台层吸金·应用层降温分化（memory 独立产品窗口收窄，对 amg 战略参考）
- **20:00 deep-exploration《机器人开始长身体了》c395098**: VLA 机器人基础模型——博客 399 篇零覆盖空白区首补；System 0 小脑（10M 参数替 10.9 万行 C++）/数据墙三解法全 LLM 剧本重演/评测危机（LIBERO 饱和）/机器人失眠症（MEM≈hindsight 镜像）；笔记 60aeeae 入 catalyst-research
- **20:31 罗嵩追问 ai-neuro → 20:39 定位 gateway env 真源=systemd env 文件 → 20:32 修正**（10-02 01:17 重启后 KO 验证生效）
- **全天零 dev 增量**（计数持平）+ 零回滚 346；罗嵩对话恢复（3 日沉默终结）

## 本周关键路径
1. ✅ 09-28~10-01 内容线连续四日运行（essay×4 / 深研×4 / dashboard×4 / daily×3 / creative×4；deep 10-01 缺 1=provider 故障；AI×Neuro #56 #57 后停用）
2. ⬜ trending-deep 10-02 08:00 观察（provider 瞬态 or 复发）
3. ⬜ kd 链续跑与否=罗嵩决策（手动续跑 queue 见系统状态节；或重建 cron——prompt 在 09-27 会话）
4. ⬜ README(agent-memory-graph) → npm publish + amg PyPI 人工三步 + npm 命名决策 — **BLOCKED on human action**
5. ⬜ 竞品对读（hindsight 优先；09-29 essay 已完成机制层深拆，余 benchmark 对照）
6. ✅ Tavily 工具链修复（新 dev key 全链路生效，10-02 KO 验证）
7. ⬜ amg next（09-30 深研产出）：nightly consolidation + AgentSleep 四指标评测（consolidation 前后 LongMemEval 对照）——待罗嵩排期或手动 kd 窗口

## 上次检查
- **Knowledge org: 2026-10-02 02:00** — Integrated 10-01 全天（连续第 4 纯内容日内容线 6/7：essay 70c0085《给大脑上户口》HCA/PsychAD + 深研 c395098 VLA《机器人开始长身体了》具身首覆盖 + dashboard/daily/creative；❌ 08:00 trending-deep zai provider 三级级联空响应=真实缺口入档；AI×Neuro cron 停用 8→7 #55 悬置；Tavily 新 key 三段修复闭环 KO /proc 实测生效；罗嵩对话恢复两轮；零回滚 346）。MEMORY：CF 10-01 新节+AT 链+测试快照 10-02；HEARTBEAT 全刷新；10-01 daily 补录 06:00/07:00/08:00 三条
- **Knowledge org: 2026-10-01 11:15** — 罗嵩两条指令落地：① Tavily key 更新（.env 新 dev key 实测可用，gateway 待重启加载）② ai-neuroscience-research cron 停用（58 连错误报不可接受，#55 章鱼欠账一并悬置）。cron 8→7
- **Knowledge org: 2026-10-01 02:00** — Integrated 09-30 全天（连续第 3 纯内容日 8/8 全执行；零回滚 345；Tavily 重置预测——后被证伪）
- **Knowledge org: 2026-09-30 02:00** — Integrated 09-29 全天（连续第 2 纯内容日 8/8 全绿；零回滚 344；git ls-files echo 陷阱入册）
- **Knowledge org: 2026-09-29 02:00** — Integrated 09-28 全天（缩编后首个完整日；AI×Neuro #55 章鱼超时空壳入档）
