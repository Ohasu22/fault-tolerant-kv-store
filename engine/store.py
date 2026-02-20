#pretty straight forward store ig
# just have to import all my things and lets see where we go

import time

from engine.ttl import TTLManager
from engine.wal import WriteAheadLog
from engine.eviction import LRUCache

#edit 21/02/26: adding my snapshot here
from engine.snapshot import SnapshotManager

class KeyValueStore:
    #capacity from LRUCache, for path I'll use the same variable I used in recovery
    def __init__(self, capacity, wal_path, snapshot_path = None):
        self.capacity = capacity
        self.cache = {} #key : (value, expiry_timestamp)
        self.ttl = TTLManager()
        self.lru = LRUCache(capacity)
        self.wal = WriteAheadLog(wal_path)

        # edit
        self.snapshot = SnapshotManager(snapshot_path) if snapshot_path else None

    #not the same put as my eviction
    def put(self, key, value, ttl = None):
        expiry = None
        if ttl is not None:
            expiry = time.time() + ttl

        #this is my WA log entry
        self.wal.log_put(key, value, expiry)

        #this on is for the application in memory
        self.put_internal(key, value, expiry)

        #edit(16/02/26): now I can use this
        #evict_if_needed return key value if its evicted else None
        evicted = self.lru.evict_if_needed()
        if evicted:
            self.cache.pop(evicted,None)
            self.wal.log_delete(evicted)

    # key : (value, expiry_timestamp)
    # similar to my get function in my eviction.py
    def get(self, key):
        if key not in self.cache:
            return None

        value, expiry_timestamp = self.cache[key]

        if self.ttl.is_expired(expiry_timestamp):
            self.delete(key)
            return None

        self.lru.touch(key)
        return value

    def delete(self, key):
        if key not in self.cache:
            return

        self.wal.log_delete(key)

        self.delete_internal(key)



    def put_internal(self, key, value, expiry_timestamp):
        self.cache[key] = (value, expiry_timestamp)
        self.lru.touch(key)

    def delete_internal(self, key):
        self.cache.pop(key, None)
        self.lru.remove(key)

    def close(self):
        self.wal.close()

    #edit 21/02/25
    def create_snapshot(self):
        #just needs to save the snapshot if it exists
        pass

    def recover(self):
        #will read from the snapshot_path file and redo the put_internal function
        pass




