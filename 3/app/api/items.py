from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import SessionLocal
from app.models import Item
from app.schemas import CartItem

router = APIRouter()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

@router.post("/items")
async def add_item(item: CartItem, db: AsyncSession = Depends(get_db)):
    item_db = Item(name=item.name, category=item.category)
    db.add(item_db)
    await db.commit()
    await db.refresh(item_db)  # Получаем актуальный id после добавления
    return {"status": "item_added", "id": item_db.id}

@router.get("/items")
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return items
