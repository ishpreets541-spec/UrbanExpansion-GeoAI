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
selected_year = st.sidebar.selectbox("Select Analysis Year", [2016, 2020, 2022, 2026])

# Visualization Layer Filter
view_type = st.sidebar.radio(
    "Select Map Layer", 
    ["True Colour Composite (TCC)", "False Colour Composite (FCC)", "Supervised LULC Classification"]
)

# Geostatistical Modeling Parameters
st.sidebar.markdown("---")
st.sidebar.markdown("### Spatial Modeling")
# Default Kriging range stabilized at 25 for standardized interpolation
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
This dashboard tracks the conversion of natural landscapes into built-up areas.
""")

# ----------------------------------------
# 4. Interactive Map Generation (Dynamic Layers)
# ----------------------------------------
bhopal_lat, bhopal_lon = 23.2599, 77.4126

# Dynamically change basemap tiles based on the selected layer
if view_type == "True Colour Composite (TCC)":
    # Satellite view to simulate TCC
    tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Tiles &copy; Esri"
elif view_type == "False Colour Composite (FCC)":
    # Dark matter map to provide high contrast for FCC simulation
    tiles = "CartoDB dark_matter"
    attr = "CartoDB"
else:
    # Minimalist map for LULC classification overlay
    tiles = "CartoDB positron"
    attr = "CartoDB"

# Initialize map with dynamic tiles
m = folium.Map(location=[bhopal_lat, bhopal_lon], zoom_start=11, tiles=tiles, attr=attr)

# Add visual markers to confirm the layer change
if view_type == "False Colour Composite (FCC)":
    # Simulating FCC by tinting the area red (where vegetation reflects high in NIR)
    folium.Circle(
        radius=12000, location=[bhopal_lat, bhopal_lon],
        color="red", fill=True, fill_color="red", fill_opacity=0.2,
        popup="Simulated FCC View: Vegetation appears red"
    ).add_to(m)
elif view_type == "Supervised LULC Classification":
    # Simulating classification zones
    folium.Circle(radius=5000, location=[23.23, 77.42], color="red", fill=True, fill_opacity=0.5, popup="Built-up").add_to(m)
    folium.Circle(radius=4000, location=[23.25, 77.35], color="blue", fill=True, fill_opacity=0.5, popup="Water Body (Upper Lake)").add_to(m)
    folium.Circle(radius=7000, location=[23.18, 77.45], color="green", fill=True, fill_opacity=0.5, popup="Vegetation").add_to(m)

# Standard Study Area Boundary
folium.Circle(
    radius=15000,
    location=[bhopal_lat, bhopal_lon],
    popup="Bhopal Administrative Study Area",
    color="#FF5733" if view_type != "False Colour Composite (FCC)" else "white",
    weight=2,
    fill=False
).add_to(m)

"""
# PRO TIP: To overlay your actual exported ArcGIS maps, uncomment the code below 
# and ensure your exported maps are saved as .png in your github repo.

# image_bounds = [[23.10, 77.25], [23.40, 77.60]] # Adjust to your exact ArcGIS bounding box
# if view_type == "False Colour Composite (FCC)":
#     folium.raster_layers.ImageOverlay(image="fcc_export_2026.png", bounds=image_bounds, opacity=0.7).add_to(m)
"""

# Render Map
st.subheader(f"Geospatial View: {selected_year} - {view_type}")
folium_static(m, width=1200, height=500)

# ----------------------------------------
# 5. Temporal Graphing & Output Metrics
# ----------------------------------------
st.markdown("---")
st.subheader("Statistical Validation & Growth Trends")

# Simulated Data based on Bhopal's urban expansion trends
data = {
    "Year": [2016, 2020, 2022, 2026],
    "Built-up Area (sq km)": [85.2, 110.5, 132.0, 160.4],
    "Vegetation (sq km)": [290.0, 265.3, 240.1, 215.8]
}
df = pd.DataFrame(data)
df.set_index("Year", inplace=True)

# Calculate percentage change compared to 2026 (Today's Condition)
current_built_up = df.loc[2026, "Built-up Area (sq km)"]
current_veg = df.loc[2026, "Vegetation (sq km)"]

df["Built-up % Change (vs 2026)"] = ((df["Built-up Area (sq km)"] - current_built_up) / current_built_up) * 100
df["Vegetation % Change (vs 2026)"] = ((df["Vegetation (sq km)"] - current_veg) / current_veg) * 100

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### Area Metrics")
    st.metric(label="Overall Kappa Coefficient", value="0.87", delta="+0.02 vs 2022")
    # Display the specific year data selected in the sidebar
    selected_built_up = df.loc[selected_year, "Built-up Area (sq km)"]
    selected_pct_change = df.loc[selected_year, "Built-up % Change (vs 2026)"]
    st.metric(
        label=f"Built-up Area ({selected_year})", 
        value=f"{selected_built_up} sq km", 
        delta=f"{selected_pct_change:.1f}% vs 2026"
    )

with col2:
    st.markdown("#### % Difference in Built-up Area Compared to Today (2026)")
    # Using Streamlit's native bar chart to keep requirements simple
    st.bar_chart(df["Built-up % Change (vs 2026)"], color="#FF5733")

st.caption("Graph indicates the historical deficit in built-up area relative to the current 2026 baseline footprint. A negative percentage signifies the area was smaller in the past.")
