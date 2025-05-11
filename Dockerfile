FROM python:3.10-slim

# Install FFmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install flask yt-dlp

WORKDIR /app
COPY . .

CMD ["python", "app.py"]
