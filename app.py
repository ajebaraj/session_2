from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Uploads configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

# File upload
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    size_bytes = os.path.getsize(filepath)
    size_str = (
        f"{size_bytes} B" if size_bytes < 1024
        else f"{size_bytes/1024:.1f} KB" if size_bytes < 1024*1024
        else f"{size_bytes/(1024*1024):.1f} MB"
    )

    return jsonify({
        "message": "File uploaded successfully!",
        "filename": filename,
        "size": size_str,
        "size_bytes": size_bytes,
        "type": file.mimetype or "application/octet-stream"
    })

# Serve uploaded files (for preview)
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
