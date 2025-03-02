import matplotlib.pyplot as plt
import pandas as pd


def plot_energy_data(result):
    """
    Agrège les données par mois et génère un graphique du pourcentage d'ENR dans la consommation totale.
    """
    # Agrégation par mois
    result["utc_timestamp"] = pd.to_datetime(result["utc_timestamp"])
    result.set_index("utc_timestamp", inplace=True)
    monthly_data = result.resample("M").sum()
    monthly_data["renewable_percentage"] = (monthly_data["total_generation"] / monthly_data["total_load"]) * 100

    # Création du graphique du pourcentage d'ENR
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_data.index, monthly_data["renewable_percentage"], label="Renewable Share (%)", color='blue')

    plt.xlabel("Time")
    plt.ylabel("Renewable Share (%)")
    plt.title("Monthly Renewable Energy Share in Total Consumption")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()