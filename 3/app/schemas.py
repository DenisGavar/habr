from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    name: str
    category: str

class PurchaseItem(BaseModel):
    item_id: int
    category: str

class PurchaseRequest(BaseModel):
    user_id: int
    cart: List[PurchaseItem]

class RecommendationResponse(BaseModel):
    item_id: int
    category: str

class RecommendationRequest(BaseModel):
    user_id: int
