# ralph-autonomous-agent-loop

自主 AI 编码循环：反复启动 AI 编码工具（Amp/Claude Code）直到 PRD 全部完成。

## 工作原理

1. 读取 `prd.json`，选取最高优先级未完成任务
2. 启动新 AI 实例实现该任务
3. 运行质量检查（类型检查、测试），提交代码
4. 标记 `passes: true`，记录到 `progress.txt`
5. 循环直到全部完成

## 快速开始

```bash
# 默认使用 Amp，10 次迭代
./scripts/ralph/ralph.sh

# 指定工具和迭代数
./scripts/ralph/ralph.sh --tool claude 20
```

## prd.json 核心结构

```json
{
  "branchName": "feature/xxx",
  "projectContext": "项目描述...",
  "userStories": [
    {
      "id": "story-1",
      "title": "任务标题",
      "priority": 1,
      "passes": false,
      "description": "详细描述",
      "acceptanceCriteria": ["验收标准1", "验收标准2"]
    }
  ]
}
```

## 关键文件

| 文件 | 用途 |
|------|------|
| `ralph.sh` | 主循环脚本 |
| `prompt.md` / `CLAUDE.md` | 提示模板 |
| `prd.json` | 任务列表（含完成状态） |
| `progress.txt` | 跨迭代学习记录 |

## 最佳实践

- **拆小任务**：每个 story 应在 1-2 小时内可完成
- **设质量门**：在 prompt 模板中加入项目特有的检查命令
- **监控进度**：`cat prd.json | jq '.userStories[] | {id, title, passes}'`

## 参考

- [Ralph 仓库](https://github.com/snarktank/ralph)
- [Geoffrey Huntley 的 Ralph 模式](https://ghuntley.com/ralph/)
