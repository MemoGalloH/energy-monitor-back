import requests

monitor_id = 1234

url = f"https://ymx56gmarf.execute-api.us-west-2.amazonaws.com/monitor/{monitor_id}"

body = {"Hi": "Hola"}

response = requests.post(url, json=body)

print(response.status_code, response.text)
