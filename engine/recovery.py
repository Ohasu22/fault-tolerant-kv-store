# So after any crash like in case of powercut my data will be lost because its in my RAM
# for that I'll have to create a recovery somehow
# my only point of entry for that data is WAL
# I could take a snapshot but maybe I think its an overkill or maybe I'll think about it later

# my WAL is append only so
# I can create an in memory store and then read the WAL line by line and redo the operations in order

import time

class RecoveryManager:
    # my WALPath is the path where the WAL is stored in my memory
    #edit: python says WALPath should be lowercase so changing it to wal_path
    def __init__(self, wal_path):
        self.wal_path = wal_path

    def _apply_log(self, line, store):
        if not line:
            return
        parts = line.split()
        #edit: from my wal
        # PUT key val expiry_timestamp
        # DELETE key
        if parts[0] == "PUT":
            _, key, value, expiry = parts
            expiry = None if expiry == "None" else float(expiry)

            #okay so here I can just skip the keys withch are already expired so I wouldnt need them anyway
            if expiry is not None and time.time() > expiry:
                return
            # I dont want to touch the WAL because it the code touches that it might just go into an infinite loop
            #I dont want to generate new WAL extries, just get the old ones
            # I'll make this function in my store
            store.put_internal(key, value, expiry)

        elif parts[0] == "DELETE":
            _, key = parts
            store.delete_internal(key)

    def recover(self, store):
        #edit: adding this in a try catch block for error handling is if my file is not there I dont want headache
        try:
            with open(self.wal_path, "r") as f:
                for line in f:
                    self._apply_log(line.strip(), store)
        except FileNotFoundError:
            pass

