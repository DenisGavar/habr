from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.models import UserPurchase
from app.schemas import PurchaseRequest

router = APIRouter()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

@router.post("/purchases")
async def add_purchase(request: PurchaseRequest, db: AsyncSession = Depends(get_db)):
    for item in request.cart:
        purchase = UserPurchase(user_id=request.user_id, item_id=item.item_id, category=item.category)
        db.add(purchase)
    await db.commit()
    return {"status": "purchases_added"}

