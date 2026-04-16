# Edge Agent Runtime Dashboard 🎛️

> 可视化管理界面，用于监控和控制边缘AI Agent运行时

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](https://github.com/robertsong2019/edge-agent-dashboard)

## 功能特性

- **🎯 实时监控** - Agent状态（运行/停止/错误）、资源使用（CPU、内存、网络）
- **📊 资源图表** - 实时CPU、内存、网络流量趋势图
- **📝 日志流式显示** - tail -f 风格的实时日志查看，颜色区分
- **🎮 Agent控制** - 一键启动、停止、重启Agent
- **⚙️ 配置编辑** - 在线创建和编辑Agent配置
- **🔗 WebSocket实时更新** - 毫秒级数据同步，自动重连
- **📱 响应式设计** - 支持桌面、平板、手机

## 技术栈

- **后端**：FastAPI（Python） + WebSocket + 异步架构
- **前端**：原生HTML/JS + Chart.js + Tailwind CSS
- **监控**：psutil（跨平台系统监控）
- **传输**：WebSocket（实时双向通信）

## 快速开始

### 安装

```bash
pip install edge-agent-dashboard
```

### 启动

```bash
edge-agent-dashboard
```

### 访问

浏览器打开: http://localhost:8000

### 添加Agent

点击右上角的"+ 添加Agent"按钮，填写配置：
- **Agent ID**: 唯一标识符
- **名称**: 显示名称
- **启动命令**: 如 `python agent.py`
- **工作目录**: Agent所在目录
- **自动启动**: 是否立即启动

详见 [QUICKSTART.md](QUICKSTART.md)（5分钟快速教程）

## 使用示例

### 基本使用

```bash
# 启动Dashboard
edge-agent-dashboard

# 访问Web界面
# http://localhost:8000

# 查看API文档
# http://localhost:8000/docs
```

### 添加Agent（通过API）

```bash
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-agent",
    "name": "My Agent",
    "command": "python agent.py",
    "working_dir": "/path/to/agent",
    "auto_start": true
  }'
```

### WebSocket连接

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(message.type, message.data);
};
```

## 文档

- **[QUICKSTART.md](QUICKSTART.md)** - 5分钟快速开始教程
- **[USAGE.md](USAGE.md)** - 详细使用指南和API参考
- **[SCREENSHOTS.md](SCREENSHOTS.md)** - 界面说明和布局
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 项目总结和实现细节
- **[COMPLETION_REPORT.md](COMPLETION_REPORT.md)** - 完成报告和测试结果

## 项目结构

```
edge-agent-dashboard/
├── edge_agent_dashboard/      # 主包
│   ├── main.py               # FastAPI应用
│   ├── manager.py            # Agent管理器
│   ├── monitor.py            # 资源监控器
│   ├── websocket.py          # WebSocket管理
│   └── static/               # 前端文件
│       ├── index.html
│       └── app.js
├── agents/                   # Agent配置目录
├── example_agent.py          # 示例Agent
├── setup.py                  # pip打包配置
├── requirements.txt          # 依赖列表
└── docs/                     # 文档
```

## 开发

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

# 运行测试
python test_dashboard.py
```

## 测试

项目包含完整的测试脚本：

```bash
python test_dashboard.py
```

测试覆盖：
- ✅ API连接
- ✅ Agent管理（创建、启动、停止、删除）
- ✅ 资源监控
- ✅ 日志获取

## 性能

- **启动时间**: < 2秒
- **API响应**: < 50ms
- **WebSocket延迟**: < 10ms
- **内存占用**: ~50MB
- **更新频率**: 1秒

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 作者

罗嵩 (Robert Song)

## 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [Chart.js](https://www.chartjs.org/) - 灵活的图表库
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的CSS框架
- [psutil](https://psutil.readthedocs.io/) - 跨平台系统监控库

---

**状态**: ✅ 已完成并测试通过 | **版本**: 0.1.0 | **日期**: 2026-04-13
