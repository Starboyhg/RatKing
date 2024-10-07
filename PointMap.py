import pandas as pd
import folium
from folium.plugins import HeatMap
from folium.plugins import TimestampedGeoJson


df = pd.read_csv('/content/Rats__Heat_Map-2021-2024.csv')

df['Created Date'] = pd.to_datetime(df['Created Date'])

fecha_inicio = '2023-10-04 00:00:00'
fecha_fin = '2024-10-04 11:59:00'
df_filtrado = df[(df['Created Date'] >= fecha_inicio) & (df['Created Date'] <= fecha_fin)]
df_filtrado = df_filtrado.dropna(subset=['Latitude', 'Longitude'])


m = folium.Map(location=[df_filtrado['Latitude'].mean(), df_filtrado['Longitude'].mean()], zoom_start=10)


fechas_unicas = df_filtrado['Created Date'].dt.date.unique()
fechas_unicas.sort()


features = []
heat_data = []

for fecha in fechas_unicas:
    grupo_fecha = df_filtrado[df_filtrado['Created Date'].dt.date == fecha]
    for index, row in grupo_fecha.iterrows():
        heat_data.append([row['Longitude'], row['Latitude'], 1])  

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['Longitude'], row['Latitude']],
            },
            'properties': {
                'time': row['Created Date'].strftime('%Y-%m-%d %H:%M:%S'),  
                'popup': f"{row['Incident Address']} ({fecha})"  
            }
        }
        features.append(feature)


geojson = {
    'type': 'FeatureCollection',
    'features': features
}


heat_map = folium.FeatureGroup(name='Mapa de Calor')
HeatMap(heat_data, radius=15).add_to(heat_map)  
heat_map.add_to(m)


TimestampedGeoJson(
    {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [row['Longitude'], row['Latitude']],
                },
                'properties': {
                    'time': row['Created Date'].strftime('%Y-%m-%d %H:%M:%S'),  # Convertir a string
                }
            } for _, row in df_filtrado.iterrows()
        ]
    },
    period='PT1M',
    add_last_point=True,
    min_speed=1,
    max_speed=1,
).add_to(m)


folium.LayerControl().add_to(m)


m.save('mapa_calor_creciente_eventos.html')
m
