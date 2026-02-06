# I have to create a timeframe where these keys and values exist
# my key should automatically be expired after a certain period of time
# I am not going to check each second if the ttl is expired
# Just check when the key is accessed or while doing some operation I find the key is expired then I call this function
# Or maybeeeee sometime I could do a cleaner type thing manually just to delete the expired keys

import time
#off course have to import this

class TTLManager:
    def is_expired(self, expiry_timestamp):
        if expiry_timestamp is None:
            return False
        return time.time() > expiry_timestamp

# I cant think of anything at the moment so I'll just keep it simple