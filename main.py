#Landon Aaker
#ID: 001236202

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

    print(packageHashMap.get(1)['Package ID'])
    #print(packageHashMap.map)
    Truck.load(packageHashMap)
    Node.init_everything()
    #Node.printDistArray()

main()