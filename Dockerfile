FROM python:3.13-slim AS builder
RUN pip install uv
WORKDIR /app
COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --frozen

FROM python:3.13-slim
RUN pip install uv
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY main.py ./
EXPOSE 8081
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
