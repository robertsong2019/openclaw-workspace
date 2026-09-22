# key-development-2 — C598 (2026-09-23, autoresearch 循环 B)

## 结果：KEEP ✅（banked 349 → 351，34th consecutive keep，零回滚）

## 本轮 Lane
**自述累计活动总数（self-stated cumulative totals）**——一机制两面：

| qid | 问题 | GT | 证据面 | 旧 pred（诱饵回声） |
|-----|------|----|--------|--------------------|
| 26bdc477 | How many trips have I taken my Canon EOS 80D camera on? | `five` | "I've had my Canon EOS 80D with me on **five trips now**, and it's been a beast!" | 含 "three trips to Yellowstone..." 的回声 |
| 618f13b2 | How many times have I worn my new black Converse ... sneakers? | `six` | "so that's **six times now** that I've worn them." | 含 "four times already" 的回声 |

## 机制要点
- 答案 = 用户**自己说出的运行总数**（"N trips/times now" 构式），不是 key-set 计数（C595/596/597 模式的对照组）
- **`now` 锚**区分总数 vs 裸枚举："three trips to X, Y, Z"（无 now）= 提及，永不产 3 —— 本轮核心诱饵钉子
- 同句话题墙（C591+ 纪律）：trips 面 → camera 术语；worn 面 → Converse/sneaker 术语
- 冲突总量弃权（None）：603deb26 Negroni 5-v-10 陷阱由 head 的 taken|worn 动词 + 冲突规则双重挡在门外
- 渲染照抄捕获 token（'five'/'six'）：counting_judge 数值优先 + judge_semantic 词形 fold 双路皆 bank（pre-replay 双 judge probe 两行双 CORRECT）

## 验证链
- census：strict form 全 500 恰 2 行，broader 扫描确认不偷 bake(C597)/rollercoaster/Negroni/metup/Chiefs/bake_abs
- TDD 红→绿：15 测试（form claim / no-steal / 墙 / 冲突重复 / digit 透传 / judge bank 路径）
- suite **11001 green**（263s）
- live500 replay **PASS**（1158s）：pred 变化恰 {26bdc477, 618f13b2}、drift 恰 2 全 False→True、banked 351、abs_banked 18 frozen
- commit `7d60bbb`（+332/-1：amg_bench_quality.py 3 hunks + test_cum_total_face.py；staged audit 零外来 hunk）；tsv C598 行已加

## 产物
- `/tmp/c598/live500_c598.json`（新权威链）
- `/tmp/c598/{probe2rows,live500_c598,run_suite,append_tsv}.py`

## 下轮候选（按价值排序）
1. **603deb26 Negroni**（"have I tried making"）——haystack 有 5-v-10 冲突总量，GT 应为 10；需要**时间序仲裁**（后值胜）机制，是新机制面（本轮弃权规则刻意未碰）
2. a9f6b44c（bikes serviced March，GT 2）/ 00ca467f（doctor's appointments March，GT 2）——月份窗口计数
3. 5a7937c8（faith days December，'3 days.'）/ affe2881（bird species，32）/ d682f1a2（food delivery，3）
4. ~169 NJ cascade（ollama oracle，human-blocked）仍是最大鱼
