import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering

def run_clustering_pipeline(df, features):
    """Executes PCA and dual clustering to isolate the Terrestrial cluster."""
    # 1. Log transformations for skewed data
    skewed_features = ['pl_bmasse', 'pl_rade', 'pl_insol', 'pl_orbper']
    for feat in skewed_features:
        if feat in features:
            df[f'log_{feat}'] = np.log1p(df[feat])
            
    # Swap out original features for log features in the feature list
    cluster_features = [f'log_{x}' if x in skewed_features else x for x in features]
    
    # 2. Extract matrix and handle remaining NaNs (KNN Imputation assumed prior)
    X = df[cluster_features].values
    
    # 3. Standard Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. PCA Orthogonalization (Targeting 85% variance)
    pca = PCA(n_components=0.85)
    X_pca = pca.fit_transform(X_scaled)
    print(f"PCA reduced space to {X_pca.shape} components.")
    
    # 5. K-Means Clustering (k=5 based on elbow method)
    kmeans = KMeans(n_clusters=5, init='k-means++', n_init=20, random_state=42)
    df['KMeans_Cluster'] = kmeans.fit_predict(X_pca)
    
    # 6. Agglomerative Clustering for Cross-Validation on SAME PCA SPACE
    ward = AgglomerativeClustering(n_clusters=5, linkage='ward')
    df['Ward_Cluster'] = ward.fit_predict(X_pca)
    
    return df, scaler, pca, kmeans
