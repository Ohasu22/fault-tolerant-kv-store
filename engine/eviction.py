# I am thinking because my store has limited memory capacity I need something to delete or rather remove the keys when I run out of space
# my store has two values
# I'll just keep it simple so like user:1 is key and Ojas is the value edit1: timestamp will be added here as well
# I'll use a dictionary to handle this structure, its more efficient that way I guess

'''
from collections import OrderedDict

# I need two things here, to know what my capacity is and my cache
# In this dictionary, leftmost key is the least recently used and rightmost one is the most recently used
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    # okay so now my capacity will look for the number of keys allowed in my cache and cache keeps my keys in order

    def get(self, key):
        if key not in self.cache:
            return False

        #if my key is accessed then I'll make it the most recent used
        self.cache.move_to_end(key)
        return True

    def put(self, key):
        #gotta find that key in my cache first
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            # dont care about the value now so I'll just initialise with None
            self.cache[key] = None

        # I'll evict the oldest key which is not in use for a long time and I'll return that evicted key
        if len(self.cache) > self.capacity:
            evicted_key, _ = self.cache.popitem(last=False)
            return evicted_key

        return None

    #edit: I have to add delete because its just more convenient to have another function rather that implementing it in my put function
    # this is for manual deletion, my put function is deleting automatically(LRU)
    def delete(self, key):
        self.cache.pop(key, None)

'''

# my store already is handling the get and my LRU is standalone rn
# get function is returning a bool which I dont want
# my store holds the data so I guess I wouldnt need this strategy
# my LRU should only track keys + order, thats it
# I'll give it one more function to tell which key to evict

from collections import OrderedDict

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()


    def touch(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            self.cache[key] = None

    def remove(self, key):
        self.cache.pop(key, None)

    def evict_if_needed(self):
        if len(self.cache) > self.capacity:
            evicted_key, _ = self.cache.popitem(last = False)
            return evicted_key
        return None
