from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.services.recommendation_service import get_recommendations, generate_recommendations
from app.schemas import RecommendationRequest

router = APIRouter()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

@router.post("/generate_recommendations")
async def generate_recommendations_for_user(request: RecommendationRequest, db: AsyncSession = Depends(get_db)):
    return await generate_recommendations(request.user_id, db)

@router.get("/recommendations")
async def get_user_recommendations(user_id: int, db: AsyncSession = Depends(get_db)):
    return {"recommendations": await get_recommendations(user_id, db)}

