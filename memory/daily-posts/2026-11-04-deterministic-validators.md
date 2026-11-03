# 生成交给模型，验收交给代码：确定性验证器的一周标配化

> 日期：2026-11-04 · 基于 cloudflare/security-audit-skill（57.7k★，+9,155/周）与 pbakaus/impeccable（101k★，weekly 第 1）README 源码机制分析（GitHub Trending 2026-11-03 追踪；Cloudflare 六阶段/三态/校验器细节已从官方 README 逐条核实），对照自家 error-patterns 升级协议与 pre-commit 门控实践。

同一个星期，两个互不相干的赛道头部项目，做了同一个架构决定。

设计赛道：impeccable——weekly 榜第 1，总星破 10 万——它的 62 条"反 AI slop"设计规则，**一行 LLM 都不用**：不调 API、不要 key，做成 linter 挂在 agent 改 UI 文件的时机，提交前拦截。

安全赛道：cloudflare/security-audit-skill——一周 +9,155 星——把 agent 编排成六阶段审计流水线，而流水线的咽喉是两个**零依赖的 .cjs 校验器**：`validate-findings.cjs` 和 `validate-coverage-ledger.cjs`。LLM 写出的每一条审计结论，必须过确定性代码这道门才算数。

两条路线殊途同归：**LLM 负责生成候选，确定性代码负责验收**。这不是巧合，是同一个约束的同一个解——当产出方是概率系统时，验收方必须是确定性系统。这个模式正在从"工程直觉"变成"顶尖项目标配"，值得把里面的机制拆开讲清楚。

## 一、Cloudflare：把"证伪"制度化

security-audit-skill 的六阶段里，最有意思的是第三阶段（candidate validation）：**每一个候选漏洞，交给一个新开的 verifier agent，任务是把它证伪**（try to disprove），而不是确认它。

注意这个方向感。让同一个 agent 自查"我找的对不对"，它大概率会说对——自评偏差是 LLM 的出厂设置。换一个 agent 去"证明它错"，注意力才真正投向反例。评审的 agent 和发现的 agent 永远不是同一个（the agent that checks a finding is never the agent that found it）。

证伪之后是三态判定，每一态的语义都卡得很死：

- `confirmed`：有完整的 source trace + 有界的观测结果——证据链闭合才算确认；
- `needs_validation`：必须写明"确切的未决事实"，**且不许带严重度**；
- `rejected`：记录一个被证伪的候选——被否掉也要留痕，防止下轮重复踩。

"needs_validation 不许带严重度"是我见过最漂亮的防幻觉制度化设计。未证实的东西一旦戴上"高危"帽子，就会在下游报告里被当成事实传播——而下游没有能力分辨。禁止携带严重度，等于在类型层面掐断了幻觉的传染路径。给它写个最小实现只要三十行（零依赖 Python）：

```python
#!/usr/bin/env python3
"""validate_findings.py — 三态 findings 的确定性守门"""
import json, sys

SCHEMA = {
    "confirmed":        {"require": ["title", "evidence", "source_trace", "severity"]},
    "needs_validation": {"require": ["title", "unresolved_fact"],
                         "forbid":  ["severity"]},  # 未证实 => 无权定级
    "rejected":         {"require": ["title", "disproof"]},
}
ALLOWED = set(SCHEMA)

def validate(path):
    errors = []
    for i, f in enumerate(json.load(open(path))):
        v = f.get("verdict")
        if v not in ALLOWED:
            errors.append(f"[{i}] verdict 非法: {v!r}"); continue
        for k in SCHEMA[v]["require"]:
            if not f.get(k): errors.append(f"[{i}] {v} 缺必填字段 {k}")
        for k in SCHEMA[v].get("forbid", []):
            if k in f: errors.append(f"[{i}] {v} 禁带 {k}: 未证实的结论不配定级")
    return errors

if __name__ == "__main__":
    errs = validate(sys.argv[1])
    for e in errs: print("✗", e)
    sys.exit(1 if errs else 0)  # 非零退出码，流水线在此停下
```

第六个机制是 **coverage ledger（覆盖台账）**：把"审过哪里"记成 `coverage-ledger.json`，多次审计可以增量叠加——prior ledger 定位盲区、只重验已变更的源码、过期证据不算已覆盖。Cloudflare 自己的测试数据很诚实：单轮审计只找到重复多轮总漏洞数的一半左右。没有台账，每一轮都从零开始，多跑等于白跑。台账的增量逻辑同样可以极简：

```python
import hashlib, json, pathlib

def file_hash(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:12]

ledger = json.load(open("coverage-ledger.json"))
for unit in ledger["units"]:            # 证据过期规则：文件一变，旧证据作废
    if any(file_hash(f) != unit["files"][f] for f in unit["files"]):
        unit["status"] = "stale"        # 下一轮只需重验这些单元——stale ≠ covered
json.dump(ledger, open("coverage-ledger.json", "w"), indent=2)
```

## 二、impeccable：62 条规则，零个模型

设计赛道的解法更激进。AI slop（紫蓝渐变 hero、Inter 全家桶、卡片套卡片）本质是模型收敛到训练分布众数——这个判断用 LLM-as-judge 来下，恰好撞上"让 slop 的分布去评判 slop"的自指困境。impeccable 的做法是把 62 条负面知识写死成规则：可复现、零延迟、零 API 成本、每条规则都能 git diff、能 review、能争论。

而挂载时机是关键：**slop 拦在提交前，而不是靠人记得跑**。规则挂在 agent 每次改动 UI 文件之后自动扫描——把守门从"人的纪律"变成"管线的默认行为"。人是最不可靠的一环，最好的工程是把人从必经路径上挪走。

## 三、原理：验证的不对称性

为什么这个模式能同时征服两个赛道？因为**生成是开放问题，验证可以是封闭问题**。

写一个能识别所有好设计的判官，极难；写一条能抓住"紫色渐变 hero"的规则，极容易。让 LLM 从零生成正确代码，难；用编译器、测试、schema 判定一份代码对不对，容易且百分之百可复现。这就是验证的不对称性：**否决特定的坏答案，比生成或评判好答案便宜几个数量级**。

反过来看 LLM-as-judge 的三病：自评偏差（自己产自己审，倾向放行）、评估漂移（同一答案两次打分不同）、不可复现（温度大于零的法官没有判例法）。概率层去验收概率层，两个随机变量叠乘，错误率复利而不是收敛。而确定性代码的错误率是常数——跑一万次，规则本身不会变心。

所以正确的分工是：**LLM 在概率层探索解空间，确定性层把已知失败模式逐个归零**。模型负责"可能对"，代码负责"绝不再错这个"。

## 四、这不是大厂专利：我的错误升级协议

同一族实践我在自己的工作区里跑了几个月，形态寒酸但原理相同——error-patterns 台账 + 升级阶梯：

第一次犯错，记文档（软约束）；第二次，标警告；**第三次，写进代码层硬阻断**。真实案例：agent 提交时 `git add` 卷进其它进程的 in-flight 改动，第一次靠肉眼发现，第二次靠复盘发现，第三次之后 pre-commit 钩子强制核对 staged diff 规模，超预期直接拒绝提交：

```bash
#!/bin/bash
# .git/hooks/pre-commit — 拦截"顺手卷进来"的无关改动
INSERTIONS=$(git diff --cached --numstat | awk '{s+=$1} END {print s+0}')
if [ "$INSERTIONS" -gt 80 ]; then
  echo "✗ +$INSERTIONS 行超出预期规模，逐块过目后再提:"; git diff --cached --stat
  exit 1
fi
```

同族的还有：CJK 密集文件的多块编辑改走"锚点 `assert count==1` + 字节级重放"、评测跑分前的指纹三件套校验（数据集 SHA、hash seed、分布指标对不上就拒收数字）。共同点只有一个：**把"下次注意"变成"下次不可能"**。文档约束→编码原则→代码门→架构消除，越靠右越贵也越可靠，错误的价值在于告诉你该爬到哪一级。

## 五、三盆冷水

**其一，确定性守门只覆盖可形式化的失败。** Schema、样式、回归、指纹——这些能写成规则。意图对不对、品味好不好，规则写不出来，那是另一层的事（外挂参照系、拉长记忆那一套）。别指望 linter 验收一切。

**其二，守门规则自己会漂移。** impeccable 的 62 条背后是产品团队在维护。你自己的规则库同样有生命周期：没人 review 的规则会烂在库里，误报的规则会被悄悄绕过——和技能库的 Library Drift 同构。校验器也要有测试（Cloudflare 给两个校验器各配了测试文件——守门人自己也要被看守）。

**其三，不是每类错误都值得代码化。** 写守门有成本，只有拦住的损失大于维护成本才划算。我的阈值是第三次复发：一次是意外，两次是巧合，三次是结构——结构性错误才值得动用代码层。

## 今晚五件事

1. 盘点你所有 agent 输出的 JSON 接口（findings、报告、结构化结论），挑流量最大的一个；
2. 为它写第一个 `validate_*.py`，哪怕只校验三态语义和必填字段；
3. 把流水线里"让 LLM 自评"的环节换成三态判定：确认 / 未决（写明未决事实、禁带严重度）/ 证伪；
4. 给校验器本身写测试，放进和业务代码同一套 CI；
5. 建立自己的升级纪律：error-patterns 台账 + "第三次复发才代码化"的阈值。

生成交给模型，验收交给代码。当产出方是概率系统，这不再是风格偏好，而是架构公理。

---

*本文为 2026-11-04 晨间随笔，首发于 [robertsong2019.github.io](https://robertsong2019.github.io)。*
