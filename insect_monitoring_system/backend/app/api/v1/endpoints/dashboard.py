from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.alert import Alert
from app.db.models.insect import Insect
from app.db.models.recommendation import Recommendation
from app.db.models.animal import Animal

router = APIRouter()

@router.get("/dashboard_data")
def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Retrieves and aggregates data for the frontend dashboard.
    """
    # Fetch recent alerts (e.g., last 10)
    alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(10).all()

    # Fetch insect density data
    insect_density = db.query(Insect).all()

    # Fetch spray recommendations
    recommendations = db.query(Recommendation).all()
    
    # Fetch all detected animal types
    animals = db.query(Animal).all()

    # Format data for the dashboard
    dashboard_data = {
        "alerts": [
            {"id": alert.id, "type": alert.type, "timestamp": alert.timestamp.isoformat()}
            for alert in alerts
        ],
        "insect_density": [
            {"name": insect.name, "density": insect.density}
            for insect in insect_density
        ],
        "infestation_heatmap": {
            # This would need more complex geospatial data, 
            # for now, we'll simulate it based on density.
            "locations": [
                {"lat": 20.0, "lng": 73.78, "intensity": insect.density} 
                for insect in insect_density
            ]
        },
        "spray_recommendations": [
            rec.recommendation for rec in recommendations
        ],
        "detected_animals": [
            animal.name for animal in animals
        ]
    }

    return dashboard_data