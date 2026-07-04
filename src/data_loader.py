import pandas as pd
import requests
import io

def fetch_exoplanet_data():
    """Queries the NASA Exoplanet Archive TAP service for the pscomppars table."""
    tap_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    
    # ADQL query targeting confirmed planets with required features
    query = """
    SELECT pl_name, hostname, pl_rade, pl_bmasse, pl_dens, pl_eqt, pl_insol,
           pl_orbsmax, pl_orbper, pl_orbeccen, st_teff, st_rad, st_mass, st_lum, st_logg
    FROM pscomppars
    """
    
    payload = {
        "request": "doQuery",
        "lang": "ADQL",
        "query": query,
        "format": "csv"
    }
    
    print("Executing TAP Query...")
    response = requests.post(tap_url, data=payload)
    response.raise_for_status()
    
    df = pd.read_csv(io.StringIO(response.text))
    print(f"Retrieved {len(df)} confirmed exoplanets.")
    return df
