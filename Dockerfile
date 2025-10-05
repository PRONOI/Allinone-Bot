# Use Python 3.11.9
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt

# Copy all project files
COPY . .

# (Optional) expose port — harmless for workers
EXPOSE 8080

# Start your Telegram bot
CMD ["python", "-m", "src.main"]
