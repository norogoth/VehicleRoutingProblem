from HashMap import HashMap

class Truck:

    #attributes
    packages = [[],[],[]]

    #constructor
    def __init__(self, number, package, currentNode):
        self.number = number
        self.package = package
        self.currentNode = currentNode

    def getNumber(self):
        return self.number

    #load the trucks with the packages
    def load(packageHashMap):
        if isinstance(packageHashMap, HashMap):
            #Get all the zip codes
            zipArray = []
            for kv_pair in packageHashMap.map:
                if kv_pair is not None:
                    #print(kv_pair[0][0] + ": " + kv_pair[0][1]['Zip'])
                    thisZip = kv_pair[0][1]['Zip']
                    if thisZip not in zipArray:
                        zipArray.append(thisZip)
        number_of_trucks = 2
        trucks = [] * number_of_trucks
        #Assign zip codes to trucks
        for truck in range(0,number_of_trucks):
            truck = []
            trucks.append([])
            current_truck = 0
        for zipcode in zipArray:
            trucks[current_truck].append(zipcode)
            if current_truck+1 > number_of_trucks-1:
                current_truck = 0
            else:
                current_truck += 1
        #load packages on to trucks

