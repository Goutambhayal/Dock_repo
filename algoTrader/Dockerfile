FROM python:3.10-slim

# 1️⃣ WORKDIR = folder containing manage.py
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*


# 3️⃣ Copy and install python deps first (cache-friendly)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Copy EVERYTHING into /app
COPY . .

# 5️⃣ Make project importable
ENV PYTHONPATH=/app
# 7. Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]