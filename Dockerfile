FROM python:3.11-slim

WORKDIR /app

# Install dependencies early to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m nltk.downloader punkt

# Copy rest of the source
COPY . .

# Expose ports (Webhook + Health check)
EXPOSE 8443 8080

# Start the bot
CMD ["python", "-m", "src.main"]
