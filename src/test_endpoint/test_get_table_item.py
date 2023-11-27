import requests

clientId = "1053779590"
# "client" "74f9ae48-36ce-4b4e-bdd3-3899fa886b02"  "74f9ae48-36ce-4b4e-bdd3-3899fa886b02.796b2cc2-b848-4e16-bf17-ff506b5d0602"
clientGroupMonitorId = "client"

url = f"https://vu5h0yvf80.execute-api.us-west-2.amazonaws.com/client/{clientId}/{clientGroupMonitorId}"

response = requests.get(url)

print(response.status_code, response.text, response.headers)
