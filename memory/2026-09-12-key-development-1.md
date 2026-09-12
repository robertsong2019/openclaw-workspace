# C567 — key-development-1 (2026-09-12 23:00, Saturday)

## 结果：pages-progress faces，banked 301→303（0.602→**0.606**），keep ✅

- **commits**: `04ed73d`（code+test，+354/-1 审计干净）→ `eb4beae`（tsv pin），已 push
- **suite**: 10448→**10463** junit 0F/0E 273s（+15 miniatures）
- **replay**: full-500 live 1164s，pred changes 恰 {2311e44b, 184da446}，drift 全 False→True，abs_banked=18 不变
- **权威链**: `/tmp/c567/live500_c567.json`（取代 c566）

## 两个面（同一 "on page N" 锚族，counting gate 新 form "pages"）

1. **read-so-far latest-wins**：184da446 "How many pages of 'A Short History…' have I read so far?" → s2 "on page 200" → s41 "on page 220"（跨 session 文档序取末位）= **220**
2. **pages-left**：2311e44b "How many pages do I have left to read in 'The Nightingale'?" → s38 "440 pages" − s46 "on page 250" = **190**

## 零 kill 由构造保证

- wired-head census 全 500 = 恰 3 行进 lane：2 个未 banked 目标 + 2311e44b_abs
- abs 兄弟（'Sapiens'）：pace 行 "10-20 pages a week" 被 range+pace 双 guard 拒为 total；无 Sapiens on-page 锚 → 双事实不齐 → honest fall-through，pred 字节不变
- 诱饵全灭于 user-role 墙：assistant "400 pages per book" 估算、$250 行车记录仪
- 37f165cf（440+416=856 月绑定 novel 和）与 8cf51dda（'grant aim page'）实测在 lane 外

## 坑与教训

1. **handler 返回约定**：answer_counting 的 fn map 要求单值返回，首版写成了 (ans, detail) tuple——miniatures 在 replay 前抓住，15 红先全绿
2. **tripwire 期望值算术滑差**：expect-total 手写 302，实为 C566(301)+2=**303**——replay 数据本身完美（changes/drift 恰设计集），用保存的 json 重跑 tripwire PASS。**教训：expect-total 应从 chain 文件程序化推导**（已记 TOOLS.md 显示层家族）
3. memory_graph.py 脏 hunk e04d222d 第 27 天，未混入（逐文件 add + staged 审计）

## 下轮队列

37f165cf（novel page-count sum，月绑定，同 page 族延伸）→ 372c3eed+abs（education range，Master's 须弃答，2 行一族）→ 2ebe6c90/2ebe6c92（session-date 算术，风险更高）→ ollama oracle（human-blocked，解锁 ~169 NJ cascade）
