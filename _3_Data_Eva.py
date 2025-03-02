import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])
    return df

def load_annual_stats(file_path):
    return pd.read_csv(file_path)

def compute_load_factors_and_theoretical_production(df, annual_stats, enr_types):
    df["year"] = df["utc_timestamp"].dt.year
    df = df.merge(annual_stats, on="year", suffixes=("", "_annual"))
    
    ordered_columns = []
    for enr in enr_types:
        df[f"{enr} Load Factor"] = df[enr] / df[enr + "_annual"]
        df[f"{enr} Theoretical Production"] = df[enr] / (df["renewable_percentage_annual"] / 100)
        ordered_columns.extend([enr, f"{enr} Load Factor", f"{enr} Theoretical Production"])
    
    base_columns = ["utc_timestamp", "year", "total_generation", "total_load", "renewable_percentage"]
    df = df[base_columns + ordered_columns]
    
    return df

def process_energy_analysis(file1, file2, enr_types):
    df = load_data(file1)
    annual_stats = load_annual_stats(file2)
    
    df = compute_load_factors_and_theoretical_production(df, annual_stats, enr_types)
    
    return df
