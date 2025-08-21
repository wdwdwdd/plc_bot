FROM python:3.9-slim

WORKDIR /app/backend

# Install backend-specific dependencies
COPY requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy backend source
COPY . /app/backend

ENV CONFIG_PATH=/app/config/settings.yaml

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
