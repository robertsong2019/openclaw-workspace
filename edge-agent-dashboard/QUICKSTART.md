# Edge Agent Dashboard - 5分钟快速开始 🚀

## 前置要求

- Python 3.9+
- pip

## 第1步：安装 (1分钟)

```bash
pip install edge-agent-dashboard
```

## 第2步：启动 (10秒)

```bash
edge-agent-dashboard
```

你会看到类似这样的输出：

```
╔═══════════════════════════════════════════════════════╗
║   Edge Agent Runtime Dashboard 🎛️                    ║
╠═══════════════════════════════════════════════════════╣
║   Dashboard: http://0.0.0.0:8000                      ║
║   WebSocket: ws://0.0.0.0:8000/ws                    ║
╚═══════════════════════════════════════════════════════╝

🚀 Edge Agent Dashboard started!
```

## 第3步：访问Dashboard (10秒)

打开浏览器，访问：**http://localhost:8000**

你会看到一个现代化的管理界面，包含：

- **资源监控卡片**：CPU、内存、网络使用情况
- **实时图表**：60秒内的资源趋势
- **Agent网格**：所有Agent的状态和控制按钮
- **日志查看器**：实时日志流

## 第4步：添加第一个Agent (2分钟)

### 示例1：简单的Python脚本

创建一个测试脚本：

```bash
# 创建一个简单的脚本
cat > test_agent.py << 'EOF'
import time
import random

print("Agent started!")
print("Agent ID: test-001")
print("Version: 1.0.0")

for i in range(100):
    print(f"[INFO] Working... {i}/100")
    print(f"[DEBUG] Random value: {random.random()}")
    time.sleep(1)

print("Agent completed!")
EOF
```

在Dashboard中点击 **"+ 添加Agent"** 按钮，填写：

- **Agent ID**: `test-script`
- **名称**: `测试脚本`
- **启动命令**: `python test_agent.py`
- **工作目录**: `/path/to/your/folder`
- **自动启动**: ✅

点击"创建"，Agent会自动启动！

### 示例2：长期运行的服务

创建一个长期运行的Agent：

```bash
cat > monitor_agent.py << 'EOF'
import time
import random

print("Monitor Agent started!")
while True:
    cpu_usage = random.uniform(10, 50)
    memory_usage = random.uniform(200, 800)
    print(f"[METRIC] CPU: {cpu_usage:.1f}%")
    print(f"[METRIC] Memory: {memory_usage:.1f}MB")
    time.sleep(2)
EOF
```

在Dashboard中添加：

- **Agent ID**: `monitor`
- **名称**: `监控Agent`
- **启动命令**: `python monitor_agent.py`
- **工作目录**: `/path/to/your/folder`

### 示例3：边缘设备Agent

如果你有edge-agent-micro项目，可以：

```bash
# 在edge-agent-micro目录下
cd examples/esp32_basic
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

在Dashboard中添加：

- **Agent ID**: `esp32-sensor`
- **名称**: `ESP32传感器`
- **启动命令**: `idf.py -p /dev/ttyUSB0 monitor`
- **工作目录**: `/path/to/edge-agent-micro/examples/esp32_basic`

## 第5步：监控和控制 (30秒)

### 查看实时状态

Dashboard会自动每秒更新：
- ✅ Agent状态（运行/停止/错误）
- 📊 资源使用图表
- 📝 实时日志流

### 控制Agent

每个Agent卡片都有控制按钮：

- **启动** - 启动停止的Agent
- **停止** - 停止正在运行的Agent
- **重启** - 重启Agent
- **日志** - 在日志查看器中查看该Agent的日志
- **🗑️** - 删除Agent配置

### 查看日志

1. 点击Agent卡片上的"日志"按钮
2. 或者在日志查看器顶部的下拉菜单中选择Agent
3. 日志会实时流式显示（tail -f风格）
4. 不同颜色区分：
   - 🟢 绿色 - 标准输出
   - 🔴 红色 - 错误输出

## 高级用法

### 自定义配置目录

```bash
edge-agent-dashboard --config-dir /my/custom/path
```

所有Agent配置会保存在指定目录的 `.json` 文件中。

### 修改端口和主机

```bash
edge-agent-dashboard --host 127.0.0.1 --port 9000
```

### 开发模式（自动重载）

```bash
edge-agent-dashboard --reload
```

修改代码后自动重启服务器。

## 配置文件格式

Agent配置保存在 `agents/` 目录，格式为JSON：

```json
{
  "id": "my-agent",
  "name": "我的Agent",
  "command": "python agent.py",
  "working_dir": "/path/to/agent",
  "env_vars": {
    "API_KEY": "your-key",
    "DEBUG": "true"
  },
  "auto_start": true
}
```

### 环境变量

你可以通过配置文件设置环境变量：

```json
{
  "id": "api-agent",
  "name": "API Agent",
  "command": "python api_agent.py",
  "env_vars": {
    "API_KEY": "sk-xxx",
    "API_URL": "https://api.example.com",
    "LOG_LEVEL": "debug"
  }
}
```

## 故障排查

### Agent无法启动

1. 检查"启动命令"是否正确
2. 检查"工作目录"是否存在
3. 查看日志查看器中的错误信息
4. 确保命令可以在终端中手动运行

### Dashboard无法访问

1. 确认Dashboard正在运行
2. 检查防火墙设置
3. 尝试使用 `--host 0.0.0.0` 启动
4. 检查端口是否被占用

### WebSocket断开连接

1. 检查网络连接
2. Dashboard会自动重连（5秒间隔）
3. 查看浏览器控制台错误信息

## 下一步

- 📖 查看 [README.md](README.md) 了解完整功能
- 🔧 查看 [API文档](http://localhost:8000/docs) 了解所有API
- 🎯 添加更多Agent来管理你的边缘设备
- 📊 监控资源使用，优化性能

## 示例场景

### 场景1：智能家居控制

```bash
# 添加多个设备Agent
- 温度传感器Agent
- 摄像头监控Agent
- 灯光控制Agent
- 语音助手Agent
```

### 场景2：工业物联网

```bash
# 添加生产线Agent
- 设备状态监控Agent
- 数据采集Agent
- 预测性维护Agent
- 报警通知Agent
```

### 场景3：边缘AI推理

```bash
# 添加AI推理Agent
- 图像识别Agent
- 语音识别Agent
- 异常检测Agent
- 数据预处理Agent
```

## 卸载

```bash
pip uninstall edge-agent-dashboard
```

---

**需要帮助？** 打开浏览器控制台（F12）查看详细错误信息，或查看Dashboard日志。

**祝使用愉快！** 🎉
