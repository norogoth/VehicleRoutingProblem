from csv import DictReader
from Truck import Truck
import datetime
from datetime import timedelta

class Route:

    idCounter = 0
    distance_dictionary = {}
    nodes_to_travel = []
    priority_packages = []
    priority_nodes = []
    node_travel_timestamp = {}
    minutes_elapsed = [0, 0]
    time = [datetime.datetime(2020, 1, 1, 8, 0), datetime.datetime(2020, 1, 1, 8, 0)]
    total_miles = 0


    def __init__(self, address, distanceArray, isCompleted):
        self.id = Route.idCounter
        self.address = address
        self.isCompleted = False
        Route.idCounter += 1

    @staticmethod
    def set_priority_packages(package_hash_map):
        for item in package_hash_map.map:
            if item is not None:
                 if item[0][1]["Deadline"] != "EOD":
                     Route.priority_packages.append(item[0][1]["Package ID"])
        #print(Route.priority_packages)

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
    #O(n) algorithm iterates through every node in the Route.nodes_to_travel array for the given ID only.
    def select_node(package_hash_map, current_node_id):
        lowest = 10000000000
        lowest_node_id = -1
        #print("nodes to travel is ", Route.nodes_to_travel)
        #print("priority nodes are ", Route.priority_nodes)
        if len(Route.priority_packages) > 0:
            for i in Route.nodes_to_travel:
                distance_to_this_node = Route.distance_dictionary[str(current_node_id)][str(i)]
                if float(distance_to_this_node) < float(lowest):
                    if id != i:
                        lowest_node_id = i
                        lowest = distance_to_this_node
            return lowest_node_id
        for i in Route.nodes_to_travel:
            distance_to_this_node = Route.distance_dictionary[str(current_node_id)][str(i)]
            if float(distance_to_this_node) < float(lowest):
                if id != i:
                    lowest_node_id = i
                    lowest = distance_to_this_node
        return lowest_node_id

    @staticmethod
    def init_priority_nodes(package_hash_map):

        for item in package_hash_map.map:
            if item is not None:
                #print("item[0][1][Package ID]", item[0][1]["Package ID"], "Route.priority_packages, ", Route.priority_packages)
                if str(item[0][1]["Package ID"]) in str(Route.priority_packages):
                    Route.priority_nodes.append(item[0][1]["Address ID"])


    @staticmethod
    def get_distance_to_node(node_one, node_two):
        return Route.distance_dictionary[str(node_one)][str(node_two)]

    @staticmethod
    def verification(package_hash_map):
        packages_sent = 0
        for package in package_hash_map.map:
            if package is not None:
                if package[0][1]["Status"] == "Delivered":
                    packages_sent += 1
                else:
                    print ("Not all packages have been delivered")
                    return
        print("Total Miles traveled: ", round(Route.total_miles,2) )
        start_time = datetime.datetime(2020, 1, 1, 8, 0)
        longer_time = datetime.datetime(2020, 1, 1, 8, 0)
        if Route.time[0] > Route.time[1]:
            longer_time = Route.time[0]
        elif Route.time[1] > Route.time[0]:
            longer_time = Route.time[1]
        print("Total time elapsed: ", round((longer_time - start_time).total_seconds()/60, 2), " minutes")

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
    # ALGORITHM: Using the shortest path algorithm, we will set the routes for the trucks
    # O(n^2) algorithm. The "while" loop goes for n iterations (where n is the number of nodes with packages)
    # and the "next_node" goes for another n.
    # This code has a "for" loop for trucks, but this algorithm is O(n^2) because of the "Route.get_cloest_node" method.
    def create_route(packageHashMap):
        next_node = -1
        distance_to_next_node = 10000000
        while len(Route.nodes_to_travel) > 0:
            for truck in Truck.truck_list:
                if isinstance(truck, Truck):
                    next_node = Route.select_node(packageHashMap, truck.current_node) #get the closest node the current node of the truck
                    miles_to_next_node = Route.get_distance_to_node(truck.current_node, next_node)
                    Route.increment_time(truck.number, miles_to_next_node) #move the clock for this truck
                    Route.nodes_to_travel.remove(next_node) #take away nodes we have travelled to
                    Route.travel_to_next_node(truck, next_node)
                    Route.package_is_delivered(packageHashMap, next_node, Route.time[truck.number])
        for truck in Truck.truck_list:
            Route.travel_to_next_node(truck, 0)

    @staticmethod
    #interface
    def interface(package_hash_map):
        hour = int(input("To check a specific time for the status of packages, start by entering an hour: "))
        minute = int(input("What minute would you like to check for? "))
        date_time = datetime.datetime(2020, 1, 1, hour, minute)
        Route.print_status_at_time(package_hash_map, date_time)

    @staticmethod
    # Change the status of a package and add a timestamp
    #O(n)
    def package_is_delivered(packagehashmap, address_number, timestamp):
        for package in packagehashmap.map:
            if package is not None:
                if package[0][1]["Address ID"] == str(address_number):
                    package[0][1]["Status"] = "Delivered"
                    package[0][1]["Time Delivered"] = timestamp
                #print(package[0][1])

    @staticmethod
    def travel_to_next_node(truck, next_node):
        distance_to_next_node = float(Route.get_distance_to_node(truck.current_node, next_node))  # get distance to the next node
        Route.total_miles += distance_to_next_node
        Route.minutes_elapsed[truck.number] += Route.miles_to_minutes(float(distance_to_next_node))  # add the minutes travelled to minutes_elapsed array
        #print("Truck ", truck.number, "has traveled for ", Route.minutes_elapsed[truck.number]," minutes and ",Route.minutes_to_miles(Route.minutes_elapsed[truck.number])," miles.")
        Route.node_travel_timestamp[next_node] = Route.time[truck.number]

    # @staticmethod
    # def

    @staticmethod

    def print_status_at_time(package_hash_map, date_time):
        print( "===============================================\n"
              + "Package status by " + str(date_time.hour) + ":" + str(date_time.minute) + "\n"
        + "===============================================\n")
        print(("Package ID" + " | ").rjust(20, " ")
             + ("Address" + " |").rjust(70, " ")
             + ("Deadline: " + " | ").rjust(30, " ")
             + ("Kg" + " | ").rjust(10, " ")
             + ("Special Notes" + " | ").rjust(70, " ")
             + ("Status" + " |   ").rjust(20, " ")
             + ("TimeStamp" + " |   ").rjust(23, " ")
             )
        for item in package_hash_map.map:
            if item is not None:
                pd = item[0][1]  # Get package dictionary
                time_delivered = pd["Time Delivered"]
                if isinstance(time_delivered, datetime.datetime):
                    if time_delivered < date_time:
                        item_address_id = item[0][1]["Address ID"]
                        # print("Address ID is "+item_address_id+"|  nodes_to_travel is "+str(Route.nodes_to_travel))
                        # TODO: find status of package by linking it to nodes_to_travel then linking that to the package
                        print(("Package ID: " + str(pd["Package ID"]) + " | ").rjust(20, " ")
                              + (str(pd["Address"]) + ", " + str(pd["City"]) + ", " + str(pd["State"]) + " " + str(
                            pd["Zip"]) + " |").rjust(70, " ")
                              + (str(pd["Deadline"]) + " | ").rjust(30, " ")
                              + ((pd["Kg"]) + " | ").rjust(10, " ")
                              + (str(pd["Special Notes"]) + " | ").rjust(70, " ")
                              + (str(pd["Status"]) + " |   ").rjust(20, " ")
                              + (str(pd["Time Delivered"])).rjust(20, " ")
                              )

    @staticmethod
    #Print the status of packages for the entire day
    def print_package_statuses(package_hash_map):
        end_of_day = datetime.datetime(2020, 1, 1, 23, 59)
        Route.print_status_at_time(package_hash_map, end_of_day)

    @staticmethod
    def printDistArray():
        d = Route.distance_dictionary
        for key in d:
            print(key+": "+str(d[key]))