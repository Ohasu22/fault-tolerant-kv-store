#pretty straight forward store ig
# just have to import all my things and lets see where we go

import time

from engine.ttl import TTLManager
from engine.wal import WriteAheadLog
from engine.eviction import LRUCache

class KeyValueStore:
    #capacity from LRUCache, for path I'll use the same variable I used in recovery
    def __init__(self, capacity, wal_path):
        self.capacity = capacity
        self.cache = {} #key : (value, expiry_timestamp)
        self.ttl = TTLManager()
        self.lru = LRUCache(capacity)
        self.wal = WriteAheadLog(wal_path)

    #not the same put as my eviction
    def put(self, key, value, ttl = None):
        expiry = None
        if ttl is not None:
            expiry = time.time() + ttl


        self.wal.log_put(key, value, expiry)

        self.put_internal(key, value, expiry)

    #work in progress!!!!
    def put_internal(self, key, value, expiry):
        self.cache[key] = (value, expiry)



