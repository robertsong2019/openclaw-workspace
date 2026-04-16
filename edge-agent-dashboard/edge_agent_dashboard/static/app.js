// Edge Agent Dashboard - 前端逻辑

// WebSocket连接
let ws = null;
let agents = [];
let selectedAgentId = null;
let resourceChart = null;
let networkChart = null;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    connectWebSocket();
    setupEventListeners();
});

// WebSocket连接
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log('WebSocket connected');
        updateConnectionStatus(true);
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        handleMessage(message);
    };

    ws.onclose = () => {
        console.log('WebSocket disconnected');
        updateConnectionStatus(false);
        // 5秒后重连
        setTimeout(connectWebSocket, 5000);
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateConnectionStatus(false);
    };
}

// 更新连接状态
function updateConnectionStatus(connected) {
    const statusEl = document.getElementById('connection-status');
    if (connected) {
        statusEl.innerHTML = `
            <span class="w-2 h-2 rounded-full bg-green-500"></span>
            <span class="text-sm text-green-400">已连接</span>
        `;
    } else {
        statusEl.innerHTML = `
            <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
            <span class="text-sm text-red-400">断开连接</span>
        `;
    }
}

// 处理WebSocket消息
function handleMessage(message) {
    switch (message.type) {
        case 'init':
            agents = message.data.agents;
            renderAgents();
            if (message.data.metrics) {
                updateMetrics(message.data.metrics);
            }
            break;

        case 'agent_update':
            updateAgent(message.data);
            break;

        case 'metrics':
            updateMetrics(message.data);
            break;

        case 'log_update':
            appendLogs(message.data.agent_id, message.data.logs);
            break;
    }
}

// 更新资源指标
function updateMetrics(metrics) {
    // 更新卡片
    document.getElementById('cpu-value').textContent = `${metrics.cpu_percent.toFixed(1)}%`;
    document.getElementById('cpu-bar').style.width = `${metrics.cpu_percent}%`;

    document.getElementById('memory-value').textContent = `${metrics.memory_percent.toFixed(1)}%`;
    document.getElementById('memory-bar').style.width = `${metrics.memory_percent}%`;
    document.getElementById('memory-detail').textContent =
        `${metrics.memory_used_mb.toFixed(0)} / ${metrics.memory_total_mb.toFixed(0)} MB`;

    document.getElementById('network-sent').textContent = `${metrics.network_sent_mb.toFixed(2)} MB/s`;
    document.getElementById('network-recv').textContent = `${metrics.network_recv_mb.toFixed(2)} MB/s`;

    // 更新图表
    updateCharts(metrics);
}

// 初始化图表
function initCharts() {
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 0 },
        scales: {
            x: {
                type: 'time',
                time: {
                    displayFormats: {
                        second: 'HH:mm:ss'
                    }
                },
                grid: { color: 'rgba(255,255,255,0.1)' },
                ticks: { color: '#9ca3af' }
            },
            y: {
                beginAtZero: true,
                max: 100,
                grid: { color: 'rgba(255,255,255,0.1)' },
                ticks: { color: '#9ca3af' }
            }
        },
        plugins: {
            legend: {
                labels: { color: '#e5e7eb' }
            }
        }
    };

    // 资源图表
    const resourceCtx = document.getElementById('resource-chart').getContext('2d');
    resourceChart = new Chart(resourceCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CPU',
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: '内存',
                    data: [],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: chartOptions
    });

    // 网络图表
    const networkCtx = document.getElementById('network-chart').getContext('2d');
    networkChart = new Chart(networkCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: '发送',
                    data: [],
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: '接收',
                    data: [],
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            ...chartOptions,
            scales: {
                ...chartOptions.scales,
                y: {
                    ...chartOptions.scales.y,
                    max: null  // 不限制最大值
                }
            }
        }
    });
}

// 更新图表
function updateCharts(metrics) {
    const timestamp = new Date(metrics.timestamp);

    // 限制数据点数量
    const maxDataPoints = 60;

    // 更新资源图表
    if (resourceChart.data.labels.length > maxDataPoints) {
        resourceChart.data.labels.shift();
        resourceChart.data.datasets[0].data.shift();
        resourceChart.data.datasets[1].data.shift();
    }
    resourceChart.data.labels.push(timestamp);
    resourceChart.data.datasets[0].data.push(metrics.cpu_percent);
    resourceChart.data.datasets[1].data.push(metrics.memory_percent);
    resourceChart.update('none');

    // 更新网络图表
    if (networkChart.data.labels.length > maxDataPoints) {
        networkChart.data.labels.shift();
        networkChart.data.datasets[0].data.shift();
        networkChart.data.datasets[1].data.shift();
    }
    networkChart.data.labels.push(timestamp);
    networkChart.data.datasets[0].data.push(metrics.network_sent_mb);
    networkChart.data.datasets[1].data.push(metrics.network_recv_mb);
    networkChart.update('none');
}

// 渲染Agent列表
function renderAgents() {
    const grid = document.getElementById('agents-grid');
    document.getElementById('agent-count').textContent = `${agents.length} 个Agent`;

    if (agents.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full text-center py-12 text-gray-500">
                <div class="text-4xl mb-4">🤖</div>
                <p>还没有Agent，点击"添加Agent"开始</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = agents.map(agent => createAgentCard(agent)).join('');

    // 更新日志选择器
    const select = document.getElementById('log-agent-select');
    const currentValue = select.value;
    select.innerHTML = '<option value="">选择Agent...</option>' +
        agents.map(a => `<option value="${a.id}" ${a.id === currentValue ? 'selected' : ''}>${a.name}</option>`).join('');
}

// 创建Agent卡片
function createAgentCard(agent) {
    const statusClass = `status-${agent.state}`;
    const uptime = agent.uptime ? formatUptime(Date.now() / 1000 - agent.uptime) : '--';

    return `
        <div class="agent-card bg-gray-800 rounded-lg p-4" data-agent-id="${agent.id}">
            <div class="flex items-start justify-between mb-3">
                <div>
                    <h3 class="font-semibold text-white">${agent.name}</h3>
                    <p class="text-xs text-gray-500">${agent.id}</p>
                </div>
                <span class="status-badge ${statusClass}">${agent.state}</span>
            </div>
            <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                    <span class="text-gray-400">PID:</span>
                    <span class="text-gray-200">${agent.pid || '--'}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">运行时间:</span>
                    <span class="text-gray-200">${uptime}</span>
                </div>
                ${agent.last_error ? `
                    <div class="text-red-400 text-xs truncate" title="${agent.last_error}">
                        ⚠️ ${agent.last_error}
                    </div>
                ` : ''}
            </div>
            <div class="flex gap-2 mt-4 pt-4 border-t border-gray-700">
                ${agent.state === 'running' ? `
                    <button onclick="stopAgent('${agent.id}')" class="flex-1 bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded text-sm">
                        停止
                    </button>
                    <button onclick="restartAgent('${agent.id}')" class="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white px-3 py-1.5 rounded text-sm">
                        重启
                    </button>
                ` : `
                    <button onclick="startAgent('${agent.id}')" class="flex-1 bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded text-sm">
                        启动
                    </button>
                `}
                <button onclick="viewLogs('${agent.id}')" class="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-3 py-1.5 rounded text-sm">
                    日志
                </button>
                <button onclick="deleteAgent('${agent.id}')" class="bg-gray-600 hover:bg-red-600 text-white px-3 py-1.5 rounded text-sm">
                    🗑️
                </button>
            </div>
        </div>
    `;
}

// 更新Agent
function updateAgent(data) {
    const index = agents.findIndex(a => a.id === data.id);
    if (index !== -1) {
        agents[index] = { ...agents[index], ...data };
        renderAgents();
    }
}

// 格式化运行时间
function formatUptime(seconds) {
    if (seconds < 60) return `${Math.floor(seconds)}s`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h`;
    return `${Math.floor(seconds / 86400)}d`;
}

// Agent操作
async function startAgent(id) {
    try {
        await fetch(`/api/agents/${id}/start`, { method: 'POST' });
    } catch (error) {
        console.error('Failed to start agent:', error);
    }
}

async function stopAgent(id) {
    try {
        await fetch(`/api/agents/${id}/stop`, { method: 'POST' });
    } catch (error) {
        console.error('Failed to stop agent:', error);
    }
}

async function restartAgent(id) {
    try {
        await fetch(`/api/agents/${id}/restart`, { method: 'POST' });
    } catch (error) {
        console.error('Failed to restart agent:', error);
    }
}

async function deleteAgent(id) {
    if (!confirm('确定要删除这个Agent吗？')) return;

    try {
        await fetch(`/api/agents/${id}`, { method: 'DELETE' });
        agents = agents.filter(a => a.id !== id);
        renderAgents();
    } catch (error) {
        console.error('Failed to delete agent:', error);
    }
}

// 查看日志
function viewLogs(agentId) {
    selectedAgentId = agentId;
    document.getElementById('log-agent-select').value = agentId;
    loadLogs(agentId);
}

// 加载日志
async function loadLogs(agentId) {
    if (!agentId) {
        document.getElementById('log-viewer').innerHTML =
            '<div class="text-gray-500 text-center py-8">选择一个Agent查看日志</div>';
        return;
    }

    try {
        const response = await fetch(`/api/agents/${agentId}/logs?lines=100`);
        const logs = await response.json();

        const viewer = document.getElementById('log-viewer');
        viewer.innerHTML = logs.map(log => createLogLine(log)).join('');
        viewer.scrollTop = viewer.scrollHeight;
    } catch (error) {
        console.error('Failed to load logs:', error);
    }
}

// 创建日志行
function createLogLine(log) {
    const isErr = log.startsWith('[ERR]');
    const className = isErr ? 'log-err' : 'log-out';
    return `<div class="log-line ${className}">${escapeHtml(log)}</div>`;
}

// 追加日志
function appendLogs(agentId, logs) {
    if (selectedAgentId !== agentId) return;

    const viewer = document.getElementById('log-viewer');
    logs.forEach(log => {
        viewer.innerHTML += createLogLine(log);
    });
    viewer.scrollTop = viewer.scrollHeight;
}

// 清空日志
function clearLogs() {
    document.getElementById('log-viewer').innerHTML = '';
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 模态框
function showAddAgentModal() {
    document.getElementById('add-agent-modal').classList.remove('hidden');
    document.getElementById('add-agent-modal').classList.add('flex');
}

function hideAddAgentModal() {
    document.getElementById('add-agent-modal').classList.add('hidden');
    document.getElementById('add-agent-modal').classList.remove('flex');
    document.getElementById('add-agent-form').reset();
}

// 事件监听
function setupEventListeners() {
    // 添加Agent表单
    document.getElementById('add-agent-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const config = {
            id: document.getElementById('agent-id').value,
            name: document.getElementById('agent-name').value,
            command: document.getElementById('agent-command').value,
            working_dir: document.getElementById('agent-workdir').value || null,
            auto_start: document.getElementById('agent-autostart').checked
        };

        try {
            const response = await fetch('/api/agents', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            });

            if (response.ok) {
                const agent = await response.json();
                agents.push(agent);
                renderAgents();
                hideAddAgentModal();
            }
        } catch (error) {
            console.error('Failed to create agent:', error);
        }
    });

    // 日志选择器
    document.getElementById('log-agent-select').addEventListener('change', (e) => {
        selectedAgentId = e.target.value;
        loadLogs(selectedAgentId);
    });

    // 点击模态框外部关闭
    document.getElementById('add-agent-modal').addEventListener('click', (e) => {
        if (e.target.id === 'add-agent-modal') {
            hideAddAgentModal();
        }
    });
}
