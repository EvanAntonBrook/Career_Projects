import pandas as pd
import numpy as np

def generate_startup_universe(num_startups=2000):
    print(f"Generating synthetic unit economics for {num_startups} early-stage SaaS startups...")
    
    data = []
    for i in range(num_startups):
        # Generate realistic SaaS metrics
        mrr = np.random.lognormal(mean=10, sigma=1.5) # Monthly Recurring Revenue
        arr = mrr * 12
        
        # Customer Acquisition Cost & Lifetime Value
        cac = np.random.uniform(500, 5000)
        ltv = cac * np.random.uniform(0.5, 6.0) # LTV:CAC ratio from 0.5 (terrible) to 6.0 (amazing)
        ltv_cac_ratio = ltv / cac
        
        # Margins & Growth
        gross_margin = np.random.uniform(0.30, 0.95)
        yoy_growth = np.random.uniform(-0.20, 2.50) # -20% to +250% growth
        
        # Rule of 40 (Growth % + Profit Margin %)
        operating_margin = gross_margin - np.random.uniform(0.20, 0.80)
        rule_of_40 = (yoy_growth * 100) + (operating_margin * 100)
        
        # Cash Runway
        monthly_burn = np.random.uniform(10000, 500000)
        cash_in_bank = monthly_burn * np.random.uniform(1, 36) # 1 to 36 months of runway
        runway_months = cash_in_bank / monthly_burn
        
        data.append({
            'Startup_ID': f"STP-{1000+i}",
            'ARR': arr,
            'YoY_Growth': yoy_growth,
            'Gross_Margin': gross_margin,
            'LTV_CAC_Ratio': ltv_cac_ratio,
            'Rule_of_40': rule_of_40,
            'Monthly_Burn': monthly_burn,
            'Cash_in_Bank': cash_in_bank,
            'Runway_Months': runway_months
        })
        
    df = pd.DataFrame(data)
    df.to_csv("vc_startup_data.csv", index=False)
    print("Synthetic data saved to 'vc_startup_data.csv'. Ready for K-Means Clustering.")

if __name__ == "__main__":
    generate_startup_universe(2000)
