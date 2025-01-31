import requests
print("Teste")
url = "https://ia.jm2.tec.br//chat"
data = {"message": ""}

with requests.post(url, json=data, stream=True) as response:
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8").replace("data: ", "")
            print(decoded_line, end="", flush=True) 
