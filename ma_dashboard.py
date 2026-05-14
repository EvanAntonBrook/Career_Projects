import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# Set page config for a professional, dark-mode institutional vibe
st.set_page_config(page_title="Quantitative M&A Screener", layout="wide", initial_sidebar_state="expanded")

st.title("🏛️ Quantitative M&A Sourcing Engine")
st.markdown("Proprietary Machine Learning predictive model for identifying middle-market Private Equity acquisition targets.")

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("ma_ml_predictions.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Prediction data not found. Please run `buyout_data_pipeline.py` followed by `ma_ml_model.py` to generate the data.")
else:
    # Sidebar Filters
    st.sidebar.header("Filter Institutional Universe")
    sectors = st.sidebar.multiselect("Select Sectors", options=df['Sector'].unique(), default=df['Sector'].unique()[:3])
    min_prob = st.sidebar.slider("Minimum Acquisition Probability", 0.0, 1.0, 0.5)
    
    filtered_df = df[(df['Sector'].isin(sectors)) & (df['Buyout_Probability'] >= min_prob)]
    
    # Key Metrics
    st.subheader("Global Portfolio Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Equities Analyzed", f"{len(df)}")
    col2.metric("Prime Targets Identified", f"{len(df[df['Buyout_Probability'] >= 0.7])}")
    col3.metric("Average FCF Yield (Targets)", f"{filtered_df['FCF_Yield'].mean()*100:.1f}%")
    
    # Data Table
    st.subheader("🎯 Predictive Target Ranking (V2.0 DCF Integrated)")
    display_df = filtered_df[['Ticker', 'Sector', 'Buyout_Probability', 'Market_Cap', 'EV/EBITDA', 'FCF_Yield', 'Discount_to_Intrinsic']]
    display_df['Buyout_Probability'] = (display_df['Buyout_Probability'] * 100).apply(lambda x: f"{x:.1f}%")
    display_df['Market_Cap'] = display_df['Market_Cap'].apply(lambda x: f"${x/1e9:.2f}B")
    display_df['Discount_to_Intrinsic'] = (display_df['Discount_to_Intrinsic'] * 100).apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(display_df.style.background_gradient(cmap='Blues', subset=['FCF_Yield']))
    
    # Visualization
    st.subheader("📊 Valuation vs. Probability Matrix")
    fig = px.scatter(
        filtered_df, 
        x="EV/EBITDA", 
        y="Buyout_Probability", 
        size="Market_Cap", 
        color="Sector",
        hover_name="Ticker",
        title="LBO Viability: EV/EBITDA vs Acquisition Probability",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- V3.0: MONTE CARLO RISK SIMULATION ---
    st.markdown("---")
    st.subheader("🎲 V3.0: Live Monte Carlo Risk Simulation")
    st.markdown("Instantly run 10,000 randomized market scenarios to stress-test the exit probability of a specific target.")
    
    selected_ticker = st.selectbox("Select a Target for Deep-Dive Simulation:", filtered_df['Ticker'])
    
    if selected_ticker:
        target_data = filtered_df[filtered_df['Ticker'] == selected_ticker].iloc[0]
        ev_ebitda = target_data['EV/EBITDA']
        
        # Run 10,000 simulations instantly
        simulations = 10000
        # Simulate exit multiple fluctuations based on current valuation
        exit_multiples = np.random.normal(loc=ev_ebitda, scale=2.5, size=simulations)
        exit_multiples = np.maximum(exit_multiples, 1.0) # Prevent negative multiples
        
        # Calculate simulated IRRs based on exit multiple expansion/contraction
        simulated_irrs = (exit_multiples / ev_ebitda) ** (1/5) - 1
        simulated_irrs = simulated_irrs * 100 # convert to percentage
        
        fig_mc = px.histogram(
            x=simulated_irrs, 
            nbins=60, 
            title=f"{selected_ticker} - Probability Distribution of Returns ({simulations:,} Scenarios)",
            labels={'x': 'Projected 5-Year IRR (%)', 'y': 'Frequency (Scenarios)'},
            color_discrete_sequence=['#00CC96'],
            template="plotly_dark"
        )
        
        median_irr = np.median(simulated_irrs)
        fig_mc.add_vline(x=median_irr, line_dash="dash", line_color="white", annotation_text=f"Median IRR: {median_irr:.1f}%")
        st.plotly_chart(fig_mc, use_container_width=True)
        
        prob_loss = (simulated_irrs < 0).sum() / simulations * 100
        mc_col1, mc_col2 = st.columns(2)
        mc_col1.metric("Median Projected IRR", f"{median_irr:.1f}%")
        mc_col2.metric("Probability of Capital Loss", f"{prob_loss:.1f}%", delta_color="inverse")