from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class PredictionRequest(BaseModel):
    date: date
    product_id: int
    region: str
    weather: str
    is_festival: bool = False
    current_stock: Optional[int] = None

class PredictionResponse(BaseModel):
    predicted_demand: float
    recommendation: str
    confidence_score: float

class StockRecommendation(BaseModel):
    product_id: int
    product_name: str
    region: str
    current_stock: int
    predicted_demand: float
    recommendation: str
    restock_threshold: int

class InventoryStatus(BaseModel):
    items: List[StockRecommendation]
    total_items: int
    low_stock_count: int
    overstock_count: int 