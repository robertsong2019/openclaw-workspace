# Edge Agent Dashboard - 使用指南

## 目录

1. [快速开始](#快速开始)
2. [API参考](#api参考)
3. [配置说明](#配置说明)
4. [常见问题](#常见问题)
5. [开发指南](#开发指南)

## 快速开始

### 安装

```bash
pip install edge-agent-dashboard
```

### 启动

```bash
edge-agent-dashboard
```

访问 http://localhost:8000

### 添加Agent

点击右上角的"+ 添加Agent"按钮，填写：
- Agent ID: 唯一标识符
- 名称: 显示名称
- 启动命令: 启动Agent的命令
- 工作目录: Agent运行目录（可选）
- 自动启动: 是否自动启动（可选）

## API参考

### Agent管理

#### 获取所有Agent
```bash
GET /api/agents
```

响应：
```json
[
  {
    "id": "my-agent",
    "name": "My Agent",
    "state": "running",
    "pid": 12345,
    "uptime": 1234567890.0,
    "last_error": null,
    "config": {
      "id": "my-agent",
      "name": "My Agent",
      "command": "python agent.py",
      "working_dir": "/path/to/agent",
      "env_vars": {},
      "auto_start": false
    }
  }
]
```

#### 获取单个Agent
```bash
GET /api/agents/{agent_id}
```

#### 创建Agent
```bash
POST /api/agents
Content-Type: application/json

{
  "id": "my-agent",
  "name": "My Agent",
  "command": "python agent.py",
  "working_dir": "/path/to/agent",
  "env_vars": {
    "API_KEY": "your-key"
  },
  "auto_start": false
}
```

#### 更新Agent
```bash
PUT /api/agents/{agent_id}
Content-Type: application/json

{
  "id": "my-agent",
  "name": "Updated Agent",
  "command": "python updated_agent.py",
  "working_dir": "/path/to/agent",
  "env_vars": {},
  "auto_start": true
}
```

#### 删除Agent
```bash
DELETE /api/agents/{agent_id}
```

#### 启动Agent
```bash
POST /api/agents/{agent_id}/start
```

#### 停止Agent
```bash
POST /api/agents/{agent_id}/stop
```

#### 重启Agent
```bash
POST /api/agents/{agent_id}/restart
```

#### 获取Agent日志
```bash
GET /api/agents/{agent_id}/logs?lines=100
```

### 资源监控

#### 获取当前指标
```bash
GET /api/metrics
```

响应：
```json
{
  "timestamp": 1234567890.0,
  "cpu_percent": 45.2,
  "memory_percent": 62.8,
  "memory_used_mb": 1234.5,
  "memory_total_mb": 2048.0,
  "network_sent_mb": 1.2,
  "network_recv_mb": 3.4,
  "disk_usage_percent": 75.5,
  "load_average": 1.5
}
```

#### 获取历史指标
```bash
GET /api/metrics/history?seconds=60
```

响应：
```json
{
  "timestamps": [1234567890000, 1234567900000],
  "cpu": [45.2, 46.1],
  "memory": [62.8, 63.2],
  "network_sent": [1.2, 1.5],
  "network_recv": [3.4, 3.8]
}
```

### WebSocket

#### 连接WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  switch (message.type) {
    case 'init':
      // 初始数据
      console.log('Agents:', message.data.agents);
      console.log('Metrics:', message.data.metrics);
      break;

    case 'agent_update':
      // Agent状态更新
      console.log('Agent updated:', message.data);
      break;

    case 'metrics':
      // 资源指标更新
      console.log('Metrics:', message.data);
      break;

    case 'log_update':
      // 日志更新
      console.log('Logs:', message.data);
      break;
  }
};
```

## 配置说明

### Agent配置文件

Agent配置保存在 `agents/` 目录，每个Agent一个JSON文件：

```json
{
  "id": "my-agent",
  "name": "My Agent",
  "command": "python agent.py",
  "working_dir": "/path/to/agent",
  "env_vars": {
    "ENV_VAR_1": "value1",
    "ENV_VAR_2": "value2"
  },
  "auto_start": false
}
```

### 字段说明

- `id` (必需): Agent唯一标识符
- `name` (必需): Agent显示名称
- `command` (必需): 启动命令
- `working_dir` (可选): 工作目录
- `env_vars` (可选): 环境变量字典
- `auto_start` (可选): 是否自动启动，默认false

### 环境变量

环境变量会在Agent启动时注入到进程环境中：

```json
{
  "id": "api-agent",
  "name": "API Agent",
  "command": "python api_agent.py",
  "env_vars": {
    "API_KEY": "sk-xxx",
    "API_URL": "https://api.example.com",
    "DEBUG": "true",
    "LOG_LEVEL": "info"
  }
}
```

在Python Agent中访问：

```python
import os

api_key = os.environ.get('API_KEY')
api_url = os.environ.get('API_URL')
debug = os.environ.get('DEBUG', 'false').lower() == 'true'
```

## 常见问题

### Agent无法启动

**症状**: 点击启动按钮后，Agent状态仍为"stopped"或变为"error"

**原因**:
1. 启动命令不正确
2. 工作目录不存在
3. 缺少依赖
4. 权限不足

**解决方案**:
1. 检查启动命令是否可以在终端中手动运行
2. 确认工作目录存在且可访问
3. 查看日志查看器中的错误信息
4. 确保Agent文件有执行权限

### Dashboard无法访问

**症状**: 浏览器无法打开Dashboard

**原因**:
1. Dashboard未启动
2. 防火墙阻止
3. 端口被占用

**解决方案**:
1. 确认Dashboard正在运行
2. 检查防火墙设置
3. 使用 `--host 0.0.0.0` 启动
4. 检查端口是否被占用：`netstat -tlnp | grep 8000`

### WebSocket断开连接

**症状**: Dashboard显示"断开连接"，数据不更新

**原因**:
1. 网络问题
2. Dashboard重启
3. 浏览器问题

**解决方案**:
1. 检查网络连接
2. Dashboard会自动重连（5秒间隔）
3. 刷新浏览器页面
4. 查看浏览器控制台错误信息

### 日志不显示

**症状**: 日志查看器中没有内容

**原因**:
1. Agent未启动
2. Agent没有输出
3. 日志缓冲区未刷新

**解决方案**:
1. 确认Agent正在运行
2. Agent需要有标准输出或错误输出
3. 等待几秒钟让日志积累
4. 清空日志后重新加载

### 资源指标不更新

**症状**: CPU、内存等指标不变化

**原因**:
1. 资源监控器未启动
2. WebSocket断开
3. 系统权限问题

**解决方案**:
1. 检查Dashboard是否正常运行
2. 确认WebSocket连接正常
3. 检查系统权限（特别是psutil需要访问/proc）

## 开发指南

### 项目结构

```
edge-agent-dashboard/
├── edge_agent_dashboard/      # 主包
│   ├── __init__.py
│   ├── main.py               # FastAPI应用入口
│   ├── manager.py            # Agent管理器
│   ├── monitor.py            # 资源监控器
│   ├── websocket.py          # WebSocket管理
│   └── static/               # 静态文件
│       ├── index.html        # 前端页面
│       └── app.js            # 前端逻辑
├── agents/                   # Agent配置目录
├── setup.py                  # pip打包配置
├── requirements.txt          # 依赖列表
├── README.md                 # 项目说明
├── QUICKSTART.md            # 快速开始
└── USAGE.md                  # 使用指南
```

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/robertsong2019/edge-agent-dashboard.git
cd edge-agent-dashboard

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e .

# 运行开发服务器（自动重载）
edge-agent-dashboard --reload
```

### 添加新功能

#### 1. 添加新的API端点

在 `main.py` 中添加：

```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    return {"message": "Hello from new endpoint"}
```

#### 2. 添加新的WebSocket消息类型

在 `websocket.py` 的 `WebSocketBroadcaster` 中添加：

```python
# 在 _broadcast_loop 中添加
await self.connection_manager.broadcast({
    "type": "new_message_type",
    "data": {...}
})
```

在前端 `app.js` 中处理：

```javascript
case 'new_message_type':
    handleNewMessageType(message.data);
    break;
```

#### 3. 修改前端

编辑 `static/index.html` 或 `static/app.js`，然后刷新浏览器。

### 测试

```bash
# 运行测试（如果存在）
pytest

# 手动测试API
curl http://localhost:8000/api/agents
curl -X POST http://localhost:8000/api/agents/my-agent/start

# 测试WebSocket
wscat -c ws://localhost:8000/ws
```

### 构建和发布

```bash
# 构建包
python setup.py sdist bdist_wheel

# 发布到PyPI（需要PyPI账号）
twine upload dist/*

# 或者发布到TestPyPI
twine upload --repository testpypi dist/*
```

## 性能优化

### 减少日志缓冲区大小

在 `manager.py` 中修改：

```python
self.log_buffers[agent_id] = []
# 限制缓冲区大小
if len(self.log_buffers[agent_id]) > 500:  # 从1000改为500
    self.log_buffers[agent_id] = self.log_buffers[agent_id][-250:]  # 从-500改为-250
```

### 调整资源监控间隔

在启动时修改：

```python
resource_monitor = ResourceMonitor(update_interval=2.0)  # 从1.0改为2.0秒
```

### 限制历史数据点

在 `monitor.py` 中修改：

```python
self.max_history = 150  # 从300改为150（保留2.5分钟）
```

## 安全建议

1. **不要在生产环境中使用 `--host 0.0.0.0`**，除非有防火墙保护
2. **配置文件中不要包含敏感信息**，使用环境变量代替
3. **限制Agent命令的权限**，避免运行需要root权限的命令
4. **定期备份Agent配置**，防止数据丢失
5. **监控日志大小**，避免磁盘被日志填满

## 贡献

欢迎贡献！请遵循以下步骤：

1. Fork仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
