from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    media_type = data.get("media", "video")

    try:
        filename = "download.mp4" if media_type == "video" else "download.mp3"

        ydl_opts = {
            "outtmpl": filename,
            "format": "bestvideo+bestaudio/best",
            "retries": 5,
            "socket_timeout": 30,
            "http_chunk_size": 10485760  # 10MB chunks, may avoid range issues
        }



        if media_type == "audio":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
