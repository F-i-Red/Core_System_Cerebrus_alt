# Cerebrus OS — Core System (Prototype)
A modular, auditable, community‑driven operating system for social, ecological and civic coordination.

This repository contains a functional prototype of the Cerebrus Engine, including modules for housing, mobility, logistics, justice, education, ecology, anti‑capture mechanisms, and a public transparency layer.
It also includes a web interface (index.html) and a Flask backend (app.py) to interact with the system.

## 📦 Features
### Core Engine
Central orchestrator connecting all modules

Manages state: families, houses, vehicles, civic force members, incidents, ecological blocks, etc.

Logs all actions through a public ledger

### Modules
**Housing** — allocation, priority rules, social relevance

**Mobility** — autonomous fleet, priority routing

**Logistics** — deliveries, waste processing, anomaly detection

**Justice** — restorative justice, containment, risk evaluation

**Civic Force** — interventions, audits, safety tasks

**Education** — institutions, specializations, weighted voting

**Ecology** — water, energy, CO₂, regeneration, alerts

**Anti‑Capture** — propaganda detection, bureaucracy detection, power capture detection

**Tech & Public Data** — transparency, audit logs, encrypted private data

### Web Interface
Simple HTML interface

Buttons trigger system actions through Flask endpoints

Displays results and public logs

## 🛠 Requirements
You need:

Python 3.10+

pip

Flask (installed via pip)

A modern browser (Chrome, Edge, Firefox)

## 📥 Installation
Clone or download the repository:

```python
git clone https://github.com/yourusername/Core_System_Cerebrus.git
cd Core_System_Cerebrus
```
Install dependencies:
```python
pip install flask
```
No other external libraries are required.

## 📁 Project Structure
### Código
Core_System_Cerebrus/

│

├── 📁 core/

│   ├── ⚙️ engine.py

│   └── 📄 types.py

│

├── 📁 modules/

│   ├── 🏠 housing.py

│   ├── 🚗 mobility.py

│   ├── 📦 logistics.py

│   ├── 🛡️ civic_force.py

│   ├── ⚖️ justice.py

│   ├── 🎓 education.py

│   ├── 🌱 ecology.py

│   ├── 🧩 anti_capture.py

│   └── 🔍 tech_public_data.py

│

├── static/ (for: CSS, JS, images, assets)

│

├── templates

│   └── 🖥️ index.html

│

├── 🌐 app.py

├── ▶️ main.py

└── 📘 README.md



## 🚀 Running the System
### 1. Start the Flask backend
From the project root:
```python
python app.py
```
You should see:

Código
Running on http://127.0.0.1:5000
Debugger is active!
This means the backend is running correctly.

### 2. Open the Web Interface
Open the file:

Código
index.html
You can open it by:

Writing in your browser:
```python
http://127.0.0.1:5000
```

Double‑clicking it (might not work)

Or dragging it into your browser (might not work)

The interface will load locally and communicate with the Flask backend.

## 🌐 Using the Web Interface

The interface includes buttons for:

Requesting a house

Requesting transportation

Sending a residue (may trigger a justice incident)

Processing incidents

Triggering Civic Force intervention

Updating ecological data

Voting on a proposal

Viewing public logs

Each button sends a request to the backend and displays the result in the output panel.

## 🧪 Running the Simulation (Optional)
You can run the standalone simulation:

```python
python main.py
```
This will:

Create families, houses, vehicles

Simulate logistics

Trigger a justice incident

Dispatch the Civic Force

Update ecological data

Perform a weighted vote

Print public logs

## 📜 License
This prototype is provided for research, experimentation and creative development.
No warranty is provided.

## 🤝 Contributing
Pull requests and module improvements are welcome.
The system is intentionally modular — new blocks can be added easily.
