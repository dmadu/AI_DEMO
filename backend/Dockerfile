FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .-
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir Flask psycopg2-binary python-dotenv flask-cors

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
