# app/vrp_solver.py
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # Distance matrix for 4 locations (0 is the depot)
    data['distance_matrix'] = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def solve_vrp():
    """Solves the VRP and returns the route."""
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']),
        data['num_vehicles'],
        data['depot']
    )
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set search parameters.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        # Extract the route.
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = solution.Value(routing.NextVar(index))
        route.append(data['depot'])  # End at depot.
        return route
    else:
        return None

if __name__ == '__main__':
    route = solve_vrp()
    print("Route:", route)
