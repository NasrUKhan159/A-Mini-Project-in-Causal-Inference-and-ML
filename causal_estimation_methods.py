"""
Script for applying causal estimation methods to the following 2 datasets:
Vanguard High Dividend Yield Fund (VYM) (Higher dividend yield fund) and XGIU.L Global Inflation Linked Bond and look at
causal relations between both, and see whether the standard causal estimation methods work or not.
(Data from 1 July 2019 to 30 June 2023)
Data Sourced from Yahoo Finance (finance.yahoo.com)
Need dowhy version 0.8
"""
from dowhy import CausalModel
from data_processing import process_data

if __name__ == "__main__":
    data_filtered_nodate = process_data()
    # Adj_Close_VYM is the outcome variable
    treatment_avg = data_filtered_nodate[data_filtered_nodate.treatment == True]['Adj_Close_VYM'].mean()
    cntrl_avg = data_filtered_nodate[data_filtered_nodate.treatment == False]['Adj_Close_VYM'].mean()
    print(f"The naive estimate for the average treatment effect of the adjusted closing price for Vanguard fund is "
          f"{treatment_avg - cntrl_avg}")

    model = CausalModel(data=data_filtered_nodate, treatment='treatment', outcome='Adj_Close_VYM')
    # Get the estimand
    estimand = model.identify_effect()
    print(estimand)
    # the estimand output we get:
    #     Estimand
    #     type nonparametric - ate
    #
    #     ### Estimand : 1
    #     Estimand
    #     name: backdoor
    #     Estimand
    #     expression:
    #     d
    # ────────────(E[Adj_Close_VYM])
    # d[treatment]
    # Estimand
    # assumption
    # 1, Unconfoundedness: If
    # U→{treatment} and U→Adj_Close_VYM
    # then
    # P(Adj_Close_VYM | treatment,, U) = P(Adj_Close_VYM | treatment, )
