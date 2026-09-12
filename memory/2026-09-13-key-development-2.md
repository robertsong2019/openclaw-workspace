# C568 — key-development-2 (2026-09-13 00:00, Sunday)

## 结果：page-count sum lane，banked 303→304（0.606→**0.608**），keep ✅

- **commits**: `d7602f9`（code+test，+308/-4 审计干净）→ `6c872ea`（tsv pin），已 push
- **suite**: 10463→**10476** junit 0F/0E 252s（+13 miniatures）
- **replay**: full-500 live 1161s，pred changes 恰 {37f165cf}（垃圾引文→'856'），drift 1 条全 False→True，abs_banked=18 不变
- **权威链**: `/tmp/c568/live500_c568.json`（取代 c567）

## 这个面（37f165cf，GT 856 = 440 + 416）

- 问题："What was the page count of the two novels I finished in January and March?"
- **月份不可恢复**：全 haystack 零 January 提及；March 全是诱饵（Chicago 行程 / Marchmont / 难民听证 / Alamo 1836）；session 日期全在 May 2023 → 设计成 **month-blind** 的 just-finished 页数求和，只承诺 haystack 能支撑的语义
- 锚点：s9 "just finished … Nightingale … 440 pages"（×2，distinct 去重）+ s33 "just finished a 416-page novel"
- 诱饵：The Power（341 pages，December）——其页数不是句中 just-finished 标记后的第一个页数短语（416 在同一句先行），被"句内首个"规则天然排除；assistant 推荐行死在 user-role 墙
- guard：基数由题面 count word（"two"→_CNT_WORD2NUM）钉死，distinct 数 ≠ 2 一律 fall-through

## 坑与教训

1. **正则回溯陷阱（本周期最佳教训）**：前缀 `[\w'"]+`（\w 吃数字）+ 懒惰通配符 + 回溯，把 "416-page" 的捕获啃成 **'6'**（引擎把 416 回溯成 41，让捕获组偷走尾数字）。mega-alternation 锚点正则废弃，改为朴素位置扫描（标记后首个页数短语）；陷阱固化为永久回归 pin（单事实值必须恰为 416）
2. **sh 脚本 printf 续行断裂**：append_row.sh 的多行 `\` 续行有一处断裂，printf 输出上了 stdout、重定向失效、文件没变——且 stdout 有输出使失败不显眼。**教训：多字段 tsv append 用 Python（csv/tab-join + 断言 + 复读验证），不用 sh printf**（C565 本就如此，这次绕远路了）
3. **importlib 双模块加载**：HEAD 版与工作版 counting_form 做 500 行零漂移对比时，spec_from_file_location 必须 `sys.modules[spec.name] = mod`，否则 dataclass 内省崩（`sys.modules.get(cls.__module__)` 为 None）
4. expect-total **从 chain 文件程序化推导**已烧进 harness 默认行为（chain banked + unbanked drift 行），C567 的手算滑差不再可能复发
5. zero-drift 证明升级：不止 wired-head census，直接 HEAD-vs-工作双模块逐行 diff counting_form（500 行恰 1 处变化）

## 下轮队列

372c3eed+abs（education range，Master's 须弃答，2 行一族）→ 2ebe6c90/2ebe6c92（session-date 算术，风险更高）→ ollama oracle（human-blocked，解锁 ~169 NJ cascade）
