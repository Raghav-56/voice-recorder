from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from src import utils
import datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save-recording", methods=["POST"])
def save_recording():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    utils.ensure_recordings_directory_exists()
    filename = utils.generate_filename()
    file_path = os.path.join("recordings", filename)
    audio_file.save(file_path)

    return jsonify({"success": True, "filename": filename})


@app.route("/recordings", methods=["GET"])
def list_recordings():
    recordings = utils.list_recordings()
    return jsonify({"recordings": recordings})


@app.route("/recordings/<filename>", methods=["GET"])
def serve_recording(filename):
    return send_from_directory("recordings", filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
