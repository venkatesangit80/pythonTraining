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