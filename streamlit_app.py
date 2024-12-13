import streamlit as st
st.cache_resource.clear()
import folium
from streamlit_folium import st_folium
from datetime import date
import requests

# Configurar la aplicación
st.title("Descarga de Imágenes NDVI")
st.subheader("Dibuja un polígono y selecciona el rango de fechas")

# Configurar mapa inicial
m = folium.Map(location=[-34.6, -58.4], zoom_start=6)
folium.TileLayer('OpenStreetMap').add_to(m)
folium.LayerControl().add_to(m)

draw_control = folium.plugins.Draw(export=True)
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
        st.success("Imágenes descargadas correctamente.")
    else:
        st.error("Por favor, dibuja un polígono antes de descargar.")
