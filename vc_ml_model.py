import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def run_vc_clustering():
    print("Initiating Unsupervised Machine Learning (K-Means Clustering)...")
    
    # Load synthetic startup data
    df = pd.read_csv("vc_startup_data.csv")
    
    # Features for clustering: LTV:CAC Ratio, Rule of 40, Runway Months
    features = ['LTV_CAC_Ratio', 'Rule_of_40', 'Runway_Months']
    X = df[features]
    
    # Scale the data (critical for K-Means)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Unleash K-Means to find 3 distinct types of startups
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster_ID'] = kmeans.fit_predict(X_scaled)
    
    # Dynamically label the clusters based on their characteristics
    # We find the cluster with the highest LTV:CAC and call it High-Conviction Assets
    cluster_means = df.groupby('Cluster_ID')['LTV_CAC_Ratio'].mean()
    high_conviction_cluster = cluster_means.idxmax()
    
    # We find the cluster with the lowest runway and call it Cash Burners
    runway_means = df.groupby('Cluster_ID')['Runway_Months'].mean()
    burner_cluster = runway_means.idxmin()
    
    # The remaining cluster is Zombies
    zombie_cluster = [c for c in [0, 1, 2] if c not in [high_conviction_cluster, burner_cluster]][0]
    
    # Apply labels
    label_map = {
        high_conviction_cluster: 'Tier 1: High Conviction',
        burner_cluster: 'Tier 2: Capital Intensive',
        zombie_cluster: 'Tier 3: Growth Stagnation'
    }
    df['AI_Classification'] = df['Cluster_ID'].map(label_map)
    
    # Save the clustered data
    df.to_csv("vc_ml_predictions.csv", index=False)
    print("Unsupervised Clustering Complete. Assigned 2,000 startups to risk tranches.")
    print("Data saved to 'vc_ml_predictions.csv'.")

if __name__ == "__main__":
    run_vc_clustering()
