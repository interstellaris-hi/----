from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import requests

app = FastAPI()

API_KEY = os.getenv("API") or "sk-kkydvwztdbrvxtjsjprrvnwvhfsjvqbfjihxsmklveyzgglh"

@app.get("/api/")
def read_root():
    return {"message": "档案关键词提取助手 API"}

@app.post("/api/extract")
async def extract(request: Request):
    try:
        body = await request.json()
    except:
        body = {}
    text = body.get("text", "").strip()

    if len(text) < 20:
        return JSONResponse({"error": "文本太短，至少需要20个字符"}, status_code=400)

    if not API_KEY:
        return JSONResponse({"error": "服务器未配置 API Key"}, status_code=500)

    try:
        response = requests.post(
            "https://api.siliconflow.cn/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "Qwen/Qwen3-8B",
                "messages": [
                    {"role": "user", "content": f"从以下档案文本中提取3到5个关键词，只返回JSON数组格式，不要其他内容。文本：{text}"}
                ]
            },
            timeout=120
        )
        result = response.json()
        keywords = result["choices"][0]["message"]["content"].strip().strip("```json").strip("```").strip()
        return {"keywords": eval(keywords)}
    except Exception as e:
        return JSONResponse({"error": f"提取失败: {str(e)}"}, status_code=500)