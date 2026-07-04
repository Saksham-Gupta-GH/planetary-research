import pandas as pd
import numpy as np
from scipy.stats import norm

# Reference Earth values for habitability features (example values)
EARTH_REF = {
    "pl_rade": 1.0,  # Earth radii
    "pl_bmasse": 1.0,  # Earth masses
    "st_teff": 5778,  # K
    "st_lum": 1.0,  # Solar luminosities
    # Add more features as needed
}

def gaussian_score(row: pd.Series, feature_weights: dict = None) -> float:
    """Calculate a habitability score for an exoplanet row using Gaussian distributions.

    Each feature is compared to the Earth reference value with a Gaussian probability density.
    The overall score is the product (or weighted sum) of individual probabilities.
    """
    if feature_weights is None:
        # default equal weighting
        feature_weights = {k: 1.0 for k in EARTH_REF.keys()}
    scores = []
    for feature, weight in feature_weights.items()
        if feature not in row or pd.isna(row[feature]):
            continue
        # Standard deviation as a fraction of Earth value (adjustable)
        sigma = 0.2 * EARTH_REF[feature] if EARTH_REF[feature] != 0 else 0.1
        prob = norm.pdf(row[feature], loc=EARTH_REF[feature], scale=sigma)
        scores.append(weight * prob)
    if not scores:
        return 0.0
    # Combine scores (geometric mean for multiplicative effect)
    return np.prod(scores) ** (1.0 / len(scores))

def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'habitability_score' column to the DataFrame."""
    df = df.copy()
    df['habitability_score'] = df.apply(gaussian_score, axis=1)
    return df

if __name__ == "__main__":
    from data_loader import fetch_exoplanet_data
    raw_df = fetch_exoplanet_data()
    # Assume preprocessing steps have been applied and data saved
    processed_df = pd.read_csv('data/clean_exoplanet_data.csv')
    scored_df = compute_scores(processed_df)
    scored_df.to_csv('data/scored_exoplanet_data.csv', index=False)
    print('Scores computed and saved to data/scored_exoplanet_data.csv')
