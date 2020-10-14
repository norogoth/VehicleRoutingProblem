from HashMap import HashMap

class Truck:

    #attributes
    number_of_trucks = 2
    all_truck_zips = [] * number_of_trucks
    truck_list = []

    #constructor
    def __init__(self, number, package, current_node):
        self.number = number
        self.package = package
        self.current_node = current_node
        self.zip_array = []

    def getNumber(self):
        return self.number

    #load the trucks with the packages
    @staticmethod
    def load(package_hash_map):
        zipArray = []
        if isinstance(package_hash_map, HashMap):
            #Get all the zip codes
            for kv_pair in package_hash_map.map:
                if kv_pair is not None:
                    this_zip = kv_pair[0][1]['Zip']
                    if this_zip not in zipArray:
                        zipArray.append(this_zip)

        #Assign zip codes to all_truck_zips
        # TODO: make this all OOP instead of arrays and stuff
        for truck_zips in range(0,Truck.number_of_trucks):
            Truck.all_truck_zips.append([])
        current_truck = 0
        for zipcode in zipArray:
            Truck.all_truck_zips[current_truck].append(zipcode)
            if current_truck+1 > Truck.number_of_trucks-1:
                current_truck = 0
            else:
                current_truck += 1
        #load packages on to all_truck_zips
        for package in package_hash_map.get_map():
            if package is not None:
                for truck_zips in Truck.all_truck_zips:
                    if package[0][1]['Zip'] in truck_zips:


