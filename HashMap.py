class HashMap:
    def __init__(self):
        self.size = 100
        self.map = [None] * self.size

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

        if self.map[key_hash] is None:
            self.map[key_hash] = list([kv_pair])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(kv_pair)
            return True

    def addToDict(self,key_for_hash, key_for_dict, value_for_dict ):
        key_hash = self.get_hash(key_for_hash)
        if self.map[key_hash] is not None:
            my_dictionary = self.map[key_hash][0][1]
            if isinstance(my_dictionary, dict):
                my_dictionary[key_for_dict] = value_for_dict


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
