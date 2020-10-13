from csv import DictReader
class Node:

    idCounter = 0
    distance_dictionary = {}

    def __init__(self, address, distanceArray, isCompleted):
        self.id = Node.idCounter
        self.address = address
        self.isCompleted = False
        Node.idCounter += 1

    @staticmethod
    def init_everything():
        #initialize Distance Table
        with open('Resources/DistanceTable4.csv', 'r') as distanceArrayCSV:
            dict_read_dist_array = DictReader(distanceArrayCSV)
            column_names = dict_read_dist_array.fieldnames
            column_names[0] = 'ID'
            for row in dict_read_dist_array:
                #print(row['ID']+":   "+str(row))
                Node.distance_dictionary[row['ID']] = row
        #Get Table to translate IDs into Distance Table

    def printDistArray():
        d= Node.distance_dictionary
        for key in d:
            print(key+": "+str(d[key]))