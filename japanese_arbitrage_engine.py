import pandas as pd
import numpy as np

def run_yen_carry_trade_sim(capital_usd=100_000_000):
    print(f"*** GLOBAL YIELD ARBITRAGE ENGINE (Yen Carry Trade) ***")
    print(f"Institutional Capital: ${capital_usd:,.0f}")
    
    # Current Macro Inputs (Sampled for May 2026)
    usd_rate = 0.0525 # Fed Funds Rate 5.25%
    jpy_rate = 0.0010 # BoJ Rate 0.10%
    
    spot_jpy_usd = 155.50 # 1 USD = 155.50 JPY
    forward_jpy_usd = 151.20 # 1-Year Forward Rate (Currency Hedged)
    
    # 1. THE CARRY (Interest Rate Differential)
    gross_carry = usd_rate - jpy_rate
    print(f"\n1. Interest Rate Differential (Carry): {gross_carry*100:.2f}%")
    
    # 2. THE ARBITRAGE MECHANICS
    # Step A: Borrow JPY at Japan Rate
    borrowed_jpy = capital_usd * spot_jpy_usd
    interest_on_debt = borrowed_jpy * jpy_rate
    
    # Step B: Invest in USD Treasuries
    usd_investment_yield = capital_usd * usd_rate
    
    # 3. CURRENCY HEDGING (The Arbitrage Truth)
    # To truly arbitrage, we must sell USD/buy JPY in the forward market to protect against FX volatility
    # Hedge Cost = (Forward Rate - Spot Rate) / Spot Rate
    hedge_cost = (forward_jpy_usd - spot_jpy_usd) / spot_jpy_usd
    print(f"2. Currency Hedging Cost (1-Year Forward): {hedge_cost*100:.2f}%")
    
    # 4. NET ARBITRAGE PROFIT
    net_profit_pct = gross_carry + hedge_cost
    net_profit_usd = capital_usd * net_profit_pct
    
    print("-" * 50)
    print(f"NET INSTITUTIONAL ARBITRAGE PROFIT: {net_profit_pct*100:.4f}%")
    print(f"ESTIMATED ANNUAL ALPHA: ${net_profit_usd:,.2f}")
    print("-" * 50)
    
    if net_profit_pct > 0:
        print("CONCLUSION: Arbitrage window is OPEN. Recommend institutional scale deployment.")
    else:
        print("CONCLUSION: Arbitrage window is CLOSED. Covered Interest Parity (CIP) holds.")

if __name__ == "__main__":
    run_yen_carry_trade_sim()
