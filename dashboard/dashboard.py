import pandas as pd
import streamlit as st
import plotly.express as px


# Load data
my_df = pd.read_csv('https://raw.githubusercontent.com/reaperizy/csv/main/Dicoding%20CSV/main_data.csv')
df = my_df[['year', 'month', 'day', 'hour', 'PM2.5', 'PM10', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'station']]
df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

# Set page configuration
st.set_page_config(
    page_title="Air Quality Index",
    # page_icon=":bar_chart:",
    layout="wide"
)

# Sidebar
st.sidebar.image("https://teamnepalac.com.np/wp-content/uploads/2021/03/aqi.png")
st.sidebar.header("Filter:")

# Temperature filter
temp_filter = st.sidebar.slider(
    "Temperature °C:",
    min_value=df["TEMP"].min(),
    max_value=df["TEMP"].max(),
)

# Station filter
st_filter = st.sidebar.multiselect(
    "Station:",
    options=df["station"].unique(),
    default=df["station"].unique()
)

# Year filter
year_filter = st.sidebar.multiselect(
    "Year:",
    options=df["year"].unique(),
    default=df["year"].unique()
)

# Apply filters
df_selection = df.query("station == @st_filter & year == @year_filter & TEMP >= @temp_filter")

# Main page
st.title(":bar_chart: Air Quality Dashboard")

# Display selected filters
st.sidebar.markdown("### Selected Filters:")
st.sidebar.markdown(f"**Station(s):** {', '.join(st_filter)}")
st.sidebar.markdown(f"**Year(s):** {', '.join(map(str, year_filter))}")
st.sidebar.markdown(f"**Temperature ≥:** {temp_filter} °C")

# Summary statistics
st.markdown("---")
st.header("Summary Statistics")

# Display summary statistics in a row
col1, col2, col3 = st.columns(3)

# Days in total
with col1:
    st.metric("Days in Total", df_selection["date"].nunique())

# Average Temperature
with col2:
    st.metric("Average Temp °C", round(df_selection["TEMP"].mean(), 1))

# Average Pressure
with col3:
    st.metric("Average Pressure", round(df_selection["PRES"].mean(), 2))

# Menampilkan teks peringatan di kolom tengah
st.warning("If PM2.5 levels: 50 is Dangerous")
st.warning("If PM10  levels: 60 is Dangerous")
st.warning("If CO    levels: 700 is Dangerous")

# Line charts
st.markdown("---")
st.header("Air Quality Trends Over Years")

# PM2.5 Line Chart
fig_pm25 = px.line(
    df_selection.groupby(['year', 'station'])[['PM2.5']].mean().reset_index(),
    x="year", y="PM2.5", color="station",
    markers=True, title='Average PM2.5 Particles'
).update_layout(xaxis_title="Year", yaxis_title="PM2.5 (μg/m³)")

# PM10 Line Chart
fig_pm10 = px.line(
    df_selection.groupby(['year', 'station'])[['PM10']].mean().reset_index(),
    x="year", y="PM10", color="station",
    markers=True, title='Average PM10 Particles'
).update_layout(xaxis_title="Year", yaxis_title="PM10 (μg/m³)")

# Display line charts in two columns
col4, col5 = st.columns(2)

with col4:
    st.plotly_chart(fig_pm25, use_container_width=True)

with col5:
    st.plotly_chart(fig_pm10, use_container_width=True)

# Bar charts
st.markdown("---")
st.header("Other Air Quality Metrics")

# CO Line Chart
fig_co = px.line(
    df_selection.groupby(['year', 'station'])[['CO']].mean().reset_index(),
    x="year", y="CO", color="station",
    markers=True, title='Average CO (Carbon Monoxide)'
).update_layout(xaxis_title="Year", yaxis_title="Carbon Monoxide (μg/m³)")

# O3 Bar Chart
fig_o3 = px.bar(
    df_selection.groupby(['year', 'station'])[['O3']].mean().reset_index(),
    x='year', y='O3', color="station",
    title='Average O3 (Ozon)'
).update_layout(xaxis_title="Year", yaxis_title="Ozon (DU)", width=520)

# Display line and bar charts in two columns
col6, col7 = st.columns(2)

with col6:
    st.plotly_chart(fig_co, use_container_width=True)

with col7:
    st.plotly_chart(fig_o3, use_container_width=True)

# Additional information
st.markdown("---")
st.header("Air Quality Information")

# Information about air quality
st.markdown(
    """
    The higher values of PM2.5, PM10, CO, and O3 indicate worse air quality.
    """
)

# Image
image_url = 'https://www.ankitparakh.com/wp-content/uploads/2021/12/HEALTH-EFFECTS-OF-AIR-POLLUTION-WEB.jpg'
st.image(image_url, use_column_width=True)

# Hide Streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
