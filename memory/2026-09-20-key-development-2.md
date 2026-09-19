# 2026-09-20 — key-development-2（C590，00:00 cron）

## 结果：**KEEP** — banked 337→339 = **0.678**（26 连 keep，0 回退）

C590 = coordinated-sum 双 head（e3038f8c rare-items + 60036106 reach），单机制双名词锚定面。建立在 C589（4b632c9/feb4783，suite 10828，banked 337）之上。

## 闭环

1. **幂等三查** ✓：tsv tail=C589、无当日 kd memory、无并发会话
2. **Census-first**：两个 head 正则各恰 **1/500**；无 _abs 兄弟、无 abstention 行；form 现状均 = number_total（e3038f8c pred '69' = 57+12 部分和；60036106 pred '2050' = clicks 尾巴污染）
3. **全 haystack 证据收割扫**（45/44 sessions）：定位全部 verbatim 数值行 + 两族 assistant 回声诱饵（user 墙杀）+ a3d8e134_2 干扰 session（"rare ones like that 1967 Sgt." 无品类-数字对，天然无害）
4. **TDD red-first**：19 miniatures，verbatim repr 注入 fixture；RED=ImportError → GREEN
5. **Suite**：10828→**10847**（pytest junitxml，0F/0E，精确 +19）
6. **Replay PASS**：1146s，pred changes 恰 `{e3038f8c: '69'→'99', 60036106: '2050'→'12,000'}`，drift 恰 2 全 False→True，abs_banked=18 冻结
7. **tsv + commits + push**：`17f2883`（代码 +374/-1）+ `9d6d840`（tsv 行）；`feb4783..9d6d840` 已推 GitHub

## 机制要点（新 form `coord_sum`，gate 仍 counting）

- **rare-items head**：`<num> rare <cat>` 直采 + 同句配对（"rare books … collection of 5 books"）→ 12+57+25+5=99；按品类 set 去重（57×2 一致合并）
- **reach head**：`reached … <num> people` + 动词锚定 `promoted … to <num> followers` → '12,000'（逗号渲染）；**名词锚定结构性排除 clicks 陷阱**
- **协调纪律**：单侧缺失/同锚冲突值/单品类 → None fall-through（number_total 原车道零侵犯）；user 角色墙

## 中途 3 红 = 全测试构造错误（face 无罪，C588/C589 教训第 3 次应验）

- `answer_counting` 契约是 **(ans, detail) tuple** 非 dict
- wall 微型 fixture 违反 ≥2 品类协调前提——face 返回 None 是**正确的** fall-through；修测试（加 books 侧，期望 17 而非 12）

## 环境 note

- exec preflight 拒 `cd X && python3 file.py` 链式调用 → 用绝对路径直跑
- **suite 10828/10847 是 pytest junitxml 计数**（unittest discover 只有 1361——parametrize 展开差异）；suite 命令必须用 `python3 -m pytest -q --junitxml=…`，系统 python3（venv 无 pytest）
- tsv_append.py 打印行 `back.count(b'\\n')` 是转义 bug（计数无意义），append 本身有字节级 assert 保证——下轮修

## 下轮队列（C591 候选）

- **enum-count 双题**：60159905（GT 'three' 词形：Sarah's Italian feast last week / Mike's BBQ two weeks ago / Alex's place yesterday；"hosting soon" 不算；现 pred '1'）、a3838d2b（GT '4'：Run for the Cure Oct 15 之前的 4 场；**November Bike-a-Thon 时序陷阱**；现 pred '1'）
- list renderer 三题：a40e080f / ceb54acb / 8cf51dda
- ollama oracle（human-blocked，解锁 ~169 NJ cascade）

## 工件

- `/tmp/c590/live500_c590.json`（**新权威链**）、`live500_c590.py`、`tsv_append.py`
- `/tmp/c590_junit.xml`（suite 10847 0F/0E）
- 轨迹：0.502→…→0.670(C587)→0.672(C588)→0.674(C589)→**0.678(C590)**
