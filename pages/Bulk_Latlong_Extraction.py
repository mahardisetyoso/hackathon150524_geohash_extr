import folium
import pandas as pd
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium
from polygeohasher import polygeohasher
from shapely.geometry import Polygon
from shapely.geometry import Point

try:
    CENTER_START = [-6.189991467509655, 106.84617273604809]

    #TO DEFINE SESSION STATE
    if "center" not in st.session_state:
        st.session_state["center"] = [-6.189991467509655, 106.84617273604809]

    uploaded_files = st.file_uploader("Choose a CSV file , Other than that will cause major ERROR and Please rename your latlong column using this name latiude and longitude!!", accept_multiple_files=False)
    button = st.number_input('Insert a Geohash number')
    number = int(button)
    df = pd.read_csv(uploaded_files)
    geometry = [Point(x, y) for x, y in zip(df['longitude'], df['latitude'])]
    gpd_geom = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    geohash_gdf = polygeohasher.create_geohash_list(gpd_geom, number,inner=False)
    geohash_gdf_list = polygeohasher.geohashes_to_geometry(geohash_gdf,"geohash_list")
    gpd_geohash_geom = gpd.GeoDataFrame(geohash_gdf_list, geometry=geohash_gdf_list['geometry'], crs="EPSG:4326")
    geojson_geohash = gpd_geohash_geom.to_json()
    m = folium.Map(location=st.session_state["center"],zoom_start=12)
    folium.GeoJson(
        geojson_geohash, 
        name="geohash",
        style_function = lambda x: {
            'color': 'red',
            'weight': 4,
            'interactive' : True
        }).add_to(m)
    st_folium(m, width=1200, height=800)
except (TypeError, NameError, AttributeError):
    pass
save = st.text_input('Write you files name here and press ENTER!!')
csv=gpd_geohash_geom.to_csv()
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=save + '.csv',
    mime='text/csv',
)
file_geojson = gpd_geohash_geom.to_json()
st.download_button(
     label="Download data as JSON",
     data=file_geojson,
     file_name=save + '.geojson',
  )