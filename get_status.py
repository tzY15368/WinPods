import asyncio
from bleak import discover
from var_dump import var_dump
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
def get_sys_bt():
    return
if __name__ == "__main__":
    print(fetch_status())
    #get_sys_bt()