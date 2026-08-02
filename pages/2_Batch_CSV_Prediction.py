import pandas as pd
import streamlit as st

from src.branding import apply as apply_branding
from src.sydvaluat import (load_artifacts, engineer_features, predict_with_band,
                           validate_batch, batch_template, INPUT_COLUMNS)

st.set_page_config(page_title="Batch CSV Prediction — SydValuat_AI",
                   page_icon="🏠", layout="wide")
model, meta = load_artifacts()
apply_branding("batch", title="Batch CSV prediction")

st.markdown(
    f"Upload a CSV with one row per property and these columns: "
    f"`{'`, `'.join(INPUT_COLUMNS)}`. "
    "Leave `land_size_m2` empty for units. Download the template to see the exact format."
)
st.download_button("Download CSV template",
                   batch_template().to_csv(index=False).encode(),
                   file_name="sydvaluat_batch_template.csv", mime="text/csv")

uploaded = st.file_uploader("Upload properties CSV", type=["csv"])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"That file could not be read as a CSV: {e}")
        st.stop()

    problems = validate_batch(df)
    if problems:
        st.error("The file needs fixing before predictions can run:")
        for p in problems:
            st.markdown(f"- {p}")
        st.stop()

    X = engineer_features(df, meta)
    point, lo, hi = predict_with_band(model, meta, X)
    results = df[INPUT_COLUMNS].copy()
    results["predicted_price"] = point.round(0)
    results["lower_90"] = lo.round(0)
    results["upper_90"] = hi.round(0)

    st.success(f"Predicted {len(results)} properties.")
    st.dataframe(results.style.format({c: "${:,.0f}" for c in
                                       ["predicted_price", "lower_90", "upper_90"]}),
                 use_container_width=True)
    st.download_button("Download predictions CSV",
                       results.to_csv(index=False).encode(),
                       file_name="sydvaluat_predictions.csv", mime="text/csv")
    st.caption(
        f"Each row carries the 90% conformal band (×/÷ {meta['conformal_90_multiplier']:.2f}). "
        "Predictions for suburbs other than Blacktown, Marrickville, and Mosman are "
        "extrapolations outside the training data and should not be trusted."
    )
