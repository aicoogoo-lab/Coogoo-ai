from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")

    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://api.ollama.com/v1/chat",
        json=payload
    )

    data = response.json()

    # محاولة استخراج الرد من عدة أماكن محتملة
    reply = None

    # 1) بعض واجهات Ollama ترجع: data["message"]["content"]
    if isinstance(data.get("message"), dict):
        reply = data["message"].get("content")

    # 2) بعض النسخ ترجع: data["messages"][0]["content"]
    if not reply and isinstance(data.get("messages"), list):
        if len(data["messages"]) > 0:
            reply = data["messages"][0].get("content")

    # 3) بعض النسخ ترجع: data["response"]
    if not reply:
        reply = data.get("response")

    # 4) لو ما حصلنا أي رد
    if not reply:
        reply = "لم أستطع فهم الرسالة."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
