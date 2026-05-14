# Quantitative M&A Sourcing Engine 🏛️

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Production%20V3.0-brightgreen)

## Executive Summary
This repository contains an institutional-grade Private Equity deal-sourcing architecture. The engine autonomously scrapes fundamental market data, calculates Discounted Cash Flow (DCF) intrinsic valuations, and utilizes a Machine Learning Random Forest Classifier to predict the probability of a Leveraged Buyout (LBO). 

The output is visualized through a high-performance interactive web dashboard featuring a 10,000-scenario Monte Carlo risk simulation.

## System Architecture

### 1. Data Pipeline (`buyout_data_pipeline.py`)
*   **API Integration:** Dynamically extracts fundamental metrics (EV, EBITDA, FCF, Debt) for 100+ mid-cap equities via the Yahoo Finance API.
*   **Intrinsic Valuation Engine:** Algorithmically projects 5-year Free Cash Flow using a 9% WACC and 2.5% Terminal Growth rate to calculate the company's true intrinsic value and its current trading discount.

### 2. Machine Learning Brain (`ma_ml_model.py`)
*   **Algorithm:** `scikit-learn` Random Forest Classifier (100 estimators).
*   **Heuristics:** Trains on historical PE capital structure profiles (High FCF Yield, Low Leverage, Valuation Discount).
*   **Output:** Assigns a 0-100% predictive Acquisition Probability score to every equity in the universe.

### 3. Executive Dashboard (`ma_dashboard.py`)
*   **Decoupled UI:** Built on Streamlit and Plotly for instant, zero-latency rendering of large institutional datasets.
*   **Monte Carlo Risk Simulator:** Allows users to select any target and instantly run 10,000 randomized market scenarios to calculate the exact probability of capital loss upon exit.

## How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install scikit-learn streamlit plotly yfinance pandas numpy`
3. Generate the data: `python buyout_data_pipeline.py`
4. Train the AI: `python ma_ml_model.py`
5. Launch the Dashboard: `streamlit run ma_dashboard.py`

---
*Developed by Evan Brook | Target Market: Pacific Northwest Private Equity & Venture Capital*
