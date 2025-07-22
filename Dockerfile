FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create database directory
RUN mkdir -p src/database

# Expose port
EXPOSE 8080

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "src.main:app"]

