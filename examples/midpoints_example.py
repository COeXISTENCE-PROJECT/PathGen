import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), './')))

import pandas as pd

from graph_builders import build_digraph
from path_generators import basic_generator
from visualizers import show_multi_routes
from utils import iterable_to_string


"""
This script demonstrates the generation of paths between origins and destinations in a transportation network using
specific midpoints. It builds a directed graph from network files, generates paths through midpoints, and visualizes 
the resulting routes.

Workflow:
1. The script builds a directed graph using network files.
2. Paths are generated from the origin to each midpoint, and then from each midpoint to the destination.
3. The generated routes are concatenated and stored in a DataFrame.
4. If `show_routes` is enabled, the paths are visualized and saved as images.
5. The generated routes are saved to a CSV file.

Output:
- Visualizations of the generated routes are saved as PNG files in the `examples/figures/` directory.
- The list of routes is saved as a CSV file in the specified `routes_csv_path`.
"""


##################### PARAMS ############################

origins = ["441496282#0"]
destinations = ["-115604057#1"]

#mid_points = ["-115602933#4", "441496282#4", "279952229#4"]
#mid_points = ["279952229#4", "-115604047#2", "115604047#1"]
mid_points = ["-115602933#0", "279952229#5", "-819269916#3"]

connection_file_path = "examples/network_files/csomor1.con.xml"
edge_file_path = "examples/network_files/csomor1.edg.xml"
route_file_path = "examples/network_files/csomor1.rou.xml"
nod_file_path = "examples/network_files/csomor1.nod.xml"

xcrop = (1500, 3000)
ycrop = (300, 1200)

show_routes = True
routes_csv_path = "examples/results/routes.csv"

kwargs = {
    "random_seed": 42,
    "num_samples": 50,
    "number_of_paths": 1,
    "beta" : -2
}

########################################################
    
if __name__ == "__main__":
    # Generate network and paths
    network = build_digraph(connection_file_path, edge_file_path, route_file_path)
    routes = list()
    for mid_point in mid_points:
        route_to_midpoint = basic_generator(network, origins, [mid_point], **kwargs)
        route_to_midpoint = route_to_midpoint["path"].values[0]
        route_to_midpoint = iterable_to_string(route_to_midpoint.split(",")[:-1], ',')
        
        route_from_midpoint = basic_generator(network, [mid_point], destinations, **kwargs)
        route_from_midpoint = route_from_midpoint["path"].values[0]
        
        routes.append({
            "origins": origins[0],
            "destinations": destinations[0],
            "path": route_to_midpoint + "," + route_from_midpoint
        })
        
    # Merge routes
    routes = pd.DataFrame(routes)
    
    if show_routes:
        # Visualize paths
        for origin_idx, origin in enumerate(origins):
            for dest_idx, destination in enumerate(destinations):
                save_path = f"examples/figures/{origin_idx}_{dest_idx}.png"
                routes_to_show = routes[(routes["origins"] == origin) & (routes["destinations"] == destination)]['path']
                routes_to_show = [route.split(",") for route in routes_to_show]
                
                show_multi_routes(nod_file_path, edge_file_path, routes_to_show, origin, destination, \
                    xcrop=xcrop, ycrop=ycrop, save_file_path=save_path, title=f"Origin: {origin_idx}({origin}), Destination: {dest_idx}({destination})")
        
    routes.to_csv(routes_csv_path, index=False)