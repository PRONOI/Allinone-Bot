# Use Python 3.11.9 slim
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt

# Copy project files
COPY . .

# Expose port for Render Web Service
EXPOSE 8080

# Start FastAPI webhook server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
