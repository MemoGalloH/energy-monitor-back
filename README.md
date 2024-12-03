# Monitor Endpoint

## URL
`POST https://vu5h0yvf80.execute-api.us-west-2.amazonaws.com/monitor/{monitor_id}`

## Path Parameters
- `monitor_id` (string): The unique identifier for the monitor.

## Request Body
The request body should be a JSON object with the following structure:

```json
{
    "clientId": "string",
    "groupId": "string",
    "data": [number]
}
```
# Get Table Item Endpoint

## URL
`GET https://vu5h0yvf80.execute-api.us-west-2.amazonaws.com/client/{clientId}/{clientGroupMonitorId}`

## Path Parameters
- `clientId` (string): The unique identifier for the client.
- `clientGroupMonitorId` (string): The combined identifier for the client group and monitor.

## Query Parameters
- `fd` (string): The start date in `YYYY-MM-DD` format.
- `ld` (string): The end date in `YYYY-MM-DD` format.

## Example Request
```python
import requests

clientId = "1053779590"
clientGroupMonitorId = "74f9ae48-36ce-4b4e-bdd3-3899fa886b02.796b2cc2-b848-4e16-bf17-ff506b5d0602"

url = f"https://vu5h0yvf80.execute-api.us-west-2.amazonaws.com/client/{clientId}/{clientGroupMonitorId}?fd=2024-01-01&ld=2024-12-31"

response = requests.get(url)

print(response.status_code, response.text, response.headers)