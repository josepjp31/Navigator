# This file contains all the required routines to make an A* search algorithm.
#
__author__ = '1710404'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2023 - 2024
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    expansio = []

    for i in map.connections[path.last]:
        pathAct = copy.deepcopy(path)
       
        pathAct.add_route(i)
        expansio.append(pathAct)


    return expansio


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """

    path_sinCiclos = []
    
    for path in path_list:
        
        if path.last not in path.route[:-1]:
            path_sinCiclos.append(path)
            
    return path_sinCiclos


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    
    
    return expand_paths + list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    cami = [Path(origin_id)]
    while cami and cami[0].last != destination_id:
        expansio = remove_cycles(expand(cami[0],map))
        cami = insert_depth_first_search(expansio, cami[1:])
    
    if cami:
        return cami[0]
    else:
        print("No existeix Solucio")


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """

    return list_of_path + expand_paths


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    cami = [Path(origin_id)]
    while cami and cami[0].last != destination_id:
        expansio = remove_cycles(expand(cami[0],map))
        cami = insert_breadth_first_search(expansio, cami[1:])
    
    if cami:
        return cami[0]
    else:
        print("No existeix Solucio")


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    
    for path in expand_paths:
        
        if type_preference == 0:
            cost = 1
            
        elif type_preference == 1:
       
            cost = map.connections[path.last][path.penultimate]
                 
        elif type_preference == 2:
            
            if map.stations[path.penultimate]['line'] != map.stations[path.last]['line']:
                cost = 0
            else:
               cost = map.velocity[map.stations[path.last]['line']] * map.connections[path.last][path.penultimate]
            
        elif type_preference == 3:
            
            if map.stations[path.penultimate]['line'] != map.stations[path.last]['line']:
                cost = 1
            else:
                cost = 0
        path.update_g(cost)

                
        
    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """

    path_ordenat = list_of_path + expand_paths 
    path_ordenat.sort(key=lambda path: path.g)
    
    

    return path_ordenat


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    cami = [Path(origin_id)]
    while cami and cami[0].last != destination_id:
        expansio = calculate_cost(remove_cycles(expand(cami[0],map)), map,type_preference)
        cami = insert_cost(expansio, cami[1:])


    
    if cami:
        return cami[0]
    else:
        print("No existeix Solucio")


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    
    for path in expand_paths:
        
        if type_preference == 0:
            if path.last == destination_id: 
                h =0
            else:
                h = 1
            
        elif type_preference == 1:
            velocidadMax= max(map.velocity.values())
            destino = (map.stations[destination_id]['x'], map.stations[destination_id]['y'])
            actual = (map.stations[path.last]['x'], map.stations[path.last]['y'])
            distancia = euclidean_dist(actual, destino)
            
            h = distancia/ velocidadMax
            
                 
        elif type_preference == 2:
            
            destino = (map.stations[destination_id]['x'], map.stations[destination_id]['y'])
            actual = (map.stations[path.last]['x'], map.stations[path.last]['y'])
            h = euclidean_dist(actual, destino)
            
        elif type_preference == 3:
            
            if map.stations[path.penultimate]['line'] != map.stations[path.last]['line']:
                h = 1
            else:
                h = 0
                
        path.update_h(h)

                
        
    return expand_paths



def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()

    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    camiSinRed = []
    
    for path in expand_paths:
        if path.last in visited_stations_cost.keys():
            if path.g < visited_stations_cost[path.last]:
                visited_stations_cost[path.last] = path.g
                list_of_path = [p for p in list_of_path if p.last != path.last] 
                camiSinRed.append(path)
        else:
            visited_stations_cost[path.last] = path.g
            camiSinRed.append(path)
    
    return camiSinRed, list_of_path, visited_stations_cost

        

def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    path_ordenat = list_of_path + expand_paths

    return sorted(path_ordenat, key=lambda path: path.f)


def distance_to_stations(coord, map):
    """
        From coordinates, it computes the distance to all stations in map.
        Format of the parameter is:
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    distancias = {}
            
    for clauId, clauInfo in map.stations.items():
        coordEstacion = [clauInfo['x'], clauInfo['y']]
        distancias[clauId] = math.dist(coord, coordEstacion)

   
    distancias_ordenades = dict(sorted(distancias.items(), key=lambda item: (item[1], item[0])))

    return distancias_ordenades


def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    distancias = {} 
    cami = [Path(origin_id)] 

    while cami and cami[0].last != destination_id:
        expansio = expand(cami[0], map)
        expansio = remove_cycles(expansio)
        expansio = calculate_cost(expansio, map, type_preference)
        expansio = calculate_heuristics(expansio, map, destination_id)
        expansio = update_f(expansio)
        
        expansio, cami, distancias = remove_redundant_paths(expansio, cami, distancias)
        cami = insert_cost_f(expansio, cami[1:])
        
        if not cami:
            break

    if cami:
        return cami[0]
    else:
        print("No existeix Solució")

def Astar_improved(origin_coord, destination_coord, map):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
            destination_coord (list): Two REAL values, which refer to the coordinates of the final position
            map (object of Map class): All the map information

        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
    """
    
    map.add_station(0, "Origin", 0, origin_coord[0], origin_coord[1])
    map.add_station(-1, "Destination", 0, destination_coord[0], destination_coord[1])

    
    map.connections[0] = {}
    map.connections[-1] = {}

    
    for station, station_data in map.stations.items():
        map.connections[0][station] = euclidean_dist(origin_coord, [station_data["x"], station_data["y"]]) / 5
        map.connections[-1][station] = euclidean_dist(destination_coord, [station_data["x"], station_data["y"]]) / 5

    for station in map.stations:
        map.connections[station][0] = map.connections[0][station]
        map.connections[station][-1] = map.connections[-1][station]


    map.connections[0][-1] = euclidean_dist(origin_coord, destination_coord) / 5
    map.connections[-1][0] = euclidean_dist(origin_coord, destination_coord) / 5


    return Astar(0, -1, map, 1)