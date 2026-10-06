# 🚇 Navigator — Metro Route Finder with Search Algorithms

A metro navigation system written in Python that finds the best route between two stations (or two arbitrary coordinates) on a city metro map. It implements classic **uninformed** and **informed** search algorithms and lets the user choose the optimisation criterion: fewest stops, minimum time, minimum distance, or fewest line transfers.

Developed as **Project 1** of the *Artificial Intelligence* course at the **Universitat Autònoma de Barcelona (UAB)**.

---

## ✨ Features

- **Four search algorithms**: Depth-First Search, Breadth-First Search, Uniform-Cost Search and A\*.
- **Four optimisation criteria** for the optimal algorithms (Uniform-Cost and A\*):

  | `type_preference` | Criterion          | Cost `g`                                       | Heuristic `h` (A\*)                          |
  |:-----------------:|--------------------|------------------------------------------------|----------------------------------------------|
  | `0`               | Adjacency (stops)  | 1 per connection                               | 0 at the goal, 1 elsewhere                   |
  | `1`               | Minimum time       | Travel time from the time matrix               | Euclidean distance / maximum line speed      |
  | `2`               | Minimum distance   | Line speed × travel time (0 on line transfers) | Euclidean distance to the destination        |
  | `3`               | Minimum transfers  | 1 per line change                              | 1 if the step is a line change, else 0       |

- **Redundant-path pruning** in A\*: keeps a table of the best known cost to each station and discards worse partial paths.
- **Cycle removal** so paths never revisit a station.
- **`Astar_improved`**: A\* from/to *coordinates* instead of stations. The user can walk in a straight line (speed 5) to any station and from any station to the destination, or walk directly to the destination.
- **`distance_to_stations`**: distance from any point of the map to every station, sorted by distance and then by station ID.
- Unit tests (`unittest`) and ready-to-use sample cities.

---

## 🧠 How it works

### Map representation

The city is modelled with two classes in `SubwayMap.py`:

- **`Map`**: stores the stations (`name`, `line`, `x`, `y`, `velocity`), the connections (a cost/adjacency dictionary built from the time matrix) and the velocity of each line.
- **`Path`**: a route stored as a list of station IDs (root first, current node last), together with its real cost `g`, heuristic `h` and total estimate `f = g + h`.

Stations that belong to several lines are **duplicated, one node per line**, so a line change is just another edge in the graph (this is already done in the provided `Time.txt` matrices).

### Algorithms

| Algorithm            | Function               | Type                   | Optimal |
|----------------------|------------------------|------------------------|:-------:|
| Depth-First Search   | `depth_first_search`   | Uninformed             | ❌      |
| Breadth-First Search | `breadth_first_search` | Uninformed             | ❌      |
| Uniform-Cost Search  | `uniform_cost_search`  | Uninformed, cost-based | ✅      |
| A\*                  | `Astar`                | Informed (heuristic)   | ✅      |
| A\* from coordinates | `Astar_improved`       | Informed (heuristic)   | ✅ (time) |

All of them share the same skeleton: expand the first path of the list, remove cycles, and insert the children into the list according to a different policy (front, back, ordered by `g`, ordered by `f`).

---

## 📁 Project structure

```
NAVIGATOR/
├── CityInformation/          # City data (stations, time matrices, line speeds)
│   ├── Lyon_smallCity/
│   └── Barcelona_City/
├── docs/                     # Assignment statements (Part 1 and Part 2) and slides
├── src/
│   ├── SearchAlgorithm.py    # All search algorithms (the core of the project)
│   ├── SubwayMap.py          # Map and Path classes
│   ├── utils.py              # File readers and helpers
│   ├── TestCases.py          # Unit tests
│   ├── testing_file.py       # Sandbox to try the functions on the small Lyon map
│   └── answers_exam.py       # Script used to answer the practical exam questions
├── .gitignore
└── README.md
```

### City data format (`CityInformation/<city>/`)

- `Stations.txt`: one station per line, tab-separated: `ID`, `name`, `line`, `x`, `y`.
- `Time.txt`: adjacency matrix with travel times between stations (`0` = no connection).
- `InfoVelocity.txt`: constant speed of each metro line.

---

## 🚀 Getting started

### Requirements

- Python 3.8+
- [NumPy](https://numpy.org/)

```bash
pip install numpy
```

### Clone and run

```bash
git clone https://github.com/josepjp31/Navigator.git
cd navigator
python src/testing_file.py
```

> ⚠️ Run the scripts **from the repository root**: the data paths (`./CityInformation/...`) are relative to the current working directory.

### Usage example

```python
import os
from SearchAlgorithm import *
from SubwayMap import *
from utils import *

ROOT_FOLDER = './CityInformation/Lyon_smallCity/'

# Load the city
map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
map.add_connection(read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt')))
map.add_velocity(read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt')))

# Uninformed search
print(breadth_first_search(2, 7, map).route)

# Uniform-cost search, minimum time (type_preference = 1)
path = uniform_cost_search(9, 3, map, 1)
print(path.route, path.g)

# A*, minimum distance (type_preference = 2)
path = Astar(9, 4, map, 2)
print(path.route, path.f)

# A* between two coordinates (the path starts with 0 and ends with -1)
path = Astar_improved([80, 100], [100, 240], map)
print(path.route, path.f)
```

### Run the tests

```bash
cd src
python -m unittest TestCases -v
```

The tests read the data from `./CityInformation/Lyon_smallCity/`, so make sure the folder name and your working directory match your setup.

---

## 🎓 Context

- **University**: Universitat Autònoma de Barcelona (UAB)
- **Course**: Artificial Intelligence
- **Assignment**: Project 1 — Navigator (Part 1: uninformed search; Part 2: informed search)
- The assignment statements are available in the [`docs/`](docs) folder.

## 📜 License

This project was developed for educational purposes. Feel free to read and learn from it, but if you are taking the same course, please respect your university's academic integrity policy.
