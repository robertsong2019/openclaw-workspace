# Key Development Task 3 (Loop C) - 2026-09-27 01:00

## C611: fitness_week face — banked 365→366/500 (0.732), 47 连 keep，15 连 replay 首试 PASS

**commit `c596d1f`**（amg monorepo：amg_bench_quality.py +82/-1、test_fitness_week_face.py +331、test_inventory_count.py +9/-2 pin 更新）

### 目标与机制
- C610 交接候选里选了 **2788b940** "How many fitness classes do I attend in a typical week?"（GT int 5，v=WRONG，冻结 pred 是 meal-prep 回声）。弃选理由：doctors/kitchen GT 是长句（判分风险+噪声大）；clothing 双动作歧义（C607 已判偏重）；albums 只有 2 个可辨识购买但 GT=3。
- 机制：**(class, day) set-dedup 周课次计数**——strict head + 双墙：
  - 课名墙 `zumba|body ?pump|hip hop abs|yoga`（\b 保证 yogurt 不咬 yoga）
  - 星期墙 `monday..sunday s?`（裸 'days'/'weekdays' 永不匹配）
- 证据：Zumba{Tue,Thu}=2 + BodyPump{Mon}=1 + yoga{Sun}=1 + HipHopAbs{Sat}=1 → **5** ✓
- 暗区全验证：s1:10 四课名罗列无天、meal-prep on Sundays、sculpting classes、"on days when I have BodyPump classes"、yoga routines 无天、assistant 全程表回声。
- Census 三步：strict head 恰 1/500；keyed 10 句（比预期多 2 句 BodyPump-Monday 重提，dedup 安全）；loose 表亲 a08a253f 实为 **freq_days 既有领地（已 banked pred '4'）**——census 阶段先误记为"下轮候选"，查链后修正。

### 本轮流程事故（2 个，均当场修复）
1. **后台 exec log 捕获失效**：suite 跑了 3 次才拿到 log——前两次后台会话 0 字节（一次 exit 1 无输出、一次 exit 0 空 log 幽灵）。修复：Tee 类把 pytest 输出直接落盘 /tmp/c611/suite.log，不再依赖 exec 捕获。**Tee 必须 has isatty()=False**，否则 pytest TerminalReporter INTERNALERROR（第一次 Tee 版就死在这）。
2. **stale whitelist pin**：`test_inventory_count.py::test_form_gate_whitelist_only` 钉死了该问题应返回 None——首跑全量 suite 1 红（11271 passed）。这是 C511 时代的历史 pin，本轮有意变更 → 更新 pin 为 `fitness_week` + freq_days 表亲断言。face-only 绿对跨文件 pin 盲（与 C610 的 _SPT_ 教训同族：**全量 suite 是唯一真相**）。

### 验证链
| 关卡 | 结果 |
|------|------|
| RED | ImportError（预期） |
| face GREEN | 26/26 首试 |
| 全量 suite | 首跑 1 红（stale pin）→ 修 pin → **11272 全绿**（244.6s） |
| 真 adapter probe | 2788b940 → form=fitness_week pred='5'，GT int 5 三判全 CORRECT；9 先辈 face + a08a253f(freq_days '4') + a4996e51(None) 全不动 |
| full-500 replay | **PASS 首试**（1148s）：pred-change==drift=={2788b940}（meal-prep 回声→'5'），banked **366/500** |

### 链状态（留给下一轮）
- banked **366/500 (0.732)**，unbanked 134
- 权威链 /tmp/c611/live500_c611.json；suite 基线 11272；amg head c596d1f
- 下一轮候选（从 /tmp/c611 链 unbanked 看）：
  - `gpt4_f2262a51` doctors（GT 长句 'three different doctors: primary care physician, ENT specialist, dermatologist'——clinic 系统讨论噪声重，需 _cnt_numval 长句数值抽取验证）
  - `gpt4_ab202e7f` kitchen 5 items（coffee maker 只有 'donated + upgrade' 无 replace/fix 动词——需 donate→replace 语义墙，设计偏重）
  - `bf659f65` albums GT=3 但只辨识出 2 个购买（第三个缺口在 Telluride 'their EP' 是否独立 item——语义歧义高）
  - `0a995998` clothing（C607 判偏重，boots return vs new-pair pickup 归并歧义）
  - `6d550036`/`60472f9c` 项目对（证据分散）
  - 另一族：pref-gate NEEDS_JUDGE 行（行为未知，风险高）
- replay harness：/tmp/c611/{replay.py, build_replay.py}（6 锚点 count==1/2 验证 + diff 审计恰 6 hunk 组）
- **教训（给下轮）**：(1) 后台跑长 suite 必须用 Tee 落盘模式（/tmp/c611/run_suite.py 范本），exec 后台捕获不可信；(2) 新 form 认领的行要 grep test_*.py 里是否有历史 pin（`grep -rn "fitness classes" test_*.py` 式三步 census 之外加第四步：**pin census**）；(3) loose 表亲要查链上 banked 状态再下结论（a08a253f 误判两分钟）。

### 遗留
- memory_graph.py `_search_cache` 脏 hunk + temporal_test_data.json/test_optimization.py/test_status.log 三个 untracked 杂物（C604 起挂账，五轮未动）——仍未清理，非本轮引入，未卷入 commit。

## 工件
- commit `c596d1f`
- /tmp/c611/：dump_cands.py、dump_out.txt、inspect_target.py、census_fitness.py、run_face_tests.py、run_suite.py（Tee 范本）、run_patched.py、probe_adapter.py、build_replay.py、replay.py、append_tsv.py、check_cousins.py、live500_c611.json（新权威链）
- memory/experiments.tsv C611 行
