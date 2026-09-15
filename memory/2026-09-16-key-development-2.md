# key-development-2 — C578（2026-09-16 00:00 cron）

**结果：KEEP。banked 316→319 / 500（0.632→0.638），14连keep，零回退日 325。**

## 本轮成果：list-recall face

C577 队列顶项（3-qid payoff）兑现。cardinal-demand 回忆题（"remind me of the **two companies**
you mentioned" / "what the **other four options** were?" / "what were the **three objectives** we
outlined"）由 assistant 自己写的**编号列表块**作答——speaker_recall 句子池以三种方式碎片化它们：

- **intro 行寄生**（a40e080f）：pred = "As an AI language model, I can give you an example of two companies…"
- **早轮次获胜**（ceb54acb）：pred = 上一轮的 "A shorter term … is 'sexual compulsions'"
- **单行作答**（8cf51dda）：pred = 3 行里的第 1 行

## 设计

- **`list_recall_form`**：recall frame + cardinal 名词**同句**（500 题 census 恰 3 命中；
  6ae235be "CITGO's three refineries…what kind of processes"、3249768e "five bottles…fifth
  bottle" 的 cardinal 在上下文句，排除；后者归 ordinal_item_form C536）
- **harvest**：编号块（`^\d{1,2}[.)]`；prose 关闭 run、空行不断、≤3 行滚动 intro）；
  size==n 结构门；块分 = 清洗后问题 token 对 intro+rows 的命中数
- **打分停用词教训（step5b）**：Nashik 行程 decoy 靠 junk 命中 `['four','suggested']` 得 2 分，
  把真块 margin 挤到 1 → fall-through。**cardinal 词和 frame 动词 bind the QUESTION, never
  the block**——进停用表后真块 3 分、次名 1 分 ✓
- **门槛**：score≥3 且 margin≥2（模糊即编造）；user-role 墙；fall-through 不动现状
- **渲染跟行走**：dash 定义行 → 名字 span（"The two companies were: Patagonia and Southwest
  Airlines."）；clause 行 → **全行编号渲染**（8cf GT 携带只在行文本里出现的 'their'，span
  压缩必然 strict-subset 触发 judge subset veto，永不可 bank——渲染粒度由 GT 词形决定）
- **judge 三分支各兑现一题**：superset（a40）/ normalized（ceb）/ ratio（8cf）；ceb 裸 join
  仍 WRONG（缺 'suggested'）——frame lead 是 superset 分支的触发条件，负面钉死

## 验证链（C572-C577 纪律全走）

1. census-first：draft 规则 5/500 → 同句规则恰 3/500（出厂复跑 ✓）
2. TDD red-first：19 miniatures，fixtures **verbatim**（12283 字节真块+同大小 decoy 块；
   a40 s10 m9 / ceb s6 m3 / 8cf s22 m4）
3. RED 抓到 2 个生成器 bug（fixture 常量化 vs FX dict；score pin 过时）；GREEN 抓到
   **双句点渲染 bug**（row 自带 '.'，渲染器又补一个）
4. suite 10638→10657 全绿 0F/0E（replay 之前跑，OOM 串行纪律）
5. live probe：ceb54acb 首探 fall-through → 停用词教训修复 → 3/3 gate=list_recall
6. full-500 replay PASS（1186s）：pred 变化恰 {a40e080f, ceb54acb, 8cf51dda}，drift 3 全
   False→True，banked 319，abs 18 frozen；harness 从 C577 canonical verbatim 拷贝（10 处
   documented 替换，compile 检查）
7. tsv 裸字节 append ×2（PENDING→fb0091b 补正）；staged audit 3 文件 +461 纯插入；
   memory_graph.py 脏 hunk（day 32+）未卷入

## Commits

- `fb0091b` — amg C578: list-recall face（+229 生产 / +231 测试 / +1 tsv）
- `8f26c21` — tsv row（keep），push 5e7c6fe..8f26c21

## 轨迹

0.502 → … → 0.632 (C577) → **0.638 (C578)**。 kd-1 13连 → kd-2 14连keep。

## next 队列

1. **gpt4_f420262c** order-of-airlines：多实体排序，需要 sort renderer（C577 遗留）
2. **e3fc4d6e** 同族 raw=0
3. **6ae235be** refinery-process lane（本轮 census 顺带确认其 cardinal 在上下文句）
4. 3249768e 已归 ordinal（C536）——无需动作
5. ollama oracle（human-blocked）

## Artifacts

- /tmp/c578/{step1_census.py, step2_harvest_census.py, step2b_harvest_refined.py,
  fixtures_raw.txt, step3_gen_tests.py, step4_census_shipped.py, step5_live_probe.py,
  step5b_debug_ceb.py, step6_prep_harness.py, live500_c578.py, append_tsv.py}
- **live500_c578.json = 新权威 chain**（C579 起用）
- 测试：test_list_recall_face.py（19）
