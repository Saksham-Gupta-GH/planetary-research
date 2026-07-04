import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering

def kmeans_clustering(df: pd.DataFrame, n_clusters: int = 5, random_state: int = 42):
    """Run K‑Means clustering on the numeric columns of the DataFrame.
    Returns the cluster labels and the fitted model.
    """
    numeric = df.select_dtypes(include=["number"]).dropna()
    model = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = model.fit_predict(numeric)
    return labels, model

def agglomerative_clustering(df: pd.DataFrame, n_clusters: int = 5, linkage: str = "ward"):
    """Run Agglomerative (hierarchical) clustering.
    Returns the cluster labels and the fitted model.
    """
    numeric = df.select_dtypes(include=["number"]).dropna()
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
    labels = model.fit_predict(numeric)
    return labels, model

if __name__ == "__main__":
    # Simple demo when run directly
    from data_loader import fetch_exoplanet_data
    df = fetch_exoplanet_data()
    # Assume preprocessing already applied
    k_labels, _ = kmeans_clustering(df)
    a_labels, _ = agglomerative_clustering(df)
    print("KMeans cluster distribution:", pd.Series(k_labels).value_counts())
    print("Agglomerative cluster distribution:", pd.Series(a_labels).value_counts())
