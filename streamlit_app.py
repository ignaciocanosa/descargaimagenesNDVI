import streamlit as st
import ee
import folium
from datetime import date
from streamlit_folium import st_folium

# Inicializa GEE
ee.Initialize()

# Interfaz de usuario
st.title("Visualizador de NDVI con Google Earth Engine")

# Selección de fechas
st.sidebar.header("Seleccione Periodos")
start_dates = st.sidebar.date_input("Fechas de inicio", [date(2024, 1, 15)], min_value=date(2015, 1, 1))
end_dates = st.sidebar.date_input("Fechas de fin", [date(2024, 3, 25)], min_value=date(2015, 1, 1))

# Dibujar el polígono en el mapa
st.sidebar.header("Dibuje el área")
m = folium.Map(location=[-34, -64], zoom_start=5)
st_folium(m, width=700, height=500)

# Procesar imágenes en GEE al hacer clic
if st.sidebar.button("Procesar NDVI"):
    polygon = ee.Geometry.Polygon([[
        [-65, -35], [-63, -35], [-63, -33], [-65, -33], [-65, -35]
    ]])  # Reemplazar por el polígono dibujado
    
    all_images = ee.ImageCollection([])

    for start, end in zip(start_dates, end_dates):
        images = ee.ImageCollection('COPERNICUS/S2') \
            .filterDate(str(start), str(end)) \
            .filterBounds(polygon) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5)) \
            .select(['B4', 'B8'])  # Bandas para NDVI
        all_images = all_images.merge(images)

    def add_ndvi(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi).clip(polygon)
    
    all_images = all_images.map(add_ndvi)

    # Mostrar resultados
    ndvi_params = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
    for img in all_images.toList(all_images.size()).getInfo():
        date_img = ee.Image(img).date().format('YYYY-MM-dd').getInfo()
        folium.Map.add_child(
            folium.TileLayer(
                tiles=ee.Image(img).getMapId(ndvi_params)['tile_fetcher'].url_format,
                name=f"NDVI {date_img}",
                overlay=True
            )
        )

    st_folium(m, width=700, height=500)
