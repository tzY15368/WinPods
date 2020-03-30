import os
import win32api
import win32con
import win32gui_struct
import win32gui
from time import sleep
import threading
import get_status
from PIL import ImageTk,Image
Main = None

def validate_result(r):#r=='a' seems to indicate that airpods are in case with case open?
    if r['LEFT']  and r['RIGHT'] and r['CASE'] in [1,2,3,4,5,6,7,8,9,10,0,'1','2','3','4','5','6','7','8','9','0','10','f','a']:
        return True
    else:
        return False
class SysTrayIcon(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 1314

    def __init__(s,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None, ):
        s.icon = icon
        s.hover_text = hover_text
        s.on_quit = on_quit

        menu_options = menu_options + (('退出', None, s.QUIT),)
        s._next_action_id = s.FIRST_ID
        s.menu_actions_by_id = set()
        s.menu_options = s._add_ids_to_menu_options(list(menu_options))
        s.menu_actions_by_id = dict(s.menu_actions_by_id)
        del s._next_action_id

        s.default_menu_index = (default_menu_index or 0)
        s.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): s.refresh_icon,
                       win32con.WM_DESTROY: s.destroy,
                       win32con.WM_COMMAND: s.command,
                       win32con.WM_USER + 20: s.notify, }
        # 注册窗口类。
        window_class = win32gui.WNDCLASS()
        window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = s.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # 也可以指定wndproc.
        s.classAtom = win32gui.RegisterClass(window_class)

    def show_icon(s):
        # 创建窗口。
        hinst = win32gui.GetModuleHandle(None)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        s.hwnd = win32gui.CreateWindow(s.classAtom,
                                       s.window_class_name,
                                       style,
                                       0,
                                       0,
                                       win32con.CW_USEDEFAULT,
                                       win32con.CW_USEDEFAULT,
                                       0,
                                       0,
                                       hinst,
                                       None)
        win32gui.UpdateWindow(s.hwnd)
        s.notify_id = None
        s.refresh_icon()

        win32gui.PumpMessages()

    def show_menu(s):
        menu = win32gui.CreatePopupMenu()
        s.create_menu(menu, s.menu_options)
        # win32gui.SetMenuDefaultItem(menu, 1000, 0)

        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(s.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                s.hwnd,
                                None)
        win32gui.PostMessage(s.hwnd, win32con.WM_NULL, 0, 0)

    def destroy(s, hwnd, msg, wparam, lparam):
        if s.on_quit: s.on_quit(s)  # 运行传递的on_quit
        nid = (s.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # 退出托盘图标

    def notify(s, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass  # s.execute_menu_option(s.default_menu_index + s.FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP:  # 单击右键
            #if Main: Main.window.deiconify()
            s.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 单击左键
            nid = (s.hwnd, 0)
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
            win32gui.PostQuitMessage(0)  # 退出托盘图标
            if Main: Main.window.deiconify()
        return True
        """ 可能的鼠标事件：
        WM_MOUSEMOVE
        WM_LBUTTONDOWN
        WM_LBUTTONUP
        WM_LBUTTONDBLCLK
        WM_RBUTTONDOWN
        WM_RBUTTONUP
        WM_RBUTTONDBLCLK
        WM_MBUTTONDOWN
        WM_MBUTTONUP
        WM_MBUTTONDBLCLK"""

    def _add_ids_to_menu_options(s, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in s.SPECIAL_ACTIONS:
                s.menu_actions_by_id.add((s._next_action_id, option_action))
                result.append(menu_option + (s._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               s._add_ids_to_menu_options(option_action),
                               s._next_action_id))
            s._next_action_id += 1
        return result

    def refresh_icon(s, **data):
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(s.icon):  # 尝试找到自定义图标
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       s.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:  # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if s.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        s.notify_id = (s.hwnd,
                       0,
                       win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                       win32con.WM_USER + 20,
                       hicon,
                       s.hover_text)
        win32gui.Shell_NotifyIcon(message, s.notify_id)

    def create_menu(s, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = s.prep_menu_icon(option_icon)

            if option_id in s.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                s.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(s, icon):
        # 首先加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # 填满背景。
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # "GetSysColorBrush返回缓存的画笔而不是分配新的画笔。"
        #  - 暗示没有DeleteObject
        # 画出图标
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(s, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        s.execute_menu_option(id)

    def execute_menu_option(s, id):
        menu_action = s.menu_actions_by_id[id]
        if menu_action == s.QUIT:
            win32gui.DestroyWindow(s.hwnd)
        else:
            menu_action(s)


class _Main:
    def main(s):
        import tkinter as tk
        if get_status.check_bt():
            print('went here')
            s.window = tk.Tk()
            s.window.iconbitmap(default=r'./img/Airpods.ico')
            s.window.title('WinPods')
            s.window.geometry('360x230')
            s.window.resizable(0, 0)
            s.window.configure(background='white')

            s.canvas = tk.Canvas(s.window, width=360, height=155, bg='white')
            s.canvas.config(highlightthickness=0)
            s.canvas.pack()

            s.left_Image = tk.PhotoImage(file="./img/left.png")
            s.right_Image = tk.PhotoImage(file='./img/right.png')
            s.case_Image = tk.PhotoImage(file='./img/case.png')

            s.canvas.create_image(0, 15, anchor='nw', image=s.left_Image)
            s.canvas.create_image(240, 15, anchor='ne', image=s.right_Image)
            s.canvas.create_image(360, 15, anchor='ne', image=s.case_Image)

            s.q_img = ImageTk.PhotoImage(Image.open('./img/q.png'))
            s.battery_left_label = tk.Label(s.window)
            s.battery_left_label.config(image=s.q_img, background='white')
            s.battery_left_label.image = s.q_img
            s.battery_case_label = tk.Label(s.window)
            s.battery_case_label.config(image=s.q_img, background='white')
            s.battery_case_label.image = s.q_img
            s.battery_right_label = tk.Label(s.window)
            s.battery_right_label.config(image=s.q_img, background='white')
            s.battery_right_label.image = s.q_img
            s.battery_left_label.pack(side='left')
            s.battery_right_label.pack(side='left', padx=15)
            s.battery_case_label.pack(side='left')

            icons = './img/Airpods.ico'
            hover_text = "WinPods"  # 悬浮于图标上方时的提示
            menu_options = ()
            # menu_options = (('更改 图标', None, s.switch_icon),
            #               ('二级 菜单', None, (('更改 图标', None, s.switch_icon),)))
            s.sysTrayIcon = SysTrayIcon(icons, hover_text, menu_options, on_quit=s.exit, default_menu_index=1)

            s.window.bind("<Unmap>", lambda event: s.Unmap() if s.window.state() == 'iconic' else False)
            s.window.protocol('WM_DELETE_WINDOW', s.exit)
            s.window.resizable(0, 0)
            s.upd()
            s.window.mainloop()
        else:
            print('2222')
            s.ErrorWindow = tk.Tk()
            s.ErrorWindow.resizable(0,0)
            s.ErrorWindow.iconbitmap(default=r'./img/Airpods.ico')
            s.ErrorWindow.title('Error')
            s.ErrorWindow.geometry('228x128')
            s.ErrorWindow.configure(background='white')

            s.btmissing_img = ImageTk.PhotoImage(Image.open('./img/btmissing.png'))
            s.btmissing_label = tk.Label(s.ErrorWindow)
            s.btmissing_label.config(image=s.btmissing_img, background='white')
            s.btmissing_label.image = s.btmissing_img
            def opensettings():
                import os
                os.system('explorer /e,/root,ms-settings:bluetooth')
            s.InfoLabel = tk.Label(s.ErrorWindow, text="""系统蓝牙未启用""",background='white',anchor="nw", justify="left")
            s.button = tk.Button(s.ErrorWindow,text="前往设置",command=opensettings)

            s.btmissing_label.pack(side='left')
            s.button.pack(side='bottom', pady=10)
            s.InfoLabel.pack(side='bottom')

            s.ErrorWindow.mainloop()


    def upd_img(self):
        while True:
            # result = test.do_test()##CHANGE HERE-----------------
            img_waiting = ImageTk.PhotoImage(Image.open('./img/q.png'))
            self.battery_case_label.config(image=img_waiting)
            self.battery_case_label.image = img_waiting
            self.battery_left_label.config(image=img_waiting)
            self.battery_left_label.image = img_waiting
            self.battery_right_label.config(image=img_waiting)
            self.battery_right_label.image = img_waiting
            print('----!')
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

            self.battery_left_label.config(image=img_left)
            self.battery_left_label.image = img_left

            self.battery_right_label.config(image=img_right)
            self.battery_right_label.image = img_right

            self.battery_case_label.config(image=img_case)
            self.battery_case_label.image = img_case
            sleep(55)

    def upd(self):
        print('starting upd:')
        t = threading.Thread(target=self.upd_img)
        t.daemon = True
        t.start()

    def switch_icon(s, _sysTrayIcon, icons='D:\\2.ico'):
        _sysTrayIcon.icon = icons
        _sysTrayIcon.refresh_icon()
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon

    def Unmap(s):
        s.window.withdraw()
        s.sysTrayIcon.show_icon()

    def exit(s, _sysTrayIcon=None):
        s.window.destroy()
        print('exit...')


if __name__ == '__main__':
    Main = _Main()
    Main.main()