from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    PredictionRequest,
    PredictionResponse,
    StockRecommendation,
    InventoryStatus
)
from app.services.model_service import ModelService
from app.services.weather_service import WeatherService
from typing import List
import pandas as pd

router = APIRouter()
model_service = ModelService()
weather_service = WeatherService()

@router.post("/predict", response_model=PredictionResponse)
async def predict_demand(request: PredictionRequest):
    """Predict demand for given input parameters."""
    try:
        data = request.dict()
        # If weather is not provided, fetch from WeatherAPI
        if not data.get('weather') and data.get('region') and data.get('date'):
            weather_info = weather_service.get_weather(data['region'], str(data['date']))
            data['weather'] = weather_info['condition']
        # Make prediction
        predicted_demand, confidence_score = model_service.predict(data)
        # Get recommendation if current_stock is provided
        recommendation = "N/A"
        if request.current_stock is not None:
            recommendation = model_service.get_stock_recommendation(
                predicted_demand,
                request.current_stock,
                60  # Default restock threshold
            )
        return PredictionResponse(
            predicted_demand=float(predicted_demand),
            recommendation=recommendation,
            confidence_score=float(confidence_score)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommend", response_model=InventoryStatus)
async def get_inventory_recommendations():
    """Get stock recommendations for all products."""
    try:
        df = model_service.load_data()
        latest_data = df.sort_values('date').groupby(['product_id', 'region']).last().reset_index()
        recommendations = []
        low_stock_count = 0
        overstock_count = 0
        for _, row in latest_data.iterrows():
            # Fetch weather for the region and today if not present
            weather = row['weather']
            if not weather:
                weather_info = weather_service.get_weather(row['region'], str(pd.Timestamp.now().date()))
                weather = weather_info['condition']
            data = {
                'date': pd.Timestamp.now().date(),
                'product_id': row['product_id'],
                'region': row['region'],
                'weather': weather,
                'is_festival': bool(row['is_festival'])
            }
            predicted_demand, _ = model_service.predict(data)
            recommendation = model_service.get_stock_recommendation(
                predicted_demand,
                row['current_stock'],
                row['restock_threshold']
            )
            if recommendation == "Restock":
                low_stock_count += 1
            elif recommendation == "Overstock":
                overstock_count += 1
            rec = StockRecommendation(
                product_id=row['product_id'],
                product_name=row['product_name'],
                region=row['region'],
                current_stock=row['current_stock'],
                predicted_demand=float(predicted_demand),
                recommendation=recommendation,
                restock_threshold=row['restock_threshold']
            )
            recommendations.append(rec)
        return InventoryStatus(
            items=recommendations,
            total_items=len(recommendations),
            low_stock_count=low_stock_count,
            overstock_count=overstock_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train")
async def train_model():
    """Train the demand forecasting model."""
    try:
        metrics = model_service.train_model()
        return {"message": "Model trained successfully", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 