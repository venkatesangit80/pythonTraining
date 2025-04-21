import requests
import xml.etree.ElementTree as ET

# === CONFIGURATION ===
controller_url = "https://<your-domain>.saas.appdynamics.com"
app_name = "<YourAppName>"  # Case-sensitive
access_token = "<YourAccessToken>"
headers = {
    "Authorization": f"Bearer {access_token}"
}

# === Recursive Crawler ===
def get_metric_items(app_name, metric_path):
    url = f"{controller_url}/controller/rest/applications/{app_name}/metrics"
    params = {
        "metric-path": metric_path,
        "output": "XML"
    }

    response = requests.get(url, headers=headers, params=params)
    items = []

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        for item in root.findall("metric-item"):
            mtype = item.find("type").text
            name = item.find("name").text
            full_path = f"{metric_path}|{name}" if metric_path else name
            items.append({
                "type": mtype,
                "name": name,
                "metric_path": full_path
            })
    else:
        print(f"❌ Error getting items for: {metric_path} — {response.status_code}")
    return items

# === Build All Leaf Metric Paths ===
def collect_all_leaf_metrics(app_name, root_path="Application Infrastructure Performance"):
    queue = [root_path]
    leaf_metrics = []

    while queue:
        current_path = queue.pop(0)
        print(f"📂 Scanning: {current_path}")
        items = get_metric_items(app_name, current_path)

        for item in items:
            if item["type"] == "folder":
                queue.append(item["metric_path"])
            elif item["type"] == "metric":
                leaf_metrics.append(item)

    return leaf_metrics

# === Run ===
if __name__ == "__main__":
    all_leaf_metrics = collect_all_leaf_metrics(app_name)

    print(f"\n✅ Found {len(all_leaf_metrics)} real metric paths.\n")
    for m in all_leaf_metrics[:20]:  # Show only top 20
        print(f"📈 {m['metric_path']}")
