# 1. Use an official Python image
FROM python:3.10-slim

# 2. Set environment variables (prevents Python from buffering output)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory inside the container
WORKDIR /ALGO_TRADER

# 4. Install system dependencies (Required for MySQL and Celery)

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt /ALGO_TRADER/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your project code
COPY . /ALGO_TRADER/

# 7. Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]