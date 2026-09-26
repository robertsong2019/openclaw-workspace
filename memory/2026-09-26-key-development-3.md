# key-development-3 — C608 (2026-09-26)

**art_events face（qid `2ce6a0f2`）keep。banked 362→363（0.724→0.726），第 44 连 keep。commit `2c6fb80`。**

## 目标与结果
- kd-2（C607）交接队列唯一候选 `2ce6a0f2` art events past month——直取，未再挖新（census 三步全绿后无换道理由）。
- 结果：真 adapter probe pred='4' CORRECT（GT 4 纯数字，counting_judge 数值路径；8 邻居含 6 prior face + 3 cousin 全不动）；**full-500 replay PASS 首试**（1193s，第 13 次连续首试）：pred-change set == drift set == `{2ce6a0f2}`（旧 pred 是 Heifer International 无关回声 → '4'），banked **363/500**。suite 11177→**11202** green（+25 新测试，304s）。

## 机制（distinct-date 计数，C607 workshop_days 的姊妹形状）
- 证据链（4 句全 user、全句自含）：s8 'volunteered at the Children's Museum for their "Art Afternoon" event on **February 17th**' + s24 'attended a lecture at the Art Gallery on 'The Evolution of Street Art' on **March 3rd**' + s38 '"Women in Art" exhibition which I **attended** on **February 10th**' + s40 '**went on** a guided tour at the History Museum on **February 24th**' → date keys {(2,10),(2,17),(2,24),(3,3)} = **4** ✓GT。
- 三重墙：topic（\bart\b|exhibition|gallery|museum|lecture|tour——\bart\b 天然不咬 artists/Pinterest）+ 过去参与动词（attended|volunteered|went on——seeing/visiting/participated/look-forward-to-attending 全暗）+ month-first 月日锚（4 句证据全此形状；day-first 不需要，Simplicity First 砍掉）。user-role 墙由 _map_sents 内置。
- 去重：set-dedup by (month,day)，别名归一（March/Mar→3，sept→9）；Mar 3 重提句 'after seeing some of the work at the lecture' 无参与动词天然暗（双保险）。
- 窗口判定省略的依据：全 47 session 日期都是 2023/03/08，'past month' 相对窗无出窗风险——不加窗逻辑（census 零出窗命中验证过）。
- 关键暗句（全 verbatim pin 进测试）：'attended a charity yoga event'（有动词无 topic）；pottery 'guided tour at the History Museum'（有 topic 无日期无动词）；'looking for ... local art events'（有 topic 无动词无日期）；'participated in a similar chat'；'visiting some local art studios'；'looking forward to attending ... graduation party'（将来时）；'Sufi artists'（\bart\b 词界）。
- Census 三步：strict head 恰 1/500；行内 KEYED 恰 4 句；loose 堂兄弟 gpt4_59149c78（where-was-it-held）不同头无偷道风险。

## 过程
1. 幂等四查过（tsv tail=C607、amg head=25b4fd0、无 C608 工件、无 live kd 进程、权威链 /tmp/c607/live500_c607.json 在）。
2. 证据 dump 两轮（先宽后窄：art|exhibit|museum|gallery|lecture 全 turns 太噪 → 聚焦 user-only + 日期/动词）→ census 三步一步到位（census.py）。
3. TDD：`test_art_events_face.py` 25 tests（verbatim fixtures + 结构墙 pin：re-mention 暗/别名去重/单句双日期加法/动词无 topic 暗等）→ RED（ImportError）→ 3 hunks（regex+handler+mon 表 94 行 / classifier claim / dispatch）→ **GREEN 25/25 首试**。
4. Suite 11202 green（304s，=基线 11177+恰 25，第 12 连首试）。
5. 真 adapter probe：2ce6a0f2 pred='4' form=art_events；6 prior face（funrun '2'/coins '38'/weddings '3'/workshop '3'/faith '3'）+ 3 cousin pred 全不动。
6. Replay：build_replay.py 字节级替换（count==1 assert ×6）+ diff 审计（恰 6 hunk 组）→ **PASS 首试**（1193s）。⚠️ build 脚本初版 --out anchor 写错（C607 的 --out 已指 c607，不能复用 c606 串）——grep 实查后修正 anchor 重跑；教训：build 前先 grep 上游 replay 的实际 default 串，勿照抄上一轮 diff。
7. staged diff 审计过（恰 2 文件 +94/-1 与 +315，无外来 hunk；memory_graph.py 脏 hunk 未卷入）；amg monorepo 相对路径 add。

## 状态与队列
- banked **363/500**（0.726），44 连 keep，零回退；abs 30（18 abs + 12 held）冻结；suite 11202；链 `/tmp/c608/live500_c608.json` 新权威。
- unbanked 剩 137。C607 交接的 counting 族强候选已消化完毕（0a995998 衣服/2788b940 健身课/6d550036+60472f9c 项目/bf659f65 专辑/gpt4_31ff4165 设备——C607 判全偏重，仍待验）。从 live500_c608 链看下一梯队：`gpt4_e05b82a6` rollercoasters July–October '10 times'（跨 4 月计数+单位 GT）；`370a8ff4` temporal_arith 15 weeks（flu 康复→第 10 次慢跑，跨 gate 需 arith 管线）；`0a995998` 衣服 3 件（pick up or return 双动作枚举）；`60472f9c`/`6d550036` 项目对（证据分散风险）。pref-gate 12 行 NEEDS_JUDGE 是另一族（行为未知，风险高）。
- **流程教训（给下轮）**：(1) build_replay 的 anchor 串必须先 grep 上游 replay.py 实际值（C607 已把 --out 指向自己的 c607 链，逐轮滑动）；(2) kd-2 交接候选必须先查链上 banked 状态（C607 白占教训仍有效，本轮直取队列候选前先在 unbanked.txt 确认）。
- 遗留：memory_graph.py `_search_cache` 脏 hunk + temporal_test_data.json/test_optimization.py/test_status.log 三个 untracked 杂物仍未清理（C604 起挂账，四轮未动）。

## 工件
- commit `2c6fb80`（amg_bench_quality.py +94/-1、test_art_events_face.py +315）
- `/tmp/c608/`：list_unbanked.py、unbanked.txt、dump_art.py、census_art.py、census.py、run_face_tests.py、run_suite.py、probe_adapter.py、build_replay.py、replay.py、append_tsv.py、live500_c608.json（新权威链）
- workspace memory/experiments.tsv C608 行（短格式）
