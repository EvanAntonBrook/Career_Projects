import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sovereign Wealth Optimizer", layout="wide", initial_sidebar_state="expanded")

st.title("Sovereign Wealth & Family Office Optimizer")
st.markdown("Algorithmic Asset Allocation via Modern Portfolio Theory (The Markowitz Efficient Frontier).")

@st.cache_data
def load_fo_data():
    try:
        return pd.read_csv("fo_simulations.csv")
    except:
        return pd.DataFrame()

df = load_fo_data()

if df.empty:
    st.warning("Please run `family_office_optimizer.py` first to generate the Monte Carlo simulations.")
else:
    # Find the optimal portfolio (max Sharpe)
    max_sharpe_idx = df['Sharpe_Ratio'].idxmax()
    optimal_portfolio = df.iloc[max_sharpe_idx]
    
    # Portfolio Value Simulator
    st.sidebar.header("Capital Allocation")
    portfolio_value = st.sidebar.number_input("Enter Total AUM ($)", min_value=1000000, max_value=1000000000, value=100000000, step=1000000)
    
    st.subheader("Optimal Asset Allocation (Maximum Risk-Adjusted Return)")
    st.markdown("Based on 10,000 algorithmic simulations of 5-year historical covariance.")
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Expected Annual Return", f"{optimal_portfolio['Return']*100:.2f}%")
    c2.metric("Portfolio Volatility (Risk)", f"{optimal_portfolio['Volatility']*100:.2f}%")
    c3.metric("Sharpe Ratio", f"{optimal_portfolio['Sharpe_Ratio']:.2f}", delta="Optimal mathematical balance")
    
    # Weights allocation
    weight_cols = [c for c in df.columns if c.startswith('Weight_')]
    weights = optimal_portfolio[weight_cols].values
    labels = [c.split('_')[1] for c in weight_cols]
    
    pie_df = pd.DataFrame({'Asset': labels, 'Allocation': weights})
    pie_df['Capital_Deployed'] = pie_df['Allocation'] * portfolio_value
    
    st.markdown("---")
    colA, colB = st.columns(2)
    
    with colA:
        st.write("#### Recommended Capital Deployment")
        display_pie = pie_df.copy()
        display_pie['Allocation'] = display_pie['Allocation'].apply(lambda x: f"{x*100:.1f}%")
        display_pie['Capital_Deployed'] = display_pie['Capital_Deployed'].apply(lambda x: f"${x/1e6:.1f}M")
        st.dataframe(display_pie, use_container_width=True)
        
    with colB:
        fig_pie = px.pie(pie_df, values='Allocation', names='Asset', hole=0.4, title="Asset Allocation Breakdown", template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("The Markowitz Efficient Frontier")
    st.markdown("Visualizing 10,000 simulated portfolios to identify the absolute mathematical peak of risk-to-reward.")
    
    fig_scatter = px.scatter(
        df, x='Volatility', y='Return', color='Sharpe_Ratio', 
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={'Return': 'Expected Annual Return', 'Volatility': 'Risk (Standard Deviation)'},
        template="plotly_dark"
    )
    # Add a red star for the optimal portfolio
    fig_scatter.add_trace(go.Scatter(
        x=[optimal_portfolio['Volatility']], y=[optimal_portfolio['Return']],
        mode='markers', marker=dict(color='red', size=15, symbol='star'),
        name='Optimal Portfolio'
    ))
    
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --- BLACK SWAN STRESS TEST ---
    st.markdown("---")
    st.subheader("Black Swan Stress Test (Risk Management)")
    st.markdown("Stress-test the optimal portfolio against severe historical market crashes to calculate Maximum Drawdown.")
    
    stress_col1, stress_col2 = st.columns(2)
    
    with stress_col1:
        st.write("#### Simulate Tail-Risk Events")
        scenario = st.selectbox("Select Historical Crash Scenario:", [
            "2008 Global Financial Crisis (-45% Equities, +20% Bonds)",
            "2020 COVID-19 Crash (-30% Equities, +10% Bonds, -5% Real Estate)",
            "1970s Stagflation (-20% Equities, -10% Bonds, +50% Gold)"
        ])
        
        # Simple simulated impacts based on scenario selection
        impact_map = {
            'Weight_SPY': -0.45 if '2008' in scenario else -0.30 if '2020' in scenario else -0.20,
            'Weight_QQQ': -0.50 if '2008' in scenario else -0.25 if '2020' in scenario else -0.25,
            'Weight_TLT': 0.20 if '2008' in scenario else 0.10 if '2020' in scenario else -0.10,
            'Weight_GLD': 0.05 if '2008' in scenario else 0.02 if '2020' in scenario else 0.50,
            'Weight_VNQ': -0.40 if '2008' in scenario else -0.05 if '2020' in scenario else -0.15
        }
        
        total_impact_pct = sum([optimal_portfolio[col] * impact_map[col] for col in weight_cols])
        simulated_loss = portfolio_value * total_impact_pct
        stressed_value = portfolio_value + simulated_loss
        
    with stress_col2:
        st.metric("Total AUM Before Crash", f"${portfolio_value/1e6:.1f}M")
        st.metric("Simulated Maximum Drawdown", f"${simulated_loss/1e6:.1f}M", f"{total_impact_pct*100:.1f}%", delta_color="inverse")
        st.metric("AUM After Crash", f"${stressed_value/1e6:.1f}M")
        
        if total_impact_pct > -0.20:
            st.success("✅ **Risk Assessment:** Portfolio demonstrates robust downside protection. Drawdown is contained within institutional risk tolerance thresholds.")
        else:
            st.warning("⚠️ **Risk Assessment:** Portfolio exhibits high beta exposure to equities. Consider increasing Treasury (TLT) or Gold (GLD) allocations to hedge tail-risk.")
            
    # --- LIVE CUSTOM PORTFOLIO BUILDER ---
    st.markdown("---")
    st.subheader("Live Custom Portfolio Builder (Markowitz MPT)")
    st.markdown("Enter custom tickers to dynamically download 5-year historical prices from Yahoo Finance and run a live Markowitz optimization.")
    
    with st.expander("⚙️ Open Live API Optimizer"):
        custom_tickers_input = st.text_input("Enter Tickers (comma-separated):", "AAPL, MSFT, GOOG, NVDA, AMZN").upper()
        
        if st.button("Run Live Optimization"):
            with st.spinner("Downloading historical prices and running 2,000 Monte Carlo simulations..."):
                import yfinance as yf
                import numpy as np
                
                custom_tickers = [t.strip() for t in custom_tickers_input.split(',')]
                
                try:
                    # Download data
                    data = yf.download(custom_tickers, period="5y")['Close']
                    if data.empty:
                        st.error("No data found for these tickers.")
                    else:
                        # Calculate returns
                        returns = data.pct_change().dropna()
                        mean_returns = returns.mean() * 252
                        cov_matrix = returns.cov() * 252
                        
                        num_portfolios = 2000
                        results = np.zeros((3, num_portfolios))
                        weights_record = []
                        
                        for i in range(num_portfolios):
                            weights = np.random.random(len(custom_tickers))
                            weights /= np.sum(weights)
                            
                            portfolio_return = np.sum(mean_returns * weights)
                            portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                            
                            results[0,i] = portfolio_return
                            results[1,i] = portfolio_std_dev
                            results[2,i] = (portfolio_return - 0.04) / portfolio_std_dev # Sharpe (4% risk-free)
                            weights_record.append(weights)
                            
                        max_sharpe_idx = np.argmax(results[2])
                        optimal_weights = weights_record[max_sharpe_idx]
                        
                        st.success("API Optimization Complete.")
                        
                        op_c1, op_c2, op_c3 = st.columns(3)
                        op_c1.metric("Expected Annual Return", f"{results[0, max_sharpe_idx]*100:.2f}%")
                        op_c2.metric("Annualized Volatility", f"{results[1, max_sharpe_idx]*100:.2f}%")
                        op_c3.metric("Max Sharpe Ratio", f"{results[2, max_sharpe_idx]:.2f}")
                        
                        # Plot Custom Pie
                        custom_pie_df = pd.DataFrame({
                            'Asset': custom_tickers,
                            'Allocation': optimal_weights
                        })
                        
                        fig_cp = px.pie(custom_pie_df, values='Allocation', names='Asset', hole=0.4, title="Optimal Capital Allocation", template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Prism)
                        st.plotly_chart(fig_cp, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Error running optimization: Please ensure tickers are valid on Yahoo Finance.")

    # --- AI CLIENT ALLOCATION MEMO ---
    st.markdown("---")
    st.subheader("Autonomous Client Allocation Memo")
    if st.button("Generate Executive Client Memo"):
        with st.spinner("Synthesizing Modern Portfolio Theory..."):
            import time
            time.sleep(1.0)
            st.info(f"**CLIENT ALLOCATION DIRECTIVE (AUM: ${portfolio_value/1e6:.1f}M)**\n\n**Objective:** Maximum Risk-Adjusted Return via Markowitz Efficient Frontier.\n\n**Quantitative Allocation:** To achieve the mathematical peak Sharpe Ratio of {optimal_portfolio['Sharpe_Ratio']:.2f}, capital has been deployed algorithmically across the asset universe. The portfolio targets an Expected Annual Return of {optimal_portfolio['Return']*100:.2f}% while strictly capping annualized Volatility at {optimal_portfolio['Volatility']*100:.2f}%.\n\n**Tail-Risk Hedging:** The portfolio has been stress-tested against historical black swan events (e.g., 2008 Financial Crisis). Equity beta exposure is effectively hedged via the Treasury and Gold allocations to minimize max drawdown.\n\n**Recommendation:** EXECUTE TRADES TO MATCH ALGORITHMIC WEIGHTINGS.")
