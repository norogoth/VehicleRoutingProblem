from HashMap import HashMap

class Truck:

    #attributes
    number_of_trucks = 0
    all_truck_zips = [] * number_of_trucks
    truck_list = []
    truck_counter = 0

    #constructor
    def __init__(self):
        self.number = Truck.truck_counter
        Truck.truck_counter += 1
        self.packages = []
        self.current_node = 0
        self.zip_array = []

    def getNumber(self):
        return self.number

    #load the trucks with the packages
    @staticmethod
    def create_trucks():
        truck_one = Truck()
        truck_two = Truck()
        Truck.truck_list.append(truck_one)
        Truck.truck_list.append(truck_two)
        Truck.number_of_trucks = len(Truck.truck_list)

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
        # Assigning trucks packages based on zip code
        current_truck = 0
        for zipcode in zipArray:
            if isinstance(Truck.truck_list[current_truck], Truck):
                Truck.truck_list[current_truck].zip_array.append(zipcode)
                if current_truck+1 > Truck.number_of_trucks-1:
                    current_truck = 0
                else:
                    current_truck += 1
        #load packages on trucks based on zip code
        print(Truck.truck_list[0].zip_array)
        for truck in Truck.truck_list:
            for package in package_hash_map.get_map():
                if package is not None:
                    #print(package[0][1]['Zip'])
                    if package[0][1]['Zip'] in truck.zip_array:
                        truck.packages.append(package[0][1])

