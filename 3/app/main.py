from fastapi import FastAPI
from app.api import items, purchases, recommendations

app = FastAPI()

app.include_router(items.router, prefix="/api")
app.include_router(purchases.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
