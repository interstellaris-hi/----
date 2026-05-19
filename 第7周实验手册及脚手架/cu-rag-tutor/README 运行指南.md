# NCU RAG Tutor — 智能伴读助手运行指南

## 一、项目概述

### 1.1 项目背景

南昌大学智慧课程平台 - 零幻觉企业微信课后伴学助教专属代理。基于RAG（检索增强生成）技术的智能问答系统，可上传课件、讲义、手册等文档，向系统提问时会**严格基于上传的文档内容**回答，不会编造答案。

### 1.2 核心功能

- 文档上传与管理
- 混合检索（BM25 + ChromaDB向量检索）
- 交叉精排（Qwen3-Reranker）
- 大模型生成回答
- 企业微信回调集成
- 管理员后台

---

## 二、系统架构

### 2.1 技术栈

| 层级 | 技术选型 |
|-----|---------|
| Web框架 | FastAPI + Uvicorn |
| 前端 | 静态HTML + JavaScript |
| 检索增强 | LangChain + LangGraph |
| 向量数据库 | ChromaDB |
| 关键字检索 | BM25 |
| 大模型 | Qwen3.5-35B-A3B (SiliconFlow) |
| 向量化模型 | Qwen3-Embedding-8B |
| 重排序模型 | Qwen3-Reranker-8B |

### 2.2 架构流程

```
用户提问 → 混合检索（BM25 关键字 + ChromaDB 向量）→ 交叉精排（Qwen3-Reranker）→ 大模型生成回答
```

---

## 三、快速启动

### 3.1 环境要求

- Python 3.10+
- SiliconFlow API Key

### 3.2 启动步骤

```bash
# 1. 进入项目目录
cd cu-rag-tutor

# 2. 创建并激活虚拟环境
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python main.py
```

### 3.3 访问地址

- 管理后台: http://localhost:8000/admin/
- 考试中心: http://localhost:8000/exam
- 健康检查: http://localhost:8000/health

---

## 四、预设问题与答案

### 4.1 系统操作类

**Q1: 如何上传文档？**
A: 在管理后台找到「上传文档」按钮，选择Markdown文件上传，点击「入库」按钮等待完成。

**Q2: 如何清空知识库？**
A: 删除 `data/chroma` 文件夹，然后重启服务：
```bash
rm -rf data/chroma
python main.py
```

**Q3: 端口被占用怎么办？**
A: 关闭占用端口的程序，或修改main.py中的端口号。

### 4.2 技术原理类

**Q4: 什么是RAG技术？**
A: RAG（检索增强生成）是一种结合检索系统和生成模型的技术。系统先从知识库中检索相关文档，再将检索结果提供给大模型生成回答，确保回答基于真实文档而非编造。

**Q5: 什么是混合检索？**
A: 混合检索同时使用BM25关键字匹配和向量语义匹配两种方法：
- BM25: 适合精确关键词匹配
- 向量检索: 适合语义相似度匹配
两者结合可提高召回率和准确性。

**Q6: 什么是重排序（Reranker）？**
A: 重排序模型对初步检索结果进行二次排序，筛选出最相关的内容送入大模型，减少无关信息干扰。

### 4.3 使用场景类

**Q7: 上传文档后为什么回答还是说"不知道"？**
A: 请确认已完成「入库」操作，入库过程会将文档切片并存入知识库。

**Q8: 首次提问响应很慢怎么办？**
A: 首次提问需要初始化向量数据库，可能需要10-20秒。后续提问会快很多。

---

## 五、API接口

### 5.1 管理员接口 `/api/v1/admin`

| 方法 | 路径 | 功能 |
|-----|------|-----|
| POST | /upload | 上传文档 |
| POST | /ingest | 入库文档 |
| GET | /files | 获取文件列表 |
| DELETE | /files/{id} | 删除文件 |

### 5.2 企业微信回调 `/api/v1/wecom`

| 方法 | 路径 | 功能 |
|-----|------|-----|
| POST | /callback | 微信消息回调 |
| GET | /callback | 验证回调 |

### 5.3 健康检查

- GET /health - 返回系统健康状态、LLM目标地址、RAG持久化目录

---

## 六、常见问题

### 6.1 启动问题

**Q: 启动报错 `ModuleNotFoundError`？**
A: 确认已激活虚拟环境（终端提示符前有 `(venv)` 字样），执行 `pip install -r requirements.txt`。

**Q: 看到黄色警告正常吗？**
A: 是的，`LangChainDeprecationWarning` 和 `BM25 索引跳过` 提示是正常的，不影响使用。

### 6.2 使用问题

**Q: 回答内容不准确？**
A: 检查文档内容是否清晰，尝试调整文档格式或重新入库。

**Q: API调用失败？**
A: 检查 `.env` 文件中的 API Key 是否正确，确保网络能访问 SiliconFlow。

---

## 七、文件结构

```
cu-rag-tutor/
├── main.py              # 主入口
├── ingest.py           # 文档导入脚本
├── query.py            # 查询脚本
├── requirements.txt    # 依赖列表
├── .env                # 环境配置
├── app/
│   ├── api/            # API路由
│   │   ├── admin.py    # 管理员接口
│   │   ├── webhook.py  # 企业微信回调
│   │   └── auth.py     # 认证接口
│   ├── core/
│   │   └── config.py   # 配置管理
│   ├── services/
│   │   └── rag_engine.py  # RAG引擎
│   └── static/         # 静态文件
└── data/
    ├── chroma/         # 向量数据库
    └── documents/     # 原始文档
```

---

## 八、安全配置

### 8.1 网关鉴权

系统配置了网关来源拦截鉴权，防止公网非法访问。有效IP段：
- 127.0.0.1 / localhost（本地）
- 172.*（Docker虚拟网桥）
- 192.168.8.*（家网，排除192.168.8.88）

### 8.2 缓存控制

管理后台和HTML页面强制不缓存，确保用户获取最新内容。

---

## 九、扩展开发

### 9.1 添加新模型

在 `.env` 中修改模型名称：
```
LLM_MODEL_NAME=your_model_name
```

### 9.2 自定义文档解析

在 `ingest.py` 中添加新的文档处理逻辑。

### 9.3 前端定制

修改 `app/static/` 目录下的HTML和JS文件。

---

## 十、版本信息

- 当前版本: 1.1.0
- 更新日期: 2026年
- 技术支持: 南昌大学智慧课程平台