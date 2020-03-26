import tkinter as tk
import asyncio
import test
import get_status
import threading
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
info = loop.run_until_complete(get_status.run())
print(info)
#test.do_test()#{'RSSI':0}
#info = {'RSSI':-55,'ADDR':'12:34:45:56','MODEL':'e','LEFT':3,'RIGHT':2,'CASE':'f','CHARGE':'b'}
async def get_info():
    result = await test.do_test()
    print(result)
    return result
window = tk.Tk()
window.iconbitmap(default=r'./img/Airpods.ico')
window.title('WinPods')
window.geometry('360x230')
window.resizable(0,0)

canvas = tk.Canvas(window,width=360,height=230, bg='white')
canvas.pack()
#在画布上创建文字
#canvas.create_text(20,170,text=info['ADDR'],fill="blue",font=("Times",16))
#在画布上创建图片，tkinter只能显示gif文
left_Image=tk.PhotoImage(file="./img/left.png")
right_Image = tk.PhotoImage(file='./img/right.png')
case_Image = tk.PhotoImage(file='./img/case.png')
if info['STATUS']==1:
    battery_left_image = tk.PhotoImage(file='./img/'+info['LEFT']+'.png')
    battery_right_image = tk.PhotoImage(file='./img/'+info['RIGHT']+'.png')
    battery_case_image = tk.PhotoImage(file='./img/'+info['CASE']+'.png')
else:
    battery_left_image = tk.PhotoImage(file='./img/unknown.png')
    battery_right_image = tk.PhotoImage(file='./img/unknown.png')
    battery_case_image = tk.PhotoImage(file='./img/unknown.png')
#以(10,70)为西北角显示图像
canvas.create_image(0, 15, anchor='nw', image=left_Image)
canvas.create_image(240,15, anchor='ne', image=right_Image)
canvas.create_image(360,15, anchor='ne', image=case_Image)

canvas.create_image(13,135, anchor='nw', image=battery_left_image)
canvas.create_image(225,135, anchor='ne', image=battery_left_image)
canvas.create_image(347,135, anchor='ne', image=battery_left_image)
window.mainloop()