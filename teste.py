import requests

print("Teste")

url = "https://ia.jm2.tec.br/chat"
data = {"message": "gere uma classe em python que calcula o fatorial de um número"}

with requests.post(url, json=data, stream=True) as response:
    inside_code_block = False  # Flag para controlar se estamos dentro de um bloco de código
    
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8").replace("data: ", "").strip()

            # Se encontrar um marcador de código ```python ou ```, indica que um bloco de código começou ou terminou
            if decoded_line.startswith("```"):
                if inside_code_block:
                    print("\n" + decoded_line + "\n")  # Finaliza o bloco de código corretamente
                    inside_code_block = False
                else:
                    print("\n" + decoded_line)  # Inicia o bloco de código com uma quebra de linha
                    inside_code_block = True
            else:
                # Se estiver dentro de um bloco de código, mantém a indentação correta
                if inside_code_block:
                    print("    " + decoded_line)  # Mantém indentação para evitar blocos quebrados
                else:
                    print("\n" + decoded_line, end="\n\n", flush=True)  # Adiciona espaçamento correto entre parágrafos
