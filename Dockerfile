FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.11-slim
WORKDIR /app
# 安装uv
RUN pip install uv uvicorn
# 复制项目配置文件
COPY pyproject.toml ./
# 设置版本环境变量（根据您的项目名称调整）
ENV SETUPTOOLS_SCM_PRETEND_VERSION_FOR_GEMINI_WEBAPI=1.0.0
# 先创建虚拟环境
RUN uv venv

# 复制项目文件
COPY . /app
# 从 pyproject.toml 安装依赖
RUN uv pip install -e .
# 暴露端口
EXPOSE 8000
# 启动FastAPI服务
CMD [".venv/bin/python", "-m", "uvicorn", "src.gemini_webapi.openai_api:app", "--host", "0.0.0.0", "--port", "8000"]
