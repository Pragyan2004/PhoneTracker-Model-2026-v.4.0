# 📡 PhoneTracker Model 2026 v.4.0

### *High-Precision Geospatial Tracking & Intelligence System*

![Version](https://img.shields.io/badge/Version-v.4.0-blue.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg?style=for-the-badge)
![Framework](https://img.shields.io/badge/Framework-Flask-black.svg?style=for-the-badge)

---

## 🚀 Overview

**PhoneTracker Model 2026** is a premium intelligence platform designed for high-accuracy phone number geolocation and carrier identification. Leveraging the power of the OpenCage Geocoding API and the Python `phonenumbers` library, it provides real-time geospatial data, terminal-style carrier reports, and interactive mapping visualizations.

## ✨ Key Features

- 🌍 **Global Geospatial Resolution**: Resolve any international phone number to its precise geographical region.
- 🗺️ **Interactive Mapping**: Powered by Folium and CartoDB, offering high-fidelity visual representations of target coordinates.
- 📊 **Intelligence Dashboard**: A centralized hub for managing search history and intelligence packets.
- 🔒 **Secure Authentication**: Robust user management with hashed password security and session-based clearance.
- 📱 **Carrier Identification**: Instant detection of service providers, line types (Mobile/Fixed), and local time zones.
- 🌫️ **Modern Aesthetic**: Ultra-sleek, dark-themed UI with glassmorphism effects for a premium "2026 Model" feel.

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Geocoding**: OpenCage Data API
- **Mapping**: Folium (Leaflet.js integration)
- **Number Parsing**: Google's `phonenumbers` library
- **Security**: Flask-Login, Werkzeug Security
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System)

## ⚙️ Configuration & Setup

### 1. Prerequisite
Ensure you have an **OpenCage API Key**. You can obtain one at [opencagedata.com](https://opencagedata.com/).

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=
OPENCAGE_API_KEY=
FIREBASE_API_KEY=
FIREBASE_AUTH_DOMAIN=
FIREBASE_PROJECT_ID=
FIREBASE_STORAGE_BUCKET=
FIREBASE_MESSAGING_SENDER_ID=
FIREBASE_APP_ID=
FIREBASE_MEASUREMENT_ID=
```

### 3. Installation
```bash
# Clone the repository
git clone https://github.com/Pragyan2004/PhoneTracker-Model-2026-v.4.0.git

# Install dependencies
pip install -r requirements.txt
```

### 4. Initialization
The application automatically handles database creation on the first run.
```bash
python app.py
```

Access the terminal via: `http://localhost:8000`

## 📖 Usage Guide

1. **Clearance Acquisition**: Register a new account to gain access to the tracking protocols.
2. **Uplink Establishment**: Enter an international format number (e.g., `+1234567890`) in the tracking interface.
3. **Intelligence Retrieval**: View detailed carrier info, timezone data, and the visual map.
4. **Archive Management**: Visit the Dashboard to review past intelligence packets or purge history logs.

---

## 🔒 Security & Privacy Notice
*This tool is designed for educational and professional demonstration purposes. Users are responsible for ensuring compliance with local laws and regulations regarding privacy and tracking.*

---
**Developed by [Pragyan Kumar](https://github.com/Pragyan2004)**
*Advancing Geospatial Intelligence.*

