from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API")
print(f"API Key loaded: {'Yes' if API_KEY else 'No'}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()
    text = data.get("text", "").strip()

    if len(text) < 20:
        return jsonify({"error": "文本太短，至少需要20个字符"}), 400

    if not API_KEY:
        return jsonify({"error": "服务器未配置 API Key"}), 500

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
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.text}")
        result = response.json()
        keywords = result["choices"][0]["message"]["content"].strip().strip("```json").strip("```").strip()
        return jsonify({"keywords": eval(keywords)})
    except Exception as e:
        return jsonify({"error": f"提取失败: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)