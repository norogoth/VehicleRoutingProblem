class HashMap:

    def __init__(self):
        self.size = 100
        self.current_total = 0
        self.map = [None] * self.size

    def self_adjust(self):
        if self.current_total > self.size * .9:
            self.size = self.size * 11
            temp_map = self.map
            self.map = [None] * self.size
            for item in temp_map:
                self.add(item)

    def get_map(self):
        return self.map

    def get_hash(self, key):
        hash_var = 0
        for char in str(key):
            hash_var += ord(char)
        hash_var += int(key)
        return hash_var % self.size

    def add(self, key, value):
        key_hash = self.get_hash(key)
        kv_pair = [key, value]
        self.self_adjust()
        if self.map[key_hash] is None:
            self.map[key_hash] = list([kv_pair])
            self.current_total += 1
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(kv_pair)
            self.current_total += 1

    def addToDict(self,key_for_hash, key_for_dict, value_for_dict ):
        key_hash = self.get_hash(key_for_hash)
        if self.map[key_hash] is not None:
            my_dictionary = self.map[key_hash][0][1]
            if isinstance(my_dictionary, dict):
                my_dictionary[key_for_dict] = value_for_dict

    def get_address_id(self, package_id):
        for item in self.map:
            if item is not None:
                if int(item[0][1]["Package ID"]) == int(package_id):
                    return item[0][1]["Address ID"]
        else:
            return -1


    def get(self, key):
        key = str(key)
        key_hash = self.get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        key_hash = self.get_hash(key)
        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    def print(self):
        for item in self.map:
            if item is not None:
                print(str(item[0]))
