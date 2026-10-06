from SearchAlgorithm import *
from SubwayMap import *
from utils import *

if __name__=="__main__":
    ROOT_FOLDER = './CityInformation/Barcelona_City/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)



    ### BELOW HERE YOU CAN CALL ANY FUNCTION THAT yoU HAVE PROGRAMED TO ANSWER THE QUESTIONS OF THE EXAM ###
    ### this code is just for you, you won't have to upload it after the exam ###


    #this is an example of how to call some of the functions that you have programed
    example_path=uniform_cost_search(9, 3, map, 1)
    print_list_of_path_with_cost([example_path])

    camino=breadth_first_search(23, 18, map)
    print_list_of_path([camino])
    
    cami=Astar(16, 9, map,1)
    print_list_of_path_with_cost([cami])
    
    
    
    camino =  [1,2]
    
    total_cost = 0
    for i in range(len(camino) - 1):
        nodo = camino[i]
        siguiente = camino[i + 1]

        if map.stations[nodo]['line'] != map.stations[siguiente]['line']:
            cost = 0
        else:
            cost = map.velocity[map.stations[nodo]['line']] * map.connections[siguiente][nodo]

        total_cost += cost
    
    print(f"COSTE TOTAL EN DISTANCIA: {total_cost}")
    
    for i in range(len(camino) - 1):
        h= 0
        nodo = camino[i]
        siguiente = camino[i + 1]
        velocidadMax= max(map.velocity.values())
        destino = (map.stations[6]['x'], map.stations[6]['y'])
        actual = (map.stations[siguiente]['x'], map.stations[siguiente]['y'])
        distancia = euclidean_dist(actual, destino)
        
        h = distancia/ velocidadMax
    
    f= total_cost+h
    print(h)
    print(f)
    paths= remove_redundant_paths([Path([2, 5, 1], [2, 5, 3], [2, 5, 7], [2, 5, 8])], [Path([2, 7, 3], [2, 1], [2, 7, 6, 4], [2, 7, 6, 9])], {7: 1.0, 5: 1.5, 1: 4.0, 3: 2.0, 6: 1.1, 4: 3.1, 9: 2.6})
    