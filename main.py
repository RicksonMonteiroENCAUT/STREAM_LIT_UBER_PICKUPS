import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

st.title('Uber pickups in NYC')
@st.cache
def load_data(nrows):
    data=pd.read_csv('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz', nrows=nrows)
    data.rename(lambda x: str(x).lower(), inplace=True, axis=1)
    data['date/time']=pd.to_datetime(data['date/time'])
    return data

data=load_data(10000)
if st.checkbox('Show dataframe:'):
    st.dataframe(data)

#Histograma
st.subheader("Number of pickups by hour")
hist_values= np.histogram(data['date/time'].dt.hour, bins=24, range=(0,24))
st.bar_chart(hist_values[0])

#-----
st.subheader("Map of all pickups")
#st.map(data)
st.pydeck_chart(pdk.Deck(
    layers=[pdk.Layer(
    "HeatmapLayer",
    data=data,
    opacity=0.9,
    get_position=["lon", "lat"],
    aggregation=pdk.types.String("MEAN"),
    color_range=[[240, 249, 232],
                [204, 235, 197],
                [168, 221, 181],
                [123, 204, 196],
                [67, 162, 202],
                [8, 104, 172]],
    threshold=1,
    pickable=True,
    )],
    initial_view_state=pdk.ViewState(latitude=40.720589, longitude= -73.856084, zoom=8, min_zoom=5,
                                                            max_zoom=15, pitch=40.5, bearing=-27.36),

    tooltip={"text": "Concetration of pickups"}
))

#slider
st.subheader('Map of pickups by hour')
hour_filter = st.slider('Select hour', 0,23,17)
#mapa
layer = pdk.Layer(
    "GridLayer", data[data['date/time'].dt.hour==hour_filter][['lon','lat']].dropna(), pickable=True, extruded=True, cell_size=200, elevation_scale=4,
    get_position=['lon','lat'], auto_highlight=True
)
view_state = pdk.ViewState(latitude=40.720589, longitude= -73.856084, zoom=8, min_zoom=5, max_zoom=15, pitch=40.5, bearing=-27.36)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Position: {position}\nPickups: {count}"}
)

st.pydeck_chart(r)
