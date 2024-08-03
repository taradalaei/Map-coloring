import argparse
from enum import Enum
from CSP import CSP
from Solver import Solver
from map_generator import generate_borders_by_continent
from graphics import draw
import random

class Continent(Enum):
    asia = "Asia"
    africa = "Africa"
    america = "America"
    europe = "Europe"

    def __str__(self):
        return self.value
    

def main():
    """
    Main function to solve the map coloring problem using CSP.

    The function takes command-line arguments to customize the solving process.

    Command-line arguments:
    - -m, --map: Specify the map to solve the coloring problem on. Must be one of [Asia, Africa, America, Europe].
    - -lcv, --lcv: Enable least constraint value (LCV) as an order-type optimizer.
    - -mrv, --mrv: Enable minimum remaining values (MRV) as an order-type optimizer.
    - -ac3, --arc-consistency: Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution.
    - -ND, --Neighborhood-distance: The value determines the threshold for neighboring regions' similarity in color, with a default of 1 ensuring adjacent regions have distinct colors; increasing it, for instance to 2, extends this dissimilarity to the neighbors of neighbors.
    """
    parser = argparse.ArgumentParser(
        prog="Map Coloring",
        description="Utilizing CSP to solve map coloring problem",
    )

    parser.add_argument(
        "-m",
        "--map",
        type=Continent,
        choices=list(Continent),
        help="Map must be: [Asia, Africa, America, Europe]",
    )
    parser.add_argument(
        "-lcv",
        "--lcv",
        action="store_true",
        help="Enable least constraint value (LCV) as a order-type optimizer"
    )
    parser.add_argument(
        "-mrv",
        "--mrv",
        action="store_true",
        help="Enable minimum remaining values (MRV) as a order-type optimizer"
    )
    parser.add_argument(
        "-ac3",
        "--arc-consistency",
        action="store_true",
        help="Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution"
    )
    parser.add_argument(
        "-ND",
        "--Neighborhood-distance",
        type=int,
        default=1,
        help="The value determines the threshold for neighboring regions' similarity in color, with a default of 1 ensuring adjacent regions have distinct colors; increasing it, for instance to 2, extends this dissimilarity to the neighbors of neighbors."
    )

    args = parser.parse_args()
    borders = generate_borders_by_continent(continent=str(args.map))
    
    "*** YOUR CODE HERE ***"
    

    if(borders):
        csp = CSP(*list(borders.keys()),**borders)
        solver = Solver(csp=csp)
        result = solver.backtrack_solver() #your solution
        finalresult = {}
        for i in result:
            finalresult[i[0]] = i[1]
        assignments_number = solver.csp.assignments_number #number of assignments that you can get it from solver.csp.assignments_number
        draw(solution=finalresult, continent=str(args.map), assignments_number=assignments_number)
    else:
        print("no borders")


if __name__ == '__main__':
    main()