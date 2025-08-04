
# 🛡️ TravelAware – Real-Time Safety Assistant

![TravelAware Banner](https://user-images.githubusercontent.com/123456789/TravelAwareBanner.png)

> Your smart companion for navigating unfamiliar cities with real-time crime awareness and safety insights.

---

## 🌍 Overview

TravelAware is a **real-time safety assistant** built using Python, Streamlit, and machine learning. It empowers **tourists**, **international students**, and **locals** to:
- Get **live crime heatmaps**
- See **realistic safe route suggestions**
- Receive **smart safety alerts** and **SOS support**
- Predict **urgency** and **response time** when reporting crimes

---

## 🔥 Features

### 📍 Live Geolocation and Map View
- Auto-detects user location
- Heatmap + Marker Cluster switch
- Cluster view with polygon-highlighted high-risk zones

### 🚨 Smart Warnings & Alerts
- Detects if user is in/near danger zones
- Alert banner showing 24hr crime count nearby

### 🧭 Safe Route Advisor
- Suggests safe travel routes (e.g., “Avoid King St. and take University Ave.”)
- Street-aware advisories

### 📝 Report a Crime
- Form to simulate crime reporting with:
  - Crime type
  - Description
  - Time occurred
- Predicts urgency level and ETA using ML models

### 📰 Crime Feed
- Scrollable crime timeline with timestamp, zone, and location

---

## 🧠 Machine Learning Models

| Task                      | Model                  | Metric          |
|---------------------------|------------------------|------------------|
| Crime Urgency Prediction  | RandomForestClassifier | ~86% Accuracy    |
| Response Time Estimation | RandomForestRegressor  | RMSE ~69 mins (demo) |

Models trained using WRPS 2023 Open Dataset:
[WRPS Official Crime Dataset](https://wrps.ca/resource/2023-wrps-annual-data-extract-csv)

---

## 📁 Project Structure

```
📦 TravelAware
├── travelaware.py              # Streamlit App
├── TravelAware_Notebook.ipynb # Model Training
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/yourusername/TravelAware.git
cd TravelAware

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run travelaware.py
```

---

## 🎯 Vision Board Summary

| Category       | Details                                                                 |
|----------------|-------------------------------------------------------------------------|
| **Vision**     | Help people stay safe when visiting new places with live crime awareness |
| **Target Group** | Tourists, International Students                                       |
| **Needs Solved** | Real-time safety alerts, crime hotspots, route guidance                |
| **Standout Factor** | Realistic simulations, ML-powered decisions, beautiful UI            |
| **Business Potential** | Premium alerts for parents, travel company integrations             |

---

## 📸 Screenshots

| Feature | View |
|--------|------|
| Map with Heatmap & Cluster | ![Map View](https://user-images.githubusercontent.com/123456789/heatmap.png) |
| Crime Report Form | ![Crime Report](https://user-images.githubusercontent.com/123456789/report.png) |
| Smart Warning | ![Smart Warning](https://user-images.githubusercontent.com/123456789/alert.png) |

---

## ✨ Credits

Developed by **Krishna Reddy** as part of the Agile ML App Project (2025).  
Machine Learning + Streamlit + Real Data = TravelAware.

---

## 📬 Contact

Reach out via [GitHub](https://github.com/yourusername) for collaborations, feedback, or demos.
