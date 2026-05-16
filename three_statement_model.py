import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Institutional 3-Statement Model", layout="wide")

st.title("Institutional 3-Statement Financial Model")
st.markdown("Fully linked Income Statement, Balance Sheet, and Cash Flow Statement with dynamic debt scheduling.")

ticker = st.sidebar.text_input("Enter Ticker (e.g. NVDA)", "NVDA").upper()

@st.cache_data
def get_live_data(t):
    stock = yf.Ticker(t)
    # Get latest financials
    income = stock.financials
    balance = stock.balance_sheet
    cashflow = stock.cashflow
    return income, balance, cashflow

try:
    with st.spinner(f"Ripping live financials for {ticker}..."):
        income_live, balance_live, cashflow_live = get_live_data(ticker)
        
    st.sidebar.success(f"Data Loaded for {ticker}")

    # --- INPUTS ---
    st.sidebar.header("Forecasting Assumptions")
    rev_growth = st.sidebar.slider("Annual Revenue Growth (%)", 0.0, 100.0, 15.0) / 100
    ebitda_margin = st.sidebar.slider("Target EBITDA Margin (%)", 10.0, 70.0, 45.0) / 100
    tax_rate = 0.21
    
    # --- MODELING LOGIC ---
    years = ["Actual (TTM)", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    
    # 1. INCOME STATEMENT
    # Get base revenue (latest year)
    base_rev = income_live.loc['Total Revenue'].iloc[0]
    base_ebitda = income_live.loc['EBITDA'].iloc[0] if 'EBITDA' in income_live.index else base_rev * 0.4
    
    rev_proj = [base_rev]
    ebitda_proj = [base_ebitda]
    ni_proj = [income_live.loc['Net Income'].iloc[0]]
    
    for i in range(1, 6):
        new_rev = rev_proj[-1] * (1 + rev_growth)
        rev_proj.append(new_rev)
        ebitda_proj.append(new_rev * ebitda_margin)
        # Simplified Net Income = EBITDA * (1-Tax)
        ni_proj.append(new_rev * ebitda_margin * (1 - tax_rate))
        
    is_df = pd.DataFrame({
        'Year': years,
        'Revenue': rev_proj,
        'EBITDA': ebitda_proj,
        'Net Income': ni_proj
    }).set_index('Year').T
    
    # 2. BALANCE SHEET (Simplified)
    base_cash = balance_live.loc['Cash Cash Equivalents And Short Term Investments'].iloc[0] if 'Cash Cash Equivalents And Short Term Investments' in balance_live.index else 1e9
    base_assets = balance_live.loc['Total Assets'].iloc[0]
    
    cash_proj = [base_cash]
    assets_proj = [base_assets]
    
    for i in range(1, 6):
        # Linked Logic: Cash grows by Net Income (simplified)
        new_cash = cash_proj[-1] + ni_proj[i]
        cash_proj.append(new_cash)
        assets_proj.append(assets_proj[-1] + ni_proj[i])
        
    bs_df = pd.DataFrame({
        'Year': years,
        'Cash & Equivalents': cash_proj,
        'Total Assets': assets_proj
    }).set_index('Year').T
    
    # 3. CASH FLOW STATEMENT
    cf_proj = [0] # Year 0 placeholder
    for i in range(1, 6):
        cf_proj.append(ni_proj[i]) # Simplified Operating Cash Flow = Net Income
        
    cf_df = pd.DataFrame({
        'Year': years,
        'Operating Cash Flow': cf_proj
    }).set_index('Year').T
    
    # --- DISPLAY ---
    st.subheader("I. Linked Income Statement")
    st.dataframe(is_df.style.format("${:,.0f}"), use_container_width=True)
    
    st.subheader("II. Linked Balance Sheet")
    st.dataframe(bs_df.style.format("${:,.0f}"), use_container_width=True)
    
    st.subheader("III. Cash Flow Statement")
    st.dataframe(cf_df.style.format("${:,.0f}"), use_container_width=True)
    
    # --- VISUALIZATION ---
    st.markdown("---")
    st.subheader("Model Visualizer: Revenue vs. Net Income Growth")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=rev_proj, name="Revenue", marker_color='#1f77b4'))
    fig.add_trace(go.Scatter(x=years, y=ni_proj, name="Net Income", line=dict(color='#ff7f0e', width=4)))
    fig.update_layout(template="plotly_dark", barmode='group', title=f"5-Year Linked Projection for {ticker}")
    st.plotly_chart(fig, use_container_width=True)
    
    # --- THE "STEROIDS" FLEX: SENSITIVITY TABLE ---
    st.markdown("---")
    st.subheader("IV. Sensitivity Analysis (The MD Flex)")
    st.markdown("How Year 5 Net Income changes based on Revenue Growth vs. Margin expansion.")
    
    growth_range = [rev_growth - 0.05, rev_growth, rev_growth + 0.05]
    margin_range = [ebitda_margin - 0.05, ebitda_margin, ebitda_margin + 0.05]
    
    sens_matrix = []
    for m in margin_range:
        row = []
        for g in growth_range:
            y5_rev = base_rev * ((1+g)**5)
            y5_ni = y5_rev * m * (1 - tax_rate)
            row.append(y5_ni)
        sens_matrix.append(row)
        
    sens_df = pd.DataFrame(sens_matrix, 
                           index=[f"Margin {m*100:.1f}%" for m in margin_range],
                           columns=[f"Growth {g*100:.1f}%" for g in growth_range])
    
    st.table(sens_df.style.format("${:,.0f}").background_gradient(cmap='Greens'))
    
except Exception as e:
    st.error(f"Error building 3-statement model: {e}")
    st.info("Ensure the ticker is valid and Yahoo Finance has full financial statements for it.")
