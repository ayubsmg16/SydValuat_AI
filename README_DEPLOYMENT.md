# SydValuat_AI — Streamlit App Deployment Guide

## Repository layout expected by the app
```
SydValuat_AI/
├── streamlit_app.py
├── pages/
│   ├── 1_Single_Property_Prediction.py
│   ├── 2_Batch_CSV_Prediction.py
│   ├── 3_Market_Insights.py
│   ├── 4_Model_Explanation.py
│   └── 5_About.py
├── src/
│   ├── __init__.py
│   └── sydvaluat.py
├── models/
│   ├── property_price_model.joblib      # from notebook Section 15
│   └── model_metadata.json              # from notebook Section 15
├── data/raw/Property_Sales_Dataset.csv  # already in the repo
├── .streamlit/config.toml
└── requirements.txt
```

## Before deploying — one critical check
Open `models/model_metadata.json` and read the `sklearn_version` value **from your
Colab run**. Edit `requirements.txt` so the pinned line matches it exactly, e.g.
`scikit-learn==1.6.1`. A joblib pipeline is only guaranteed to load under the same
scikit-learn version it was trained with; the Home page will warn you if they differ.

## Run locally (optional)
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud (free)
1. Commit all files above to the GitHub repo (main branch).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Create app -> pick `ayubsmg16/SydValuat_AI`, branch `main`,
   main file path `streamlit_app.py` -> Deploy.
4. First build takes a few minutes; the app URL is then public and stable —
   put it in the report.

## Screenshots for the report (Part 6 requires them)
Capture at least: (1) Home with the market snapshot; (2) Single Property Prediction
with a completed estimate showing the three-figure band; (3) Batch prediction results
table with the download button; (4) Market Insights suburb boxplot; (5) Model
Explanation importance chart. Use a wide browser window; Ctrl/Cmd+Shift+P ->
"Capture screenshot" in Chrome DevTools gives clean full-page images.
