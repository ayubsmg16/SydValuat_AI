"""Feature engineering helpers."""
import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create or transform features for modeling."""
    df = df.copy()
    # placeholder: example create age from year_built
    if 'year_built' in df.columns:
        df['age'] = 2026 - df['year_built']
    return df
