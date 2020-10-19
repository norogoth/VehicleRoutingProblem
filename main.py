#Landon Aaker
#ID: 001236202

from HashMap import HashMap
from Route import Route
from Truck import Truck
import csv
from csv import DictReader
import datetime

def main():

    package_hash_map = HashMap()

    with open('Resources/packageCSV.csv','r') as packageCSV:
        dict_read_package = DictReader(packageCSV)
        column_names = dict_read_package.fieldnames
        column_names[0] = 'Package ID'
        for row in dict_read_package:
            package_hash_map.add(row['Package ID'], row)
    packageCSV.close()

    Truck.create_trucks()
    Truck.load(package_hash_map) #load all the trucks with the packages. Clustered by zip code. Round robin zip code assignment.
    Route.init_distance_table()
    Route.init_nodes()
    Route.set_priority_packages(package_hash_map)
    Route.init_priority_nodes(package_hash_map)
    Route.create_route(package_hash_map)

    # nine_datetime = datetime.datetime(2020, 1, 1, 9, 00)
    # ten_datetime = datetime.datetime(2020, 1, 1, 10, 00)
    # one_datetime = datetime.datetime(2020, 1, 1, 13, 00)
    # Route.print_status_at_time(package_hash_map, nine_datetime)
    # Route.print_status_at_time(package_hash_map, ten_datetime)
    # Route.print_status_at_time(package_hash_map, one_datetime)

    Route.print_package_statuses(package_hash_map)
    package_hash_map.self_adjust()
    Route.verification(package_hash_map)
    Route.interface(package_hash_map)

    Route.set_priority_packages(package_hash_map)
    Route.init_priority_nodes(package_hash_map)

main()