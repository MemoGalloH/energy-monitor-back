import requests

monitor_id = "796b2cc2-b848-4e16-bf17-ff506b5d0602"

url = f"https://ymx56gmarf.execute-api.us-west-2.amazonaws.com/monitor/{monitor_id}"

body = {"clientId": "1053779590", "groupId": "74f9ae48-36ce-4b4e-bdd3-3899fa886b02"}

response = requests.post(url, json=body)

print(response.status_code, response.text)
