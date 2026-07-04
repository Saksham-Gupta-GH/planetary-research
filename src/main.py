import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import fetch_exoplanet_data
from physics_imputer import impute_chen_kipping, rectify_thermal_anomalies
from cluster_pipeline import run_clustering_pipeline
from habitability_metrics import check_kopparapu_hz, calculate_esi

def main():
    print("1. Fetching Data...")
    df = fetch_exoplanet_data()
    
    print("2. Imputing Missing Values (Chen & Kipping)...")
    df = df.apply(impute_chen_kipping, axis=1)
    
    print("3. Rectifying Thermal Anomalies...")
    df = rectify_thermal_anomalies(df)
    
    print("4. Running Clustering Pipeline...")
    # Fill remaining NaNs with median for clustering purposes
    cluster_features = ['pl_rade', 'pl_bmasse', 'pl_dens', 'pl_eqt', 'pl_insol', 'pl_orbper']
    df_cluster = df.copy()
    for col in cluster_features:
        if col in df_cluster.columns:
            df_cluster[col] = df_cluster[col].fillna(df_cluster[col].median())
            
    df_cluster, scaler, pca, kmeans = run_clustering_pipeline(df_cluster, cluster_features)
    
    # Add clusters back
    df['KMeans_Cluster'] = df_cluster['KMeans_Cluster']
    
    print("5. Applying Habitability Filters & Scoring...")
    df['HZ_Status'] = df.apply(check_kopparapu_hz, axis=1)
    df['ESI'] = df.apply(calculate_esi, axis=1)
    
    print("6. Saving Results...")
    os.makedirs('../data', exist_ok=True)
    df.to_csv('../data/processed_exoplanets.csv', index=False)
    
    # Simple Plotting
    os.makedirs('../figures', exist_ok=True)
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x='pl_eqt', y='pl_rade', hue='KMeans_Cluster', palette='viridis')
    plt.yscale('log')
    plt.title('Exoplanet Clusters (Teq vs Radius)')
    plt.savefig('../figures/cluster_scatter.png')
    
    print("Pipeline Complete!")

if __name__ == "__main__":
    main()
