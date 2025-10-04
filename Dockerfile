FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
COPY . .
EXPOSE 8443 8080
CMD ["python", "-m", "src.main"]
