import folium
import polyline

def draw_route_in_html(directions):
    # Get the coordinates of the route's start and end points
    start_lat = directions[0]["legs"][0]["start_location"]["lat"]
    start_lng = directions[0]["legs"][0]["start_location"]["lng"]
    end_lat = directions[0]["legs"][0]["end_location"]["lat"]
    end_lng = directions[0]["legs"][0]["end_location"]["lng"]

    # Create a folium map
    map_route = folium.Map(location=[(start_lat + end_lat) / 2, (start_lng + end_lng) / 2], zoom_start=7, tiles='OpenStreetMap')

    # Add start and end points to the map
    folium.Marker(location=[start_lat, start_lng], icon=folium.Icon(color="green"), popup="Start").add_to(map_route)
    folium.Marker(location=[end_lat, end_lng], icon=folium.Icon(color="red"), popup="End").add_to(map_route)

    # Add the route polyline to the map
    polyline_points = []
    for step in directions[0]["legs"][0]["steps"]:
        polyline_points.extend(polyline.decode(step["polyline"]["points"]))
    folium.PolyLine(polyline_points, color="blue", weight=5, opacity=1).add_to(map_route)

    # Return the map as an HTML string
    return map_route._repr_html_()


print("draw_result_map.py finished!") 