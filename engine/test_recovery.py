# At this point I am done with the project I guess, time to test and pluck my hair out while debugging I guess
# fun fun

from engine.store import KeyValueStore
import time

print("Starting store...")

#capacity, wal_path, snapshot_path = None for reference from store
store = KeyValueStore(
    capacity= 3,
    wal_path="wal.log",
    snapshot_path="snapshot.json"
)

store.put("user:1", "ElonMa")
store.put("user:2", "AkiraHayabuza")
store.put("user:3", "XiaoXina", ttl= 5)

print("Store in full capacity.")

print("Crashing the store...")
del store

print("\nRestarting the store...")

store2 = KeyValueStore(
    capacity=3,
    wal_path="wal.log",
    snapshot_path="snapshot.json"
)

store2.recover()

print("Recovered values: ")
print("user:1 ->", store2.get("user:1"))
print("user:2 ->", store2.get("user:2"))
print("user:3 ->", store2.get("user:3"))

