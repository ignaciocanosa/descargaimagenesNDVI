import streamlit as st
st.cache_resource.clear()
import folium
from streamlit_folium import st_folium
import geemap
import ee
from folium.plugins import Draw

# Autenticarte con GEE (esto solo es necesario la primera vez)
# ee.Authenticate() 

# Iniciar la sesión de GEE
ee.Initialize()

# Configurar la aplicación
st.title("Descarga de Imágenes NDVI desde GEE")
st.subheader("Dibuja un polígono y selecciona el rango de fechas")

# Configuración de mapa con Folium
m = folium.Map(location=[-34.6, -58.4], zoom_start=6)

# Agregar herramientas de dibujo para polígono
draw_control = Draw(export=True)
m.add_child(draw_control)

# Mostrar el mapa
output = st_folium(m, width=700, height=500)

# Selección de fechas
start_date = st.date_input("Fecha de inicio", date(2023, 1, 1))
end_date = st.date_input("Fecha de fin", date(2023, 12, 31))

# Función para descargar imágenes NDVI desde GEE
def download_ndvi_image(polygon, start_date, end_date):
    # Convertir el polígono a objeto de GEE
    polygon = ee.Geometry.Polygon(polygon['coordinates'])

    # Definir las fechas de inicio y fin
    start_date_str = str(start_date)
    end_date_str = str(end_date)

    # Filtrar imagen de satélite Sentinel-2 para el periodo deseado
    collection = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(polygon) \
        .filterDate(ee.Date(start_date_str), ee.Date(end_date_str)) \
        .map(lambda image: image.normalizedDifference(['B8', 'B4']).rename('NDVI'))  # NDVI usando bandas B8 (NIR) y B4 (Red)

    # Obtener la imagen más reciente de la colección
    image = collection.median().clip(polygon)

    # Mostrar la imagen NDVI en el mapa
    vis_params = {
        'min': -1,
        'max': 1,
        'palette': ['blue', 'white', 'green']
    }

    # Añadir la imagen NDVI como capa en el mapa
    folium.TileLayer(
        tiles=image.getMapId(vis_params)['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name='NDVI',
        overlay=True,
        control=True
    ).add_to(m)

    # Retornar URL de la imagen (si se desea)
    image_url = image.getMapId(vis_params)['tile_fetcher'].url_format
    return image_url

# Botón para descargar NDVI
if st.button("Descargar NDVI"):
    if output and 'last_active_drawing' in output:
        polygon = output['last_active_drawing']['geometry']
        st.json(polygon)  # Mostrar el polígono

        # Descargar la imagen NDVI usando la función
        image_url = download_ndvi_image(polygon, start_date, end_date)
        
        # Mostrar la imagen NDVI en el app
        st.image(image_url, caption="Imagen NDVI", use_column_width=True)

        # Simular la descarga del archivo (esto debería modificarse según el flujo de datos que desees)
        file_name = st.text_input("Nombre del archivo:", "ndvi_imagen.tiff")
        with open(file_name, "w") as f:
            f.write("Simulación de archivo NDVI")
        st.success(f"Archivo guardado como {file_name}.")
    else:
        st.error("Por favor, dibuja un polígono antes de descargar.")

