import pandas as pd
import numpy as np

def check_kopparapu_hz(row):
    """Determines if a planet falls in the Conservative or Optimistic HZ."""
    teff = row['st_teff']
    insol = row['pl_insol']
    
    if pd.isna(teff) or pd.isna(insol):
        return 'Unknown'
        
    t_star = teff - 5780
    
    # Polynomial limits (S_eff)
    recent_venus = 1.776 + 2.136e-4*t_star + 2.533e-8*(t_star**2) - 1.332e-11*(t_star**3) - 3.097e-15*(t_star**4)
    runaway_gh = 1.107 + 1.332e-4*t_star + 1.580e-8*(t_star**2) - 8.308e-12*(t_star**3) - 1.931e-15*(t_star**4)
    max_gh = 0.356 + 6.19e-4*t_star + 1.37e-8*(t_star**2) - 4e-11*(t_star**3) - 2e-15*(t_star**4)
    early_mars = 0.320 + 5.54e-4*t_star + 1.09e-8*(t_star**2) - 3e-11*(t_star**3) - 1e-15*(t_star**4)
    
    if max_gh <= insol <= runaway_gh:
        return 'Conservative HZ'
    elif early_mars <= insol <= recent_venus:
        return 'Optimistic HZ'
    return 'Outside HZ'

def calculate_esi(row):
    """Calculates the Earth Similarity Index (ESI) based on Schulze-Makuch (2011)."""
    # Earth reference values
    ref = {'R': 1.0, 'rho': 5.51, 'vesc': 11.18, 'T': 288.0}
    weights = {'R': 0.57, 'rho': 1.07, 'vesc': 0.70, 'T': 2.26}
    
    # Extract planet values
    R = row['pl_rade']
    rho = row['pl_dens'] if pd.notna(row['pl_dens']) else (row['pl_bmasse'] / (R**3)) * 5.51
    vesc = np.sqrt(row['pl_bmasse'] / R) * 11.18 if pd.notna(row['pl_bmasse']) else np.nan
    T = row['pl_eqt']
    
    if any(pd.isna(x) for x in [R, rho, vesc, T]):
        return np.nan
        
    # Calculate geometric distance components
    esi_R = (1 - abs((R - ref['R']) / (R + ref['R']))) ** weights['R']
    esi_rho = (1 - abs((rho - ref['rho']) / (rho + ref['rho']))) ** weights['rho']
    esi_vesc = (1 - abs((vesc - ref['vesc']) / (vesc + ref['vesc']))) ** weights['vesc']
    esi_T = (1 - abs((T - ref['T']) / (T + ref['T']))) ** weights['T']
    
    total_weight = sum(weights.values())
    esi_global = (esi_R * esi_rho * esi_vesc * esi_T) ** (1 / total_weight)
    
    return esi_global
