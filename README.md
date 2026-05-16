# Evan Brook - Quantitative Portfolio

Welcome to my portfolio. I specialize in building institutional-grade Python architectures that automate corporate finance, venture capital, and private equity workflows.

Below are the quantitative models I have engineered.

---

## Project 1: Quantitative M&A Sourcing Model (Private Equity)

An autonomous Machine Learning pipeline that identifies undervalued mid-cap equities for Leveraged Buyout (LBO) targets.

*   **Valuation Math:** Programmed live 5-year DCF models and an **Institutional LBO Debt Waterfall & Cash Sweep** engine to algorithmically tranche debt and simulate principal paydown.
*   **Machine Learning:** Uses a Random Forest Classifier to assign an Acquisition Probability score to the target based on historical buyout data.
*   **Risk Engine:** Integrates a live 10,000-scenario Monte Carlo simulation to stress-test exit multiples and IRR.
*   **[Read the Methodology Whitepaper here](Quantitative_MA_Whitepaper.md)**

[View the Live Interactive Dashboard](https://evanbrook-ma.streamlit.app)

---

## Project 2: Venture Capital Unit Economics Model (VC / Tech Strategy)

An Unsupervised Machine Learning architecture designed to autonomously evaluate early-stage SaaS startup unit economics and predict capital efficiency.

*   **Clustering Algorithm:** Deploys scikit-learn K-Means clustering to autonomously group 2,000 synthetic startups into distinct capital risk tranches (High-Conviction, Capital Intensive, Growth Stagnation).
*   **Unit Economics:** Mathematically evaluates the Rule of 40 and LTV:CAC ratios to determine operational efficiency via a Live Pitch Deck Intake module.
*   **Capitalization Math:** Models Series A dilution, Post-Money Cap Tables, and calculates the exact equity injection required to secure 24 months of operational runway.
*   **[Read the Methodology Whitepaper here](VC_Engine_Whitepaper.md)**

[View the Live Interactive Dashboard](https://evanbrook-vc.streamlit.app)

---

## Project 3: Sovereign Wealth Portfolio Optimizer (Family Office)

An algorithmic asset allocation model designed to manage nine-figure trust funds using Modern Portfolio Theory (MPT) and Markowitz Efficient Frontier math.

*   **Financial Math:** Connects to the Yahoo Finance API to generate 5-year historical covariance matrices across multiple asset classes to maximize the portfolio Sharpe Ratio.
*   **Derivatives Hedging:** Features a **Black-Scholes Options Pricing** module to algorithmically price protective put options to hedge against tail-risk.
*   **Estate Planning:** Includes a 100-year **Multi-Generational Wealth Transfer Simulator** to model trust depletion, inflation impact, and principal preservation across three generations.
*   **[Read the Methodology Whitepaper here](Family_Office_Whitepaper.md)**

[View the Live Interactive Dashboard](https://evanbrook-wealth.streamlit.app)

---

## Project 4: Dynamic 3-Statement Financial Model (Investment Banking)

A fully linked, institutional-grade financial model that captures the real-time interplay between the Income Statement, Balance Sheet, and Cash Flow Statement.

*   **Live Data Ingestion:** Rips actual TTM (Trailing Twelve Months) financials for any global ticker using the Yahoo Finance API.
*   **Linked Architecture:** Features dynamic forecasting where changes in Revenue growth or EBITDA margins automatically propagate through all three financial statements.
*   **Sensitivity Analysis:** Includes a professional Sensitivity Matrix to stress-test bull and bear scenarios for Year 5 Net Income.

[View the Codebase](three_statement_model.py)
