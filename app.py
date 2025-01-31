from flask import Flask, Response, request
import ollama
import logging

app = Flask(__name__)

# Configuração do logger para depuração
logging.basicConfig(level=logging.INFO)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    app.logger.info(f"Recebida mensagem: {user_message}")

    def generate():
        try:
            response = ollama.chat(
                model="deepseek-coder:latest",
                messages=[{"role": "user", "content": user_message}],
                stream=True, 
            )
            for message in response:
                if "message" in message and "content" in message["message"]:
                    yield f"{message['message']['content']}\n\n"  # Adicionando \n\n corretamente
                else:
                    app.logger.warning(f"Resposta inválida: {message}")
        except Exception as e:
            app.logger.error(f"Erro no streaming: {str(e)}")
            yield f"Erro interno no servidor\n\n"
    return Response(generate(), content_type="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
