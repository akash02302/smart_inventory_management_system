import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from typing import Tuple, Dict
from app.core.config import settings
from app.services.feature_engineering import FeatureEngineer

class ModelService:
    def __init__(self):
        self.model = None
        self.feature_engineer = FeatureEngineer()
        self.feature_names = None
        
    def load_data(self) -> pd.DataFrame:
        """Load and preprocess the dataset."""
        df = pd.read_csv(settings.DATA_PATH)
        return df
    
    def prepare_training_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features and target for training."""
        # Process features
        df_processed = self.feature_engineer.process_data(df)
        
        # Define target variable
        y = df_processed['quantity_sold']
        
        # Remove target and non-numeric columns from features
        X = df_processed.drop(['quantity_sold', 'product_name', 'category', 'recommendation'], axis=1, errors='ignore')
        
        # Drop any column named 'date' (case-insensitive)
        X = X.loc[:, ~X.columns.str.lower().isin(['date'])]
        
        # Drop any remaining datetime columns
        X = X.select_dtypes(exclude=['datetime64[ns]', 'datetime64[ns, UTC]'])
        
        return X, y
    
    def train_model(self) -> Dict:
        """Train the XGBoost model and return metrics."""
        # Load and prepare data
        df = self.load_data()
        X, y = self.prepare_training_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Initialize and train model
        self.model = XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            early_stopping_rounds=10,
            verbose=False
        )
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Save model and feature names
        joblib.dump(self.model, settings.MODEL_PATH)
        joblib.dump(list(X.columns), settings.MODEL_PATH + '.columns')
        
        return {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'r2': r2
        }
    
    def load_model(self):
        """Load the trained model and feature names."""
        try:
            self.model = joblib.load(settings.MODEL_PATH)
            self.feature_names = joblib.load(settings.MODEL_PATH + '.columns')
        except FileNotFoundError:
            raise Exception("Model not found. Please train the model first.")
    
    def predict(self, data: Dict) -> Tuple[float, float]:
        """Make a prediction for given input data."""
        if self.model is None or self.feature_names is None:
            self.load_model()
        
        # Prepare features
        features = self.feature_engineer.prepare_prediction_features(data)
        
        # Drop any column named 'date' (case-insensitive)
        features = features.loc[:, ~features.columns.str.lower().isin(['date'])]
        
        # Drop any remaining datetime columns
        features = features.select_dtypes(exclude=['datetime64[ns]', 'datetime64[ns, UTC]'])
        
        # Reindex to match training features
        features = features.reindex(self.feature_names, axis=1, fill_value=0)
        
        # Make prediction
        prediction = self.model.predict(features)[0]
        
        # Get feature importance for confidence score
        feature_importance = self.model.feature_importances_
        confidence_score = np.mean(feature_importance)
        
        return prediction, confidence_score
    
    def get_stock_recommendation(self, predicted_demand: float, current_stock: int, restock_threshold: int) -> str:
        """Generate stock recommendation based on predicted demand and current stock."""
        if current_stock <= restock_threshold:
            return "Restock"
        elif current_stock > predicted_demand * 2:
            return "Overstock"
        else:
            return "Stock OK" 