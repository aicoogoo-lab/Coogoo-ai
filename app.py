from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")
    response = f"استلمت رسالتك: {user_message}"
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
