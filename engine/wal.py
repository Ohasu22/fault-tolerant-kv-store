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


# One thing I noticed is that I dont think this is optimised tbh
# If my laptop turns off unexpectedly then I have to read my whole WAL again and redo every log
# Okay for small logs but for like 1M+ it will the bottleneck

# I might have to use something else altogether for recovery or maybe I could store it somewhere so I dont have to delete this code
# At least my replay function works, I just need to find something that would store the logs just in case which is faster than reading the WAL again
# I could use the store but how do I know from which time stamp to start or which timestamp to end
