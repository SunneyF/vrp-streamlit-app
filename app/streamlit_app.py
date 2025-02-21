import streamlit as st
import pydeck as pdk
import pandas as pd
from vrp_solver import solve_vrp

def main():
    st.title("VRP Solver Visualization - Updated!- automation")
    st.subheader("An improved version of our VRP Solver demo")
    st.write("This updated app solves a simple VRP instance using OR-Tools and visualizes the optimal route on a map.")

    if st.button("Solve VRP"):
        route = solve_vrp()
        if route:
            st.success("VRP Solved!")
            st.write("Optimal Route:", " → ".join(map(str, route)))
            
            # Define fixed coordinates for nodes (example: nodes in San Francisco)
            node_coords = {
                0: {"lat": 37.77, "lon": -122.42},
                1: {"lat": 37.78, "lon": -122.41},
                2: {"lat": 37.76, "lon": -122.43},
                3: {"lat": 37.77, "lon": -122.41}
            }
            
            # Build the coordinate list according to the route
            coords = [node_coords[node] for node in route]
            
            # Create a DataFrame for scatter points (the nodes)
            df_points = pd.DataFrame(coords)
            
            # Build line data for consecutive nodes along the route
            line_data = []
            for i in range(len(coords) - 1):
                line_data.append({
                    "start_lat": coords[i]["lat"],
                    "start_lon": coords[i]["lon"],
                    "end_lat": coords[i+1]["lat"],
                    "end_lon": coords[i+1]["lon"]
                })
            
            # Define a Pydeck layer to draw the connecting lines (route)
            line_layer = pdk.Layer(
                "LineLayer",
                data=line_data,
                get_source_position=["start_lon", "start_lat"],
                get_target_position=["end_lon", "end_lat"],
                get_color=[255, 0, 0],
                get_width=5,
            )
            
            # Define a Pydeck layer to draw the node points
            point_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_points,
                get_position=["lon", "lat"],
                get_color=[0, 0, 255],
                get_radius=50,
            )
            
            # Set the view state to center around the average coordinates
            avg_lat = sum(d["lat"] for d in coords) / len(coords)
            avg_lon = sum(d["lon"] for d in coords) / len(coords)
            view_state = pdk.ViewState(
                latitude=avg_lat,
                longitude=avg_lon,
                zoom=12,
                pitch=0
            )
            
            # Create the deck and display it
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
