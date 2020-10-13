from HashMap import HashMap
from Node import Node
from Truck import Truck
import csv
from csv import DictReader

def main():

    packageHashMap = HashMap()

    with open('Resources/packageCSV.csv','r') as packageCSV:
        dict_read_package = DictReader(packageCSV)
        column_names = dict_read_package.fieldnames
        column_names[0] = 'Package ID'
        for row in dict_read_package:
            packageHashMap.add(row['Package ID'], row)
    packageCSV.close()

    # with open('Resources/AddressIdMap.csv','r') as distanceArrayCSV:
    #    dict_read_dist_array = DictReader(distanceArrayCSV)
    #    column_names = dict_read_dist_array.fieldnames
    #    column_names[0] = 'ID'
    #    for row in dict_read_dist_array:
    #         print(row)
    # distanceArrayCSV.close()
    #
    # with open('Resources/DistanceTable4.csv','r') as distanceArrayCSV:
    #    dict_read_dist_array = DictReader(distanceArrayCSV)
    #    column_names = dict_read_dist_array.fieldnames
    #    column_names[0] = 'ID'
    #    for row in dict_read_dist_array:
    #         print(row)
    # distanceArrayCSV.close()

    #packageHashMap.print()
    #print(packageHashMap.map)
    Truck.load(packageHashMap)
    Node.init_everything()
    #Node.printDistArray()

main()