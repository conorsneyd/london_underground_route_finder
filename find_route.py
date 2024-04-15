from underground import underground
from print_route import print_route

def find_route(start, end):
    #find route between input stations
    if start == end:
        return("<ul><li>You're already there!</li></ul>", start, end)
    else:
        #initialise queue for processing routes
        routes = []
        shortest_complete_route = []
           
        #add one route to queue in each direction per line at starting station
        for station in underground.graph_dict:
            if station == start:
                lines = underground.graph_dict[station].value[1]
                for line in lines:
                    routes.append([0, 0, [[station, line, 1]]])
                    routes.append([0, 0, [[station, line, 2]]])

        while routes:
            #pop route from front of queue and extract required variables
            current_route = routes.pop(0)
            current_route_time = current_route[0]
            current_route_transfers = current_route[1]
            current_route_stations = current_route[2]
            current_route_stations_names = [station[0] for station in current_route_stations]
            latest_station = current_route[-1][-1][0]
            latest_line = current_route[-1][-1][1]
            latest_direction = current_route[-1][-1][2]

            #if route is complete, check whether it's shorter than current shortest complete route and replace if so
            if latest_station == end:
                if not shortest_complete_route or current_route[0] <= shortest_complete_route[0]:
                    if not shortest_complete_route or current_route[1] < shortest_complete_route[1]:
                        shortest_complete_route = current_route

            #if route incomplete, check edges of latest station vertex
            else:
                for neighbour in underground.graph_dict[latest_station].edges:
                    add_route = True
                    #for each neighbour station, make sure it's not already in the current route or another route with a shorter time   
                    if neighbour not in current_route_stations_names:
                        for route in routes:
                            route_stations = route[2]
                            route_stations_names = [station[0] for station in route_stations]
                            if neighbour in route_stations_names and route[0] < current_route_time:
                                add_route = False
                        if add_route == True:
                            neighbour_lines = underground.graph_dict[latest_station].edges[neighbour][0]
                            neighbour_distance = underground.graph_dict[latest_station].edges[neighbour][1]
                            neighbour_direction = underground.graph_dict[latest_station].edges[neighbour][2]
                            for neighbour_line in neighbour_lines:
                                #if neighbour station on latest line, and route time not greater than shortest complete route, add station to current route and add updated route to queue
                                #(if latest station is starting station, make sure neighbour direction equals latest direction to prevent routes flipping directions at starting station)
                                if neighbour_line == latest_line and (neighbour_direction == latest_direction or len(current_route_stations) > 1):
                                    new_route_time = current_route_time + neighbour_distance
                                    if not shortest_complete_route or new_route_time <= shortest_complete_route[0]:
                                        new_route_stations = current_route_stations + [[neighbour, neighbour_line, neighbour_direction]]
                                        routes.append([new_route_time, current_route_transfers, new_route_stations])

                                #if neighbour station on different line, and route time not greater than shortest complete route, add station to current route and add updated route to queue
                                #(make sure latest line not in neighbour lines to prevent routes jumping back and forth between lines passing through same sequence of stations)
                                #(make sure latest station is not starting station to prevent routes hopping between lines at starting station)
                                elif neighbour_line != latest_line and latest_line not in neighbour_lines and len(current_route_stations) > 1:
                                    new_route_time = current_route_time + neighbour_distance + 4
                                    new_route_transfers = current_route_transfers + 1
                                    if not shortest_complete_route or new_route_time <= shortest_complete_route[0]:
                                        new_route_stations = current_route_stations + [[neighbour, neighbour_line, neighbour_direction]]
                                        if not shortest_complete_route or new_route_time <= shortest_complete_route[0]:
                                            new_route_stations = current_route_stations + [[neighbour, neighbour_line, neighbour_direction]]
                                            routes.append([new_route_time, new_route_transfers, new_route_stations])

                        
        
        return print_route(shortest_complete_route)
