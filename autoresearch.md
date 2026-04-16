# autoresearch.md — Catalyst 自主研究方法论

> 灵感来源：karpathy/autoresearch
> 核心理念：编程方法论，而非编程具体行为

## 原则

1. **明确指标** — 每个任务必须有可量化的成功标准
2. **快速循环** — 每轮改进必须在时间预算内完成并评估
3. **保留/回退** — 改进了保留（git commit），没改进回退（git reset）
4. **积累性** — 后续任务必须在前序任务成果上积累，而非从零开始
5. **简洁优先** — 删代码得到相同结果 > 加代码得到更好结果 > 加大量代码得到微小改进

## 实验记录格式

每个项目目录下维护 `experiments.tsv`：

```
timestamp\tcommit\tmetric\tvalue\tstatus\tdescription
2026-04-14T13:00\ta1b2c3d\ttest_pass_rate\t100%\tkeep\tbaseline
2026-04-14T13:30\tb2c3d4e\ttest_pass_rate\t100%\tkeep\trefactor without losing coverage
```

## 任务改造清单

### ✅ 已改造
- (待填充)

### 🔄 待改造
- github-creative-evening → 改为有目标的项目实验循环
- deep-exploration-evening → 改为有输出的深度研究
- code-lab-evening → 改为有测试指标的开发循环
- tool-development-evening → 改为有功能清单的工具开发
