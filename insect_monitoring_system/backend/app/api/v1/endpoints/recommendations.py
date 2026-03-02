from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.insect import Insect
from app.db.models.recommendation import Recommendation
from app.ml_models.recommendation.sprayer import get_spray_recommendation

router = APIRouter()

@router.get("/recommendations")
def get_recommendations(db: Session = Depends(get_db)):
    """
    Generates and retrieves spray recommendations based on current insect density.
    """
    insects = db.query(Insect).all()

    # This is a placeholder for how you might map insects to zones.
    # In a real system, you'd have a more robust way to associate 
    # detections with specific field zones.
    insect_density_map = {i + 1: insect.density for i, insect in enumerate(insects)}
    
    # Placeholder for field zone configuration
    field_zones = [{"id": i + 1} for i in range(len(insects))]

    if not insects:
        return {"recommendations": ["No insect data available to generate recommendations."]}

    # Generate new recommendations
    new_recommendations = get_spray_recommendation(insect_density_map, field_zones)

    # Clear old recommendations and save new ones
    db.query(Recommendation).delete()
    for zone_id, rec in new_recommendations.items():
        if rec["action"] != "NO_ACTION_NEEDED":
            db_rec = Recommendation(recommendation=rec["message"])
            db.add(db_rec)
    db.commit()

    # Fetch and return all current recommendations
    recommendations = db.query(Recommendation).all()
    
    return {"recommendations": [rec.recommendation for rec in recommendations]}