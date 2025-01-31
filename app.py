from flask import Flask, Response, request, jsonify
import ollama
import logging

app = Flask(__name__)

# Configuração do logger para depuração
logging.basicConfig(level=logging.INFO)

@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint para comunicação com o modelo deepseek-coder-v2 via streaming"""
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Mensagem vazia"}), 400

    app.logger.info(f"Mensagem recebida: {user_message}")

    def generate():
        try:
            response = ollama.chat(
                model="deepseek-coder-v2",
                messages=[{"role": "user", "content": user_message}],
                stream=True, 
            )
            for message in response:
                if "message" in message and "content" in message["message"]:
                    formatted_response = message["message"]["content"]
                    yield f"data: {formatted_response} \n\n"  # Adiciona um espaço no final para evitar palavras grudadas
                else:
                    app.logger.warning(f"Resposta inválida: {message}")
        except Exception as e:
            app.logger.error(f"Erro no streaming: {str(e)}")
            yield f"data: Erro interno no servidor\n\n"

    return Response(generate(), content_type="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
