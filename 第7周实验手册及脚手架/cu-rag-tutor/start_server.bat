@echo off
chcp 65001 >nul
set SILICONFLOW_API_KEY=sk-kkydvwztdbrvxtjsjprrvnwvhfsjvqbfjihxsmklveyzgglh
python -m uvicorn main:app --host 127.0.0.1 --port 8000
pause