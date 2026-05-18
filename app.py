@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")

    import requests

    payload = {
        "model": "llama3.2",
        "prompt": user_message
    }

    response = requests.post(
        "https://api.ollama.com/v1/chat",
        json=payload
    )

    reply = response.json().get("reply", "لم أستطع فهم الرسالة.")

    return jsonify({"reply": reply})
