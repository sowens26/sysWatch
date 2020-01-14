#!/mnt/e/winProgs/Python/python.exe 
from _sql_functions_ import *
from _listener_functions_ import *
from _globals_ import *

from win32process import *;

def postRecord():
    global record#, sql_conn, sql_ctrl, sql_record;
    if (record != ""): 
        record = setEndTime();
        postSqlRecord();
        #print( record, end="\n\n" );

def resetRecord():
    global record#, active_pid, active_window_title;
    resetSqlRecord();
    record = setStartTime();
    #record += ">{}\n>{}\n\t".format(active_pid, active_window_title);

def checkActiveWindow():
    global active_window_title, active_pid;
    if (active_pid != GetForegroundWindow()):
        active_pid = GetForegroundWindow();
        sqlSetWindowPid(active_pid);
        if active_window_title != GetWindowText(GetForegroundWindow()):
            active_window_title  = GetWindowText(GetForegroundWindow());
            sqlSetWindowTitle(active_window_title);
            if (active_window_title not in ignore_titles):
                print(GetCurrentProcessId());
                postRecord();
                resetRecord();
                

if __name__ == "__main__":
    initSql();
    initListeners();
    while 1:
        checkActiveWindow();
    closeSqlConnection();
