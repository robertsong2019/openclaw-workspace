"""
Edge Agent Runtime Dashboard - 主应用入口
"""

import uvicorn
import argparse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional

from .manager import AgentManager, AgentConfig, AgentInfo
from .monitor import ResourceMonitor
from .websocket import ConnectionManager, WebSocketBroadcaster


# 创建FastAPI应用
app = FastAPI(title="Edge Agent Runtime Dashboard", version="0.1.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局实例
agent_manager: Optional[AgentManager] = None
resource_monitor: Optional[ResourceMonitor] = None
connection_manager: Optional[ConnectionManager] = None
broadcaster: Optional[WebSocketBroadcaster] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global agent_manager, resource_monitor, connection_manager, broadcaster

    # 启动时初始化
    agent_manager = AgentManager()
    resource_monitor = ResourceMonitor(update_interval=1.0)
    connection_manager = ConnectionManager()
    broadcaster = WebSocketBroadcaster(connection_manager, agent_manager, resource_monitor)

    await resource_monitor.start()
    await broadcaster.start()

    print("🚀 Edge Agent Dashboard started!")

    yield

    # 关闭时清理
    await broadcaster.stop()
    await resource_monitor.stop()
    print("🛑 Edge Agent Dashboard stopped!")


app.router.lifespan_context = lifespan


# 挂载静态文件
app.mount("/static", StaticFiles(directory="edge_agent_dashboard/static"), name="static")


# ========== API 路由 ==========

@app.get("/")
async def root():
    """根路径 - 重定向到dashboard"""
    from fastapi.responses import HTMLResponse
    with open("edge_agent_dashboard/static/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/agents")
async def list_agents() -> List[AgentInfo]:
    """获取所有Agent列表"""
    return await agent_manager.get_agents()


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str) -> AgentInfo:
    """获取单个Agent信息"""
    agent = await agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@app.post("/api/agents")
async def create_agent(config: AgentConfig) -> AgentInfo:
    """创建新Agent"""
    return await agent_manager.create_agent(config)


@app.put("/api/agents/{agent_id}")
async def update_agent(agent_id: str, config: AgentConfig) -> AgentInfo:
    """更新Agent配置"""
    agent = await agent_manager.update_agent_config(agent_id, config)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@app.delete("/api/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """删除Agent"""
    success = await agent_manager.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted"}


@app.post("/api/agents/{agent_id}/start")
async def start_agent(agent_id: str):
    """启动Agent"""
    success = await agent_manager.start_agent(agent_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to start agent")
    return {"message": "Agent started"}


@app.post("/api/agents/{agent_id}/stop")
async def stop_agent(agent_id: str):
    """停止Agent"""
    success = await agent_manager.stop_agent(agent_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to stop agent")
    return {"message": "Agent stopped"}


@app.post("/api/agents/{agent_id}/restart")
async def restart_agent(agent_id: str):
    """重启Agent"""
    success = await agent_manager.restart_agent(agent_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to restart agent")
    return {"message": "Agent restarted"}


@app.get("/api/agents/{agent_id}/logs")
async def get_agent_logs(agent_id: str, lines: int = 100) -> List[str]:
    """获取Agent日志"""
    logs = await agent_manager.get_agent_logs(agent_id, lines=lines)
    return logs


@app.get("/api/metrics")
async def get_metrics():
    """获取当前资源指标"""
    return resource_monitor.get_current_metrics()


@app.get("/api/metrics/history")
async def get_metrics_history(seconds: int = 60):
    """获取资源指标历史"""
    return resource_monitor.get_history_dict(seconds)


# ========== WebSocket 路由 ==========

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点 - 实时数据推送"""
    await connection_manager.connect(websocket)

    try:
        # 发送初始数据
        agents = await agent_manager.get_agents()
        await connection_manager.send_personal({
            "type": "init",
            "data": {
                "agents": [a.model_dump() for a in agents],
                "metrics": resource_monitor.get_current_metrics().model_dump() if resource_monitor.get_current_metrics() else None
            }
        }, websocket)

        # 保持连接
        while True:
            data = await websocket.receive_text()
            # 可以处理客户端消息（如心跳）
            pass

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)


# ========== 命令行入口 ==========

def cli():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="Edge Agent Runtime Dashboard")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--config-dir", default="./agents", help="Agent config directory")

    args = parser.parse_args()

    # 更新全局配置
    global agent_manager
    agent_manager = AgentManager(config_dir=args.config_dir)

    print(f"""
╔═══════════════════════════════════════════════════════╗
║   Edge Agent Runtime Dashboard 🎛️                    ║
╠═══════════════════════════════════════════════════════╣
║   Dashboard: http://{args.host}:{args.port}              ║
║   WebSocket: ws://{args.host}:{args.port}/ws            ║
╚═══════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "edge_agent_dashboard.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        lifespan="on"
    )


if __name__ == "__main__":
    cli()
