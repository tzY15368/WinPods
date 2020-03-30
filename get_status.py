import asyncio,threading
from bleak import discover
from bluetooth import discover_devices
from time import time,sleep
def isFlipped(b):
    return True#str(int(int(''+b[10],16)+0x10,2))[3]=='0'
async def run():
    devices = await discover()
    result = {'STATUS':0}
    for d in devices:
        if True or d.rssi >=-690 and 76 in d.metadata['manufacturer_data'] and len(d.metadata['manufacturer_data'][76].hex())==54:
            print('================')
            #print(var_dump(d))
            print(d.rssi)
            try:
                data = d.metadata['manufacturer_data'][76]
                b = data.hex()
                print(b)
                # print(len(b))
                print(isFlipped(b))

                if result['STATUS']!=1:
                    print('ADDR:'+d.address)
                    print('MODEL:'+b[7])
                    print('LEFT:'+b[12]+' RIGHT:'+b[13])
                    print('CASE:'+b[15])
                    print('inCharge:'+b[14])
                    result['RSSI'] = d.rssi
                    result['ADDR'] = d.address
                    result['MODEL'] = b[7]
                    result['LEFT'] = b[12]
                    result['RIGHT'] = b[13]
                    result['CASE'] = b[15]
                    result['CHARGE'] = b[14]
                    result['STATUS'] = 1
                else:
                    if d.rssi > result['RSSI']:
                        result['RSSI'] = d.rssi
                        result['ADDR'] = d.address
                        result['MODEL'] = b[7]
                        result['LEFT'] = b[12]
                        result['RIGHT'] = b[13]
                        result['CASE'] = b[15]
                        result['CHARGE'] = b[14]
                        result['STATUS'] = 1
            except Exception as e:
                #pass
                print(e)
            print('-----------------')
    return result
def fetch_status():
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(run())
    return a


class bt(object):
    def __init__(self):
        self.btStatus = True

    def set_status(self, val):
        self.btStatus = val
    def get_status(self):
        while True:
            print(self.btStatus)
            sleep(0.8)
    def get_sys_bt(self):
        print("performing inquiry...")
        time1 = time()
        nearby_devices = discover_devices(lookup_names=True)
        print("found %d devices" % len(nearby_devices))
        time2 = time()
        print('time taken:' + str(time2 - time1))
        for name, addr in nearby_devices:
            print(" %s - %s" % (addr, name))
        re = len(nearby_devices)
        print('re:' + str(re))
        if re == 0:
            self.set_status(False)
        self.set_status(False)
        return
def check_bt():
    mybt = bt()
    print(mybt.btStatus)
    t = threading.Thread(target=mybt.get_sys_bt)
    t.daemon = True
    t.start()
    sleep(0.1)
    print('returning status:',mybt.btStatus)
    return mybt.btStatus


if __name__ == "__main__":
    #print(fetch_status())
    #get_sys_bt()
    t1 = time()
    print(check_bt())
    t2 = time()
    print('taken:',t2-t1)