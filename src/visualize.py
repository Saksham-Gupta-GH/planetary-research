import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure output directories exist
os.makedirs('figures', exist_ok=True)

def plot_mass_radius(df: pd.DataFrame):
    """Scatter plot of planet mass vs radius with density coloring."""
    plt.figure(figsize=(8,6))
    scatter = plt.scatter(df['pl_bmasse'], df['pl_rade'], c=df['habitability_score'], cmap='viridis', alpha=0.7)
    plt.xlabel('Planet Mass (Earth Masses)')
    plt.ylabel('Planet Radius (Earth Radii)')
    plt.title('Mass vs Radius colored by Habitability Score')
    cbar = plt.colorbar(scatter)
    cbar.set_label('Habitability Score')
    plt.tight_layout()
    plt.savefig('figures/mass_radius.png', dpi=300)
    plt.close()

def plot_score_distribution(df: pd.DataFrame):
    """Histogram of habitability scores."""
    plt.figure(figsize=(8,4))
    sns.histplot(df['habitability_score'], bins=30, kde=True)
    plt.xlabel('Habitability Score')
    plt.title('Distribution of Habitability Scores')
    plt.tight_layout()
    plt.savefig('figures/score_distribution.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    # Load the scored data
    scored_path = 'data/scored_exoplanet_data.csv'
    if not os.path.exists(scored_path):
        raise FileNotFoundError(f"Scored data not found at {scored_path}. Run the scoring script first.")
    df = pd.read_csv(scored_path)
    plot_mass_radius(df)
    plot_score_distribution(df)
    print('Figures saved to figures/ directory.')
