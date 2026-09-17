# 2026-09-18 02:00 knowledge-organization-morning

## 幂等三查
- MEMORY.md / HEARTBEAT.md 近 5 分钟无写入；sessions 无并发 KO 会话；C585（kd-3 01:50 收尾）为最新基线 → 增量成立
- HEARTBEAT.md 有一处 C583 会话留下的未提交改动（最高优先级 bullet 半更新，方向正确），本轮回统一并提交

## 过去 24h 增量整合（09-17 02:00 → 09-18 02:00）
- **amg kd 链 C582→C585 四连 keep**：banked 0.652→**0.664**（326→332/500），suite 10705→**10765**，C565 起 **21 连**，day 332 🏆
  - C582 where-precision（R2 do-form 降级 + R3 assistant 让位；**R1 被 replay 正确 FAIL**＝retrieval-miss 非降级问题；session_N≠answer_session_ids 索引陷阱）
  - C583 counting ordinal-quantity（序数后缀；bare-quantity 毒理图谱：子句数字通常绑定另一名词，2 banked kill 硬门）
  - C584 chord + demand-noun（**结构性判别>分数调整**——本周期最重要架构教训，demand 名词=硬过滤非分数）
  - C585 year-begin（user 证据面新领域：NP 全实词锚代替角色墙，C584 教训直接迁移）
  - speaker_recall stragglers 8 qids 分类结案（2 banked/2 deferred/4 judge-unbankable）
- **工具线**：sotk 591→607（拓扑漂移 #4：pocket-agent/openclaw-mcp-server/a2a-trust-prototype/agent-observability 归 monorepo）/ acs 三连击 3135→3173（content_complexity 真 bug）/ langgraph-bridge 302→307（silent-hang 第 5 例）
- **内容线**：doc efa3939（TUTORIAL §5.31-33，原则第 12 条）/ essay《评测失败的三层归因》5fb327b / CodeAct 深研博客 7b28e31 / trending security-audit-skill / dashboard 18ac2ce

## MEMORY.md 更新
- Current Focus 09-18 新节（C582-C585 全量 + 工具/内容线）；Active Theme 328→332 天 + 新四连摘要前置
- 测试表全刷：amg 10765、sotk 607、四项目 13251、全项目 ~24030（较 09-16 +213）；bridge 307 / acs 3173 / prompt-mgr 447 / mc 33 / agent-log 75 / a2a-min 48 过时计数清掉
- 213KB→214KB（+2.6KB 纯增量，无归档——Current Focus 09-14/09-15 旧节标为下轮归档候选）

## HEARTBEAT.md 更新
- 标题日期、系统状态（10765 @C585 / 权威链 /tmp/c585）、近期活动全换 09-17~09-18、kd 队列重排（e8a79c70 / coordinated-sum / 830ce83f / 07741c45 / 9ea5eabc / 3249768e）、上次检查 +09-18 -09-15、已知问题 4 处（cron 连续四日正常 / npm 13251 / /tmp c585 基线 / 脏 hunk day 38 / MEMORY size）

## 过程教训（本 KO 自身）
- edit 工具长段精确匹配又两败：①oldText 漏 `lab/` 前缀 ②给行中段文本加了行首 `- `——**HEARTBEAT/MEMORY 的节级替换一律走落盘脚本（re.S 锚定 + assert 唯一），edit 只用于短锚点**
- exec preflight 拒 `cd x && python3 file`（与昨日 06:00 日志同款新拦截）→ workdir 参数直跑，一次过
