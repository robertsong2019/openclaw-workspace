#!/bin/bash
# Mini-MCP 演示脚本

echo "🧪 Mini-MCP 工具演示"
echo "===================="
echo ""

echo "1️⃣  获取当前时间（上海时区）"
python3 /root/.openclaw/workspace/code-lab/mini-mcp/mini_mcp.py --call time
echo ""

echo "2️⃣  数学计算：sin(π/4) × 2 + √16"
python3 /root/.openclaw/workspace/code-lab/mini-mcp/mini_mcp.py --call calc '{"expr": "sin(pi/4) * 2 + sqrt(16)"}'
echo ""

echo "3️⃣  生成 5 个随机颜色（带亮度值）"
python3 /root/.openclaw/workspace/code-lab/mini-mcp/mini_mcp.py --call color '{"count": 5}'
echo ""

echo "4️⃣  SHA256 哈希生成"
python3 /root/.openclaw/workspace/code-lab/mini-mcp/mini_mcp.py --call hash '{"text": "Hello AI Agent!", "algorithm": "sha256"}'
echo ""

echo "5️⃣  统计计算（斐波那契数列前10项）"
python3 /root/.openclaw/workspace/code-lab/mini-mcp/mini_mcp.py --call stats '{"numbers": [0,1,1,2,3,5,8,13,21,34]}'
echo ""

echo "6️⃣  JSON 格式化"
python3 /root/.openclaw/workspace/code-lab/mini-mcp/mini_mcp.py --call json_fmt '{"json_str": "{\"project\":\"mini-mcp\",\"lines\":150,\"tools\":7}"}'
echo ""

echo "7️⃣  Base64 编码"
python3 /root/.openclaw/workspace/code-lab/mini-mcp/mini_mcp.py --call base64 '{"text": "Mini-MCP is awesome!", "mode": "encode"}'
echo ""

echo "✅ 演示完成！"
echo ""
echo "💡 提示：运行 'python3 mini_mcp.py' 进入交互模式"
