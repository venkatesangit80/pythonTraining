import requests
import xml.etree.ElementTree as ET

# AppDynamics API Config
controller_url = "https://<your-domain>.saas.appdynamics.com"
access_token = "<your_access_token>"

# GET applications (will return XML)
url = f"{controller_url}/controller/rest/applications"
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    root = ET.fromstring(response.text)
    apps = []

    for app in root.findall("application"):
        app_id = app.find("id").text
        app_name = app.find("name").text
        apps.append({"id": app_id, "name": app_name})

    print("✅ Retrieved applications:")
    for app in apps:
        print(app)
else:
    print("❌ Error fetching applications:", response.status_code)


import requests

# === Replace these with your actual values ===
domain = "yourdomain.saas.appdynamics.com"
client_id = "<client-id>@<account-name>"
client_secret = "<client-secret>"
token_url = f"https://{domain}/controller/api/oauth/access_token"

# === Payload as a string ===
payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

# === Custom header with versioning ===
headers = {
    "Content-Type": "application/x-www-form-urlencoded;v=1"
}

# === Make the POST request ===
response = requests.post(token_url, data=payload, headers=headers)

# === Handle the response ===
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get("access_token")
    print("✅ Access token received:", access_token)
else:
    print("❌ Failed to get token")
    print("Status Code:", response.status_code)
    print("Response:", response.text)



import requests
import json

# === Configuration ===
controller_url = "https://<your-account>.saas.appdynamics.com"
client_id = "<client-id>@<account-name>"
client_secret = "<client-secret>"

app_name = "MyApp"  # Case-sensitive AppDynamics application name
metric_path = "Application Infrastructure Performance|<Tier>|<Node>|CPU Usage %"
duration_in_mins = 60  # How far back to pull data

# === Step 1: Get Access Token ===
def get_access_token():
    token_url = f"{controller_url}/controller/api/oauth/access_token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Access token retrieved.")
        return token
    else:
        print("❌ Failed to get token:", response.text)
        return None

# === Step 2: Get Metrics ===
def get_metric_data(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    metric_url = f"{controller_url}/controller/rest/applications/{app_name}/metric-data"

    params = {
        "metric-path": metric_path,
        "time-range-type": "BEFORE_NOW",
        "duration-in-mins": duration_in_mins,
        "rollup": "false",
        "output": "JSON"
    }

    response = requests.get(metric_url, headers=headers, params=params)
    if response.status_code == 200:
        metrics = response.json()
        print("✅ Metric data retrieved.")
        return metrics
    else:
        print("❌ Failed to get metrics:", response.text)
        return []

# === Run ===
if __name__ == "__main__":
    token = get_access_token()
    if token:
        metric_data = get_metric_data(token)
        print(json.dumps(metric_data, indent=2))