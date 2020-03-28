import tkinter as tk
import asyncio
import test
import get_status
import threading
from PIL import Image,ImageTk
'''
result['RSSI'] = d.rssi
                result['ADDR'] = d.address
                result['MODEL'] = b[7]
                result['LEFT'] = b[12]
                result['RIGHT'] = b[13]
                result['CASE'] = b[15]
                result['CHARGE'] = b[14]
'''
loop = asyncio.get_event_loop()
#info = loop.run_until_complete(get_status.run())
info = {'RSSI':0,'STATUS':0}
print(info)

#test.do_test()#{'RSSI':0}
#info = {'RSSI':-55,'ADDR':'12:34:45:56','MODEL':'e','LEFT':3,'RIGHT':'f','CASE':'f','CHARGE':'b'}
async def get_info():
    result = await test.do_test()
    print(result)
    return result
def get_test():
    img = Image.open('./img/5.png')
    img = ImageTk.PhotoImage(img)
    test.do_test()
    #v.set('888')
    w.config(image=img)
    w.image = img
    return
def validate_result(r):
    if r['LEFT']  and r['RIGHT'] and r['CASE'] in [1,2,3,4,5,6,7,8,9,10,0,'1','2','3','4','5','6','7','8','9','0','10','f']:
        return True
    else:
        return False
def upd_img():
    result = test.do_test()##CHANGE HERE-----------------
    print(result)
    if result['STATUS']==1 and validate_result(result):
        left_battery_dir = './img/'+str(result['LEFT'])+'.png'
        right_battery_dir = './img/' + str(result['RIGHT']) + '.png'
        case_battery_dir = './img/' + str(result['CASE']) + '.png'
    else:
        left_battery_dir = './img/f.png'
        right_battery_dir = './img/f.png'
        case_battery_dir = './img/f.png'
    img_left = ImageTk.PhotoImage(Image.open(left_battery_dir))
    img_right = ImageTk.PhotoImage(Image.open(right_battery_dir))
    img_case = ImageTk.PhotoImage(Image.open(case_battery_dir))

    battery_left_label.config(image=img_left)
    battery_left_label.image = img_left

    battery_right_label.config(image=img_right)
    battery_right_label.image = img_right

    battery_case_label.config(image=img_case)
    battery_case_label.image = img_case
    return
def upd():
    t = threading.Thread(target=upd_img)
    t.start()



window = tk.Tk()
window.iconbitmap(default=r'./img/Airpods.ico')
window.title('WinPods')
window.geometry('360x230')
window.resizable(0,0)
window.configure(background='white')
'''
v = tk.StringVar()
w = tk.Label(window,textvariable=v)
v.set('test123')
w.pack()
'''
'''
img = Image.open('./img/10.png')
img = ImageTk.PhotoImage(img)
w = tk.Label(window)
w.config(image=img)
w.image = img
w.pack()
'''

canvas = tk.Canvas(window,width=360,height=155, bg='white')
canvas.config(highlightthickness=0)
canvas.pack()
#在画布上创建文字
#canvas.create_text(20,170,text=info['RSSI'],fill="blue",font=("Times",16))
#在画布上创建图片，tkinter只能显示gif文
left_Image=tk.PhotoImage(file="./img/left.png")
right_Image = tk.PhotoImage(file='./img/right.png')
case_Image = tk.PhotoImage(file='./img/case.png')
'''
if info['STATUS']==1:
    battery_left_image = tk.PhotoImage(file='./img/'+info['LEFT']+'.png')
    battery_right_image = tk.PhotoImage(file='./img/'+info['RIGHT']+'.png')
    battery_case_image = tk.PhotoImage(file='./img/'+info['CASE']+'.png')
else:
    battery_left_image = tk.PhotoImage(file='./img/unknown.png')
    battery_right_image = tk.PhotoImage(file='./img/unknown.png')
    battery_case_image = tk.PhotoImage(file='./img/unknown.png')
'''

#以(10,70)为西北角显示图像
canvas.create_image(0, 15, anchor='nw', image=left_Image)
canvas.create_image(240,15, anchor='ne', image=right_Image)
canvas.create_image(360,15, anchor='ne', image=case_Image)


q_img = ImageTk.PhotoImage(Image.open('./img/q.png'))
battery_left_label = tk.Label(window)
battery_left_label.config(image=q_img,background='white')
battery_left_label.image = q_img
battery_case_label = tk.Label(window)
battery_case_label.config(image=q_img,background='white')
battery_case_label.image = q_img
battery_right_label = tk.Label(window)
battery_right_label.config(image=q_img,background='white')
battery_right_label.image = q_img
battery_left_label.pack(side='left')
battery_right_label.pack(side='left',padx=15)
battery_case_label.pack(side='left')

upd()
window.mainloop()