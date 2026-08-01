"""Model evaluation utilities."""
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    preds = model.predict(X_test)
    return {
        'mse': mean_squared_error(y_test, preds),
        'r2': r2_score(y_test, preds)
    }
