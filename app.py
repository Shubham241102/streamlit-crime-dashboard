import streamlit as st
import pandas as pd
import pydeck as pdk

# --- Page Configuration ---
st.set_page_config(
    page_title="Chicago Crime Analytics",
    page_icon="🚨",
    layout="wide",
)

# --- Data Loading ---
# We use the processed file for speed
PROCESSED_DATA_FILE = 'data/chicago_crimes_processed.csv'

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hour'] = df['Date'].dt.hour
    return df

df = load_data(PROCESSED_DATA_FILE)
all_crime_types = df['Primary Type'].unique()

# --- Sidebar Filters ---
st.sidebar.header("Filter Crimes")
selected_crime_types = st.sidebar.multiselect(
    'Select Crime Type(s) (you can type to search)',
    options=all_crime_types,
    default=['BATTERY', 'THEFT', 'ASSAULT', 'CRIMINAL DAMAGE']
)

hour_to_filter = st.sidebar.slider(
    'Filter by Hour of Day',
    min_value=0,
    max_value=23,
    value=(0, 23) # A tuple for a range slider
)

# --- Main Page Content ---
st.title("🚨 Chicago Crime Geospatial Dashboard")
st.markdown("An interactive dashboard to analyze crime patterns in Chicago.")

# --- Filtering Logic ---
# Filter data based on selections
filtered_df = df[
    (df['Primary Type'].isin(selected_crime_types)) &
    (df['Hour'] >= hour_to_filter[0]) &
    (df['Hour'] <= hour_to_filter[1])
]

# --- Display Metrics and Map ---
st.metric("Total Crimes Displayed", f"{filtered_df.shape[0]:,}")

st.subheader("Geospatial Crime Hotspots")

# Define the viewport for the map centered on Chicago
view_state = pdk.ViewState(
    latitude=41.8781,
    longitude=-87.6298,
    zoom=9.5,
    pitch=50, # Angle of the map
)

# Define the Hexagon Layer
layer = pdk.Layer(
    'HexagonLayer',
    data=filtered_df[['Longitude', 'Latitude']],
    get_position='[Longitude, Latitude]',
    radius=200,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
)

# Render the map in Streamlit
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "{elevationValue} crimes in this area"}
))

if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data for Selected Filters")
    st.write(filtered_df)