# Use a lightweight Python 3.14 image as the base image.
FROM python:3.14-slim

# Set the working directory inside the Docker container.
WORKDIR /app

# Prevent Python from creating .pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Send Python output directly to the container logs.
ENV PYTHONUNBUFFERED=1

# Install system packages required to build mysqlclient
# and connect Django to the MariaDB/MySQL database.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python dependency list into the container.
COPY requirements.txt .

# Install all Python packages required by the NewsHub application.
# --no-cache-dir keeps the Docker image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container.
COPY . .

# Document that the Django development server uses port 8000.
EXPOSE 8000

# Start the Django development server when the container starts.
# 0.0.0.0 allows the application to be accessed from outside
# the container.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]