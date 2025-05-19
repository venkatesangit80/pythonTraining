import requests

url = "url"

payload = {
    "requestId": [],
    "appId": [],
    "environment": [],
    "intakeStatus": [],
    "dataCenter": [],
    "primaryNetworkType": [],
    "cio": [],
    "assignedTdm": []
}

headers = {
    "Content-Type": "application/json"
    # Add "Authorization": "Bearer <token>" if needed
}

response = requests.post(url, json=payload, headers=headers)

# Output the result
print("Status Code:", response.status_code)
print("Response Body:", response.json())