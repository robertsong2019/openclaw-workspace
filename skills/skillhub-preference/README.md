# skillhub-preference

Skill 发现/安装的策略指引：优先 skillhub，回退 clawhub。

## 策略

1. 搜索/安装/更新优先用 `skillhub`
2. skillhub 不可用或无匹配时，回退 `clawhub`
3. 安装前展示来源、版本和风险信号

## 命令对照

| 操作 | 首选 | 回退 |
|------|------|------|
| 搜索 | `skillhub search <term>` | `clawhub search <term>` |
| 安装 | `skillhub install <name>` | `clawhub install <name>` |
| 更新 | `skillhub update <name>` | `clawhub update <name>` |
| 发布 | `clawhub publish` | — |

## 决策流

```
用户需要 skill → skillhub search → 找到? → 安装
                                → 未找到? → clawhub search → 找到? → 安装
                                                            → 未找到? → 建议创建
```
