"""Data preparation utilities."""
from typing import Any
import pandas as pd


def load_raw_data(path: str) -> pd.DataFrame:
    """Load raw dataset from a CSV file."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Perform basic cleaning steps."""
    df = df.copy()
    # example: drop duplicates
    df = df.drop_duplicates()
    return df
