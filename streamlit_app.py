import streamlit as st
st.cache_resource.clear()
import ee
import geopandas as gpd
import folium
from folium import plugins
import geopandas as gpd

# Autenticación con Google Earth Engine usando las claves almacenadas en los secretos de Streamlit
def authenticate_gee():
    private_key = st.secrets["GEE_PRIVATE_KEY"]
    project_id = st.secrets["GEE_PROJECT_ID"]
    client_email = st.secrets["GEE_CLIENT_EMAIL"]
    client_id = st.secrets["GEE_CLIENT_ID"]
    
    # Autenticación en Google Earth Engine usando las credenciales proporcionadas
    credentials = ee.ServiceAccountCredentials(client_email, private_key)
    ee.Initialize(credentials)

# Llamada a la función para autenticarse en Google Earth Engine
authenticate_gee()

# Título de la app
st.title("Visualización de Lotes en Google Earth Engine")

# Opción para ingresar coordenadas o cargar un archivo GeoJSON
upload_type = st.selectbox("Selecciona el tipo de entrada de datos", ["Coordenadas", "Archivo GeoJSON"])

if upload_type == "Coordenadas":
    lat = st.number_input("Latitud", min_value=-90.0, max_value=90.0, value=35.0)
    lon = st.number_input("Longitud", min_value=-180.0, max_value=180.0, value=-60.0)
else:
    uploaded_file = st.file_uploader("Sube tu archivo GeoJSON", type=["geojson"])
    if uploaded_file is not None:
        # Cargar archivo GeoJSON
        gdf = gpd.read_file(uploaded_file)
        st.write(gdf)

# Mostrar la ubicación en un mapa interactivo
if upload_type == "Coordenadas":
    map_center = [lat, lon]
else:
    map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]

# Crear mapa de Folium
m = folium.Map(location=map_center, zoom_start=12)

# Agregar marcadores según el tipo de entrada
if upload_type == "Coordenadas":
    folium.Marker([lat, lon], popup="Lote").add_to(m)
elif upload_type == "Archivo GeoJSON":
    folium.GeoJson(gdf).add_to(m)

# Mostrar el mapa en Streamlit
folium_static(m)

# Agregar plugin para dibujar
draw = plugins.Draw(export=True)
draw.add_to(m)

st.write("Usa la herramienta para dibujar un lote en el mapa.")
