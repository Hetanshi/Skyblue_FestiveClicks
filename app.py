from flask import Flask, render_template, request
import base64, os
from datetime import datetime

app = Flask(__name__)

# Home route - show camera page
@app.route('/')
def index():
    return render_template('index.html')

# Save photo route
@app.route('/save_photo', methods=['POST'])
def save_photo():
    try:
        img_data = request.form['image'].split(",")[1]
        img_bytes = base64.b64decode(img_data)

        # Create static/photos folder if not exists
        photos_path = os.path.join(app.static_folder, "photos")
        os.makedirs(photos_path, exist_ok=True)

        # Save with timestamp filename
        filename = datetime.now().strftime("photo_%Y%m%d_%H%M%S.png")
        filepath = os.path.join(photos_path, filename)

        with open(filepath, "wb") as f:
            f.write(img_bytes)

        return f"Saved as {filename}"
    except Exception as e:
        return f"Error: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)