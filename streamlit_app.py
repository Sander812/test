import streamlit as st
import pandas as pd
import pydeck as pdk
from geopy.geocoders import GoogleV3

# Initialiser Google Geocoder med din API-nøkkel
geolocator = GoogleV3(api_key='Your_API_Key_Here')

# Funksjon for å få nåværende lokasjon basert på IP-adresse
def get_current_location():
    # Forsøk å hente nåværende posisjon fra nettleseren
    try:
        # Hent nåværende posisjon fra HTML5 Geolocation-funksjonen
        position = st.query_params()['current_position']
        return position.split(',')
    except:
        # Hvis posisjon ikke kan hentes, bruk en standard posisjon
        return 0, 0

# Last inn Excel-arket
df = pd.read_excel(r"C:\Users\sander\Ved\ProduktLagerSalg.xlsm", sheet_name='Map')

# Splitt 'LatLong'-kolonnen til to nye kolonner 'latitude' og 'longitude'
df[['latitude', 'longitude']] = df['LatLong'].str.split(',', expand=True)

# Konverter 'latitude' og 'longitude' til numeriske verdier (float)
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# Hent nåværende posisjon
current_latitude, current_longitude = get_current_location()

# Vis kartet med sanntids posisjonssporing
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=current_latitude,
        longitude=current_longitude,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'ScatterplotLayer',
           data=df,
           get_position=['longitude', 'latitude'],
           get_color='[200, 30, 0, 160]',
           get_radius=10,
           pickable=True
        ),
        pdk.Layer(
           'ScatterplotLayer',
           data=[{'position': [current_longitude, current_latitude]}],
           get_position='position',
           get_color='[0, 0, 255, 160]',
           get_radius=100,
           pickable=False
        )
    ],
    tooltip={
        'html': '<b>Adresse:</b> {Adresse} <br><b>Status:</b> {Status}',
        'style': {
            'color': 'white'
        }
    }
))
