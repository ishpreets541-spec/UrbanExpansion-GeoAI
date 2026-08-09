import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

# ----------------------------------------
# 1. Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="UrbanExpansion-GeoAI",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------------------
# 2. Sidebar Controls
# ----------------------------------------
st.sidebar.title("🌍 UrbanExpansion-GeoAI")
st.sidebar.markdown("### Temporal Analysis of Urban Growth in Bhopal")

# Temporal Filter
selected_year = st.sidebar.selectbox("Select Analysis Year", ["2016", "2020", "2022", "2026"])

# Visualization Layer Filter
view_type = st.sidebar.radio(
    "Select Map Layer", 
    ["True Colour Composite (TCC)", "False Colour Composite (FCC)", "Supervised LULC Classification"]
)

# Geostatistical Modeling Parameters
st.sidebar.markdown("---")
st.sidebar.markdown("### Spatial Modeling")
# Set to 25 based on updated kriging parameters
kriging_range = st.sidebar.slider("Kriging Interpolation Range", min_value=5, max_value=100, value=25)

st.sidebar.markdown("---")
st.sidebar.info("""
**Data Overview:**
* **Source:** Copernicus Browser (Sentinel-2A)
* **Bands:** B2, B3, B4, B8
* **Boundary:** Mpgov.in (Bhopal District)
""")

# ----------------------------------------
# 3. Main Dashboard Layout
# ----------------------------------------
st.title("Bhopal Urban Expansion & LULC Analysis")
st.markdown(f"""
Visualizing land transformation and urban sprawl in Bhopal, Madhya Pradesh for the year **{selected_year}**. 
Tracking the conversion of natural landscapes into built-up areas via spatial analysis.
""")

# ----------------------------------------
# 4. Interactive Map Generation
# ----------------------------------------
bhopal_lat, bhopal_lon = 23.2599, 77.4126

# Dynamically change basemap tiles based on the selected layer
if view_type == "True Colour Composite (TCC)":
    tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Tiles &copy; Esri"
elif view_type == "False Colour Composite (FCC)":
    tiles = "CartoDB dark_matter"
    attr = "CartoDB"
else:
    tiles = "CartoDB positron"
    attr = "CartoDB"

# Initialize map
m = folium.Map(location=[bhopal_lat, bhopal_lon], zoom_start=11, tiles=tiles, attr=attr)

# Add visual layers based on selection
if view_type == "False Colour Composite (FCC)":
    folium.Circle(
        radius=12000, location=[bhopal_lat, bhopal_lon],
        color="#ff0000", fill=True, fill_color="#ff0000", fill_opacity=0.15,
        popup="Simulated FCC View: Healthy vegetation reflects highly in NIR (Red)"
    ).add_to(m)
elif view_type == "Supervised LULC Classification":
    folium.Circle(radius=5000, location=[23.23, 77.42], color="red", fill=True, fill_opacity=0.5, popup="Built-up Area").add_to(m)
    folium.Circle(radius=4000, location=[23.25, 77.35], color="blue", fill=True, fill_opacity=0.5, popup="Upper Lake (Water Body)").add_to(m)
    folium.Circle(radius=7000, location=[23.18, 77.45], color="green", fill=True, fill_opacity=0.5, popup="Vegetation").add_to(m)

# Standard Study Area Boundary
folium.Circle(
    radius=15000,
    location=[bhopal_lat, bhopal_lon],
    popup="Bhopal Administrative Boundary",
    color="#FF5733" if view_type != "False Colour Composite (FCC)" else "white",
    weight=2,
    fill=False
).add_to(m)

# PRO TIP: To overlay your actual exported ArcGIS maps, uncomment the block below.
# Ensure your exported maps are saved as .png in your github repo.
#
# image_bounds = [[23.10, 77.25], [23.40, 77.60]] # Adjust to your exact ArcGIS bounding box
# if view_type == "False Colour Composite (FCC)":
#     folium.raster_layers.ImageOverlay(image="fcc_export_2026.png", bounds=image_bounds, opacity=0.7).add_to(m)

# Render Map in Streamlit UI
st.subheader(f"Geospatial View: {selected_year} - {view_type}")
folium_static(m, width=1000, height=500)

# ----------------------------------------
# 5. Temporal Graphing & Output Metrics
# ----------------------------------------
st.markdown("---")
st.subheader("Urban Growth Trends & Validation")

# Simulated Data representing temporal urban growth in Bhopal
data = {
    "Year": ["2016", "2020", "2022", "2026"],
    "Built-up Area (sq km)": [85.2, 110.5, 132.0, 160.4],
    "Vegetation (sq km)": [290.0, 265.3, 240.1, 215.8]
}
df = pd.DataFrame(data).set_index("Year")

# Calculate metrics against current conditions (2026)
current_built_up = df.loc["2026", "Built-up Area (sq km)"]
selected_built_up = df.loc[selected_year, "Built-up Area (sq km)"]

# Percentage change formula: ((Selected Year - 2026) / 2026) * 100
pct_change_vs_2026 = ((selected_built_up - current_built_up) / current_built_up) * 100

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### Key Metrics")
    st.metric(label="Overall Kappa Coefficient", value="0.87", delta="High Accuracy")
    
    st.metric(
        label=f"Built-up Area in {selected_year}", 
        value=f"{selected_built_up} sq km", 
        delta=f"{pct_change_vs_2026:.1f}% vs 2026 Conditions",
        delta_color="normal" if pct_change_vs_2026 >= 0 else "inverse"
    )

with col2:
    st.markdown("#### Expansion of Built-up Area (2016 - 2026)")
    # Line chart showing the temporal increase of urban area
    st.line_chart(df["Built-up Area (sq km)"], color="#FF4B4B")

st.caption("Graph indicates the steady expansion of built-up areas across Bhopal over the study period. Negative percentage changes in the metrics indicate historical deficits compared to the current 2026 urban footprint.")
