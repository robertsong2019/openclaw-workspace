# 2026-09-15 kd-1 — C577 named-holiday entity face (23:00 cron)

- **结果：keep**。banked **315→316 (0.630→0.632)**，C565 起**十三连 keep**；suite 10621→**10638** 绿（+17，0F/0E）；零回滚率 day 324。
- **commits**: 68b7d56（代码+测试，+381 纯新增）/ f85ee5c（tsv 行）。已 push。
- **face**：`What was the airline that I flied with on Valentine's day?` → 固定日期节假日表（无 moveable 假日，Easter/Thanksgiving 诚实 fall-through）→ 问题日之前最近的假日出现（2023/03/02→2023-02-14）→ 假日当天 session 的 user 行扫 realized 标记（`my <A> flight` / `experience with <A>` / `flew with <A>`）→ 恰 1 家航司即答。gate=`holiday_entity`，答案为纯实体串走默认 exact_judge 分支（GT "American Airlines" 精确匹配），**judge 零改动**。
- **判别器**：预订意向行永不携带 realized 标记（"leaning towards the JetBlue option" / "I'll book the return flight on Delta"）；"Delta SkyMiles" 忠诚度产物败于后缀名核心；日期门排除同叙事换日重述（session_35 的 "today" 航班在 02/20 非情人节）。
- **census-first**：500 题中 flew/flied 恰 2 行（目标 + gpt4_f420262c order 题，结构不相交）；holiday 提及恰 1 行（c8090214 的 "Holiday Market" 是专有名词非表内假日）；shipped form census = 恰 1 行，构造性零杀。
- **wire-format 教训（本 cycle 最有价值）**：miniature 首跑 2 红——dated_lines 携带 `[role] ` 前缀，裸文本池会静默跳过 user-wall，且 **assistant-wall 测试以错误理由通过**（unknown-role 跳过 ≠ 正确拒绝 assistant）。修法：helper 统一加前缀，钉住真实契约。与 09-15 上午 test-shape 永久规则同族：写断言前必读被测方法的输入契约。
- **replay**：1202s PASS，pred 变化恰 {gpt4_f420262d}（"I don't know"→"American Airlines"），drift 全 False→True，abs_banked=18 frozen。新权威链 **/tmp/c577/live500_c577.json**。
- **队列裁决**：list-body 多项 GT（a40e080f/ceb54acb/8cf51dda）证据确认需 list renderer（GT 2/4/3 项）——deferred，下轮 3-qid payoff 候选；370a8ff4 维持 C571 phantom 判决；gpt4_f420262c（order-of-airlines）是新发现的 order-gate 邻居，需多实体排序，未动。
- **next**：list renderer（3 qid）/ gpt4_f420262c order face / e3fc4d6e 同族 raw=0 / ollama oracle（human-blocked）。
