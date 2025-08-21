FROM python:3.9-slim

WORKDIR /app/collector

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

COPY . /app/collector

ENV CONFIG_PATH=/app/config/devices.yaml

CMD ["python", "main.py"]

