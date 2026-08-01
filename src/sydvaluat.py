"""SydValuat_AI shared logic: artifact loading, feature engineering, prediction.

Every page imports from this module so the engineering recipe recorded in
model_metadata.json is reproduced in exactly one place.
"""
import json
import os
from datetime import date

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------- constants
MODEL_CANDIDATES = ["models/property_price_model.joblib",
                    "property_price_model.joblib",
                    "artifacts/property_price_model.joblib"]
META_CANDIDATES = ["models/model_metadata.json",
                   "model_metadata.json",
                   "artifacts/model_metadata.json"]
DATA_CANDIDATES = ["data/raw/Property_Sales_Dataset.csv",
                   "data/Property_Sales_Dataset.csv",
                   "Property_Sales_Dataset.csv"]
DATA_URL = ("https://raw.githubusercontent.com/ayubsmg16/SydValuat_AI/"
            "main/data/raw/Property_Sales_Dataset.csv")

# Raw columns a user supplies (single form or batch CSV)
INPUT_COLUMNS = ["suburb", "property_type", "bedrooms", "bathrooms", "car_spaces",
                 "land_size_m2", "local_centre_km", "distance_to_school_km"]
LANDED_TYPES = ["House", "Townhouse", "Duplex"]


def _first_existing(paths):
    return next((p for p in paths if os.path.exists(p)), None)


@st.cache_resource(show_spinner="Loading valuation model...")
def load_artifacts():
    """Load the fitted pipeline and its metadata contract."""
    model_path = _first_existing(MODEL_CANDIDATES)
    meta_path = _first_existing(META_CANDIDATES)
    if model_path is None or meta_path is None:
        st.error(
            "Model artifacts not found. Commit `property_price_model.joblib` and "
            "`model_metadata.json` to the repository's `models/` folder "
            "(they are exported by Section 15 of the project notebook)."
        )
        st.stop()
    model = joblib.load(model_path)
    with open(meta_path) as f:
        meta = json.load(f)
    return model, meta


def sklearn_version_mismatch(meta):
    import sklearn
    trained = meta.get("sklearn_version")
    return (trained, sklearn.__version__) if trained != sklearn.__version__ else None


def engineer_features(df, meta, valuation_month=None):
    """Reproduce the notebook's feature-engineering recipe on raw inputs.

    Mirrors model_metadata.json -> engineering_recipe:
      effective_land_m2, log_effective_land, sale_month, ptype_group.
    """
    out = df.copy()
    out["property_type"] = out["property_type"].astype(str).str.strip().str.title()
    land_medians = meta["land_medians_by_type"]

    is_landed = out["property_type"].isin(LANDED_TYPES)
    land = pd.to_numeric(out["land_size_m2"], errors="coerce")
    land = land.fillna(out["property_type"].map(
        {k: v for k, v in land_medians.items() if v is not None}))
    out["effective_land_m2"] = np.where(is_landed, land.fillna(0.0), 0.0)
    out["log_effective_land"] = np.log1p(out["effective_land_m2"])

    if "sale_month" not in out.columns:
        month = valuation_month if valuation_month is not None else date.today().month
        out["sale_month"] = month

    out["ptype_group"] = out["property_type"].replace(
        {"Townhouse": "Townhouse/Duplex", "Duplex": "Townhouse/Duplex"})

    features = meta["features_numeric"] + meta["features_categorical"]
    for c in ["bedrooms", "bathrooms", "car_spaces",
              "local_centre_km", "distance_to_school_km"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out[features]


def predict_with_band(model, meta, X):
    """Point prediction plus the 90% conformal band from the notebook."""
    point = model.predict(X)
    band = float(meta["conformal_90_multiplier"])
    return point, point / band, point * band


def validate_batch(df):
    """Check an uploaded CSV for the required raw columns; return list of problems."""
    problems = []
    missing = [c for c in INPUT_COLUMNS if c not in df.columns]
    if missing:
        problems.append(f"Missing required columns: {', '.join(missing)}")
        return problems
    known = ["House", "Unit", "Townhouse", "Duplex"]
    bad_types = (set(df["property_type"].astype(str).str.strip().str.title())
                 - set(known))
    if bad_types:
        problems.append(f"Unknown property_type values: {', '.join(sorted(bad_types))} "
                        f"(expected one of {', '.join(known)})")
    for c in ["bedrooms", "bathrooms", "car_spaces"]:
        if pd.to_numeric(df[c], errors="coerce").isna().any():
            problems.append(f"Column '{c}' contains non-numeric or empty values")
    return problems


def batch_template():
    """A one-row example CSV users can download and fill in."""
    return pd.DataFrame([{
        "suburb": "Marrickville", "property_type": "House", "bedrooms": 3,
        "bathrooms": 1, "car_spaces": 1, "land_size_m2": 250,
        "local_centre_km": 0.4, "distance_to_school_km": 0.5,
    }])


@st.cache_data(show_spinner="Loading market data...")
def load_dataset():
    """Load and lightly clean the project dataset for the insights pages.

    Applies the same core cleaning as the notebook: drop blank export rows,
    parse price and date, standardise property_type, rename the mislabelled
    distance column.
    """
    path = _first_existing(DATA_CANDIDATES) or DATA_URL
    df = pd.read_csv(path)
    df = df[df["property_id"].notna()].copy()
    df["sale_price"] = (df["sale_price ($)"].astype(str)
                        .str.replace(r"[^0-9.]", "", regex=True).astype(float))
    df["sale_date"] = pd.to_datetime(df["sale_date"], format="%d/%m/%Y")
    df["property_type"] = df["property_type"].str.strip().str.title()
    df = df.rename(columns={"distance_to_cbd_km": "local_centre_km"})
    return df


def dollars(v):
    return f"${v:,.0f}"
