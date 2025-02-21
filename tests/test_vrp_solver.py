
from app.vrp_solver import solve_vrp

def test_solve_vrp():
    route = solve_vrp()
    # Expecting a route that starts and ends at depot (node 0)
    assert route[0] == 0, "Route should start at depot (0)"
    assert route[-1] == 0, "Route should end at depot (0)"
    # Check that all nodes are visited (for our 4-node instance)
    assert set(route) == {0, 1, 2, 3}, "Route should visit all nodes"
