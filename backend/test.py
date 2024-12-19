import requests

url = "http://127.0.0.1:5000/executar_algoritmos"
data = {
    "tabuleiro": [
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ]
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)