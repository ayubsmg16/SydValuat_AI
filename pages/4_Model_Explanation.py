import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from src.sydvaluat import load_artifacts, dollars

st.set_page_config(page_title="Model Explanation — SydValuat_AI",
                   page_icon="🏠", layout="wide")
st.title("How the model works")

model, meta = load_artifacts()

st.markdown(
    f"""
The deployed model is a **{meta['model_family']}** pipeline trained on
{meta['trained_on_records']} sold properties. It predicts the *logarithm* of the sale price
and converts back to dollars, so features act multiplicatively — the same way the market
prices land, size, and location. It was selected after a 5-fold cross-validated comparison
against Linear Regression, Ridge, and Random Forest in the project notebook.
"""
)

st.markdown("#### Measured accuracy (untouched hold-out set)")
hm = meta["holdout_metrics"]
c1, c2, c3, c4 = st.columns(4)
c1.metric("R²", f"{hm['R2']:.2f}")
c2.metric("RMSE", dollars(hm["RMSE"]))
c3.metric("MAE", dollars(hm["MAE"]))
c4.metric("MAPE", f"{hm['MAPE']:.1f}%")
st.caption(f"Cross-validated RMSE during model selection: {dollars(meta['cv_rmse_dollars'])}.")

st.markdown("#### What drives an estimate")
try:
    inner = model.regressor_.named_steps["model"]
    prep = model.regressor_.named_steps["prep"]
    names = prep.get_feature_names_out()
    if hasattr(inner, "feature_importances_"):
        imp = pd.Series(inner.feature_importances_, index=names)
        label = "Share of the model's decisions"
    elif hasattr(inner, "coef_"):
        imp = pd.Series(np.abs(inner.coef_), index=names)
        label = "Absolute standardised coefficient"
    else:
        imp = None
    if imp is not None:
        imp = imp.sort_values().tail(10)
        clean = (imp.rename(index=lambda s: s.replace("num__", "").replace("cat__", "")
                            .replace("_", " ")))
        fig, ax = plt.subplots(figsize=(8, 4))
        clean.plot.barh(ax=ax, color="#14535B")
        ax.set_xlabel(label)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        st.pyplot(fig, use_container_width=True)
        st.caption(
            "Location dominates: knowing the suburb moves an estimate more than any other "
            "single fact. Within a suburb, size (bedrooms, bathrooms, effective land) and "
            "position do the remaining work."
        )
except Exception as e:
    st.info(f"Feature-importance display unavailable for this artifact ({e}).")

st.markdown("#### Why every estimate comes as a range")
st.markdown(
    f"""
The band shown with every prediction is **not decoration**. It comes from a conformal-style
procedure: the model's own out-of-fold errors on the training data define a 90% quantile, and
that quantile becomes a multiplicative band of **×/÷ {meta['conformal_90_multiplier']:.2f}**
around any new estimate. On the hold-out set this band achieved its intended coverage.

The band is wide because the honest uncertainty *is* wide: with
{meta['trained_on_records']} observations and only listing-visible features, the model cannot
see interior condition, renovation quality, views, or street position — and in premium
markets those unobserved factors can move a sale by millions. The notebook's failure analysis
found that all five of the largest prediction errors were Mosman prestige houses for exactly
this reason.
"""
)

st.markdown("#### When to trust it less")
st.markdown(
    """
- **Prestige and top-of-market properties** — few comparables exist, and unobserved quality dominates the price.
- **Anything outside Blacktown, Marrickville, or Mosman** — the model has never seen other markets and silently extrapolates.
- **Heavily renovated or unrenovated stock** — condition is invisible to the feature set.
- **Development sites** — value rests on potential, not on the dwelling the features describe.

In these situations the estimate is a starting point for human judgment, not a substitute for it.
"""
)
