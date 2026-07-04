import pandas as pd
import numpy as np

def impute_chen_kipping(row):
    """Imputes missing radius or mass using Chen & Kipping (2017) piecewise power laws."""
    mass = row['pl_bmasse']
    radius = row['pl_rade']
    
    if pd.isna(radius) and pd.notna(mass):
        log_m = np.log10(mass)
        if mass < 2.04:
            radius = 10**(0.00346 + 0.2790 * log_m)
        elif mass < 132:
            radius = 10**(-0.0925 + 0.589 * log_m)
        elif mass < 26600:
            radius = 10**(1.25 - 0.044 * log_m)
        else:
            radius = 10**(-2.85 + 0.881 * log_m)
        row['pl_rade'] = radius
    elif pd.isna(mass) and pd.notna(radius):
        log_r = np.log10(radius)
        if radius < 1.23: # Approx boundary for M < 2.04
            mass = 10**((log_r - 0.00346) / 0.2790)
        elif radius < 11.1:
            mass = 10**((log_r + 0.0925) / 0.589)
        else:
            mass = 10**((log_r - 1.25) / -0.044) # Simplified Jovian inversion
        row['pl_bmasse'] = mass
    return row

def rectify_thermal_anomalies(df, albedo=0.3):
    """Recalculates Teq to fix archive anomalies (e.g., Kepler-186 f at 697K)."""
    # Recalculate Teq based on Insolation assuming Earth-like Bond albedo
    calculated_teq = 278.0 * (df['pl_insol'])**0.25 * ((1 - albedo)/(1 - 0.3))**0.25
    
    # If archive Teq deviates by more than 50K from physical expectation, overwrite
    anomaly_mask = np.abs(df['pl_eqt'] - calculated_teq) > 50
    df.loc[anomaly_mask, 'pl_eqt'] = calculated_teq[anomaly_mask]
    return df
