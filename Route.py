from csv import DictReader
from Truck import Truck
class Route:

    idCounter = 0
    distance_dictionary = {}
    nodes_to_travel = []
    node_travel_timestamp = {}
    minutes_elapsed = [0,0]

    def __init__(self, address, distanceArray, isCompleted):
        self.id = Route.idCounter
        self.address = address
        self.isCompleted = False
        Route.idCounter += 1

    @staticmethod
    #Sets which nodes need to be travelled
    def init_nodes():
        for i in range(1, 27):
            Route.nodes_to_travel.append(i)

    @staticmethod
    def init_everything():
        #initialize Distance Table
        with open('Resources/DistanceTable4.csv', 'r') as distanceArrayCSV:
            dict_read_dist_array = DictReader(distanceArrayCSV)
            column_names = dict_read_dist_array.fieldnames
            column_names[0] = 'ID'
            for row in dict_read_dist_array:
                #print(row['ID']+":   "+str(row))
                Route.distance_dictionary[row['ID']] = row
        #Get Table to translate IDs into Distance Table

    @staticmethod
    #return the distance dictionary for the given item
    def get_dist_dict(id):
        return Route.distance_dictionary[str(id)]

    @staticmethod
    def get_closet_node(id):
        lowest = 10000000000
        lowest_node_id = -1
        i = -1
        for i in Route.nodes_to_travel:
            #print(Route.distance_dictionary[str(id)][str(i)])
            distance_to_this_node = Route.distance_dictionary[str(id)][str(i)]
            if float(distance_to_this_node) < float(lowest):
                if id != i:
                    lowest_node_id = i
                    lowest = distance_to_this_node
        #print("lowest is ", lowest)
        return lowest_node_id
        Route.nodes_to_travel.append(lowest_node_id)
        #print("lowest for ",id," is :",i)

    @staticmethod
    def get_distance_to_node(node_one, node_two):
        return Route.distance_dictionary[str(node_one)][str(node_two)]

    @staticmethod
    def miles_to_hour(miles):
        return float(miles)/18.0

    @staticmethod
    def miles_to_minutes(miles):
        return 60 * float(miles) / 18.0

    @staticmethod
    def minutes_to_miles(minutes):
        return 18 * float(minutes) / 60

    @staticmethod
    # Using the shortest path algorithm, we will set the routes for the trucks
    def create_route():
        truck_one = Truck.truck_list[0]
        truck_two = Truck.truck_list[1]
        next_node = -1
        distance_to_next_node = 10000000
        while len(Route.nodes_to_travel) > 0:
            for truck in [truck_one, truck_two]:
                if isinstance(truck, Truck):
                    next_node = Route.get_closet_node(truck.current_node) #get the closest node the current node of the truck
                    #print("next node will be: ", next_node)
                    Route.nodes_to_travel.remove(next_node) #take away nodes we have travelled to
                    Route.travel_to_next_node(truck, truck.current_node, next_node)
        #print("going home")
        for truck in [truck_one, truck_two]:
            Route.travel_to_next_node(truck, truck.current_node, 0)


    @staticmethod
    def travel_to_next_node(truck, current_node, next_node):
        distance_to_next_node = Route.get_distance_to_node(truck.current_node, next_node)  # get distance to the next node
        Route.minutes_elapsed[truck.number] += Route.miles_to_minutes(float(distance_to_next_node))  # add the minutes travelled to minutes_elapsed array
        #print("Truck ", truck.number, "has traveled for ", Route.minutes_elapsed[truck.number]," minutes and ",Route.minutes_to_miles(Route.minutes_elapsed[truck.number])," miles.")
        Route.node_travel_timestamp[next_node] = float(Route.minutes_elapsed[truck.number]) + float(
            Route.get_distance_to_node(truck.current_node, next_node))

    @staticmethod
    def print_package_statuses(packageHashMap):
        for item in packageHashMap.map:
            if item is not None:
                pd = item[0][1] #Get package dictionary
                print(("Package ID: " + str(pd["Package ID"])+" | ").rjust(20," ")
                        +("Address: " + str(pd["Address"])+" | ").rjust(50," ")
                        +("City: " + str(pd["City"])+" | ").rjust(30," ")
                        +("State: " + str(pd["State"])+" | ").rjust(20," ")
                      + ("Zip: " + str(pd["Zip"]) + " | ").rjust(17," ")
                      + ("Deadline: " + str(pd["Deadline"]) + " | ").rjust(30," ")
                      + ("Kg: " + str(pd["Kg"]) + " | ").rjust(10," ")
                      + ("Special Notes" + str(pd["Special Notes"]) + " | ").rjust(90," ")
                      + ("Status: " ).rjust(20," ")
                )

    @staticmethod
    def printDistArray():
        d = Route.distance_dictionary
        for key in d:
            print(key+": "+str(d[key]))