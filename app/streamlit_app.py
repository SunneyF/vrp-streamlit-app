import streamlit as st
import pydeck as pdk
import pandas as pd
from vrp_solver import solve_vrp

def main():
    # Updated title and subtitle
    st.title("VRP Solver Visualization - Enhanced!")
    st.subheader("Now with improved insights and interactivity")
    st.write("This app solves a simple VRP instance and visualizes the optimal route on an interactive map.")

    if st.button("Solve VRP"):
        route = solve_vrp()
        if route:
            st.success("VRP Solved!")
            st.write("Optimal Route:", " → ".join(map(str, route)))
            
            # Visualization logic remains, perhaps with added features or improved layout
            node_coords = {
                0: {"lat": 37.77, "lon": -122.42},
                1: {"lat": 37.78, "lon": -122.41},
                2: {"lat": 37.76, "lon": -122.43},
                3: {"lat": 37.77, "lon": -122.41}
            }
            coords = [node_coords[node] for node in route]
            df_points = pd.DataFrame(coords)
            line_data = []
            for i in range(len(coords) - 1):
                line_data.append({
                    "start_lat": coords[i]["lat"],
                    "start_lon": coords[i]["lon"],
                    "end_lat": coords[i+1]["lat"],
                    "end_lon": coords[i+1]["lon"]
                })
            line_layer = pdk.Layer(
                "LineLayer",
                data=line_data,
                get_source_position=["start_lon", "start_lat"],
                get_target_position=["end_lon", "end_lat"],
                get_color=[255, 0, 0],
                get_width=5,
            )
            point_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_points,
                get_position=["lon", "lat"],
                get_color=[0, 0, 255],
                get_radius=50,
            )
            avg_lat = sum(d["lat"] for d in coords) / len(coords)
            avg_lon = sum(d["lon"] for d in coords) / len(coords)
            view_state = pdk.ViewState(
                latitude=avg_lat,
                longitude=avg_lon,
                zoom=12,
                pitch=0
            )
            deck = pdk.Deck(
                layers=[line_layer, point_layer],
                initial_view_state=view_state,
                tooltip={"text": "Latitude: {lat}, Longitude: {lon}"}
            )
            st.pydeck_chart(deck)
        else:
            st.error("No solution found.")

if __name__ == '__main__':
    main()
