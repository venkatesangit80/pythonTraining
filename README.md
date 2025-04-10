# 📊 Synthetic Monitoring Dataset (January 2023)

This repository contains 1-minute interval synthetic monitoring data for multiple applications, each represented by a separate CSV file (e.g., `App1_Jan2023.csv`, `App2_Jan2023.csv`, etc.). These datasets are ideal for experiments in anomaly detection, time series forecasting, and performance monitoring.

---

## 🧱 Schema

Each row in the dataset represents a single metric value at a given timestamp for a specific component of an application.

| Column Name       | Description |
|-------------------|-------------|
| `timestamp`       | Date and time of the metric (ISO format, 1-minute resolution) |
| `application`     | Top-level application name (e.g., `App1`, `App2`) |
| `sub_application` | Sub-component, named like `AppX-Web`, `AppX-DB`, etc. |
| `component`       | One of: `Web`, `App`, `DB`, `ETL`, `Middleware` |
| `metric_name`     | Metric identifier (e.g., `Response Time (ms)`, `JVM_Metric_1`) |
| `metric_value`    | Numeric value of the metric |

---

## 🧩 Components

Each application includes these 5 core components:
- `Web`: Front-end / user interface
- `App`: Business logic layer
- `DB`: Database system
- `ETL`: Data processing/batch jobs
- `Middleware`: Integration services

---

## 📈 Metrics

### ✅ User Experience (UX) Metrics (all components)
- `Response Time (ms)`
- `Throughput`
- `Error Count`

### ✅ Backend Metrics (App, Middleware, ETL only)
Each app uses one of three stacks:

- **Java Apps**: `JVM_Metric_1` to `JVM_Metric_5`
- **Python Apps**: `Python_Metric_1` to `Python_Metric_5`
- **.NET Apps**: `DotNet_Metric_1` to `DotNet_Metric_5`

---

## 🔁 Patterns

- **Business hours (9am–6pm)** → High load
- **Night (2am–4am)** → ETL batch jobs
- **Random anomalies** → Injected unlabeled issues (e.g. CPU spikes, drops in throughput)
- **Correlations** → Backend metrics influence UX behavior

---

## 📂 File Naming

Each file corresponds to a single application for the month of **January 2023**:

```
App1_Jan2023.csv
App2_Jan2023.csv
...
```

---

## 🔍 Analysis Tips

- Pivot and group by metric/application/component for time series analysis
- Use anomaly detection models to uncover embedded issues
- Correlate backend and UX metrics for root cause analysis

---

## 🧠 Use Cases

- Anomaly detection (unsupervised)
- Capacity & performance modeling
- Time-series forecasting
- AIOps simulations

---

Enjoy exploring the data!
