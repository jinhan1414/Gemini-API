FROM python:3.11-slim
WORKDIR /app
# 安装uv
RUN pip install uv uvicorn
# 复制项目配置文件
COPY pyproject.toml uv.lock ./
# 只安装依赖，不安装项目本身
RUN uv sync --frozen --no-dev --no-install-project
# 复制项目文件
COPY . /app
# 暴露端口
EXPOSE 8000
# 启动FastAPI服务
CMD ["uv", "run", "uvicorn", "src.gemini_webapi.openai_api:app", "--host", "0.0.0.0", "--port", "8000"]
