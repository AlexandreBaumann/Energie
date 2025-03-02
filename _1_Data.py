import pandas as pd
from pyexcel_ods3 import save_data
from collections import OrderedDict

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])
    return df

def compute_generation(df, enr_types):
    result = pd.DataFrame({"utc_timestamp": df["utc_timestamp"]})
    
    for enr in enr_types:
        enr_columns = [col for col in df.columns if enr in col]
        result[enr] = df[enr_columns].sum(axis=1)
    
    result["total_generation"] = result[enr_types].sum(axis=1)
    
    load_columns = [col for col in df.columns if "load_actual_entsoe_transparency" in col]
    result["total_load"] = df[load_columns].sum(axis=1)
    
    result["renewable_percentage"] = (result["total_generation"] / result["total_load"]) * 100
    result["year"] = result["utc_timestamp"].dt.year
    
    return result

def compute_capacity(result, enr_types):
    capacity_df = pd.DataFrame()
    capacity_df["Année"] = sorted(result["year"].unique())
    
    for enr in enr_types:
        capacity_df[f"{enr} (MW)"] = [result[result["year"] == year][enr].max() for year in capacity_df["Année"]]
    
    capacity_df["Total (MW)"] = capacity_df[[f"{enr} (MW)" for enr in enr_types]].sum(axis=1)
    
    # Calcul de la capacité installée théorique nécessaire
    min_renewable_percentage = [result[result["year"] == year]["renewable_percentage"].min() / 100 for year in capacity_df["Année"]]
    capacity_df["Capacité théorique requise (MW)"] = capacity_df["Total (MW)"] / min_renewable_percentage
    
    return capacity_df

def save_to_ods(result, capacity_df, file_name="enr_generation_summary.ods"):
    ods_data = OrderedDict()
    ods_data["Données ENR"] = [result.columns.tolist()] + result.astype(str).values.tolist()
    ods_data["Capacités Installées"] = [capacity_df.columns.tolist()] + capacity_df.values.tolist()
    save_data(file_name, ods_data)

def process_energy_data(file_path):
    enr_types = ["solar_generation_actual", "wind_onshore_generation_actual", "wind_offshore_generation_actual"]
    df = load_data(file_path)
    result = compute_generation(df, enr_types)
    capacity_df = compute_capacity(result, enr_types)
    save_to_ods(result, capacity_df)
    return result