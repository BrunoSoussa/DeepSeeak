import requests
print("Teste")
url = "http://127.0.0.1:5000/chat"
data = {"message": "Explique o conceito de Machine Learning"}

with requests.post(url, json=data, stream=True) as response:
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8").replace("data: ", "")
            print(decoded_line, end="", flush=True)  # Exibir a resposta em tempo real
