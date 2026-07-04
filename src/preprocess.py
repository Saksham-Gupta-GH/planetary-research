import pandas as pd
import numpy as np
import sys, os
# Ensure the src directory is in the Python path for local imports
sys.path.append(os.path.dirname(__file__))
from data_loader import load_exoplanet_data
from sklearn.impute import KNNImputer
from scipy import stats

def filter_mandatory(df: pd.DataFrame, required_columns: list) -> pd.DataFrame:
    """Drop rows missing any of the required columns."""
    return df.dropna(subset=required_columns)

def impute_knn(df: pd.DataFrame, n_neighbors: int = 5) -> pd.DataFrame:
    """Impute missing values using KNN imputer (numeric columns only)."""
    numeric = df.select_dtypes(include=[np.number])
    imputer = KNNImputer(n_neighbors=n_neighbors)
    imputed_array = imputer.fit_transform(numeric)
    df[numeric.columns] = imputed_array
    return df

def remove_outliers_zscore(df: pd.DataFrame, z_thresh: float = 3.0) -> pd.DataFrame:
    """Remove rows where any numeric feature has a Z‑score beyond the threshold."""
    numeric = df.select_dtypes(include=[np.number])
    z_scores = np.abs(stats.zscore(numeric, nan_policy='omit'))
    mask = (z_scores < z_thresh).all(axis=1)
    return df[mask]

if __name__ == "__main__":
    # Example pipeline usage
    df = load_exoplanet_data()
    required = ["pl_name", "pl_orbper", "pl_rade", "pl_bmasse", "st_teff", "st_rad", "st_mass", "st_logg", "st_lum", "st_age", "st_metfe"]
    df = filter_mandatory(df, required)
    df = impute_knn(df)
    df = remove_outliers_zscore(df)
    df.to_csv("data/clean_exoplanet_data.csv", index=False)
    print("Preprocessed data saved.")
