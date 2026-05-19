@echo off
chcp 65001 >nul
echo ===== NCU RAG Tutor 启动脚本 =====
echo.

REM 检查Python版本
python --version

REM 检查并创建虚拟环境
if not exist "venv" (
    echo 正在创建虚拟环境...
    python -m venv venv
    echo 虚拟环境创建完成
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt

REM 检查.env文件
if not exist ".env" (
    if exist ".env.test" (
        echo 复制 .env.test 为 .env
        copy .env.test .env
        echo 请编辑 .env 文件，填入您的 API Key
    )
)

echo.
echo ===== 启动服务 =====
echo 访问地址: http://localhost:8000/admin/
echo 健康检查: http://localhost:8000/health
echo.
echo 按 Ctrl+C 停止服务
echo.

python main.py
pause