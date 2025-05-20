import pandas as pd
import numpy as np
from typing import List, Dict
from app.core.config import settings

class FeatureEngineer:
    def __init__(self):
        self.lag_features = settings.LAG_FEATURES
        self.rolling_windows = settings.ROLLING_WINDOWS
        self.categorical_columns = ['product_id', 'region', 'weather', 'is_festival']
        
    def create_lag_features(self, df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
        """Create lag features for specified columns."""
        for lag in self.lag_features:
            df[f'quantity_sold_lag_{lag}'] = df.groupby(group_cols)['quantity_sold'].shift(lag)
        return df
    
    def create_rolling_features(self, df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
        """Create rolling window features."""
        for window in self.rolling_windows:
            df[f'quantity_sold_rolling_mean_{window}'] = df.groupby(group_cols)['quantity_sold'].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
            df[f'quantity_sold_rolling_std_{window}'] = df.groupby(group_cols)['quantity_sold'].transform(
                lambda x: x.rolling(window=window, min_periods=1).std()
            )
        return df
    
    def encode_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical features using one-hot encoding."""
        for col in self.categorical_columns:
            if col in df.columns:
                dummies = pd.get_dummies(df[col], prefix=col)
                df = pd.concat([df, dummies], axis=1)
                df = df.drop(col, axis=1)
        return df
    
    def create_date_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create date-based features."""
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['day_of_month'] = df['date'].dt.day
        return df
    
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the entire dataset."""
        # Create date features
        df = self.create_date_features(df)
        
        # Create lag features
        group_cols = ['product_id', 'region']
        df = self.create_lag_features(df, group_cols)
        
        # Create rolling features
        df = self.create_rolling_features(df, group_cols)
        
        # Encode categorical features
        df = self.encode_categorical_features(df)
        
        # Fill missing values
        df = df.fillna(method='ffill')
        df = df.fillna(0)  # Fill any remaining NaNs with 0
        
        return df
    
    def prepare_prediction_features(self, data: Dict) -> pd.DataFrame:
        """Prepare features for a single prediction."""
        # Convert input data to DataFrame
        df = pd.DataFrame([data])
        
        # Create date features
        df = self.create_date_features(df)
        
        # Encode categorical features
        df = self.encode_categorical_features(df)
        
        return df 