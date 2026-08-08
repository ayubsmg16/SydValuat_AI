import matplotlib.pyplot as plt
import streamlit as st

from src.branding import apply as apply_branding, style_fig, TEAL, TEAL_LT, GOLD
from src.sydvaluat import load_artifacts, dollars, dollars_md, feature_importances

st.set_page_config(page_title="Model Explanation — SydValuat_AI",
                   page_icon="🏠", layout="wide")
model, meta = load_artifacts()
apply_branding("explain", title="How the model works")

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
st.caption("Cross-validated RMSE during model selection: "
           f"{dollars_md(meta['cv_rmse_dollars'])}.")

st.markdown("#### What drives an estimate")
try:
    imp, label = feature_importances(model, meta)
    if imp.empty:
        st.info("Feature-importance display is unavailable for this artifact.")
    else:
        top = imp.head(10).iloc[::-1]
        pretty = top["feature"].str.replace("_", " ")
        colors = [GOLD if i == len(top) - 1 else (TEAL_LT if i >= len(top) - 3 else TEAL)
                  for i in range(len(top))]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(pretty, top["importance"], color=colors)
        ax.set_xlabel(label)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        st.pyplot(style_fig(fig), use_container_width=True)

        leader = imp.iloc[0]["feature"].replace("_", " ")
        basis = meta.get("permutation_importance_basis")
        provenance = (f"Basis: {basis}." if basis else
                      "Basis: the estimator's own gain-based importances — the notebook's "
                      "permutation figures are not present in this model_metadata.json.")
        st.caption(
            f"**{leader}** dominates: knowing it moves an estimate more than any other "
            "single fact, and the one-hot levels of a categorical feature are summed so "
            "location appears as one bar rather than several. Within a suburb, size and "
            f"position do the remaining work. {provenance}"
        )
except Exception as e:
    st.info(f"Feature-importance display unavailable for this artifact ({e}).")

st.markdown("#### Why every estimate comes as a range")
st.markdown(
    f"""
The band shown with every prediction is **not decoration**. It comes from a conformal-style
procedure: the model's own out-of-fold errors on the training data define a 90% quantile, and
that quantile becomes a multiplicative band of **×/÷ {meta['conformal_90_multiplier']:.2f}**
around any new estimate. On the hold-out set it covered all 20 sales — above its nominal 90%,
though with only 20 properties that estimate carries roughly ±13 percentage points of noise.

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
