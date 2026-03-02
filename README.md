# Smart Insect Detector

This repository contains an edge-to-cloud IoT platform for detecting insects, animals, and crop issues using edge inference, sensor telemetry, and an interactive dashboard.

See the investor-ready overview in `README_STARTUP.md` and architecture notes in `docs/architecture.md`.

**High-level tech stack**
- Backend: FastAPI, Uvicorn, SQLAlchemy, PostgreSQL
- Edge: Python, ONNX Runtime / OpenVINO (optional), Pi Camera, Adafruit DHT, MCP3008
- Frontend: React, Tailwind CSS, WebSockets
- Messaging: MQTT (Mosquitto)

## Project layout (relevant folders)
```
.
├── backend_fastapi/         # FastAPI backend, models, API, MQTT worker
├── insect_monitoring_system/frontend/  # React dashboard
├── tools/                  # Model conversion & benchmarking scripts
├── sensors/ vision/ actuator/ mqtt_client/  # Edge node modules
├── datasets/               # (large) training data — consider Git LFS
├── docs/                   # Architecture and setup docs
└── README_STARTUP.md       # Startup-grade README
```

## Quick start (developer)

1) Backend (Windows / dev):

```powershell
cd backend_fastapi
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
copy .env.example .env
# edit .env to set DATABASE_URL
alembic revision --autogenerate -m "init"
alembic upgrade head
python -m app.main
```

2) Frontend:

```bash
cd insect_monitoring_system/frontend
npm install
npm start
```

3) Edge (Raspberry Pi) — on the Pi:

```bash
# Install Pi-specific packages on the Pi
pip3 install -r requirements.txt  # on the Pi, not on Windows
# Ensure ONNX model is available at ./models
python main.py  # runs the edge node
```

# Smart Insect Detector

Edge-to-cloud agricultural monitoring platform: edge inference (insect/animal detection), sensor telemetry ingestion, and a responsive dashboard.

Quickstart (developer)

- Backend (development):

	```powershell
	cd insect_monitoring_system/backend
	python -m venv venv
	.\venv\Scripts\Activate.ps1
	pip install -r requirements-dev.txt
	copy .env.example .env
	# set DATABASE_URL in .env for production DBs
	alembic upgrade head
	python -m app.main
	```

- Frontend (development):

	```powershell
	cd insect_monitoring_system/frontend
	npm install
	npm start
	```

Recent updates

- Added multilingual support (English / Hindi / Marathi) and Devanagari fonts for proper rendering.
- Improved settings save/load flow and synced SPA/server language keys (`language` and `i18nextLng`).
- Added server-side logging for `/api/settings` to aid debugging.

Notes

- Large datasets live under `datasets/`. For sharing or pushes, consider using Git LFS or pruning large files.
- Platform-specific packages (Pi libraries) should be installed on a Raspberry Pi, not on Windows.

Docs and structure

- Backend: `insect_monitoring_system/backend`
- Frontend: `insect_monitoring_system/frontend`
- Docs: `docs/`

If you'd like, I can scan the frontend for remaining hardcoded UI strings and convert them to translation keys.
