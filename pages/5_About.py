import streamlit as st

from src.sydvaluat import load_artifacts

st.set_page_config(page_title="About — SydValuat_AI", page_icon="🏠", layout="wide")
st.title("About SydValuat_AI")

model, meta = load_artifacts()

st.markdown(
    f"""
**SydValuat_AI** is the deployment deliverable of the SIG720/SIT720 Machine Learning mini
project at Deakin University: *Sydney Housing Price Prediction and Decision Support System*.

**Author.** Ayuba Sule (Student ID 226653319), MSc Data Science, School of Information
Technology, Deakin University.

**Repository.** https://github.com/ayubsmg16/SydValuat_AI — includes the full project
notebook, the raw dataset, this application, and the trained model artifacts.

**Data provenance.** {meta['trained_on_records']} sold-property records collected
**manually** from publicly available listings on realestate.com.au between February and
July 2026, at least 30 from each of Mosman, Marrickville, and Blacktown. No scraping and no
synthetic data; every record retains its source URL. Known limitations are documented in the
project notebook, including sparse coverage of build year, internal size, and amenities, a
mislabelled distance column discovered during quality assessment, and strata-site land areas
recorded against individual units.

**Model.** {meta['model_family']} on log-transformed prices inside a scikit-learn pipeline
(trained {meta['trained_at'][:10]}, scikit-learn {meta['sklearn_version']},
random seed {meta['random_state']}).

**Ethics and appropriate use.** Automated valuation trained on past sales can entrench
historical pricing patterns, including socio-economic ones, if used to *set* prices rather
than to sanity-check them. Three suburbs cannot represent Sydney; sold listings
over-represent professionally marketed properties; and listing-visible features cannot see
condition or quality. This prototype therefore presents every estimate with an explicit 90%
uncertainty band and is intended for decision support and education only — it is not a
professional valuation.
"""
)
