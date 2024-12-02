# Maritime SeaRoute Finder

Maritime Seaport Route Finder is a tool designed to compute optimal sea routes between global seaports. This project, created as part of the Algorithm Analysis and Design course, leverages 
**Dijkstra's algorithm** to calculate routes that minimize distance, fuel costs, and travel time, while also allowing users to specify constraints like avoiding certain regions.


# Features

**Optimal Route Calculation**: Uses Dijkstra's algorithm to find the shortest or most efficient path between two seaports.
**Customizable Parameters**: Supports optimization based on distance, fuel cost, or travel time.
**Region Avoidance**: Allows users to specify regions or ports to bypass for safety or geopolitical reasons.
**Scalable Dataset**: Works with real-world maritime data (ports.csv and routes.csv) to ensure accurate calculations.

# Project Structure

├── data/
│   ├── ports.csv           % Contains port details (ID, name, country, latitude, longitude)
│   ├── routes.csv          % Contains route details (source, destination, distance, travel time)
├── MaritimeRoute.ipynb     % Colab notebook for running the algorithm and visualizing results
├── README.md               % Project documentation
├── requirements.txt        % Python dependencies
└── utils/
    ├── graph_utils.py      % Graph construction and handling
    ├── dijkstra.py         % Implementation of Dijkstra's algorithm
