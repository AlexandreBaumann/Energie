#_1_DataPrep.py

import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])
    return df

def compute_generation(df, enr_types):
    result = pd.DataFrame({"utc_timestamp": df["utc_timestamp"], "year": df["utc_timestamp"].dt.year})
    
    for enr in enr_types:
        enr_columns = [col for col in df.columns if enr in col]
        result[enr] = df[enr_columns].sum(axis=1)
    
    result["total_generation"] = result[enr_types].sum(axis=1)
    result["total_load"] = df[[col for col in df.columns if "load_actual_entsoe_transparency" in col]].sum(axis=1)
    result["renewable_percentage"] = (result["total_generation"] / result["total_load"]) * 100
    
    return result 

def process_energy_data(file_path,enr_types):
    df = load_data(file_path)
    result = compute_generation(df, enr_types)
    return result 
