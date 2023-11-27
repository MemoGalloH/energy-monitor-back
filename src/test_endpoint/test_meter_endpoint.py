import requests

monitor_id = "796b2cc2-b848-4e16-bf17-ff506b5d0602"

url = f"https://vu5h0yvf80.execute-api.us-west-2.amazonaws.com/monitor/{monitor_id}"

body = {
    "clientId": "1053779590",
    "groupId": "74f9ae48-36ce-4b4e-bdd3-3899fa886b02",
    "data": [20.5, 120.34, 117.28, 121.43, 300.33, 304.33],
}

response = requests.post(url, json=body)

print(response.status_code, response.text)
