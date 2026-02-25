# my snapshot is like the carbon copy of the memory so if my WAL goes blank for like a powercut or some error, I got my backup
# have to be similar to how redis works, edit: hearing a word truncated a lot, reasearch on this topic
# I have to:
# save the state of memory
# load that state if requested
# learned some fancy way to write code on codeforce so gotta implement starting here


import json
import time

#edit: dont need this line here
# give this error: ImportError: cannot import name 'KeyValueStore' from partially initialized module '
# engine.store' (most likely due to a circular import) (C:\Users\Ojas Gharde\Downloads\kv_store\engine\store.py)
# reason: the import is going in circular fashion, snapshot is importing store and store is importing snapshot
#from engine.store import KeyValueStore


class SnapshotManager:

    def __init__(self, snapshot_path: str):
        self.snapshot_path = snapshot_path

    def save(self, store : "KeyValueStore"):

        #my backup store
        data = {}

        # key : (value, expiry_timestamp)
        for key, (value,expiry) in store.cache.items():
            #just gonna ignore the expired keys to free up my space
            if expiry is not None and time.time() > expiry:
                continue

            data[key] = {
                "value": value,
                "expiry": expiry
            }
        #kinda proud of myself for this genius thinking
        #with is opening or creating the file at the path given and I dump the dictionary as JSON
        # after dumping with block automatically saves and closes the file
        with open(self.snapshot_path,"w") as f:
            json.dump(data, f)


    def load(self,store: "KeyValueStore"):
        try:
            with open(self.snapshot_path,"r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        for key, entry in data.items():
            value = entry["value"]
            expiry = entry["expiry"]

            #gotta check again if its expired or not
            if expiry is not None and time.time() > expiry:
                continue

            store.put_internal(key, value, expiry)
