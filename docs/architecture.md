# Architecture

This document contains a simple Mermaid diagram and notes describing the high‑level architecture of Smart Insect Detector.

```mermaid
graph LR
  subgraph Edge
    A[Pi Camera] --> B[Edge Inference (ONNXRuntime)]
    C[DHT22 / Soil Sensor] --> D[Sensor Daemon]
    B --> E[MQTT Client]
    D --> E
    E --> F[Local SQLite Queue]
  end

  subgraph Network
    F -->|MQTT| G[Broker (Mosquitto)]
  end

  subgraph Cloud
    G --> H[Backend (FastAPI)]
    H --> I[Postgres]
    H --> J[Rule Engine]
    H --> K[WebSocket Clients]
  end
```

Notes:
- The edge persists messages locally to a lightweight SQLite queue to survive network outages.
- ONNXRuntime is the baseline for CPU inference; optionally use OpenVINO when available for better performance.
- The backend ingests MQTT messages with a background worker and broadcasts live updates via WebSocket to the dashboard.
