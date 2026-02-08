#!/bin/bash

# 开发环境启动脚本

echo "🔧 启动开发环境..."

# 启动后端
echo "📦 启动后端..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
python run.py &
BACKEND_PID=$!
cd ..

# 启动前端
echo "🎨 启动前端..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "安装 npm 依赖..."
    npm install
fi
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ 开发环境启动完成！"
echo ""
echo "📝 访问地址："
echo "  前端: http://localhost:5173"
echo "  后端: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待中断信号
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
