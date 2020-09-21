"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

DATE_TIME = "date/time"
select_date = st.sidebar.selectbox('Date :' , ['01/01/2019','02/01/2019','03/01/2019','04/01/2019','05/01/2019'])

if select_date=='01/01/2019':
    DATA_URL = ("https://raw.githubusercontent.com/warm9441/Streamlit/master/ODsample/01012019.csv")
elif select_date=='02/01/2019':
    DATA_URL = ("https://raw.githubusercontent.com/warm9441/Streamlit/master/ODsample/02012019.csv")
elif select_date=='03/01/2019':
    DATA_URL = ("https://raw.githubusercontent.com/warm9441/Streamlit/master/ODsample/03012019.csv")
elif select_date=='04/01/2019':
    DATA_URL = ("https://raw.githubusercontent.com/warm9441/Streamlit/master/ODsample/04012019.csv")
elif select_date=='05/01/2019':
    DATA_URL = ("https://raw.githubusercontent.com/warm9441/Streamlit/master/ODsample/05012019.csv")

st.title("Uber_6030816421")
st.markdown(
"""
This is an example of a Streamlit app that represents the Uber pickups
geographical distribution in New York City in five days.

[See source code](https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/app.py)
""")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)

hour = st.slider("Hour to look at", 0, 23)

data = data[data[DATE_TIME].dt.hour == hour]

st.subheader("Geo data between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data[DATE_TIME].dt.hour >= hour) & (data[DATE_TIME].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)

if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)
