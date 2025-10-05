ARG BASE_IMAGE="python:3.13-slim"

FROM ${BASE_IMAGE}

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir uv && uv pip install --no-cache-dir -r requirements.txt
COPY src/titanic_classification/ .
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
CMD ["python", "-m", "titanic_classification"]
