import time,threading,sys,os
from PIL.Image import open
#from var_dump import var_dump
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
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
'''
imgpath = './img/1.png'
img = Image.open(resource_path(imgpath))
filename = resource_path(os.path.join("res","a.txt"))
print(filename)
img.show()'''
img = open('./img/1.png')
import subprocess
#p = subprocess.run('explorer /e,/root,ms-settings:bluetooth',
#                     shell=True)
                     #stdin=subprocess.PIPE,
                     #stdout=subprocess.PIPE,
                     #stderr=subprocess.PIPE)
#a = os.popen('explorer /e,/root,ms-settings:bluetooth')