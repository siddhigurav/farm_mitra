# Windows development notes

1) Sensor libraries (Adafruit‑DHT, `picamera`) and some Linux‑only runtime wheels (e.g., `onnxruntime` for Linux) will fail to install on Windows. For local development on Windows, use `backend_fastapi/requirements-dev.txt` which excludes those packages.

2) To install backend dependencies on Windows (from project root):

```powershell
cd backend_fastapi
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install -r requirements-dev.txt
```

3) Running Mosquitto on Windows: either install natively or run a container:

```powershell
# Docker (recommended if Docker Desktop is available)
docker run -d --name mosquitto -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

4) Adafruit sensor code and Raspberry Pi camera should be installed and tested on the Pi itself. On the Pi run:

```bash
pip3 install Adafruit-DHT picamera2 onnxruntime
```

5) Alembic: If you see "No 'script_location' key found", create `alembic.ini` in `backend_fastapi` (done) and ensure the working directory is `backend_fastapi` when running alembic commands.

Example:

```powershell
cd backend_fastapi
.\\venv\\Scripts\\Activate.ps1
set DATABASE_URL=postgresql://user:pass@localhost:5432/smartdb
alembic revision --autogenerate -m "init"
alembic upgrade head
```

6) If `docker-compose` is not found on Windows, use `docker compose` (space) if Docker CLI plugins are installed, or install Docker Compose separately.
