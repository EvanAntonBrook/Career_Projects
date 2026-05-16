import yfinance as yf
import pandas as pd
import numpy as np
import time

def run_lbo_screener(tickers):
    results = []
    
    print("Initializing Titan LBO Deal Sourcing Engine...")
    
    for ticker in tickers:
        print(f"Scraping financial data for {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract key valuation metrics
            market_cap = info.get('marketCap', 0)
            total_debt = info.get('totalDebt', 0)
            total_cash = info.get('totalCash', 0)
            ebitda = info.get('ebitda', 0)
            fcf = info.get('freeCashflow', 0)
            
            if ebitda <= 0 or market_cap == 0:
                print(f"  [!] Skipping {ticker}: Negative EBITDA or missing data.")
                continue
                
            # Enterprise Value Calculation
            enterprise_value = market_cap + total_debt - total_cash
            ev_ebitda_multiple = enterprise_value / ebitda
            
            # --- LBO MATH ENGINE ---
            # Assume PE firm buys the company at current EV
            entry_multiple = ev_ebitda_multiple
            
            # Max debt a bank will lend is typically 4.0x EBITDA
            max_debt = ebitda * 4.0
            
            # If current EV is lower than max debt, PE firm can buy it with very little equity (highly unlikely in public mkts, but good for screening)
            # Realistic Equity Check = Purchase Price (EV) - Debt Used
            debt_used = min(max_debt, enterprise_value * 0.6) # Cap debt at 60% of purchase price
            equity_check = enterprise_value - debt_used
            
            if equity_check <= 0:
                continue
                
            # 5-Year Projection (Assuming 5% annual EBITDA growth)
            year_5_ebitda = ebitda * (1.05 ** 5)
            
            # Assume 50% of Free Cash Flow is used to pay down debt over 5 years
            total_cash_generated = fcf * 5
            debt_paid_down = min(total_cash_generated * 0.5, debt_used)
            ending_debt = debt_used - debt_paid_down
            
            # Exit Valuation (Assuming we sell at the same multiple we bought it for)
            exit_enterprise_value = year_5_ebitda * entry_multiple
            exit_equity_value = exit_enterprise_value - ending_debt
            
            # Return Calculations
            multiple_on_money = exit_equity_value / equity_check
            # CAGR formula for 5 years: (Ending Value / Beginning Value) ^ (1/5) - 1
            irr = (multiple_on_money ** (1/5)) - 1
            
            results.append({
                'Ticker': ticker,
                'Sector': info.get('sector', 'N/A'),
                'EV / EBITDA': round(ev_ebitda_multiple, 2),
                'EBITDA ($B)': round(ebitda / 1e9, 2),
                'Equity Check ($B)': round(equity_check / 1e9, 2),
                'Projected IRR': round(irr * 100, 2),
                'MoM (Multiple on Money)': round(multiple_on_money, 2)
            })
            
            # Sleep to respect Yahoo Finance API limits
            time.sleep(1)
            
        except Exception as e:
            print(f"  [X] Error processing {ticker}: {e}")
            
    # Convert to DataFrame and sort by best IRR
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values(by='Projected IRR', ascending=False).reset_index(drop=True)
        df.to_csv("Titan_LBO_Targets.csv", index=False)
        print("\nScreening Complete. Results saved to 'Titan_LBO_Targets.csv'.")
        print("\nTop 5 Buyout Targets:")
        print(df.head(5).to_string())
    else:
        print("No valid LBO targets found in this batch.")

if __name__ == "__main__":
    # A list of mid-cap to large-cap tech, industrial, and consumer stocks to screen
    target_list = ['YELP', 'GPRO', 'DBX', 'FSLR', 'PINS', 'ETSY', 'ZBRA', 'CROX', 'WEN', 'SHAK']
    run_lbo_screener(target_list)
