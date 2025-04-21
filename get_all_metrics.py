import requests
import xml.etree.ElementTree as ET
import pandas as pd

# === Configuration ===
controller_url = "https://<your-domain>.saas.appdynamics.com"
access_token = "<your_access_token>"
headers = {
    "Authorization": f"Bearer {access_token}"
}
UX_METRICS = {"Throughput", "Response Time (ms)", "Error Count"}

# === Step 1: Get All Applications ===
def get_applications():
    url = f"{controller_url}/controller/rest/applications"
    response = requests.get(url, headers=headers)
    apps = []
    if response.ok:
        root = ET.fromstring(response.text)
        for app in root.findall("application"):
            app_id = app.find("id").text
            app_name = app.find("name").text
            apps.append({"app_id": app_id, "app_name": app_name})
    return apps

# === Step 2: Get Tiers for App ===
def get_tiers(app_id):
    url = f"{controller_url}/controller/rest/applications/{app_id}/tiers"
    response = requests.get(url, headers=headers)
    tiers = []
    if response.ok:
        root = ET.fromstring(response.text)
        for tier in root.findall("tier"):
            tier_name = tier.find("name").text
            tiers.append(tier_name)
    return tiers

# === Step 3: Get Metrics for Tier ===
def get_metric_paths(app_id, tier_name):
    base_path = f"Application Infrastructure Performance|{tier_name}"
    url = f"{controller_url}/controller/rest/applications/{app_id}/metrics"
    params = {"metric-path": base_path, "output": "XML"}
    response = requests.get(url, headers=headers, params=params)
    metric_names = []
    if response.ok:
        root = ET.fromstring(response.text)
        for metric in root.findall("metric"):
            name = metric.find("name").text
            full_path = metric.find("path").text
            metric_names.append({"metric_name": name, "metric_path": full_path})
    return metric_names

# === Step 4: Combine Everything ===
def collect_metrics():
    apps = get_applications()
    records = []

    for app in apps:
        print(f"Processing App: {app['app_name']} (ID: {app['app_id']})")
        tiers = get_tiers(app['app_id'])
        for tier in tiers:
            metric_paths = get_metric_paths(app['app_id'], tier)
            for metric in metric_paths:
                mname = metric['metric_name'].strip()
                metric_type = "UX" if mname in UX_METRICS else "Backend"
                records.append({
                    "app_id": app['app_id'],
                    "app_name": app['app_name'],
                    "tier_name": tier,
                    "metric_name": mname,
                    "metric_path": metric['metric_path'],
                    "metric_type": metric_type
                })

    return pd.DataFrame(records)

# === Run and Save ===
if __name__ == "__main__":
    df_metrics = collect_metrics()
    df_metrics.to_csv("appdynamics_metrics_catalogue.csv", index=False)
    print("✅ Metrics collected and saved to CSV")
