FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn requests pytest

EXPOSE 8000

CMD ["uvicorn", "fastApi:app", "--host", "0.0.0.0", "--port", "8000"]