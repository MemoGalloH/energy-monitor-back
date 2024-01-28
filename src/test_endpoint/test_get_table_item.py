import requests

clientId = "1053779590"
# "client" "74f9ae48-36ce-4b4e-bdd3-3899fa886b02"  "74f9ae48-36ce-4b4e-bdd3-3899fa886b02.796b2cc2-b848-4e16-bf17-ff506b5d0602"
clientGroupMonitorId = (
    "74f9ae48-36ce-4b4e-bdd3-3899fa886b02.796b2cc2-b848-4e16-bf17-ff506b5d0602"
)

# f"https://vu5h0yvf80.execute-api.us-west-2.amazonaws.com/client/{clientId}/{clientGroupMonitorId}?fd=2024-01-01&ld=2024-12-31"

url = f"https://vu5h0yvf80.execute-api.us-west-2.amazonaws.com/client/{clientId}/{clientGroupMonitorId}?fd=2024-01-01&ld=2024-12-31"

response = requests.get(url)

print(response.status_code, response.text, response.headers)
