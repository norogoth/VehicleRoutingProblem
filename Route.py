from csv import DictReader
from Truck import Truck
import datetime
from datetime import timedelta

class Route:

    idCounter = 0
    distance_dictionary = {}
    nodes_to_travel = []
    node_travel_timestamp = {}
    minutes_elapsed = [0, 0]
    time = [datetime.datetime(2020, 1, 1, 8, 0), datetime.datetime(2020, 1, 1, 8, 0)]


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
    def increment_time(truck_number, miles):
        minutes_passed = Route.miles_to_minutes(miles)
        Route.time[truck_number] += timedelta(minutes=minutes_passed)

    @staticmethod
    def init_distance_table():
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

    def create_route(packageHashMap):
        truck_one = Truck.truck_list[0]
        truck_two = Truck.truck_list[1]
        next_node = -1
        distance_to_next_node = 10000000
        while len(Route.nodes_to_travel) > 0:
            for truck in [truck_one, truck_two]:
                if isinstance(truck, Truck):
                    next_node = Route.get_closet_node(truck.current_node) #get the closest node the current node of the truck
                    miles_to_next_node = Route.get_distance_to_node(truck.current_node, next_node)
                    Route.increment_time(truck.number, miles_to_next_node) #move the clock for this truck
                    Route.nodes_to_travel.remove(next_node) #take away nodes we have travelled to
                    Route.travel_to_next_node(truck, next_node)
                    Route.package_is_delivered(packageHashMap, next_node, Route.time[truck.number])
        for truck in [truck_one, truck_two]:
            Route.travel_to_next_node(truck, 0)

    @staticmethod
    def package_is_delivered(packagehashmap, address_number, timestamp):
        for package in packagehashmap.map:
            if package is not None:
                if package[0][1]["Address ID"] == str(address_number):
                    package[0][1]["Status"] = "Delivered"
                    package[0][1]["Time Delivered"] = timestamp
                print(package[0][1])

    @staticmethod
    def travel_to_next_node(truck, next_node):
        distance_to_next_node = Route.get_distance_to_node(truck.current_node, next_node)  # get distance to the next node
        Route.minutes_elapsed[truck.number] += Route.miles_to_minutes(float(distance_to_next_node))  # add the minutes travelled to minutes_elapsed array
        #print("Truck ", truck.number, "has traveled for ", Route.minutes_elapsed[truck.number]," minutes and ",Route.minutes_to_miles(Route.minutes_elapsed[truck.number])," miles.")
        Route.node_travel_timestamp[next_node] = Route.time[truck.number]

    # @staticmethod
    # def

    @staticmethod
    def print_package_statuses(packageHashMap):
        for item in packageHashMap.map:
            if item is not None:
                pd = item[0][1] #Get package dictionary
                item_address_id = item[0][1]["Address ID"]
                #print("Address ID is "+item_address_id+"|  nodes_to_travel is "+str(Route.nodes_to_travel))
                #TODO: find status of package by linking it to nodes_to_travel then linking that to the package
                print(("Package ID: " + str(pd["Package ID"])+" | ").rjust(20," ")
                        +("Address: " + str(pd["Address"])+", "+str(pd["City"])+", "+ str(pd["State"])+ " " + str(pd["Zip"]) +" |").rjust(65," ")
                      + ("Deadline: " + str(pd["Deadline"]) + " | ").rjust(30," ")
                      + ("Kg: " + str(pd["Kg"]) + " | ").rjust(10," ")
                      + ("Special Notes" + str(pd["Special Notes"]) + " | ").rjust(90," ")
                      + ("Status: "+ str(pd["Status"])).rjust(20," ")
                      + ("Status: " + str(pd["Time Delivered"])).rjust(20, " ")
                )

    @staticmethod
    def printDistArray():
        d = Route.distance_dictionary
        for key in d:
            print(key+": "+str(d[key]))