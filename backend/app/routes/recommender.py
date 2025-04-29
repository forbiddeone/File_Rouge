from fastapi import APIRouter, HTTPException
from app.database import con
from ml.recommender import get_recommendations_for_user

router = APIRouter()

@router.post("/{user_id}")
def recommend_movies(user_id: int):
    try:
        recommendations = get_recommendations_for_user(user_id, con=con)
        return {
            "user_id": user_id,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
