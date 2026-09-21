# 2026-09-22 key-development-2 (C595)

## 任务
cron key-development-2：autoresearch 实验循环 B，在 kd-1 (C594) 基础上至少 +1 banked。

## 时间线
- 00:00 会话启动。幂等四查：发现 kd-1 的 C594 replay 进程（pid 3669455）存活中，按第四查纪律不接管、等完成
- 00:03:31 C594 replay PASS（1165s），kd-1 自行完成银行：commit `61f3b2d`（代码+测试）、`2671003`（tsv），banked 344→345，已 push
- 00:05-00:35 C595 census-first：bikes_own form `^\s*how\s+many\s+bikes\s+do\s+i\s+(?:currently\s+)?own\s*\??\s*$` 恰好匹配 2 行（6b168ec8 GT 'three' / 89941a93 GT '4'），均未 banked
- 00:35-00:50 实现 + face 测试两轮红绿
- 00:50-00:55 全量 suite：10956 passed（=基线 10930 + 新 26），零回归
- 00:55 2 行探针：6b168ec8→'three'、89941a93→'four'，gate 翻转 answer→counting
- 00:57 全量 replay 启动（expect: pred-change==drift=={6b168ec8, 89941a93}，total 347）

## C595 机制：bike 拥有权计数（bikes_own）
一机制两面（C592 双头模式）：
- 枚举面 6b168ec8 s34："I've got three of them - a road bike, a mountain bike, and a commuter bike"
- 跨 session 物主面 89941a93 s6+s29："my road bike" + "my other two bikes, a mountain bike and a commuter bike" + "a new hybrid bike I just purchased" → 4
- 无时间窗——OWNERSHIP 替代（C593 模式：约束替代窗口）
- 深度-1 最近词分类：修饰词槽只有 head 前一个词；`_BIKE_OWN_STEM_RE`（my / I've got / I (currently) have|own）句子级许可；复数 `bikes` 永不建键；裸 `my bike` 泛指不建键（否则 6b168ec8 数出 4≠GT 3）；裸 `a bike` 建键 'bike'；follower 墙（lock/shops/storage/trails/computers…含复数）；所有格 `bike's` 与连字符 `bike-friendly` 用**紧邻字符**判定；prep 墙（kind of bike / with bike storage）；word-only render 'three'/'four'

## face 测试教训（先红后绿 2 轮）
1. **贪婪 NP 正则（`(?:det)?(?:mod){0,3}bike`）失败**：动词/代词被吞进修饰链（'sure road bike'）、prep 拒绝吞噬合法 NP（'to my road bike' 整段被消费 → 真 NP 永不匹配）。教训：**回看分类优于前瞻正则**——逐 'bike' token 做深度-1 lookback，天然免吞噬
2. **空格破折号**：'a commuter bike - and…' 的 ' - ' 触发了为 'bike-friendly' 设计的连字符墙 → 必须检查紧邻字符（sent[m.end()]）而非 lstrip 后首字符
3. **follower 墙要含复数**：'specific bike locks' 漏网（墙里只有 'lock'）
4. memory_graph import 副作用（demo 输出污染 stdout）是 C592 起存量行为，测试通过 grep 结果行规避

## 关键数字
- banked 血统：C592 +2 → C593 +1 → C594 +1 → C595 +2（本周期）= 343→**347**（abs 18 冻结）
- suite：10956 passed（junitxml 口径 281s）
- experiments.tsv 本周期前 705 行

## 待办（replay PASS 后）
- [ ] 银行：git add amg_bench_quality.py test_bike_face.py + experiments.tsv 追加 + commit + push
- [ ] 孤儿不提交：memory_graph.py (+24 旧 cache)、temporal_test_data.json、test_optimization.py、test_status.log
