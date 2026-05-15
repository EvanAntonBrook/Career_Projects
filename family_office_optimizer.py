import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import warnings
warnings.filterwarnings('ignore')

def run_portfolio_optimization():
    print("Initializing Sovereign Wealth / Family Office Optimizer...")
    
    # Asset Universe for UHNWI Portfolio
    # Core Equities (SPY), Tech Growth (QQQ), Treasuries (TLT), Gold (GLD), Real Estate (VNQ)
    tickers = ['SPY', 'QQQ', 'TLT', 'GLD', 'VNQ']
    
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=5*365) # 5 years of historical data
    
    print(f"Downloading 5-year historical institutional data for: {tickers}")
    data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Close']
    
    # Calculate daily logarithmic returns
    returns = np.log(data / data.shift(1)).dropna()
    
    # Annualize returns and covariance matrix (252 trading days)
    annual_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    
    num_portfolios = 10000
    risk_free_rate = 0.04 # 4% Risk-Free Rate assumption
    
    results = np.zeros((3 + len(tickers), num_portfolios))
    
    print("Executing Monte Carlo simulations for Modern Portfolio Theory...")
    for i in range(num_portfolios):
        # Generate random weights
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights) # Normalize to 1.0 (100%)
        
        # Calculate expected return and volatility
        portfolio_return = np.sum(annual_returns * weights)
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Calculate Sharpe Ratio
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std_dev
        
        # Store results
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = sharpe_ratio
        
        # Store weights
        for j in range(len(weights)):
            results[3+j, i] = weights[j]
            
    # Create DataFrame
    columns = ['Return', 'Volatility', 'Sharpe_Ratio'] + [f'Weight_{ticker}' for ticker in tickers]
    simulations_df = pd.DataFrame(results.T, columns=columns)
    
    # Save the massive simulation dataset
    simulations_df.to_csv("fo_simulations.csv", index=False)
    
    # Find the Optimal Portfolio (Max Sharpe)
    max_sharpe_idx = simulations_df['Sharpe_Ratio'].idxmax()
    optimal_portfolio = simulations_df.iloc[max_sharpe_idx]
    
    optimal_portfolio.to_frame(name='Metrics').to_csv("fo_optimal_portfolio.csv")
    
    print("✅ Optimization Complete. 10,000 Portfolios simulated.")
    print("✅ Data saved to 'fo_simulations.csv'. Ready for Dashboarding.")

if __name__ == "__main__":
    run_portfolio_optimization()
