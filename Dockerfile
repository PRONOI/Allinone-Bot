# Use official Python slim image
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK punkt if needed
RUN python -m nltk.downloader punkt

# Copy the entire src folder
COPY src/ ./src

# Expose port for Render
EXPOSE 8080

# Start bot
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
