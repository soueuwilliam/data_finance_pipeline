import pandas as pd
from data import data


data = data()

bank_stocks = ["ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "SANB11.SA", "BPAC11.SA"]
df_final = pd.DataFrame()

for stock in bank_stocks:
    df_temp = data.get_data_ticker(ticker=stock)
    df_final = pd.concat([df_final, df_temp], ignore_index=True)
    
print(df_final)

