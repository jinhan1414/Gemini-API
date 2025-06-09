FROM python:3.11-slim

WORKDIR /app

# 安装uv
RUN pip install uv uvicorn

# 复制项目文件
COPY . /app

# 安装依赖
RUN uv pip install --system --no-cache-dir -r /app/uv.lock || true

# 暴露端口
EXPOSE 8000

# 可通过docker run -e SECURE_1PSID=xxx -e SECURE_1PSIDTS=xxx 传递环境变量
# 或在此处取消注释并填写默认值：
# ENV SECURE_1PSID="your_psid" SECURE_1PSIDTS="your_psidts"

# 启动FastAPI服务
CMD ["uvicorn", "src.gemini_webapi.openai_api:app", "--host", "0.0.0.0", "--port", "8000"] 