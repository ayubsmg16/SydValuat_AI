"""Model training script."""
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd


def train_model(X: pd.DataFrame, y: pd.Series, output_path: str = 'models/model.joblib') -> None:
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, output_path)


if __name__ == '__main__':
    print('This module provides train_model() to train and save a model.')
