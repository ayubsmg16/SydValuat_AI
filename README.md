# SydValuat_AI

Sydney Housing Price Prediction & Market Intelligence

This repository contains code and notebooks for collecting, preparing, modeling, and evaluating Sydney housing price data. It includes a Streamlit app for quick exploration and model serving.

Structure
- data/: raw, processed, and sample datasets
- notebooks/: exploratory notebooks and data collection
- src/: reusable Python modules for preprocessing, feature engineering, training, and evaluation
- models/: trained model artifacts
- app/: Streamlit application

Usage
1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

2. Run the Streamlit app:

```bash
streamlit run app/app.py
```
