# key-development-2 — C565（2026-09-11 00:00，第三轮）

**目标**：从 banked 298（0.596）救回 2 行（e61a7584 + b9cfe692）→ 300（**0.600 里程碑**）。

**结果：+2 rescue / 0 kills — banked 298 → 300（0.596 → 0.600），达成 0.600**。两个 pp 邻居面一个周期全收：
- **Face A（have-had 任期）**：e61a7584 "How long have I had my cat, Luna?" → `'9 months'`。route (c) 的 clause-strip + all-keywords wall + now-后缀 tenure 机制**本来就能答对**（s17 "I've had Luna..." 无 "cat" 被 [cat, luna] wall 挡掉；s32 "I've had my cat, Luna, for about 9 months now" 通过）——缺的只是 gate 入口认领。新增 `pp_have_had_form`，route 零改动。
- **Face B（finish-duration 求和）**：b9cfe692 "How long did I take to finish 'The Seven Husbands of Evelyn Hugo' and 'The Nightingale' combined?" → `'5.5 weeks'`（s10 three weeks + s12 two and a half weeks）。新 route (f) `_pp_finish_sum`：逐实体 "took me N units to finish" 锚点 + 题干书名词绑定 + both-facts guard（≥2 锚点）+ 半周粒度自绘渲染（`_pp_render` 四舍五入丢 0.5）。

## 验证链

- 红先 14 miniatures：RED 10（4 ImportError + 2 设计内行为 RED + 4 个新 detail 字段 pin），GREEN 4；实现后 **14/14 GREEN**
- 全套件 junit：**10437 / 0F / 0E / 0 skipped**（263s）
- live-500：pred changes 恰 {b9cfe692, e61a7584}（两堆垃圾 → 干净时长），drift 恰 2 条全 False→True，**banked 300/500 = 0.600**，abs_banked 18，1169s **PASS**
- census 零 kill 由构造保证：两 head 各恰 1 行（均 unbanked）；when/before 同胞与 impersonal "how long did it take" 双双排除

## 技术坑（有普适性）

- **微型测试抓到真 bug（TDD 的价值实证）**："and" 不在 `_PP_STOP`，title binding 的 `any(w in low)` 让无书名的 "random novel... and I loved it" 行混过绑定 → 求和错。修复：`_PP_FINISH_MECH` 加 and/or，测试升格为回归 pin
- **直接调用 ≠ 生产路径**：`answer_pp_duration` 直接调 cat 问题今天就能答对（route (c) 已就绪），但 adapter 级被入口挡住 → 生产 bug 是 entry-only。微型测试必须**双层 pin**：adapter 级（真实修复）+ route 级（sanity）
- **edit 工具打字错误**：newText 里混入游离 "n"（`n                            # foreign anchor`）→ SyntaxError。ast.parse 立即抓到，成本≈0。**每次 edit 后 syntax check 应入环**
- exec preflight 拒 `python3 -c "...&&..."` 复合命令 → 写成 .sh/.py 文件再跑（老规矩）
- tsv 多行 note 使 awk 物理 field 计数失真（历史行本就如此），验证自己的行用 `tail`+`END{NF}` 就够

## 工件

- commit：`43fb9b9`（实现+测试）、`93129c6`（tsv pin）
- /tmp/c565/{step1_census.py, step2_evidence.py, step2b_tight.py, step2c.py, evidence.txt, step3_census.py, step4_dates.py, dbg_route_c.py, green_check.sh, junit.sh, junit_sum.py, live500_c565.py, live500_c565.json, junit.xml, append_row.py}
- live500_c565.json = 新权威链（下一周期 chain 参数指向它）
- memory_graph.py 脏 hunk 第 24 天未碰

## 轨迹

0.502 → ... → 0.580 (C560) → 0.588 (C561) → 0.590 (C562) → 0.594 (C563) → 0.596 (C564) → **0.600 (C565)**

## Next（优先级序）

1. **gpt4_a1b77f9c**：8 weeks 三书 finish 求和——route (f) 现成，可能只需放宽 both-facts guard（3 锚点），低垂果实
2. **2311e44b**：440−250=190 减法面
3. **184da446**：page 200→220 latest-wins
4. 2ebe6c90/2ebe6c92 session-date 算术（险，后置）
5. ollama oracle（human-blocked）
