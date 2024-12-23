"""
Process Vanguard High Dividend Yield Fund (VYM) (Higher dividend yield fund) and XGIU.L Global Inflation Linked Bond data
"""

import pandas as pd
import numpy as np

def process_data(vanguard_file: str = "VYM.csv", inflation_bond_file: str = "XGIU_L.csv") -> pd.DataFrame:
    VYM = pd.read_csv(vanguard_file)
    XGIU_L = pd.read_csv(inflation_bond_file)
    # some preprocessing
    VYM = VYM.rename(columns={'Adj Close': 'Adj_Close_VYM', 'Volume': 'Volume_VYM'})
    XGIU_L = XGIU_L.rename(columns={'Adj Close': 'Adj_Close_XGIU_L', 'Volume': 'Volume_XGIU_L'})
    # some more preprocessing
    data = pd.merge(VYM, XGIU_L, on='Date', how='outer')
    data = data.dropna()
    data = data[data.Volume_XGIU_L != 0]
    # Extract cols of interest
    data_filtered = data[['Date', 'Adj_Close_VYM', 'Volume_VYM', 'Adj_Close_XGIU_L', 'Volume_XGIU_L']]
    # We are interested in Adj_Close_VYM as the outcome variable and the other 3 variables as the explanatory variables.
    # Observations are assigned to the treatment group if |Adj_Close_XGIU_L / Volume_XGIU_L| <= mean(Adj_Close_XGIU_L / Volume_XGIU_L)
    data_filtered['treatment'] = np.where(
        data_filtered['Adj_Close_XGIU_L'] <= np.mean(data_filtered['Adj_Close_XGIU_L']), True, False)
    # Let's also set a time index which may be used as one of our causal variables
    data_filtered = data_filtered.reset_index(drop=True)
    data_filtered['time'] = data_filtered.index + 1
    # drop the date column so that we can feed the whole dataframe into a CausalModel object to be instantiated
    data_filtered_nodate = data_filtered.drop(columns=['Date'])
    # data_filtered_nodate.treatment.value_counts()
    # the output of the above line should give:
    # False    329
    # True     267
    # Hence the classes are balanced
    return data_filtered_nodate
