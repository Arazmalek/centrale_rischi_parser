# Use a Python base image optimized for Slim for smaller size
FROM python:3.10-slim

# Prevents Python from writing pyc files and buffering (Best Practices)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirement files first for better Docker caching
COPY requirements.txt /app/

# Install dependencies (using --no-cache-dir for clean layer size)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (Source Structure: api, core, storage)
COPY src /app/src

# Expose the port that the application listens on.
EXPOSE 5000

# Run your Python script using Gunicorn
# CMD refers to app:app inside the src/api folder
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "1800", "--access-logfile", "-", "--error-logfile", "-", "src.api.app:app"]
