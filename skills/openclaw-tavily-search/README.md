# openclaw-tavily-search

通过 Tavily API 进行 Web 搜索，替代 Brave Search。

## 前置条件

设置 API Key（二选一）：
- 环境变量：`TAVILY_API_KEY=...`
- 配置文件：`~/.openclaw/.env` 添加 `TAVILY_API_KEY=...`

## 用法

```bash
# JSON 输出
python3 scripts/tavily_search.py --query "..." --max-results 5

# 含 AI 摘要
python3 scripts/tavily_search.py --query "..." --include-answer

# 兼容 Brave 格式
python3 scripts/tavily_search.py --query "..." --format brave

# Markdown 列表
python3 scripts/tavily_search.py --query "..." --format md
```

## 输出格式

| 格式 | 说明 |
|------|------|
| raw (默认) | JSON: `query`, `answer?`, `results[{title,url,content}]` |
| brave | JSON: `query`, `answer?`, `results[{title,url,snippet}]` |
| md | Markdown 列表 |

## 注意

- 建议 `max-results` 保持 3–5，避免 token 浪费
