FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.11-slim
WORKDIR /app
# 安装uv
RUN pip install uv
# 设置版本环境变量（根据您的项目名称调整）
ENV SETUPTOOLS_SCM_PRETEND_VERSION_FOR_GEMINI_WEBAPI=1.0.0
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# 复制项目文件到容器中
COPY . /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=.

# 暴露端口
EXPOSE 8000
# 启动FastAPI服务
CMD ["uvicorn", "src.gemini_webapi.openai_api:app", "--host", "0.0.0.0", "--port", "8000"]
