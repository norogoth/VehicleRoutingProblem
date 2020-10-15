#Landon Aaker
#ID: 001236202

from HashMap import HashMap
from Route import Route
from Truck import Truck
import csv
from csv import DictReader
import datetime

def main():

    packageHashMap = HashMap()

    with open('Resources/packageCSV.csv','r') as packageCSV:
        dict_read_package = DictReader(packageCSV)
        column_names = dict_read_package.fieldnames
        column_names[0] = 'Package ID'
        for row in dict_read_package:
            packageHashMap.add(row['Package ID'], row)
    packageCSV.close()

    Truck.create_trucks()
    Truck.load(packageHashMap) #load all the trucks with the packages. Clustered by zip code. Round robin zip code assignment.
    Route.init_distance_table()
    Route.init_nodes()
    Route.create_route(packageHashMap)
    nine_datetime = datetime.datetime(2020, 1, 1, 9, 00)
    ten_datetime = datetime.datetime(2020, 1, 1, 10, 00)
    one_datetime = datetime.datetime(2020, 1, 1, 13, 00)
    Route.print_status_at_time(packageHashMap, nine_datetime)
    Route.print_status_at_time(packageHashMap, ten_datetime)
    Route.print_status_at_time(packageHashMap, one_datetime)
    Route.print_package_statuses(packageHashMap)

main()