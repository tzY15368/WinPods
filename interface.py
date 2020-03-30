import tkinter as tk
import asyncio
import test
import get_status
import threading
import time
from PIL import Image,ImageTk


def validate_result(r):
    if r['LEFT']  and r['RIGHT'] and r['CASE'] in [1,2,3,4,5,6,7,8,9,10,0,'1','2','3','4','5','6','7','8','9','0','10','f']:
        return True
    else:
        return False


def upd_img():
    while True:
        #result = test.do_test()##CHANGE HERE-----------------
        img_waiting = ImageTk.PhotoImage(Image.open('./img/q.png'))
        battery_case_label.config(image=img_waiting)
        battery_case_label.image = img_waiting
        battery_left_label.config(image=img_waiting)
        battery_left_label.image = img_waiting
        battery_right_label.config(image=img_waiting)
        battery_right_label.image = img_waiting

        result = get_status.fetch_status()
        print(result)
        if result['STATUS'] == 1 and validate_result(result):
            left_battery_dir = './img/' + str(result['LEFT']) + '.png'
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
        time.sleep(55)


def upd():
    t = threading.Thread(target=upd_img)
    t.daemon = True
    t.start()
def check_bt():
    import eventlet  # 导入eventlet这个模块
    eventlet.monkey_patch()  # 必须加这条代码
    with eventlet.Timeout(0.5, False):  # 设置超时时间为2秒
        return True
        print('没有跳过这条输出')
    print('跳过了输出')
window = tk.Tk()
window.iconbitmap(default=r'./img/Airpods.ico')
window.title('WinPods')
window.geometry('360x230')
window.resizable(0,0)
window.configure(background='white')


canvas = tk.Canvas(window,width=360,height=155, bg='white')
canvas.config(highlightthickness=0)
canvas.pack()


left_Image=tk.PhotoImage(file="./img/left.png")
right_Image = tk.PhotoImage(file='./img/right.png')
case_Image = tk.PhotoImage(file='./img/case.png')


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
bt_status = check_bt()
if bt_status:
    window.mainloop()
else:
    print('no bt')