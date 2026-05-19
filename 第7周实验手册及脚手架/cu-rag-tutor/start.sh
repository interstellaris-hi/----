#!/bin/bash
# NCU RAG Tutor 快速启动脚本

echo "===== NCU RAG Tutor 启动脚本 ====="
echo ""

# 检查Python版本
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "检测到 Python 版本: $python_version"

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python -m venv venv
    echo "虚拟环境创建完成"
fi

# 激活虚拟环境
echo "正在激活虚拟环境..."
source venv/bin/activate  # Linux/Mac
# Windows: call venv\Scripts\activate.bat

# 安装依赖
echo "正在安装依赖..."
pip install -r requirements.txt

# 检查.env文件
if [ ! -f ".env" ]; then
    if [ -f ".env.test" ]; then
        echo "复制 .env.test 为 .env"
        cp .env.test .env
        echo "请编辑 .env 文件，填入您的 API Key"
    else
        echo "警告: 未找到 .env 或 .env.test 文件"
    fi
fi

# 检查端口是否被占用
PORT=8000
if command -v lsof &> /dev/null; then
    if lsof -i :$PORT &> /dev/null; then
        echo "警告: 端口 $PORT 已被占用"
    fi
fi

echo ""
echo "===== 启动服务 ====="
echo "访问地址: http://localhost:$PORT/admin/"
echo "健康检查: http://localhost:$PORT/health"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python main.py