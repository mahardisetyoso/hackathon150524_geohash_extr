import folium
import pandas as pd
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium
from polygeohasher import polygeohasher
from shapely.geometry import Point

try: 
    CENTER_START = [-6.175337169759785, 106.82713616185086]
    if "center" not in st.session_state:
          st.session_state["center"] = [-6.175337169759785, 106.82713616185086]

    coordinates = st.text_input("PLease enter coordinates","-6.175337169759785, 106.82713616185086")
    coordinates_list = coordinates.split(",")
    coordinates_dict = {"latitude": float(coordinates_list[0]), "longitude": float(coordinates_list[1])}
    df = pd.DataFrame(coordinates_dict, index=[0])  # Add index for clarity
    geometry = [Point(x, y) for x, y in zip(df['longitude'], df['latitude'])]
    gpd_geom = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    try:
        latitude = float(df['latitude'].iloc[0])
        longitude = float(df['longitude'].iloc[0])
    except ValueError:
        latitude = None
        longitude = None

    if latitude is None or longitude is None:
        st.error("Invalid latitude or longitude value. Please enter valid latitude and longitude values separated by a comma.")
    else:
        st.success("Successfully converted latitude and longitude values to float.")

    st.session_state["center"] = [latitude, longitude]
    button = st.number_input('Insert a Geohash number',2)
    number = int(button)
    geohash_gdf = polygeohasher.create_geohash_list(gpd_geom, number,inner=False)
    geohash_gdf_list = polygeohasher.geohashes_to_geometry(geohash_gdf,"geohash_list")
    gpd_geohash_geom = gpd.GeoDataFrame(geohash_gdf_list, geometry=geohash_gdf_list['geometry'], crs="EPSG:4326")
    geojson_geohash = gpd_geohash_geom.to_json()
    m = folium.Map(location=CENTER_START,zoom_start=16)
    folium.GeoJson(
        geojson_geohash,
        tooltip = folium.GeoJsonTooltip(fields = ['geohash_list']),style_function = lambda x:{'color': 'blue'}).add_to(m)
     
    st_data = st_folium(m, center = st.session_state["center"], width=1200, height=800)
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