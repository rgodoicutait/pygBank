import openpyxl as xl 
import pandas as pd 

df = pd.read_excel('bancodedados.xlsx', sheet_name='Conta_Corrente')
print(df.head())