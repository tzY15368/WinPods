import time,threading
from var_dump import var_dump
def do_test():
    time.sleep(2)
    return {'STATUS':1,'RSSI':-55,'ADDR':'12:34:45:56','MODEL':'e','LEFT':3,'RIGHT':2,'CASE':'f','CHARGE':'b'}
def prints():
    for i in range(16):
        print(str(i)+str(time.time()))
        time.sleep(1)
'''
a = threading.Thread(target=prints)
#a.daemon = True
t = a.start()
var_dump(t)
'''
def check_bt():
    import eventlet
    import get_status
    eventlet.monkey_patch()
    with eventlet.Timeout(0.05, False):
        get_status.fetch_status()#BT ON
        return True
    return False#BT OFF

#print(check_bt())
import get_status
r = get_status.fetch_status()
print(r)