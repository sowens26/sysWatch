#!/mnt/e/e/winProgs/Python/python.exe
from time import time, localtime
from win32gui import GetWindowText, GetForegroundWindow

sql_conn = sql_ctrl = None;
sql_record = {"record":""};
ignore_titles = [ "", "Task Switching" ];
active_window_title = active_pid = record = "";
key_listener = mouse_listener = None;

