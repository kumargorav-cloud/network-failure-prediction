![Python](https://img.shields.io/badge/Python-3.x-blue)
![Linux](https://img.shields.io/badge/Platform-Linux-orange)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

# Network Failure Prediction System

A Linux-based network health monitoring system that predicts network degradation
before failures occur using active probing, adaptive baselines, and risk scoring.

## 🚀 Features
- Active network probing (latency, jitter, packet loss, timeouts)
- Environment-agnostic design (works in WSL, cloud, servers)
- Self-learning baseline (no hardcoded thresholds)
- Explainable network risk score (0–100)
- Automated execution using cron
- Alerting with audit logs

## 🧠 How It Works
1. Collector probes network quality using ping
2. System learns normal behavior over time
3. Latest metrics are compared against baseline
4. A weighted risk score is calculated
5. Alerts are triggered for medium/high risk

## 🛠️ Tech Stack
- Linux
- Python 3
- SQLite
- Cron

## 📂 Project Structure
collector.py # Active network probe
baseline_learner.py # Baseline learning engine
risk_engine.py # Risk score calculator
alert.py # Alert handler
run_monitor.py # Orchestration script
logs/ # Alert & cron logs


## ▶️ How to Run
```bash
python3 collector.py
python3 baseline_learner.py
python3 risk_engine.py

*/5 * * * * python3 run_monitor.py
