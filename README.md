# Evan Brook - Quantitative Portfolio

Welcome to my portfolio. I specialize in building institutional-grade Python architectures that automate corporate finance, venture capital, and private equity workflows.

Below are the quantitative models I have engineered.

---

## Project 1: Quantitative M&A Sourcing Model (Private Equity)

An autonomous Machine Learning pipeline that identifies undervalued mid-cap equities for Leveraged Buyout (LBO) targets.

*   **Valuation Math:** Algorithmically projects 5-year Free Cash Flow (9% WACC) to calculate the Discount to Intrinsic Value.
*   **Machine Learning:** Uses a Random Forest Classifier to assign an Acquisition Probability score to the target.
*   **Risk Engine:** Integrates a live 10,000-scenario Monte Carlo simulation to stress-test exit multiples.
*   **[Read the Methodology Whitepaper here](Quantitative_MA_Whitepaper.md)**

[View the Live Interactive Dashboard](#)

---

## Project 2: Venture Capital Unit Economics Model (VC / Tech Strategy)

An Unsupervised Machine Learning architecture designed to autonomously evaluate early-stage SaaS startup unit economics and predict capital efficiency.

*   **Clustering Algorithm:** Deploys scikit-learn K-Means clustering to autonomously group 2,000 synthetic startups into distinct capital risk tranches.
*   **Unit Economics:** Mathematically evaluates the Rule of 40 and LTV:CAC ratios to determine operational efficiency.
*   **Capitalization Math:** Features a dynamic Series A Capital Raise Calculator that mathematically determines the required equity injection to secure 24 months of operational runway.
*   **[Read the Methodology Whitepaper here](VC_Engine_Whitepaper.md)**

[View the Live Interactive Dashboard](#)

---

## Project 3: Sovereign Wealth Portfolio Optimizer (Family Office)

An algorithmic asset allocation model designed to manage nine-figure trust funds using Modern Portfolio Theory (MPT).

*   **Financial Math:** Connects to the Yahoo Finance API to calculate 5-year historical covariance matrices across Equities, Treasuries, Gold, and Real Estate.
*   **Monte Carlo Simulation:** Executes 10,000 randomized simulations to map the Markowitz Efficient Frontier and identify the mathematical peak of the Sharpe Ratio.
*   **Risk Management:** Features a Tail-Risk Stress Test module that subjects the optimal portfolio to historic crashes (e.g., 2008 Financial Crisis, 2020 COVID Crash) to calculate Maximum Drawdown.
*   **[Read the Methodology Whitepaper here](Family_Office_Whitepaper.md)**

[View the Live Interactive Dashboard](#)
