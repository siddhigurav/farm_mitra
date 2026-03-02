import sys
import os

# Add the parent directory to sys.path to ensure local modules are found
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime
from app.db.session import SessionLocal
from app.db.crud import get_user_by_username, create_user, get_user
from app.utils.security import verify_password
from app.db.models.crop import Crop
from app.db.models.insect import Insect
from app.db.models.remedy import RemedyApproval
from app.db.models.user import User
from app.db.models.weather import Weather
from app.db.models.alert import Alert
from app.db.models.recommendation import Recommendation
from app.db.models.animal import Animal
import requests
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'smart_farming_secret_key'  # For session management
CORS(app)  # Enable CORS for all routes

# Initialize database
from app.db.init_db import init_db
init_db()

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simulated data storage (in a real app, this would be a database)
detection_data = {
    "insects_detected": 3,
    "animals_detected": 1,
    "alerts_generated": 2,
    "detections": [
        {"id": 1, "type": "Insect", "name": "Fruit Borer", "crop": "Guava", "timestamp": "2025-10-09T10:30:00Z", "severity": "High", "remedy": "Apply neem oil spray in the evening to avoid leaf burn. Repeat every 7 days until infestation is controlled."},
        {"id": 2, "type": "Insect", "name": "Mealybug", "crop": "Guava", "timestamp": "2025-10-09T11:15:00Z", "severity": "Medium", "remedy": "Use insecticidal soap solution. Spray thoroughly on affected areas, especially under leaves. Introduce beneficial insects like ladybugs."},
        {"id": 3, "type": "Insect", "name": "Thrips", "crop": "Grapes", "timestamp": "2025-10-09T09:45:00Z", "severity": "Low", "remedy": "Introduce beneficial insects such as minute pirate bugs. Keep the area free of weeds which harbor thrips."}
    ]
}

# Farmer approval data
farmer_approvals = {
    "irrigation": [],
    "remedy": []
}

# Authentication routes
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # Get database session
    db = SessionLocal()
    try:
        user = get_user_by_username(db, username)
        if user and verify_password(password, user.hashed_password):
            session["user_id"] = user.id
            session["username"] = user.username
            return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username}})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    finally:
        db.close()

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    # Get database session
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = get_user_by_username(db, username)
        if existing_user:
            return jsonify({"error": "Username already taken"}), 400
            
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            return jsonify({"error": "Email already taken"}), 400
        
        # Create new user
        new_user = create_user(db, username, email, password)
        return jsonify({"message": "User registered successfully", "user": {"id": new_user.id, "username": new_user.username}}), 201
    finally:
        db.close()

@app.route("/api/profile")
def get_profile():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    # Get database session
    db = SessionLocal()
    try:
        user = get_user(db, session["user_id"])
        if user:
            return jsonify({"id": user.id, "username": user.username, "email": user.email})
        else:
            return jsonify({"error": "User not found"}), 404
    finally:
        db.close()

@app.route("/api/profile", methods=["PUT"])
def update_profile():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.get_json()
    
    # Get database session
    db = SessionLocal()
    try:
        user = get_user(db, session["user_id"])
        
        if user:
            # Update user data
            if "username" in data:
                # Check if username is already taken
                existing_user = get_user_by_username(db, data["username"])
                if existing_user and existing_user.id != user.id:
                    return jsonify({"error": "Username already taken"}), 400
                user.username = data["username"]
                
            if "email" in data:
                # Check if email is already taken
                existing_email = db.query(User).filter(User.email == data["email"], User.id != user.id).first()
                if existing_email:
                    return jsonify({"error": "Email already taken"}), 400
                user.email = data["email"]
                
            db.commit()
            db.refresh(user)
            
            return jsonify({"message": "Profile updated successfully", "user": {"id": user.id, "username": user.username, "email": user.email}})
        else:
            return jsonify({"error": "User not found"}), 404
    finally:
        db.close()

@app.route("/api/settings")
def get_settings():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    # Return user-specific settings from session, with defaults if not set
    return jsonify({
        "notifications": session.get("notifications", True),
        "email_alerts": session.get("email_alerts", True),
        "sms_alerts": session.get("sms_alerts", False),
        "language": session.get("language", "en"),
        "theme": session.get("theme", "light")
    })

@app.route("/api/settings", methods=["PUT"])
def update_settings():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.get_json()
    
    # Validate language option if provided
    valid_languages = ["en", "mr", "hi"]
    if "language" in data and data["language"] not in valid_languages:
        return jsonify({"error": "Invalid language option"}), 400
    
    # Validate theme option if provided
    valid_themes = ["light", "dark"]
    if "theme" in data and data["theme"] not in valid_themes:
        return jsonify({"error": "Invalid theme option"}), 400
    
    # Filter only the fields we want to update
    allowed_fields = ["notifications", "email_alerts", "sms_alerts", "language", "theme"]
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
    
    # Store settings in session
    for key, value in filtered_data.items():
        session[key] = value
    session.modified = True  # Ensure session is saved
    
    # In a real app, this would update user-specific settings in the database
    # For now, we'll just return the updated settings
    return jsonify({"message": "Settings updated successfully", "settings": filtered_data})

# Main routes
@app.route("/")
def index():
    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for('login_page'))
    
    # Get database session
    db = SessionLocal()
    try:
        # Get current user
        user = get_user(db, session["user_id"])
        if not user:
            return redirect(url_for('login_page'))
        
        # Get crops for user (in a real app, this would be filtered by user)
        crops = db.query(Crop).all()
        
        # Render dashboard with user and crop data
        return render_template('dashboard.html', user=user, crops=crops)
    finally:
        db.close()

@app.route("/login")
def login_page():
    # If user is already logged in, redirect to dashboard
    if "user_id" in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/profile")
def profile_page():
    if "user_id" not in session:
        return redirect(url_for('login_page'))
    return render_template('profile.html')

@app.route("/settings")
def settings_page():
    if "user_id" not in session:
        return redirect(url_for('login_page'))
    return render_template('settings.html')

@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy", "message": "Smart Farming Monitoring System is running"})

@app.route("/api/stats")
def get_stats():
    # Get database session
    db = SessionLocal()
    try:
        crop_count = db.query(Crop).count()
        return jsonify({
            "total_crops": crop_count,
            "pests_detected": len(detection_data["detections"]),  # Fixed to show actual count
            "pending_approvals": len(farmer_approvals["irrigation"]) + len(farmer_approvals["remedy"])
        })
    finally:
        db.close()

@app.route("/api/crops", methods=["GET"])
def get_crops():
    # Get database session
    db = SessionLocal()
    try:
        crops = db.query(Crop).all()
        # Convert to JSON-serializable format
        crops_data = []
        for crop in crops:
            crops_data.append({
                "id": crop.id,
                "crop_name": crop.crop_name,
                "crop_variety": crop.crop_variety,
                "planting_date": crop.planting_date.isoformat() if crop.planting_date else None,
                "area_in_hectares": crop.area_in_hectares,
                "irrigation_type": crop.irrigation_type
            })
        return jsonify(crops_data)
    finally:
        db.close()

@app.route("/api/crops", methods=["POST"])
def add_crop():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["crop_name", "crop_variety", "planting_date", "area_in_hectares", "irrigation_type"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Get database session
    db = SessionLocal()
    try:
        # Create new crop entry
        new_crop = Crop(
            crop_name=data["crop_name"],
            crop_variety=data["crop_variety"],
            planting_date=datetime.fromisoformat(data["planting_date"]),
            area_in_hectares=data["area_in_hectares"],
            irrigation_type=data["irrigation_type"]
        )
        
        db.add(new_crop)
        db.commit()
        db.refresh(new_crop)
        
        # Convert to JSON-serializable format
        crop_data = {
            "id": new_crop.id,
            "crop_name": new_crop.crop_name,
            "crop_variety": new_crop.crop_variety,
            "planting_date": new_crop.planting_date.isoformat() if new_crop.planting_date else None,
            "area_in_hectares": new_crop.area_in_hectares,
            "irrigation_type": new_crop.irrigation_type
        }
        
        return jsonify(crop_data), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Error adding crop: {str(e)}"}), 500
    finally:
        db.close()

@app.route("/api/crops/<int:crop_id>")
def get_crop(crop_id):
    # Get database session
    db = SessionLocal()
    try:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if crop:
            # Convert to JSON-serializable format
            crop_data = {
                "id": crop.id,
                "crop_name": crop.crop_name,
                "crop_variety": crop.crop_variety,
                "planting_date": crop.planting_date.isoformat() if crop.planting_date else None,
                "area_in_hectares": crop.area_in_hectares,
                "irrigation_type": crop.irrigation_type
            }
            return jsonify(crop_data)
        return jsonify({"error": "Crop not found"}), 404
    finally:
        db.close()

@app.route("/api/detections")
def get_detections():
    return jsonify(detection_data["detections"])

@app.route("/api/detections/<int:detection_id>", methods=["DELETE"])
def remove_detection(detection_id):
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    global detection_data
    detection_index = next((i for i, d in enumerate(detection_data["detections"]) if d["id"] == detection_id), None)
    
    if detection_index is not None:
        detection_data["detections"].pop(detection_index)
        # Update count
        detection_data["insects_detected"] = len(detection_data["detections"])
        return jsonify({"message": "Detection removed successfully"})
    else:
        return jsonify({"error": "Detection not found"}), 404

@app.route("/api/farmer_approvals")
def get_farmer_approvals():
    # Combine irrigation and remedy approvals
    all_approvals = []
    
    for i, approval in enumerate(farmer_approvals["irrigation"]):
        all_approvals.append({
            "id": i + 1,
            "type": "Irrigation",
            "crop": "Grapes",  # In a real app, this would be looked up from crop_id
            "details": f"{approval.get('duration_minutes', 30)} minutes of {approval.get('irrigation_type', 'Drip')} irrigation",
            "status": approval.get("status", "pending")
        })
    
    for i, approval in enumerate(farmer_approvals["remedy"]):
        all_approvals.append({
            "id": len(farmer_approvals["irrigation"]) + i + 1,
            "type": "Pest Treatment",
            "crop": "Guava",  # In a real app, this would be looked up from crop_id
            "details": approval.get("description", "Pest treatment recommended"),
            "status": approval.get("status", "pending")
        })
    
    return jsonify(all_approvals)

@app.route("/api/approve_request/<int:approval_id>", methods=["POST"])
def approve_request(approval_id):
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    data = request.get_json()
    approval_type = data.get("type")
    
    if approval_type == "Irrigation":
        if 0 <= approval_id - 1 < len(farmer_approvals["irrigation"]):
            farmer_approvals["irrigation"][approval_id - 1]["status"] = "approved"
            farmer_approvals["irrigation"][approval_id - 1]["approved_at"] = datetime.utcnow().isoformat()
            return jsonify({"message": f"Irrigation approval {approval_id} approved"})
        else:
            return jsonify({"error": "Approval not found"}), 404
    elif approval_type == "Remedy":
        remedy_index = approval_id - len(farmer_approvals["irrigation"]) - 1
        if 0 <= remedy_index < len(farmer_approvals["remedy"]):
            farmer_approvals["remedy"][remedy_index]["status"] = "approved"
            farmer_approvals["remedy"][remedy_index]["approved_at"] = datetime.utcnow().isoformat()
            return jsonify({"message": f"Remedy approval {approval_id} approved"})
        else:
            return jsonify({"error": "Approval not found"}), 404
    else:
        return jsonify({"error": "Invalid approval type"}), 400

# New endpoints for IoT device integration
@app.route("/api/iot/sensor_data", methods=["POST"])
def update_sensor_data():
    # In a real application, this would update crop conditions based on IoT sensor data
    data = request.get_json()
    crop_id = data.get("crop_id")
    soil_moisture = data.get("soil_moisture_level")
    
    # Simulate updating crop conditions
    return jsonify({
        "status": "Sensor data updated successfully",
        "crop_id": crop_id,
        "soil_moisture_level": soil_moisture,
        "irrigation_needed": soil_moisture < 30.0 if soil_moisture else False
    })

@app.route("/api/iot/request_irrigation", methods=["POST"])
def request_irrigation():
    # In a real application, this would create an irrigation request from IoT device
    data = request.get_json()
    crop_id = data.get("crop_id")
    duration = data.get("duration_minutes")
    
    # Simulate creating irrigation approval request
    farmer_approvals["irrigation"].append({
        "crop_id": crop_id,
        "duration_minutes": duration,
        "status": "pending",
        "requested_at": datetime.utcnow().isoformat()
    })
    
    return jsonify({
        "status": "Irrigation request submitted",
        "approval_id": len(farmer_approvals["irrigation"]),
        "crop_id": crop_id,
        "duration_minutes": duration
    })

# Weather API configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")  # Not needed for Open-Meteo
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

@app.route("/api/weather/current", methods=["GET"])
def get_current_weather():
    location = request.args.get("location", "Nashik")
    
    # Default coordinates for common locations
    locations = {
        "Nashik": {"lat": 19.9975, "lon": 73.7898},
        "Mumbai": {"lat": 19.0760, "lon": 72.8777},
        "Pune": {"lat": 18.5204, "lon": 73.8567},
        "Delhi": {"lat": 28.7041, "lon": 77.1025}
    }
    
    coords = locations.get(location, locations["Nashik"])  # Default to Nashik
    
    db = SessionLocal()
    try:
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current_weather": True,
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "Asia/Kolkata"
        }
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract relevant weather data safely (field names vary across API responses)
        current = data.get("current_weather", {})

        # wind speed key can be 'wind_speed' or 'windspeed'
        wind_speed = current.get("wind_speed") or current.get("windspeed")

        # weather code variations
        weathercode = current.get("weathercode") or current.get("weather_code")

        # Extract humidity from hourly if available; keys may vary
        humidity = None
        hourly = data.get("hourly") or {}
        if hourly:
            # possible humidity keys
            humidity_keys = ["relativehumidity_2m", "relative_humidity_2m", "relative_humidity"]
            for hk in humidity_keys:
                if hk in hourly:
                    times = hourly.get("time", [])
                    vals = hourly.get(hk, [])
                    cur_time = current.get("time")
                    if cur_time and cur_time in times:
                        try:
                            idx = times.index(cur_time)
                            humidity = vals[idx] if idx < len(vals) else (vals[0] if vals else None)
                        except Exception:
                            humidity = vals[0] if vals else None
                    else:
                        humidity = vals[0] if vals else None
                    break

        weather_data = {
            "location": location,
            "temperature": current.get("temperature"),
            "humidity": humidity,
            "pressure": None,  # Open-Meteo doesn't provide pressure in free tier
            "wind_speed": wind_speed,
            "description": get_weather_description(weathercode),
            "timestamp": datetime.utcnow()
        }

        # Store in database
        weather_entry = Weather(**weather_data)
        db.add(weather_entry)
        db.commit()
        db.refresh(weather_entry)

        return jsonify(weather_data)

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch weather data: {str(e)}"}), 500
    finally:
        db.close()

def get_weather_description(weathercode):
    """Convert Open-Meteo weather codes to descriptions"""
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return codes.get(weathercode, "Unknown")

@app.route("/api/weather/history", methods=["GET"])
def get_weather_history():
    limit = int(request.args.get("limit", 10))
    db = SessionLocal()
    try:
        weather_records = db.query(Weather).order_by(Weather.timestamp.desc()).limit(limit).all()
        return jsonify([
            {
                "id": record.id,
                "location": record.location,
                "temperature": record.temperature,
                "humidity": record.humidity,
                "pressure": record.pressure,
                "wind_speed": record.wind_speed,
                "description": record.description,
                "timestamp": record.timestamp.isoformat()
            }
            for record in weather_records
        ])
    finally:
        db.close()

@app.route("/api/dashboard_data")
def get_dashboard_data():
    db = SessionLocal()
    try:
        # Fetch recent alerts
        alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(10).all()

        # Fetch insect density data
        insects = db.query(Insect).all()

        # Fetch spray recommendations
        recommendations = db.query(Recommendation).all()

        # Fetch all detected animal types
        animals = db.query(Animal).all()

        # Fetch recent weather
        recent_weather = db.query(Weather).order_by(Weather.timestamp.desc()).first()

        # Format data for the dashboard
        dashboard_data = {
            "alerts": [
                {"id": alert.id, "type": alert.type, "timestamp": alert.timestamp.isoformat()}
                for alert in alerts
            ],
            "insect_density": [
                {"name": insect.name, "density": insect.density}
                for insect in insects
            ],
            "infestation_heatmap": {
                "locations": [
                    {"lat": 20.0, "lng": 73.78, "intensity": insect.density} 
                    for insect in insects
                ]
            },
            "spray_recommendations": [
                rec.recommendation for rec in recommendations
            ],
            "detected_animals": [
                animal.name for animal in animals
            ],
            "current_weather": {
                "temperature": recent_weather.temperature if recent_weather else None,
                "humidity": recent_weather.humidity if recent_weather else None,
                "description": recent_weather.description if recent_weather else None,
                "timestamp": recent_weather.timestamp.isoformat() if recent_weather else None
            } if recent_weather else None
        }

        return jsonify(dashboard_data)
    finally:
        db.close()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)