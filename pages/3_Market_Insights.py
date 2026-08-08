import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from src.branding import (apply as apply_branding, style_fig, SUBURB_COLORS,
                          NAVY_3, TEAL_PALE)
from src.sydvaluat import load_dataset, dollars, dollars_md

st.set_page_config(page_title="Market Insights — SydValuat_AI",
                   page_icon="🏠", layout="wide")
apply_branding("insights", title="Market insights")

df = load_dataset()

st.markdown(
    f"The dataset behind the model: **{len(df)} sold properties** collected manually from "
    f"public listings between {df['sale_date'].min():%B %Y} and "
    f"{df['sale_date'].max():%B %Y}."
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Recorded sales", len(df))
c2.metric("Median price (all)", dollars(df["sale_price"].median()))
c3.metric("Cheapest sale", dollars(df["sale_price"].min()))
c4.metric("Dearest sale", dollars(df["sale_price"].max()))
st.caption(
    f"Every figure on this page is computed across all {len(df)} collected sales. The "
    "project notebook quotes slightly different suburb medians because its exploratory "
    "analysis is restricted to the 80-record training partition — the 20 hold-out "
    "properties are never inspected before the model is evaluated."
)

order = df.groupby("suburb")["sale_price"].median().sort_values().index.tolist()

tab1, tab2, tab3 = st.tabs(["Suburb price structure", "Size effects", "Sales timeline"])

with tab1:
    fig, ax = plt.subplots(figsize=(9, 4.2))
    sns.boxplot(data=df, x="suburb", y="sale_price", order=order, hue="suburb",
                palette=SUBURB_COLORS, legend=False, ax=ax)
    sns.stripplot(data=df, x="suburb", y="sale_price", order=order, color=TEAL_PALE,
                  size=3.5, alpha=0.7, ax=ax)
    ax.set_ylabel("Sale price ($)"); ax.set_xlabel("")
    ax.yaxis.set_major_formatter(lambda v, _: f"${v/1e6:.1f}m")
    st.pyplot(style_fig(fig), use_container_width=True)
    med = df.groupby("suburb")["sale_price"].median()
    iqr = df.groupby("suburb")["sale_price"].quantile(.75) - \
        df.groupby("suburb")["sale_price"].quantile(.25)
    widest = iqr.idxmax()
    st.caption(
        f"Three genuinely different markets, though the difference is not mainly in the "
        f"median: those run from {dollars_md(med[order[0]])} ({order[0]}) to "
        f"{dollars_md(med[order[-1]])} ({order[-1]}), a {med[order[-1]]/med[order[0]]:.1f}× gap. "
        f"The sharper contrast is spread — {widest}'s interquartile range of "
        f"{dollars_md(iqr[widest])} is {iqr[widest]/iqr.drop(widest).max():.1f}× the next "
        "widest, which is why its properties are the hardest for the model to price."
    )

with tab2:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    sns.stripplot(data=df, x="bedrooms", y="sale_price", hue="suburb",
                  palette=SUBURB_COLORS, dodge=True, alpha=0.8, ax=axes[0])
    axes[0].set_title("Price vs bedrooms"); axes[0].set_ylabel("Sale price ($)")
    axes[0].yaxis.set_major_formatter(lambda v, _: f"${v/1e6:.0f}m")
    houses = df[df["property_type"] == "House"]
    sns.scatterplot(data=houses, x="land_size_m2", y="sale_price", hue="suburb",
                    palette=SUBURB_COLORS, ax=axes[1], legend=False)
    axes[1].set_xscale("log"); axes[1].set_title("Price vs land size (houses)")
    axes[1].set_ylabel(""); axes[1].yaxis.set_major_formatter(lambda v, _: f"${v/1e6:.0f}m")
    plt.tight_layout()
    st.pyplot(style_fig(fig), use_container_width=True)
    st.caption("Bedrooms carry clear signal inside every suburb; land size scales house "
               "prices roughly multiplicatively, which is why the model works on the log "
               "scale.")

with tab3:
    tmp = df.assign(month=df["sale_date"].dt.to_period("M").astype(str))
    monthly = tmp.groupby(["month", "suburb"])["sale_price"].median().reset_index()
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.lineplot(data=monthly, x="month", y="sale_price", hue="suburb",
                 palette=SUBURB_COLORS, marker="o", ax=ax)
    ax.set_ylabel("Median sale price ($)"); ax.set_xlabel("")
    ax.yaxis.set_major_formatter(lambda v, _: f"${v/1e6:.1f}m")
    st.pyplot(style_fig(fig), use_container_width=True)
    st.caption("Month-to-month movement reflects which properties happened to sell, not "
               "market drift — the observation window is too short for trend analysis, a "
               "documented limitation of the dataset.")
