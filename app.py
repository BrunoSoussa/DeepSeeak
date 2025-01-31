from flask import Flask, Response, request
import ollama

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    def generate():
        response = ollama.chat(
            model="deepseek-coder-v2",
            messages=[{"role": "user", "content": user_message}],
            stream=True, 
        )
        for message in response:
            yield f"data: {message['message']['content']}\n\n"

    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
