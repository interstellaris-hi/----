# 档案关键词提取助手

基于 Flask + 硅基流动 API 的档案关键词智能提取工具。

## 功能
- 输入档案原文文本
- 一键提取3~5个关键词
- 支持复制结果

## 部署
1. 安装依赖：`pip install -r requirements.txt`
2. 设置环境变量：`export GEMINI_API_KEY=你的密钥`
3. 运行：`gunicorn app:app --bind 0.0.0.0:$PORT`

## 技术栈
- 后端：Flask
- AI：qwen3
- 前端：HTML/CSS/JavaScript
