from flask import Flask, render_template, request, send_from_directory, make_response, redirect
import base64, os

app = Flask(__name__)

# Add ngrok header to all responses
@app.after_request
def after_request(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

# Add a route that sets custom User-Agent to bypass ngrok warning
@app.before_request
def before_request():
    # This won't help with the initial warning page, but helps with subsequent requests
    pass

# Alternative route to bypass ngrok warning
@app.route("/ngrok-skip-browser-warning")
def skip_warning():
    return redirect("/")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save_photo", methods=["POST"])
def save_photo():
    try:
        data = request.form["image"]  # get base64 string
        header, encoded = data.split(",", 1)
        binary = base64.b64decode(encoded)

        # Make sure folder exists
        if not os.path.exists("static/captures"):
            os.makedirs("static/captures")

        filepath = os.path.join("static/captures", "captured.png")
        with open(filepath, "wb") as f:
            f.write(binary)

        return "Saved at " + filepath
    except Exception as e:
        return f"Error: {str(e)}", 400

@app.route("/frame")
def frame():
    return send_from_directory("static", "navratri_frame.png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)

