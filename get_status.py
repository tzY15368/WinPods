import asyncio
from bleak import discover
from var_dump import var_dump
def isFlipped(b):
    return True#str(int(int(''+b[10],16)+0x10,2))[3]=='0'
async def run():
    devices = await discover()
    for d in devices:
        if d.rssi >=-690 and 76 in d.metadata['manufacturer_data'] and len(d.metadata['manufacturer_data'][76].hex())==54:
            print('================')
            #print(var_dump(d))
            print(d.rssi)
            try:
                data = d.metadata['manufacturer_data'][76]
                b = data.hex()
                print(b)
                #print(len(b))
                print(isFlipped(b))
                print('ADDR:'+d.address)
                print('MODEL:'+b[7])
                print('LEFT:'+b[12]+' RIGHT:'+b[13])
                print('CASE:'+b[15])
                print('inCharge:'+b[14])
            except Exception as e:
                #pass
                print(e)
            print('-----------------')

loop = asyncio.get_event_loop()
loop.run_until_complete(run())