import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Venture Capital Deal Flow Engine", layout="wide", initial_sidebar_state="expanded")

st.title("Venture Capital Deal-Flow Model")
st.markdown("Unsupervised Machine Learning (K-Means Clustering) to identify high-conviction startups and flag capital-intensive outliers.")

@st.cache_data
def load_vc_data():
    try:
        return pd.read_csv("vc_ml_predictions.csv")
    except FileNotFoundError:
        return pd.DataFrame()

df = load_vc_data()

if df.empty:
    st.warning("Please run `vc_synthetic_data.py` and `vc_ml_model.py` first.")
else:
    st.sidebar.header("Filter Deal Flow")
    cluster_filter = st.sidebar.multiselect("Select AI Classifications", options=df['AI_Classification'].unique(), default=df['AI_Classification'].unique())
    
    filtered_df = df[df['AI_Classification'].isin(cluster_filter)]
    
    st.subheader("Startup Universe Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Startups Scanned", f"{len(df):,}")
    unicorns = len(df[df['AI_Classification'] == 'Tier 1: High Conviction'])
    col2.metric("Tier 1 Targets Found", f"{unicorns:,}")
    zombies = len(df[df['AI_Classification'] == 'Tier 3: Growth Stagnation'])
    col3.metric("Tier 3 Assets Avoided", f"{zombies:,}")
    
    st.markdown("---")
    st.subheader("Cluster Visualization")
    st.markdown("AI-driven multidimensional separation of SaaS unit economics.")
    
    fig_3d = px.scatter_3d(
        filtered_df,
        x='Rule_of_40',
        y='LTV_CAC_Ratio',
        z='Runway_Months',
        color='AI_Classification',
        hover_name='Startup_ID',
        color_discrete_map={
            'Tier 1: High Conviction': '#00CC96',
            'Tier 2: Capital Intensive': '#EF553B',
            'Tier 3: Growth Stagnation': '#AB63FA'
        },
        template="plotly_dark",
        title="SaaS Unit Economics: Rule of 40 vs LTV:CAC vs Cash Runway"
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Deal Flow Pipeline")
    display_df = filtered_df[['Startup_ID', 'AI_Classification', 'ARR', 'Rule_of_40', 'LTV_CAC_Ratio', 'Runway_Months']].copy()
    display_df['ARR'] = display_df['ARR'].apply(lambda x: f"${x/1e6:.2f}M")
    display_df['Rule_of_40'] = display_df['Rule_of_40'].apply(lambda x: f"{x:.1f}%")
    display_df['LTV_CAC_Ratio'] = display_df['LTV_CAC_Ratio'].apply(lambda x: f"{x:.2f}x")
    display_df['Runway_Months'] = display_df['Runway_Months'].apply(lambda x: f"{x:.1f} months")
    
    st.dataframe(display_df, use_container_width=True)

    # --- LIVE STARTUP INTAKE MODULE ---
    st.markdown("---")
    st.subheader("Live Startup Intake (Custom Unit Economics)")
    st.markdown("Input live metrics from an active pitch deck. The engine will instantly calculate the Rule of 40, LTV:CAC, and automatically classify the asset into a risk tranche.")
    
    with st.expander("➕ Open Live Startup Intake Form"):
        col_in1, col_in2, col_in3 = st.columns(3)
        custom_name = col_in1.text_input("Startup Name", "Acme SaaS")
        custom_arr = col_in1.number_input("ARR ($M)", 1.0, 100.0, 5.0, 0.5) * 1e6
        
        custom_growth = col_in2.number_input("YoY Growth (%)", -50.0, 200.0, 30.0, 5.0)
        custom_ebitda = col_in2.number_input("EBITDA Margin (%)", -100.0, 50.0, -10.0, 5.0)
        
        custom_ltv = col_in3.number_input("Customer LTV ($)", 100, 100000, 5000, 500)
        custom_cac = col_in3.number_input("Customer CAC ($)", 100, 50000, 1500, 100)
        
        col_in4, col_in5 = st.columns(2)
        custom_cash = col_in4.number_input("Cash in Bank ($M)", 0.0, 50.0, 2.0, 0.5) * 1e6
        custom_burn = col_in5.number_input("Monthly Burn ($K)", 0.0, 1000.0, 150.0, 10.0) * 1000
        
        if st.button("Evaluate Pitch Deck"):
            rule_of_40 = custom_growth + custom_ebitda
            ltv_cac = custom_ltv / custom_cac if custom_cac > 0 else 0
            runway = custom_cash / custom_burn if custom_burn > 0 else 999
            
            if rule_of_40 >= 40 and ltv_cac >= 3.0:
                calc_tier = "Tier 1: High Conviction"
                t_color = "#00CC96"
            elif rule_of_40 < 20 and runway < 12:
                calc_tier = "Tier 3: Growth Stagnation"
                t_color = "#AB63FA"
            else:
                calc_tier = "Tier 2: Capital Intensive"
                t_color = "#EF553B"
                
            st.markdown(f"### AI Classification: <span style='color:{t_color}'>{calc_tier}</span>", unsafe_allow_html=True)
            
            out1, out2, out3 = st.columns(3)
            out1.metric("Rule of 40 Score", f"{rule_of_40:.1f}%", delta="Pass (>40%)" if rule_of_40 >= 40 else "Fail (<40%)", delta_color="normal" if rule_of_40 >= 40 else "inverse")
            out2.metric("LTV:CAC Ratio", f"{ltv_cac:.2f}x", delta="Pass (>3.0x)" if ltv_cac >= 3.0 else "Fail (<3.0x)", delta_color="normal" if ltv_cac >= 3.0 else "inverse")
            out3.metric("Cash Runway", f"{runway:.1f} months", delta="Critical (<12m)" if runway < 12 else "Stable", delta_color="inverse" if runway < 12 else "normal")
            
            if calc_tier == "Tier 1: High Conviction":
                st.success("✅ **Recommendation:** Asset demonstrates elite capital efficiency. Proceed to due diligence and term sheet modeling.")
            elif calc_tier == "Tier 2: Capital Intensive":
                st.warning("⚠️ **Recommendation:** Asset requires significant equity injection to maintain growth. Evaluate cash burn strictly.")
            else:
                st.error("❌ **Recommendation:** PASS. Hyper-burn with stagnant growth metrics.")

    # --- SERIES A CAPITAL RAISE CALCULATOR ---
    st.markdown("---")
    st.subheader("Series A Capital Raise Calculator")
    st.markdown("Algorithmically calculate the required equity injection to secure 24 months of operational runway.")
    
    selected_startup = st.selectbox("Select a Startup for Capitalization Analysis:", filtered_df['Startup_ID'])
    
    if selected_startup:
        target_data = filtered_df[filtered_df['Startup_ID'] == selected_startup].iloc[0]
        current_runway = target_data['Runway_Months']
        burn_rate = target_data['Monthly_Burn']
        
        # We need to secure 24 months total runway
        target_runway = 24.0
        shortfall_months = max(0, target_runway - current_runway)
        required_capital = shortfall_months * burn_rate
        
        st.write(f"**Target Profile:** {selected_startup} | **AI Classification:** {target_data['AI_Classification']}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Current Cash Runway", f"{current_runway:.1f} Months", delta=f"{current_runway - 24:.1f} from 24m Target", delta_color="normal" if current_runway >= 24 else "inverse")
        c2.metric("Monthly Cash Burn", f"${burn_rate/1000:.1f}k / mo")
        c3.metric("Required Series A Raise", f"${required_capital/1e6:.2f}M", delta="To secure 24m operations", delta_color="off")
        
        if required_capital > 0:
            st.error(f"**Investment Thesis:** {selected_startup} requires a **${required_capital/1e6:.2f}M** capital injection to hit the 24-month operational benchmark required for a Series A round. Based on their Rule of 40 score ({target_data['Rule_of_40']:.1f}%), this equity injection is categorized as a **{'Moderate' if target_data['Rule_of_40'] > 40 else 'Extreme'} Risk** investment.")
        else:
            st.success(f"**Investment Thesis:** {selected_startup} is already capitalized for over 24 months. No immediate equity dilution is required, signaling strong operational leverage.")
            
        st.markdown("---")
        st.write("#### 12-Month Capital Depletion Curve")
        
        # Simulate 12 month cash burn trajectory
        months = [f"M{i}" for i in range(1, 13)]
        starting_cash = current_runway * burn_rate
        
        # Net cash drops by the monthly burn rate each month
        projected_cash = [starting_cash - (burn_rate * i) for i in range(1, 13)]
        
        proj_df = pd.DataFrame({
            'Month': months,
            'Capital Reserve ($)': projected_cash
        })
        
        # Determine if cash goes negative
        proj_df['Status'] = proj_df['Capital Reserve ($)'].apply(lambda x: 'Bankrupt' if x < 0 else 'Solvent')
        
        fig_burn = px.bar(
            proj_df,
            x='Month',
            y='Capital Reserve ($)',
            title=f"{selected_startup} - Projected Cash Balance vs Burn Rate",
            color='Status',
            color_discrete_map={'Solvent': '#00CC96', 'Bankrupt': '#EF553B'},
            template="plotly_dark"
        )
        st.plotly_chart(fig_burn, use_container_width=True)
        
        # --- AI PARTNER PITCH MEMO ---
        st.markdown("---")
        st.subheader("Autonomous Partner Pitch Memo")
        if st.button(f"Generate VC Deal Memo for {selected_startup}"):
            with st.spinner("Synthesizing Unit Economics into Partner Memo..."):
                import time
                time.sleep(1.0)
                st.info(f"**PARTNER PITCH MEMO: {selected_startup}**\n\n**AI Classification:** {target_data['AI_Classification']}\n\n**Unit Economics:** The startup is currently generating ${target_data['ARR']/1e6:.2f}M in ARR with a Rule of 40 score of {target_data['Rule_of_40']:.1f}%. Customer acquisition efficiency is highly optimized, boasting an LTV:CAC ratio of {target_data['LTV_CAC_Ratio']:.2f}x.\n\n**Capitalization:** The company is currently burning ${burn_rate/1000:.1f}k per month. To secure 24 months of runway for an upcoming Series A raise, they require a **${required_capital/1e6:.2f}M** equity injection.\n\n**Recommendation:** {'PROCEED TO TERM SHEET' if target_data['AI_Classification'] == 'Tier 1: High Conviction' else 'PASS DUE TO HYPER-BURN'}.")
