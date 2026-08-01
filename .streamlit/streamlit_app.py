import streamlit as st

from src.sydvaluat import load_artifacts, load_dataset, dollars, sklearn_version_mismatch

st.set_page_config(page_title="SydValuat_AI", page_icon="🏠", layout="wide")

model, meta = load_artifacts()

st.title("SydValuat_AI")
st.subheader("Sydney housing price prediction and market intelligence")

mismatch = sklearn_version_mismatch(meta)
if mismatch:
    st.warning(f"The model was trained with scikit-learn {mismatch[0]} but this app is "
               f"running {mismatch[1]}. Predictions may fail or drift — pin "
               f"`scikit-learn=={mismatch[0]}` in requirements.txt.")

st.markdown(
    f"""
This decision-support tool estimates residential sale prices for three contrasting Sydney
markets — **Mosman**, **Marrickville**, and **Blacktown** — using a
**{meta['model_family']}** pipeline trained on {meta['trained_on_records']} manually
collected sold-property records (February–July 2026).

Every estimate is presented **with its uncertainty**: a 90% prediction band of
×/÷ {meta['conformal_90_multiplier']:.2f} around the point estimate, derived from the
model's own out-of-fold errors. An estimate without that band would overstate what
{meta['trained_on_records']} observations can support.
"""
)

df = load_dataset()
st.markdown("#### Market snapshot (from the project dataset)")
cols = st.columns(3)
for col, suburb in zip(cols, ["Blacktown", "Marrickville", "Mosman"]):
    sub = df[df["suburb"] == suburb]
    col.metric(label=f"{suburb} — median sale price",
               value=dollars(sub["sale_price"].median()),
               delta=f"{len(sub)} recorded sales", delta_color="off")

st.markdown("#### Using this app")
st.markdown(
    """
- **Single Property Prediction** — enter one property's details and receive a priced range.
- **Batch CSV Prediction** — upload many properties at once and download the results.
- **Market Insights** — explore the underlying dataset: suburb price structure, size effects, and the sales timeline.
- **Model Explanation** — what drives the estimates, how accurate the model is, and where it fails.
- **About** — project provenance, data collection, and appropriate use.
"""
)

st.info(
    "**Appropriate use.** This is an academic decision-support prototype for SIG720/SIT720 at "
    "Deakin University. It interpolates within three suburbs and observable listing features "
    "only; it is not a professional valuation and must not be used to set prices."
)
