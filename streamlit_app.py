import streamlit as st
st.cache_resource.clear()
from datetime import date
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
import requests
import json

# Configurar la aplicación
st.title("Descarga de Imágenes NDVI")
st.subheader("Dibuja un polígono y selecciona el rango de fechas")

# Asegúrate de tener un token de Mapbox válido
MAPBOX_TOKEN = "YOUR_MAPBOX_ACCESS_TOKEN"

# Configurar mapa inicial con la capa de relieve de Mapbox
m = folium.Map(location=[-34.6, -58.4], zoom_start=6)

# Usar Mapbox para el estilo de relieve
folium.TileLayer(
    tiles=f'https://api.mapbox.com/styles/v1/mapbox/terrain-rgb-v9/tiles/{{z}}/{{x}}/{{y}}?access_token={MAPBOX_TOKEN}',
    attr='Mapbox',
    name='Relieve',
    overlay=True,
    control=True
).add_to(m)

# Agregar herramienta para dibujar polígono
draw_control = Draw(export=True)
m.add_child(draw_control)

# Mostrar el mapa
output = st_folium(m, width=700, height=500)

# Selección de fechas
start_date = st.date_input("Fecha de inicio", date(2023, 1, 1))
end_date = st.date_input("Fecha de fin", date(2023, 12, 31))

# Función para descargar imágenes NDVI usando la API de Google Earth Engine (GEE)
def download_ndvi_image(polygon, start_date, end_date):
    # Aquí deberías realizar la autenticación y solicitud a GEE o un servicio similar.
    # Este es un ejemplo con una API simulada, reemplázalo con el código correcto para acceder a GEE.

    # Convierte el polígono a GeoJSON
    geojson_polygon = json.dumps(polygon)
    
    # Configurar la solicitud (esto es un ejemplo, consulta la documentación de GEE)
    url = "https://earthengine.googleapis.com/v1/your-endpoint"
    params = {
        "polygon": geojson_polygon,
        "start_date": start_date,
        "end_date": end_date
    }

    response = requests.post(url, json=params)
    if response.status_code == 200:
        image_url = response.json().get('image_url')
        return image_url
    else:
        st.error("Error al obtener la imagen NDVI")
        return None

# Botón para procesar la descarga de NDVI
if st.button("Descargar NDVI"):
    if output and 'last_active_drawing' in output:
        polygon = output['last_active_drawing']['geometry']
        st.json(polygon)  # Mostrar el polígono

        # Llamada a la función para descargar la imagen NDVI
        image_url = download_ndvi_image(polygon, start_date, end_date)
        
        if image_url:
            st.image(image_url, caption="Imagen NDVI", use_column_width=True)

            # Proceso de guardado (esto es una simulación, reemplazar con la lógica correcta de descarga)
            file_name = st.text_input("Nombre del archivo:", "ndvi_imagen.tiff")
