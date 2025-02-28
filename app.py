from flask import Flask, Response, request, jsonify, render_template, session
import ollama
import logging
import json

app = Flask(__name__)
app.secret_key = 'deep_seeak_secret_key'

# Configuração do logger para depuração
logging.basicConfig(level=logging.INFO)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        message_history = data.get("history", [])
        model_name = data.get("model", "deepseek-coder-v2:16b")
        
        # Validação do modelo
        allowed_models = ["deepseek-coder-v2:16b", "deepseek-r1:14b", "deepseek-coder:latest"]
        if model_name not in allowed_models:
            app.logger.warning(f"Modelo inválido: {model_name}, usando padrão")
            model_name = "deepseek-coder-v2:16b"

        if not user_message:
            return jsonify({"error": "Mensagem vazia"}), 400

        # Garante que o histórico está no formato correto
        formatted_history = []
        for msg in message_history:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                formatted_history.append({
                    'role': msg['role'],
                    'content': msg['content']
                })

        app.logger.info(f"Mensagem recebida: {user_message}")
        app.logger.info(f"Modelo selecionado: {model_name}")
        app.logger.info(f"Histórico formatado: {json.dumps(formatted_history, indent=2)}")

        def generate():
            try:
                # Adiciona a mensagem atual ao histórico
                current_messages = formatted_history + [{"role": "user", "content": user_message}]
                
                app.logger.info(f"Enviando para o modelo: {json.dumps(current_messages, indent=2)}")
                
                response = ollama.chat(
                    model=model_name,
                    messages=current_messages,
                    stream=True,
                )

                for message in response:
                    if "message" in message and "content" in message["message"]:
                        yield message["message"]["content"]
                    else:
                        app.logger.warning(f"Resposta inválida: {message}")
            except Exception as e:
                app.logger.error(f"Erro no streaming: {str(e)}")
                yield f"Erro interno no servidor: {str(e)}"

        return Response(generate(), content_type="text/event-stream")
    except Exception as e:
        app.logger.error(f"Erro geral: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return render_template('chat.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
