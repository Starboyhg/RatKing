import pandas as pd
import folium
from folium.plugins import HeatMap

df = pd.read_csv('/Dataset-2021-2024.csv')


df['Created Date'] = pd.to_datetime(df['Created Date'],format='mixed')

# Filtrar los datos por una fecha específica
fecha_inicio = '2023-10-01 00:00:00'
fecha_fin = '2024-10-04 11:59:00'
df_filtrado = df[(df['Created Date'] >= fecha_inicio) & (df['Created Date'] <= fecha_fin)]
df_filtrado = df_filtrado.dropna(subset=['Latitude', 'Longitude'])

m = folium.Map(location=[df['Latitude'][0], df['Longitude'][0]], zoom_start=10)

# Crear una lista de coordenadas para el mapa de calor
heat_data = [[row['Latitude'], row['Longitude']] for index, row in df_filtrado.iterrows()]

HeatMap(heat_data, radius=15).add_to(m)
