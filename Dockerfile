FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV MOCK_MODE=true DISABLE_SCHEDULER=true
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

