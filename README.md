# Intelligent Insect & Animal Monitoring System

## Tech Stack
- **Backend**: Python, Flask
- **Machine Learning**: TensorFlow, OpenCV, Ultralytics (YOLO)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL (SQLAlchemy ORM)

## Project Structure
```
smart-insect-detector/
├── insect_monitoring_system/
│   └── backend/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py          # Flask application
│       │   ├── templates/       # HTML templates
│       │   │   └── index.html
│       │   ├── static/          # CSS, JS, images
│       │   │   ├── css/
│       │   │   │   └── main.css
│       │   │   └── js/
│       │   │       └── main.js
│       │   ├── api/             # API endpoints
│       │   │   └── v1/
│       │   │       └── endpoints/
│       │   ├── db/              # Database models
│       │   │   ├── models/
│       │   │   └── session.py
│       │   ├── ml_models/       # Machine learning models
│       │   │   ├── insect/
│       │   │   ├── animal/
│       │   │   ├── audio/
│       │   │   └── recommendation/
│       │   └── utils/           # Utility functions
│       └── requirements.txt     # Python dependencies
├── datasets/                    # Training and testing data
├── deployment/                  # Docker files and deployment configs
├── docs/                        # Documentation
├── config.py                   # Application configuration
├── run.py                      # Main application runner
└── test_app.py                 # Test script
```

## Features
- Real-time insect and animal detection using computer vision
- Audio-based detection for nocturnal monitoring
- Dashboard for monitoring detection results
- Alert system for potential threats
- Recommendation engine for pest control measures
- Heatmap visualization of infestation patterns
- **Real-time weather tracking** for disease prediction and irrigation planning

## Weather Integration

The system now includes real-time weather tracking using the **Open-Meteo API** (completely free, no API key required). The weather data includes:

- Current temperature
- Humidity levels
- Wind speed
- Weather conditions (clear, cloudy, rain, etc.)

Weather data is displayed on the dashboard and can be used for:
- Disease prediction models
- Irrigation recommendations
- Alert timing based on weather conditions

### Supported Locations
- Nashik (default)
- Mumbai
- Pune
- Delhi

To add more locations, update the coordinates in the weather endpoint.

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r insect_monitoring_system/backend/requirements.txt
   ```

## Running the Application

```bash
python run.py
```

The application will be available at http://127.0.0.1:5000

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/health` - Health check
- `GET /api/stats` - Get detection statistics
- `GET /api/weather/current` - Get current weather data
- `GET /api/weather/history` - Get weather history
- `POST /api/start_detection` - Start detection process
- `POST /api/stop_detection` - Stop detection process

## Machine Learning Models

The system uses:
- YOLO models for insect and animal detection
- Audio processing models for sound-based detection
- Coverage analysis models for infestation pattern recognition

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request