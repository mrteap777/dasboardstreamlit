dasboardstreamlit
dashboard
streamlit code
import pandas as pd

# Предположим, что у вас есть DataFrame с исходными данными
data = {
    'line': [1, 1, 2, 2],
    'station': ['A', 'B', 'A', 'B'],
    'hour': [8, 9, 8, 9],
    'num_passenger': [20, 15, 25, 10]
}
df = pd.DataFrame(data)

# Создаем новый DataFrame с уникальными маршрутами
unique_routes = df.groupby(['station']).size().reset_index().rename(columns={0: 'count'})
unique_routes['route'] = unique_routes['station']

# Отобразим уникальные маршруты
print(unique_routes[['route']])
