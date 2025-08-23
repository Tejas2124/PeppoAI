from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os, time, jwt
from google import genai
from google.genai import types
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import  load_dotenv
load_dotenv()
# ---------------- CONFIG ----------------
VIDEO_DIR = "generated_videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

SECRET = "yoursecretkey"
users = {}  # replace with your actual DB in production
app = Flask(__name__, template_folder="templates")
CORS(app)

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

# ---------------- ROUTES: PAGES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/profile")
def profile_page():
    return render_template("profile.html")

# ---------------- AUTH ROUTES ----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    users[username] = {"password": password, "api_key": None}
    return jsonify({"message": "Signup successful"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users:
        return jsonify({"error": "user does not exist"}), 401
    if users[username]["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {"username": username, "time": time.time()},
        SECRET,
        algorithm="HS256"
    )
    return jsonify({"token": token})


@app.route("/set-key", methods=["POST"])
def set_key():
    data = request.json
    token = data["token"]
    api_key = data["api_key"]

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        username = decoded["username"]
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    users[username]["api_key"] = api_key
    return jsonify({"message": "API key saved"}), 200

# ---------------- VIDEO GENERATION ----------------
@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.json
    token = data["token"]
    prompt = data["prompt"]

    # Validate token
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        username = decoded["username"]
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    api_key = users.get(username, {}).get("api_key")
    if not api_key:
        return jsonify({"error": "No API key set"}), 400

    client = genai.Client(api_key=api_key)
    model_name = "veo-3.0-generate-preview"

    operation = client.models.generate_videos(
        model=model_name,
        prompt=prompt,
    )
    operation = types.GenerateVideosOperation(name=operation.name)

    while not operation.done:
        time.sleep(20)
        operation = client.operations.get(operation)

    generated_video = operation.response.generated_videos[0]
    filename = f"{username}_{int(time.time())}.mp4"
    filepath = os.path.join(VIDEO_DIR, filename)

    generated_video.video.save(filepath)
    client.files.download(file=generated_video.video)

    return jsonify({"video_url": f"/videos/{filename}"})


# ---------------- PROFILE ----------------
@app.route("/profile-info", methods=["POST"])
def profile_info():
    data = request.json
    token = data.get("token")

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        username = decoded["username"]
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    user = users.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.get("username", "Unknown"),
        "email": user.get("email", "N/A")
    })

# ---------------- FILES ----------------
@app.route("/videos/<filename>")
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename)

# ---------------- GOOGLE LOGIN ----------------
@app.route("/google-login", methods=["POST"])
def google_login():
    data = request.json
    token = data.get("id_token")

    try:
        # Verify token with Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        userid = idinfo["sub"]  # Google unique ID
        email = idinfo.get("email")
        name = idinfo.get("name", "User")

        # Save user if new
        if userid not in users:
            users[userid] = {
                "username": name,
                "email": email,
                "api_key": None
            }

        # Create JWT for session
        jwt_token = jwt.encode(
            {"username": userid, "time": time.time()},
            SECRET,
            algorithm="HS256"
        )

        return jsonify({"token": jwt_token})
    except Exception as e:
        return jsonify({"error": f"Invalid Google token: {str(e)}"}), 401


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=False)
