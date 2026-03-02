# FastAPI Backend for IoT Agriculture Monitoring

Quick start:

1. Create .env next to `app/core/config.py` with DATABASE_URL etc.
2. Install dependencies:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run migrations with Alembic (configure `alembic.ini` `sqlalchemy.url`), then:
```
alembic upgrade head
```
4. Start app:
```
python -m app.main
```

Notes:
- This scaffolding creates SQLAlchemy models and Alembic env. Use `alembic revision --autogenerate -m "init"` to create initial migration.
- MQTT ingestion runs in a background thread and will persist messages into Postgres via CRUD helpers.
- WebSocket endpoint `/ws` broadcasts new events to connected dashboard clients.
