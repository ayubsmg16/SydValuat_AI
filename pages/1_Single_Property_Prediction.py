import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from src.branding import apply as apply_branding, style_fig, TEAL, GOLD, NAVY_3, TEAL_PALE
from src.sydvaluat import (load_artifacts, load_dataset, engineer_features,
                           predict_with_band, dollars)

st.set_page_config(page_title="Single Property Prediction — SydValuat_AI",
                   page_icon="🏠", layout="wide")
model, meta = load_artifacts()
apply_branding("predict", title="Single property prediction")

suburbs = meta["category_levels"]["suburb"]

with st.form("property_form"):
    c1, c2, c3 = st.columns(3)
    suburb = c1.selectbox("Suburb", suburbs)
    ptype = c1.selectbox("Property type", ["House", "Unit", "Townhouse", "Duplex"])
    bedrooms = c2.number_input("Bedrooms", 1, 10, 3)
    bathrooms = c2.number_input("Bathrooms", 1, 8, 2)
    car_spaces = c3.number_input("Car spaces", 0, 8, 1)
    month = c3.selectbox("Valuation month", list(range(1, 13)), index=6,
                         format_func=lambda m: pd.Timestamp(2026, m, 1).strftime("%B"))
    c4, c5, c6 = st.columns(3)
    land = c4.number_input("Land size (m², houses/townhouses; leave 0 for units)",
                           0.0, 20000.0, 0.0, step=10.0)
    local_km = c5.number_input("Distance to local centre (km)", 0.0, 10.0, 0.4, step=0.05)
    school_km = c6.number_input("Distance to nearest school (km)", 0.0, 10.0, 0.5, step=0.05)
    submitted = st.form_submit_button("Estimate sale price", type="primary")

if submitted:
    row = pd.DataFrame([{
        "suburb": suburb, "property_type": ptype, "bedrooms": bedrooms,
        "bathrooms": bathrooms, "car_spaces": car_spaces,
        "land_size_m2": land if land > 0 else np.nan,
        "local_centre_km": local_km, "distance_to_school_km": school_km,
    }])
    X = engineer_features(row, meta, valuation_month=month)
    point, lo, hi = predict_with_band(model, meta, X)
    p, l, h = float(point[0]), float(lo[0]), float(hi[0])

    st.markdown("### Estimated sale price")
    m1, m2, m3 = st.columns(3)
    m1.metric("Lower bound (90% band)", dollars(l))
    m2.metric("Point estimate", dollars(p))
    m3.metric("Upper bound (90% band)", dollars(h))
    st.caption(
        f"The band means: for properties like this, the model's historical errors imply the "
        f"actual sale price falls between {dollars(l)} and {dollars(h)} roughly 9 times in 10. "
        f"Hold-out MAPE is {meta['holdout_metrics']['MAPE']:.1f}%, RMSE "
        f"{dollars(meta['holdout_metrics']['RMSE'])}."
    )

    df = load_dataset()
    sub = df[df["suburb"] == suburb]
    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.hist(sub["sale_price"] / 1e6, bins=15, color=NAVY_3, edgecolor=TEAL_PALE)
    ax.axvline(p / 1e6, color=GOLD, lw=2.5)
    ax.axvspan(l / 1e6, h / 1e6, color=TEAL, alpha=0.25)
    ax.set_xlabel("Sale price ($ million)")
    ax.set_yticks([])
    ax.set_title(f"Your estimate against {len(sub)} recorded {suburb} sales", fontsize=11)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    st.pyplot(style_fig(fig), use_container_width=True)

    if ptype == "Unit" and land > 0:
        st.info("Note: for units, any land figure on a listing usually describes the whole "
                "strata site, so the model deliberately ignores it (units carry no private "
                "land in the feature set).")
