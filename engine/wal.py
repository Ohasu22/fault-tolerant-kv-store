# okay so if my system crashes, my data would be poof coz rn everything is stored on my ram
# I save that data to my harddrive before giving it to the memory kinda like what redis or kafka work but simpler
# its the log entry for our cache ig(I cant explain better than this)

#how can my log look like then?
# I am thinking simple so kinda like
# PUT key val expiry_timestamp
# DELETE key

import os

class WriteAheadLog:
    def __init__(self, log_path):
        self.log_path = log_path
        self.file = open(self.log_path, "a", buffering=1)

    def _write_and_flush(self, line):
        self.file.write(line)
        self.file.flush()
        os.fsync(self.file.fileno())

    def log_put(self, key, value, expiry):
        line = f"PUT {key} {value} {expiry}\n"
        self._write_and_flush(line)

    def log_delete(self, key):
        line = f"DELETE {key}\n"
        self._write_and_flush(line)

    def close(self):
        self.file.close()

