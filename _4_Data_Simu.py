import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])
    return df

def compute_accumulated_production(df, enr_types):
    df = df.sort_values("utc_timestamp").copy()
    df["Accumulated Production"] = 0
    df["Accumulated Load"] = 0
    
    accumulated_production = 0
    accumulated_load = 0
    
    for i, row in df.iterrows():
        total_production = sum(row[f"{enr} Theoretical Production"] for enr in enr_types)
        accumulated_production += total_production
        accumulated_load += row["total_load"]
        
        df.at[i, "Accumulated Production"] = accumulated_production
        df.at[i, "Accumulated Load"] = accumulated_load
    
    return df

def process_accumulated_analysis(file_path, enr_types):
    df = load_data(file_path)
    df = compute_accumulated_production(df, enr_types)
    
    max_load = df["Accumulated Load"].max()
    min_load = df["Accumulated Load"].min()
    
    print(f"Max Accumulated Load: {max_load}")
    print(f"Min Accumulated Load: {min_load}")
    
    return df