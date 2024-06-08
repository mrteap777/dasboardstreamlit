import requests
import pandas as pd

df_test = pd.read_csv(r'C:\projects\API\tabular\train\test_features (1).csv')
df_json = df_test[:5].to_json()

response = requests.post('http://127.0.0.1:5000/get_gammagpt',json=df_json)
df_pred = pd.read_json(response.json())
df_pred.to_excel('example.xlsx',index=False)