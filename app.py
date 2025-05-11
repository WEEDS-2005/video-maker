from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import tempfile

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
        # Create a temporary file for download
        tmp_dir = tempfile.mkdtemp()
        filename = "download.mp4" if media_type == "video" else "download.mp3"
        filepath = os.path.join(tmp_dir, filename)

        ydl_opts = {
            "outtmpl": filepath,  # Save to the temporary directory
            "format": "bestvideo+bestaudio/best",
            "retries": 5,
            "socket_timeout": 30,
            "http_chunk_size": 10485760  # 10MB chunks
        }

        if media_type == "audio":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send the file to the user and remove the file afterward
        response = send_file(filepath, as_attachment=True)
        os.remove(filepath)  # Clean up the temporary file
        os.rmdir(tmp_dir)    # Remove the temporary directory

        return response
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
