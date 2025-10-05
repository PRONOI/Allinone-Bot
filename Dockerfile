# Use Python 3.11.9 slim
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt

# Copy all project files
COPY . .

# Expose port for Render web service
EXPOSE 8080

# Start the FastAPI webhook server using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
