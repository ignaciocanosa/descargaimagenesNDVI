import streamlit as st
st.cache_resource.clear()
import folium
from streamlit_folium import st_folium
from datetime import date
import requests
from folium.plugins import Draw

# Configurar la aplicación
st.title("Descarga de Imágenes NDVI")
st.subheader("Dibuja un polígono y selecciona el rango de fechas")

# Configurar mapa inicial con vista satelital
m = folium.Map(location=[-34.6, -58.4], zoom_start=6, tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')
folium.TileLayer('Stamen Terrain', attr='&copy; Stamen Design').add_to(m)
folium.LayerControl().add_to(m)

draw_control = Draw(export=True)
m.add_child(draw_control)

# Mostrar el mapa
output = st_folium(m, width=700, height=500)

# Selección de fechas
start_date = st.date_input("Fecha de inicio", date(2023, 1, 1))
end_date = st.date_input("Fecha de fin", date(2023, 12, 31))

# Botón para procesar
if st.button("Descargar NDVI"):
    if output and 'last_active_drawing' in output:
        polygon = output['last_active_drawing']['geometry']
        st.json(polygon)  # Mostrar el polígono

        # Simulación de descarga
        file_name = st.text_input("Nombre del archivo:", "ndvi_poligono.geojson")
        with open(file_name, "w") as f:
            f.write(str(polygon))
        st.success(f"Archivo guardado como {file_name}.")
    else:
        st.error("Por favor, dibuja un polígono antes de descargar.")
        
