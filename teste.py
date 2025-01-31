import streamlit as st
import requests

# URL do backend
API_URL = "https://ia.jm2.tec.br/chat"

# Configuração da página
st.set_page_config(page_title="Chat LLM", layout="wide")
st.title("💬 Chatbot com LLM (Streaming)")

# Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
user_input = st.chat_input("Digite sua mensagem:")

if user_input:
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Exibir a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(user_input)

    # Placeholder para resposta do LLM
    response_placeholder = st.empty()
    buffer = ""  # Junta os chunks sem cortar palavras

    # Requisição ao backend
    with requests.post(API_URL, json={"message": user_input}, stream=True) as response:
        response.raise_for_status()  # Verifica erro na requisição

        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                if chunk.startswith("data: "):
                    chunk = chunk[len("data: "):]  # Remover prefixo SSE

                # Garantir que os caracteres sejam exibidos corretamente
                try:
                    chunk = chunk.encode("latin1").decode("utf-8")
                except UnicodeDecodeError:
                    pass  # Evita crash caso não consiga decodificar

                buffer += chunk  # Junta os chunks sem cortar palavras
                print(chunk)
                response_placeholder.markdown(buffer)  # Atualiza em tempo real

    # Adicionar resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": buffer})
