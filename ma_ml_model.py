import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

def run_ml_training():
    print("Initializing Quantitative M&A Machine Learning Model...")
    
    try:
        # Load the fundamental data generated in Phase 1
        df = pd.read_csv("ma_fundamental_dataset.csv")
    except FileNotFoundError:
        print("Error: ma_fundamental_dataset.csv not found. Please run buyout_data_pipeline.py first.")
        return

    # Drop rows with missing crucial data
    df = df.dropna(subset=['EV/EBITDA', 'FCF_Yield', 'Debt/EBITDA'])
    
    print(f"Data loaded successfully. {len(df)} institutional equities available for analysis.")

    # --- SYNTHETIC TRAINING DATA GENERATION ---
    # For MVP purposes without access to $20k/yr Pitchbook historical M&A data,
    # we algorithmically label companies as "Prime Targets" (1) based on standard PE criteria:
    # High FCF Yield, Low Debt, Solid Gross Margins.
    print("Generating training labels based on historical Private Equity acquisition heuristics...")
    
    def label_target(row):
        score = 0
        if row['FCF_Yield'] > 0.05: score += 1
        if row['Debt/EBITDA'] < 3.0: score += 1
        if row['EV/EBITDA'] < 15.0: score += 1
        if row['Insider_Ownership'] > 0.05: score += 1
        return 1 if score >= 3 else 0

    df['Historical_Target'] = df.apply(label_target, axis=1)

    # --- MACHINE LEARNING PREPARATION ---
    features = ['Market_Cap', 'EV/EBITDA', 'FCF_Yield', 'Debt/EBITDA', 'Gross_Margins', 'Insider_Ownership']
    
    # Fill remaining NaNs with median values
    for col in features:
        df[col] = df[col].fillna(df[col].median())

    X = df[features]
    y = df['Historical_Target']

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # --- RANDOM FOREST CLASSIFIER ---
    print("Training Random Forest Classifier on fundamental parameters...")
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Model Training Complete. Out-of-sample Accuracy: {accuracy * 100:.2f}%")

    # --- PREDICTION GENERATION ---
    print("Deploying model to predict forward-looking acquisition probabilities...")
    probabilities = model.predict_proba(X_scaled)[:, 1]
    df['Buyout_Probability'] = probabilities

    # Sort by highest probability
    df_results = df.sort_values(by='Buyout_Probability', ascending=False)
    
    # Save the predictions
    df_results.to_csv("ma_ml_predictions.csv", index=False)
    print("\nPredictions saved to 'ma_ml_predictions.csv'.")
    print("\nTop 5 Predictive Acquisition Targets:")
    top_5 = df_results[['Ticker', 'Sector', 'Buyout_Probability', 'EV/EBITDA', 'FCF_Yield']].head(5)
    
    for index, row in top_5.iterrows():
        print(f"  - {row['Ticker']} ({row['Sector']}): {row['Buyout_Probability']*100:.1f}% Probability")

if __name__ == "__main__":
    run_ml_training()
