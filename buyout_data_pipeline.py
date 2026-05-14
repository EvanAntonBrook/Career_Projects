import yfinance as yf
import pandas as pd
import numpy as np
import time

def build_ma_dataset(tickers):
    """
    Phase 1: Data Pipeline for the Machine Learning M&A Predictor.
    Pulls fundamental institutional-grade metrics for a basket of equities.
    """
    print("Initiating Quantitative M&A Data Pipeline...")
    data_records = []
    
    for ticker in tickers:
        print(f"Extracting fundamentals for {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # We are extracting the core metrics a Private Equity firm looks at
            # to determine if a company is ripe for a buyout.
            market_cap = info.get('marketCap', np.nan)
            enterprise_value = info.get('enterpriseValue', np.nan)
            ebitda = info.get('ebitda', np.nan)
            fcf = info.get('freeCashflow', np.nan)
            total_debt = info.get('totalDebt', np.nan)
            total_cash = info.get('totalCash', np.nan)
            revenue_growth = info.get('revenueGrowth', np.nan)
            gross_margins = info.get('grossMargins', np.nan)
            insider_percent = info.get('heldPercentInsiders', np.nan)
            inst_percent = info.get('heldPercentInstitutions', np.nan)
            
            if pd.isna(ebitda) or ebitda <= 0:
                continue # Skip companies losing money at the EBITDA level
                
            # Derived Metrics for Machine Learning Features
            ev_to_ebitda = enterprise_value / ebitda if ebitda else np.nan
            fcf_yield = fcf / enterprise_value if enterprise_value and fcf else np.nan
            debt_to_ebitda = total_debt / ebitda if ebitda else np.nan
            
            # --- V2.0: DISCOUNTED CASH FLOW (DCF) INTRINSIC VALUATION ENGINE ---
            intrinsic_value = np.nan
            discount_to_intrinsic = np.nan
            
            if pd.notna(fcf) and fcf > 0:
                wacc = 0.09 # Assume 9% Weighted Average Cost of Capital
                terminal_growth = 0.025 # 2.5% Terminal Growth Rate
                proj_growth = revenue_growth if pd.notna(revenue_growth) and revenue_growth > 0 else 0.05
                
                # Project FCF out 5 years
                projected_fcfs = [fcf * ((1 + proj_growth) ** year) for year in range(1, 6)]
                
                # Discount projected FCFs to Present Value
                pv_fcfs = sum([cf / ((1 + wacc) ** year) for year, cf in enumerate(projected_fcfs, 1)])
                
                # Calculate Terminal Value and discount it
                terminal_value = (projected_fcfs[-1] * (1 + terminal_growth)) / (wacc - terminal_growth)
                pv_terminal = terminal_value / ((1 + wacc) ** 5)
                
                # Total Intrinsic Enterprise Value
                intrinsic_value = pv_fcfs + pv_terminal
                
                # Calculate Discount (Positive % means it is undervalued)
                if pd.notna(enterprise_value) and enterprise_value > 0:
                    discount_to_intrinsic = (intrinsic_value - enterprise_value) / intrinsic_value
            
            data_records.append({
                'Ticker': ticker,
                'Sector': info.get('sector', 'Unknown'),
                'Market_Cap': market_cap,
                'Enterprise_Value': enterprise_value,
                'EBITDA': ebitda,
                'Free_Cash_Flow': fcf,
                'EV/EBITDA': ev_to_ebitda,
                'FCF_Yield': fcf_yield,
                'Debt/EBITDA': debt_to_ebitda,
                'Revenue_Growth': revenue_growth,
                'Gross_Margins': gross_margins,
                'Insider_Ownership': insider_percent,
                'Institutional_Ownership': inst_percent,
                'Intrinsic_Value': intrinsic_value,
                'Discount_to_Intrinsic': discount_to_intrinsic
            })
            
            time.sleep(0.5) # Respect API limits
            
        except Exception as e:
            print(f"Error extracting {ticker}: {e}")
            
    df = pd.DataFrame(data_records)
    df.to_csv("ma_fundamental_dataset.csv", index=False)
    print(f"\nPipeline Complete. Extracted fundamental data for {len(df)} companies.")
    print("Dataset saved to 'ma_fundamental_dataset.csv'. Ready for ML Training Phase.")

if __name__ == "__main__":
    # A massive basket of 100+ mid-cap companies (Prime PE Targets) to flood the dashboard
    ticker_str = "AAN AAON ABG ABM ACA ACCO ACHC ACIW ADTN AEIS AEO AGCO ALEX ALG ALGT ALRM AMWD ANF APAM APPN ARCB AROC ARRY ASGN ASTE ATEN ATGE ATKR ATNI ATRO AVA AVAV AVNT AWR AXS AYI AZEK AZZ BANC BANF BANR BCC BCPC BDN BHLB BHR BKE BKH BKU BLD BLDR BLMN BMRC BOH BOOT BPOP BRBR BRO BRSP BRY BSIG BUSE BXC CADE CAKE CAL CALM CAMP CASS CATC CATY CBAN CBU CCBG CNO CNOB CPTA CRVL CSWC CTBI CTRE CUBI CVI CWBC CWCO CXW CROX YELP ETSY PINS ZBRA WEN SHAK MSTR PLTR SOFI ROKU DOCU TWLO ZION CMA FHN SNX ARW"
    target_list = ticker_str.split()
    build_ma_dataset(target_list)
