import win32api, win32con, time, win32ui, pyHook, pythoncom
from ctypes import *
import ctypes, win32con, ctypes.wintypes, win32gui
import threading

global main_thread_id

class Hotkey(threading.Thread):
    def __init__(self):
        self.bExit = False
        threading.Thread.__init__(self)
        global main_thread_id
        main_thread_id = win32api.GetCurrentThreadId()

    def run(self):
        user32 = ctypes.windll.user32
        print "Register exit hotkey"
        if not user32.RegisterHotKey(None, 99, win32con.MOD_WIN, win32con.VK_F3):
            raise RuntimeError
        try:
            msg = ctypes.wintypes.MSG()
            print msg
            global main_thread_id
            while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    if msg.wParam == 99:
                        self.bExit = True
                        win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0)
                        return
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            user32.UnregisterHotKey(None, 1)

    def exited(self):
        return self.bExit