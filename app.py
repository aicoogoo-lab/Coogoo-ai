from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")

    # إرسال الرسالة إلى ذكاء مفتوح المصدر (Llama 3.2)
    payload = {
        "model": "llama3.2",
        "prompt": user_message
    }

    response = requests.post(
        "https://api.ollama.com/v1/chat",
        json=payload
    )

    # استخراج الرد
    reply = response.json().get("reply", "لم أستطع فهم الرسالة.")

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
