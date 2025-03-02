from _1_DataPrep import process_energy_data 
from _2_Data_Synth import process_energy_data
from _3_Data_Eva import process_energy_analysis 
from _4_Data_Simu import process_accumulated_analysis 

FileOrigin="time_series_60min_singleindex.csv"
File1="global_data.csv"
File2="annual_stats.csv"
File3="RWGlobal.csv"
File4="simu.csv"
enr_types = ["solar_generation_actual", "wind_onshore_generation_actual", "wind_offshore_generation_actual"]

# Exécution des fonctions
# data = process_energy_data(FileOrigin,enr_types)
# data.to_csv(File1, index=False)
# annual_stats = process_energy_data(File1,enr_types)
# annual_stats.to_csv(File2, index=False)
# eva_stats = process_energy_analysis (File1, File2,enr_types)
# eva_stats.to_csv(File3, index=False)
simu = process_accumulated_analysis(File3,enr_types)
simu.to_csv(File4, index=False) 
# plot_energy_data(data)
