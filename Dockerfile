FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/app

WORKDIR ${WORKDIR}
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "main.py"]
