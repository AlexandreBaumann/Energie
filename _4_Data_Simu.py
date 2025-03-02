import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])
    return df

def compute_accumulated_balance(df, enr_types):
    df = df.sort_values("utc_timestamp").copy()
    df["Accumulated Balance"] = 0
    
    accumulated_balance = 0
    
    for i, row in df.iterrows():
        total_production = sum(row[f"{enr} Theoretical Production"] for enr in enr_types)
        balance = total_production - row["total_load"]
        accumulated_balance += balance
        
        df.at[i, "Accumulated Balance"] = accumulated_balance
    
    return df

def plot_accumulated_balance(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df["utc_timestamp"], df["Accumulated Balance"], label="Accumulated Balance", color="b")
    plt.xlabel("Time")
    plt.ylabel("Accumulated Balance (MWh)")
    plt.title("Evolution of Accumulated Balance Over Time")
    plt.legend()
    plt.grid()
    plt.show()

def process_accumulated_analysis(file_path, enr_types):
    df = load_data(file_path)
    df = compute_accumulated_balance(df, enr_types)
    
    max_balance = df["Accumulated Balance"].max()
    min_balance = df["Accumulated Balance"].min()
    
    print(f"Max Accumulated Balance: {max_balance}")
    print(f"Min Accumulated Balance: {min_balance}")
    
    plot_accumulated_balance(df)
    
    return df