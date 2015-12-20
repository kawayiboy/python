import win32api, win32con, time, win32ui, pyHook, pythoncom
from threading import Timer

global curWinName
curWinName =''
global tick
tick = 0

global main_thread_id

#Define the clicks in the win32api
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def onclick(event):
    print event.Position
    (event_x, event_y) = event.Position
    click(event_x, event_y)
    return True

def on_timer():
	while(True):
		global tick
		tick = tick+1
		print tick
		if(tick>20):
			win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0);
			break;
		time.sleep(1)

def main():
	global main_thread_id
 	main_thread_id = win32api.GetCurrentThreadId()

	hm = pyHook.HookManager()
	hm.SubscribeMouseAllButtonsDown(onclick)
	hm.HookMouse()
	pythoncom.PumpMessages()
	hm.UnhookMouse()

if __name__ == "__main__":
	t = Timer(1.0, on_timer) # Quit after 5 seconds
	t.start()
	main()