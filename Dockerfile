FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure data directory exists for SQLite
RUN mkdir -p /app/data

EXPOSE 7070

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7070"]
