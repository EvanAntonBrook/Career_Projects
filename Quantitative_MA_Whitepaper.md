# Quantitative M&A Sourcing Engine
**Methodology and Architecture Whitepaper**

**Author:** Evan Brook
**Target Industry:** Private Equity & Venture Capital
**Date:** May 2026

---

## 1. Executive Summary
The traditional Private Equity deal-sourcing workflow relies heavily on manual financial modeling and subjective screening. To modernize this approach, I architected the **Quantitative M&A Sourcing Engine**, a Python-based algorithmic pipeline designed to autonomously identify undervalued public and private market acquisition targets. 

By integrating automated API data extraction with a Machine Learning Random Forest Classifier, this engine mathematically predicts the probability of an LBO (Leveraged Buyout) acquisition based on historical fundamental metrics.

## 2. Data Pipeline Architecture (Phase 1)
The engine utilizes a custom Python data pipeline to query live financial APIs, extracting institutional-grade metrics across a basket of middle-market equities. 
Key extracted metrics include:
*   Enterprise Value (EV)
*   Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA)
*   Free Cash Flow (FCF) Yield
*   Total Debt to EBITDA Ratios
*   Insider & Institutional Ownership Percentages

This data is dynamically cleaned using Pandas and NumPy, handling missing values and calculating complex ratios necessary for valuation multiples.

## 3. Machine Learning Predictive Model (Phase 2)
The core intelligence of the engine is built on `scikit-learn`. 

### The Algorithm
I deployed a **Random Forest Classifier** composed of 100 decision trees. The Random Forest was chosen for its resilience against overfitting in complex financial datasets and its ability to handle non-linear relationships between variables (e.g., how high debt negatively impacts buyout probability only *after* a certain threshold).

### The Valuation Heuristics (V2.0 Update)
The model identifies acquisition targets based on the optimal Private Equity capital structure profile:
1.  **Discounted Cash Flow (DCF) Intrinsic Value:** Integrated in V2.0, the pipeline algorithmically projects 5-year Free Cash Flow using a 9% WACC and 2.5% Terminal Growth rate to calculate the company's true intrinsic value. The Machine Learning model heavily weights the "Discount to Intrinsic Value" metric.
2.  **High Free Cash Flow Yield:** Ensures the target generates sufficient cash to service the debt load introduced during an LBO.
3.  **Low EV/EBITDA Multiple:** Identifies undervalued entry points to maximize Multiple on Money (MoM) at exit.
4.  **Low Existing Leverage:** Ensures the target has unused debt capacity.

## 4. UI/UX and Deployment (Phase 3)
The engine is wrapped in a high-performance **Streamlit** web application, featuring interactive data matrices and Plotly visualizations. This allows non-technical deal teams to seamlessly filter the universe of equities and interact with the Machine Learning probability scores in real-time.

## 5. Conclusion
This project demonstrates the immediate value of programmatic automation in institutional finance. By replacing manual Excel screening with a Python-based Machine Learning architecture, a Private Equity firm can increase their top-of-funnel deal flow evaluation by multiple orders of magnitude.
