# app.py
from flask import Flask, render_template, request
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Ensure folder exists
SAVE_FOLDER = os.path.join(app.static_folder, "captures")
os.makedirs(SAVE_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save_photo", methods=["POST"])
def save_photo():
    img_data = request.form.get("image")
    if not img_data:
        return "No image received", 400

    try:
        img_data = img_data.split(",")[1]
        image_bytes = base64.b64decode(img_data)

        filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(SAVE_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return f"Saved as {filename}"
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    # Use PORT env var provided by Render (or default 5000 locally)
    port = int(os.environ.get("PORT", 5002))
    # Bind to 0.0.0.0 so Render can reach the container
    app.run(host="0.0.0.0", port=port, debug=False)
