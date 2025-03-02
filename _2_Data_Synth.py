import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])
    return df

def compute_annual_statistics(df, enr_types):
    df["year"] = df["utc_timestamp"].dt.year
    
    annual_stats = df.groupby("year").agg({
        **{enr: "max" for enr in enr_types},  # Capacité installée (MW)
        "renewable_percentage": "mean"  # Moyenne annuelle de % ENR
    }).reset_index()
    
    annual_stats["Total (MW)"] = annual_stats[enr_types].sum(axis=1)  # Somme des capacités
    return annual_stats

def process_energy_data(file_path,enr_types):
    df = load_data(file_path)
    annual_stats = compute_annual_statistics(df, enr_types)
    
    
    return annual_stats
