import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster, HeatMap
import os
from src.find_distance import find_shortest_seaport_distance

# Path to the CSV file
DF_PATH = os.path.abspath(os.path.join("data", "world_seaports.csv"))

# Function that translates source and destination names to coordinates
def get_src_dst_latLng(df: pd.DataFrame, source_name: str, dest_name: str):
    source_row = df[df["name"] == source_name].iloc[0]
    dest_row = df[df["name"] == dest_name].iloc[0]

    src_lng = source_row["Longitude"]
    src_lat = source_row["Latitude"]

    dst_lng = dest_row["Longitude"]
    dst_lat = dest_row["Latitude"]

    return src_lng, src_lat, dst_lng, dst_lat

# Function to extract intermediate ports along the route (this is a simplified placeholder)
def get_intermediate_ports(route, seaport_data):
    intermediate_ports = []
    countries_crossed = set()
    
    for coord in route:
        # Find nearest port to the coordinate (this is a simplified placeholder logic)
        nearest_port = seaport_data.iloc[((seaport_data['Latitude'] - coord[0])**2 + (seaport_data['Longitude'] - coord[1])**2).idxmin()]
        port_name = nearest_port['name']
        country = nearest_port['Country']
        
        if port_name not in intermediate_ports:
            intermediate_ports.append(port_name)
            countries_crossed.add(country)
    
    return intermediate_ports, list(countries_crossed)

# Adding custom CSS styling
st.markdown("""
    <style>
    /* General App Styling */
    body {
        background-color: #f4f4f9;
        font-family: 'Arial', sans-serif;
    }
    
    h1, h2, h3, h4 {
        color: white;
        font-weight: 600;
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #34495e;
        color: white;
        padding: 1rem;
    }

    .sidebar .sidebar-content h1 {
        color: white;
    }

    .css-1gkgrw6 {
        margin-top: 20px;
    }

    /* Styling for the Map */
    .leaflet-container {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        padding: 10px;
    }

    /* Table Styling */
    .stTable {
        margin-top: 20px;
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 15px;
    }

    .stTable th {
        background-color: #2980b9;
        color: white;
    }

    .stTable td {
        color: #34495e;
    }

    /* Button Styling */
    .css-12oz5g7 {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }

    .css-12oz5g7:hover {
        background-color: #2980b9;
    }

    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    # Sidebar and main title
    st.sidebar.title("App Controls")
    st.title("Seaport Distance Finder")

    # Load data
    seaports_data = pd.read_csv(DF_PATH)

    # Sidebar dropdowns for selecting source and destination
    seaport_names = seaports_data['name'].unique()
    source_port = st.sidebar.selectbox("Source Port", seaport_names)
    destination_port = st.sidebar.selectbox("Destination Port", seaport_names)

    # Sidebar toggle for map layers
    heatmap_toggle = st.sidebar.checkbox("Show Seaport Activity Heatmap", value=False)

    # Map settings
    map_center = [20.0, 0.0]  # Neutral center
    m = folium.Map(location=map_center, zoom_start=2)

    # Adding cluster markers for all seaports (this can be optional)
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in seaports_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"<b>{row['name']}</b><br>Region: {row['D_Region']}<br>Country: {row['Country']}",
            tooltip=f"{row['name']} ({row['Country']})"
        ).add_to(marker_cluster)

    # Add heatmap layer if toggled
    if heatmap_toggle:
        heatmap_data = [[row['Latitude'], row['Longitude']] for _, row in seaports_data.iterrows()]
        HeatMap(heatmap_data).add_to(m)

    # Display the map with seaports and optional heatmap
    folium_static(m)

    # Calculate shortest sea distance and display on map
    if source_port == destination_port:
        st.write("\n")
        st.write("<H3>Source and Destination ports are the same, nothing to compute!</H3>", unsafe_allow_html=True)
    else:
        # Get lat/lng from source and destination names
        src_lng, src_lat, dst_lng, dst_lat = get_src_dst_latLng(seaports_data, source_port, destination_port)
        result_obj = find_shortest_seaport_distance(srcLng=src_lng, srcLat=src_lat, dstLng=dst_lng, dstLat=dst_lat)
        min_sea_dist = result_obj["length"]
        coord_path = result_obj["coordinate_path"]

        st.write(f"<H4>The Shortest Sea distance between  {source_port} and {destination_port} is : {min_sea_dist} Km</H4>", unsafe_allow_html=True)

        # Map for displaying the route
        m2 = folium.Map(location=map_center, zoom_start=2)

        # Draw the route between the source and destination (only the line)
        folium.PolyLine(
            coord_path,
            color="darkblue",
            weight=4,
            opacity=0.7
        ).add_to(m2)

        # Add markers for source and destination ports
        folium.Marker(
            location=[src_lat, src_lng],
            icon=folium.Icon(color="green"),
            popup=f"{source_port}",
            tooltip="Source Port"
        ).add_to(m2)

        folium.Marker(
            location=[dst_lat, dst_lng],
            icon=folium.Icon(color="red"),
            popup=f"{destination_port}",
            tooltip="Destination Port"
        ).add_to(m2)

        # Display the route map
        folium_static(m2)

        # Get intermediate ports and countries
        intermediate_ports, countries_crossed = get_intermediate_ports(coord_path, seaports_data)

        # Create DataFrames for displaying the results in tables
        # Source Port Information
        source_details = seaports_data[seaports_data["name"] == source_port].iloc[0]
        source_info = {
            "Port Name": source_port,
            "Country": source_details['Country'],
            "Region": source_details['D_Region'],
            "Latitude": source_details['Latitude'],
            "Longitude": source_details['Longitude']
        }

        # Destination Port Information
        destination_details = seaports_data[seaports_data["name"] == destination_port].iloc[0]
        destination_info = {
            "Port Name": destination_port,
            "Country": destination_details['Country'],
            "Region": destination_details['D_Region'],
            "Latitude": destination_details['Latitude'],
            "Longitude": destination_details['Longitude']
        }

        # Intermediate Ports and Countries
        intermediate_ports_df = pd.DataFrame({"Intermediate Ports": intermediate_ports})
        countries_crossed_df = pd.DataFrame({"Countries Crossed": countries_crossed})

        # Display the results in tables with CSS styling
        st.subheader("Port Details")
        port_details_df = pd.DataFrame([source_info, destination_info])
        st.table(port_details_df)

        st.subheader("Intermediate Ports along the Route")
        st.table(intermediate_ports_df)

        st.subheader("Countries Crossed along the Route")
        st.table(countries_crossed_df)

        # Show the distance
        st.write(f"**Shortest Sea Distance**: {min_sea_dist} Km")
