# 2026-09-25 — C606 key-development-1（23:00 cron）weddings_attended face

## 结果：KEEP（第 42 连 keep）

- **qid**: `gpt4_2f8be40d`（How many weddings have I attended in this year? GT 'three'）→ **361/500 = 0.722**（C605 360）
- **主 commit**: `6d899a5`（amg C606, 4 files +295/−3）；suite **11140→11154**（+14 test_weddings_attended_face.py；11154 passed rc=0, 276s）
- **replay**: PASS 一次过（1182s），pred changes == {gpt4_2f8be40d: '4'→'3'}，drift 1 False→True，0 lateral flips，abs 18 frozen
- **experiments.tsv**: workspace 短格式行已 append（C605 先例；注意 C605 append_tsv.py 是逐 cycle 脚本，C606 版在 /tmp/c606/）

## 机制

- 严格头 `^\s*how\s+many\s+weddings\s+have\s+i\s+attended\s+in\s+this\s+year\s*\??\s*$`（census 恰好 1/500）
- 出席标记墙：句内须有 `got back from|been to ... weddings?`（user-only via _map_sents）
- 事件 key = role-noun 所有格 `((college )?roommate|cousin|friend|sister|brother|colleague|classmate|neighbo[u]r)['’]s wedding`，同 key 去重（cousin 葡萄园婚礼被重提 4x、friend 婚礼 3x）；无 role key 的出席句回退整句 normalized 作 key
- 干扰墙（正是 GT=3 的语义）：own wedding（planning/venue ideas 无出席动词）+ sister's wedding（maid of honor 赞美但无出席动词）天然不计数
- 'Mike' 从未出现在 haystack——GT 枚举是 name-authoritative，数值判分（counting_judge 数字优先，_cnt_numval('three')=3.0）只看 count=3

## 过程要点

1. **判分探针先行**（HEARTBEAT 纪律）：C605 时 enum_count 读 '4'（把 sister 婚礼扫进 tally）；确认 counting_judge 数值路径后 pred '3' 即 bank，无整句枚举渲染风险
2. **smoke 绿**：真实 row → ('3', {'form': 'weddings_attended'})；own-only/sister-only → None；三事件 fixture → 3
3. **suite 首跑 2F**：`test_enum_count.py::test_form_gate_claims_plain_how_many` + `test_museum_count.py::test_form_gate_rivals_keep_their_claims`——两个 stale claim pins 断言该问题归 enum_count。属 claim-transfer 标准动作：改 pin 为 weddings_attended + C606 注记。注意短变体 "attended this year?"（无 in）/"attended?" 仍归 enum_count（pin 已隐式覆盖，我的头不匹配它们）
4. **拓扑实测**：amg 本轮无独立 .git（toplevel=workspace monorepo），git add 相对路径；staged diff 逐块审计（09-08 纪律），排除 memory_graph.py +24 脏 hunk 与 untracked 杂物（temporal_test_data.json/test_optimization.py/test_status.log 非本 cycle 产物，未动）
5. **replay harness**: cp C605 canonical + 字节级替换（count==1 assert）+ diff 审计，仅 docstring/chain/out/expect 三组默认值；chain=/tmp/c605/live500_c605.json → out=/tmp/c606/live500_c606.json（新权威链）

## 下轮 lane 备选（unbanked，census 待验证）

- `5a7937c8` faith days December（GT '3 days.'，语义类目 + 月份窗口 + 整句 GT，最重）
- `gpt4_4929293b` bridesmaid 行（'how many weddings' loose 扫描零命中他行——本 cycle census 已证）
- memory_graph.py demo-orphan 修复（C600 发现，独立 cycle，注意 _search_cache 脏 hunk 手术）

## 工件

/tmp/c606/{smoke.py, run_face_tests.py, build_replay.py, replay.py, run_suite.py, append_tsv.py, patch_tsv.py, live500_c606.json}
