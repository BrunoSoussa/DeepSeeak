import streamlit as st
import requests
import re

# URL do backend Flask que executa seu LLM
API_URL = "https://ia.jm2.tec.br/chat"

st.set_page_config(page_title="Chatbot LLM", layout="wide")
st.title("💬 Chatbot LLM com Streaming")

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de conversas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "```python" in msg["content"]:  # Se for código Python, exibir em destaque
            code_content = re.search(r"```python(.*?)```", msg["content"], re.DOTALL)
            if code_content:
                st.code(code_content.group(1), language="python")
        else:
            st.markdown(msg["content"])

# Entrada do usuário
user_input = st.chat_input("Digite sua mensagem:")

if user_input:
    # Adicionar a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Exibir a mensagem do usuário na interface
    with st.chat_message("user"):
        st.markdown(user_input)

    # Criar um placeholder para exibir a resposta do LLM
    response_placeholder = st.empty()
    full_response = ""

    # Fazer requisição ao backend com streaming
    with requests.post(API_URL, json={"message": user_input}, stream=True) as response:
        response.raise_for_status()  # Verifica erro na requisição

        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                

                # Garante que a codificação está correta (UTF-8)
                try:
                    chunk = chunk.encode("latin1").decode("utf-8")
                except UnicodeDecodeError:
                    pass  # Ignora caso falhe a conversão

                # Adiciona quebra de linha para exibição correta
                full_response += chunk + "\n\n"

                # Atualiza a interface com a resposta formatada
                response_placeholder.markdown(full_response)

    # Se houver código na resposta, exibir corretamente
    with st.chat_message("assistant"):
        if "```python" in full_response:
            code_content = re.search(r"```python(.*?)```", full_response, re.DOTALL)
            if code_content:
                st.code(code_content.group(1), language="python")
        else:
            st.markdown(full_response)

    # Adicionar resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
