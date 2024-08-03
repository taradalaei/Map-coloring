# Map Coloring CSP Solver

This repository contains a Python implementation of a Constraint Satisfaction Problem (CSP) solver for the map coloring problem. The goal is to color a map such that no two adjacent regions (countries) share the same color. This implementation uses various CSP techniques, including heuristics and arc consistency, to efficiently solve the problem.

## Overview

The project includes the following components:

- **CSP Class**: Defines the Constraint Satisfaction Problem, including variables, domains, constraints, and methods for assigning and unassigning values.
- **Solver Class**: Implements a backtracking solver with various heuristics and the AC-3 algorithm for constraint propagation.
- **Map Visualization**: Functions to visualize the solution on a map using geographic data.
- **Main Script**: Provides a command-line interface to solve the map coloring problem for different continents.

## Installation

To run the code, you'll need to install the following dependencies:

```bash
pip install geopandas pandas shapely matplotlib
```

## Usage

You can run the main script to solve the map coloring problem. The script takes several command-line arguments to customize the solving process:

### Command-Line Arguments

- `-m`, `--map`:
  Specify the continent to solve the coloring problem on. Options are: `Asia`, `Africa`, `America`, `Europe`.

- `-lcv`, `--lcv`:
  Enable Least Constraining Value (LCV) heuristic for ordering domain values.

- `-mrv`, `--mrv`:
  Enable Minimum Remaining Values (MRV) heuristic for selecting unassigned variables.

- `-ac3`, `--arc-consistency`:
  Enable AC-3 algorithm for arc consistency.

- `-ND`, `--Neighborhood-distance`:
  Set the threshold for neighboring regions' similarity in color. Default is 1.

### Example

```bash
python main.py -m Europe -lcv -mrv -ac3 -ND 2
```

This command will solve the map coloring problem for Europe, using LCV, MRV, and AC-3 with a neighborhood distance of 2.

## Files

- `CSP.py`: Contains the `CSP` class definition.
- `Solver.py`: Contains the `Solver` class definition.
- `map_generator.py`: Contains functions to generate borders by continent.
- `graphics.py`: Contains functions to visualize the solution on a map.
- `main.py`: The main script to solve the map coloring problem and visualize the results.
- `countries_dataset.csv`: A CSV file containing geographic and neighbor data for countries (used for map visualization).

## How It Works

1. **Define CSP**: Create a `CSP` instance and add variables and constraints.
2. **Solve CSP**: Use the `Solver` class to find a valid coloring using the backtracking algorithm and optional heuristics.
3. **Visualize**: Generate and display a colored map showing the solution using the `draw` function.

## Contributing

Feel free to contribute by submitting issues or pull requests. Ensure that your code follows the existing style and includes relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
