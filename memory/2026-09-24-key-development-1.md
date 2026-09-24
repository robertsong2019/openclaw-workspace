# key-development-1 — C603 (2026-09-24)

**supersede_total face（qid `a2f3aa27` + `a1eacc2a`）keep。banked 356→358（0.712→0.716），第 39 连 keep。commit `646efa6`。一机制两脸 + 新赛道：recency supersession（会话序仲裁）。**

## 目标与结果
- 队列状态：C602 后 counting 队列无现货候选（faith/delivery/demo-orphan 三 lane 已清）→ census 从 live500_c602 链 144 个 unbanked 里找新 face。23 个 how-many 候选中锁定同机制对：
  - `a2f3aa27` "How many followers do I have on Instagram now?" GT `1300`（gate=counting enum_count，旧 pred **'1250'** = 旧的先声明被勾住）
  - `a1eacc2a` "How many short stories have I written since I started writing regularly?" GT `seven`（gate=answer，旧 pred = 闲聊回声整段）
- 结果：真 adapter probe 双行 pred `'1300'`/`'7'` gate=counting v=CORRECT；**full-500 replay PASS 首试（1152s，9 连首试）**：pred-change set == drift set == `{a1eacc2a, a2f3aa27}` 全 False→True，banked **358/500**。suite 11082→**11102** green（+20 新测试，249s）。

## 机制（与 C600 的关键分野）
- C600 species_total 用**构造语义**（declaration 形状）避开 recency；本轮两行的两次声明**形状完全相同**（"I've got 1250 followers ... now" vs "close to 1300 now"；"written four so far since" vs "complete 7 short stories since I started"）——**只有会话先后能区分**，故首次引入 recency 仲裁赛道：haystack sessions 时序有序（数据集不变量），**latest session 声明 wins**，无需日期解析（`_cnt_sents` 的 si 即时序）。
- `_SPS_INSTA_HEAD_RE` / `_SPS_STORY_HEAD_RE`：全句严格头，census 各恰 1/500；宽松扫描（how many followers / how many short stories / instagram…now）零兄弟行。
- followers 分支：total RX = `<num> followers`（topic 内嵌）或 `close to <num>`（**必须** follower|instagram 同句 topic 墙——房租 decoy "$1,300" 无 topic 永不命中）。
- stories 分支：total RX = `written|wrote|complete(d) <num>` + `since I started` 同句锚。**锚不是 topic 承重**：four 声明句无 short stories 词（topic 在兄弟句 "…short stories per month?"）——C599 turn-grain 教训复用；`write 500 words`（无 written/wrote/completed 词）与 `wrote a short poem`（无数字）天然不命中 → 晚期 decoy session 不毒化仲裁。
- 仲裁规则：跨 session latest wins；**同 session 内 distinct totals → abstain**；identical repeats dedup；user-role only（assistant "congratulations on nearing 1300"/"Completing seven short stories" 永不读）。
- 渲染 captured token as stated：'1300' exact 全中；'7' vs GT 'seven' 靠 judge_semantic word-fold CORRECT + counting_judge numeric-first（**pre-test 探针钉死判分行为**后才定渲染策略）。

## 过程
1. 幂等四查过（project tsv tail=C600 长格式、workspace memory/experiments.tsv tail=C602 短格式、无 C603 工件、无 live kd 进程；git ahead 1 = 473600a demo-orphan 未推送，本轮一并推）。
2. Census 三步（/tmp/c603/census_unbanked.py → dump_two.py → census_heads.py）：144 unbanked → 23 how-many → 同机制对 2 行；严格 head 各恰 1/500；in-row user-role 候选各恰 2 且 latest==GT。
3. 现状探针：enum_count 勾 a2f3aa27 产 '1250'（错）→ 新 head hoist 在 C602 delivery 之后、generic 块之前。
4. 判分探针先行：judge_semantic('7','seven')=CORRECT、counting_judge numeric=True、exact('1300','1300')=True → 渲染 as stated 安全。
5. TDD：`test_supersede_face.py` 20 tests（verbatim fixtures：双声明对、同句冲突 abstain、晚期 decoy 不毒化、房租 decoy、topic-without-total、wrote-a 无数字）→ RED（ImportError）→ 3 hunks（head 正则+handler 86 行 / classifier hoist / dispatch）→ GREEN 20/20 首试。
6. Suite 11102 green（249s）。Replay：cp C602 canonical + sed 默认值 + **diff 审计**（恰 docstring+5 处默认值；sed 顺序坑：chain/out 同名替换链——先 sed 后 edit 修正，audit 拦截）。

## 状态与队列
- banked **358/500**（0.716），39 连 keep，零回滚 339 天；abs 30（18 abs + 12 held）冻结；suite 11102；链 `/tmp/c603/live500_c603.json` 新权威。
- kd queue 下一候选（census 初筛，未验证）：`69fee5aa` pre-1920 coins（pred 回声 37 vs GT 38，需集合计数+年代过滤）；`gpt4_2f8be40d` weddings this-year（pred 4 vs GT 3，需年窗+枚举总声明）；`21d02d0d` fun-runs missed-in-March（C599 明示 no-steal lane，需 miss+work 归因语义）。`a1eacc2a` 的 supersession 机制或可复用检查 `gpt4_2f8be40d`（两次声明形状？未验证）。
- 473600a（demo-orphan）+ 646efa6（C603）待推送。

## 产物
- commit `646efa6`（amg_bench_quality.py +101/-1、test_supersede_face.py +289）
- `/tmp/c603/`：census_unbanked.py、dump_two.py、census_heads.py、probe_current.py、probe_judge.py、probe_adapter.py、run_face_tests.py、run_suite.py、replay.py、live500_c603.json（新权威链）
- workspace memory/experiments.tsv C603 行（短格式，沿 C601/C602 惯例）
