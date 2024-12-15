from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from collections import defaultdict
from app.models import UserPurchase, Item, Recommendation
import asyncio

async def generate_recommendations(user_id: int, db: AsyncSession):
    # Получаем покупки пользователя
    result = await db.execute(select(UserPurchase).filter(UserPurchase.user_id == user_id))
    user_purchases = result.scalars().all()

    # Создаем список всех товаров, которые покупал пользователь
    user_items = set(purchase.item_id for purchase in user_purchases)

    # Получаем все покупки для построения матрицы совместной покупки
    result = await db.execute(select(UserPurchase))
    all_purchases = result.scalars().all()

    # Строим матрицу совместной покупки
    item_pairs = defaultdict(int)
    for purchase in all_purchases:
        for other_purchase in all_purchases:
            if purchase.user_id == other_purchase.user_id and purchase.item_id != other_purchase.item_id:
                item_pairs[(purchase.item_id, other_purchase.item_id)] += 1

    # Рекомендуем товары, которых нет в истории покупок пользователя
    recommendations = []
    for item_id in user_items:
        for (item1, item2), count in item_pairs.items():
            if item1 == item_id and item2 not in user_items:
                recommendations.append((item2, count))

    # Сортируем по популярности (по количеству покупок)
    recommendations.sort(key=lambda x: x[1], reverse=True)

    # Добавляем самую популярную рекомендацию
    if recommendations:
        recommended_item_id = recommendations[0][0]
        recommendation = Recommendation(user_id=user_id, item_id=recommended_item_id)
        db.add(recommendation)
        await db.commit()
        return {"status": "recommendations_generated"}
    return {"status": "no_recommendations"}

async def get_recommendations(user_id: int, db: AsyncSession):
    result = await db.execute(select(Recommendation).filter(Recommendation.user_id == user_id))
    recommendations = result.scalars().all()
    return [{"item_id": recommendation.item_id} for recommendation in recommendations]
