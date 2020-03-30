import time
from var_dump import var_dump
def do_test():
    time.sleep(2)
    return {'STATUS':1,'RSSI':-55,'ADDR':'12:34:45:56','MODEL':'e','LEFT':3,'RIGHT':2,'CASE':'f','CHARGE':'b'}
from bluetooth import *

print ("performing inquiry...")
time1 = time.time()
nearby_devices = discover_devices(lookup_names = True)

print ("found %d devices" % len(nearby_devices))
time2 = time.time()
print('time taken:'+str(time2-time1))
for name, addr in nearby_devices:
     print(" %s - %s" % (addr, name))
for i in nearby_devices:
    print(i)