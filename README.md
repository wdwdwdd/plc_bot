# PLC Monitor / plc_bot

A containerized PLC data monitoring system with three services:
- Collector: reads from PLC via Modbus and writes data to PostgreSQL
- Backend (FastAPI): exposes REST APIs for devices, data, events, export
- Frontend (Vue): dashboards to display devices, data and events

## Architecture
- PostgreSQL stores devices, production data and events
- Collector periodically polls devices and persists data
- Backend provides APIs under `/api/*`
- Frontend calls backend to render dashboards

## Quick start (Docker Compose)

Prerequisites:
- Docker and Docker Compose

Steps:
1. Build images
   ```bash
   docker-compose build
   ```
2. Initialize database tables and admin user
   ```bash
   python scripts/init_db.py
   ```
3. Start services
   ```bash
   docker-compose up -d
   ```
4. Verify
   - Backend health: http://localhost:8000/api/health
   - Frontend: http://localhost/

## Configuration
- `config/settings.yaml`: database, collector, api, logging
- `config/devices.yaml`: PLC devices and points

Environment overrides (used in docker-compose for container-to-container networking):
- DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
- CONFIG_PATH (default `/app/config/settings.yaml`)
- DEVICES_CONFIG_PATH (collector devices file)
- COLLECT_INTERVAL (optional override of settings.yaml)

## Logging
- Backend and Collector read logging settings from `config/settings.yaml`
- Logs directory is mounted at `./logs` in docker-compose

## APIs (samples)
- Devices: `GET /api/devices/`
- Recent data: `GET /api/data/recent/{device_id}?hours=24`
- Events: `GET /api/events/`
- Export: `GET /api/export/data/{device_id}?start_time=...&end_time=...`

## Development tips
- Python deps for backend: `backend/requirements.txt`
- Python deps for collector: `collector/requirements.txt`
- Root `requirements.txt` is legacy; prefer per-service files for containers

## Next steps (roadmap)
- Alarm engine with per-point thresholds, event creation and UI
- Auth (JWT) and user management API
- Observability (request logging middleware, metrics)
- Frontend: charts and events page, Vite-based setup

## License
MIT

