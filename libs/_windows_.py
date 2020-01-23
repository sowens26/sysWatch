#!/usr/bin/python3
from _sql_functions_ import *
from _listener_functions_ import *
from _globals_ import *
from win32gui import GetWindowText, GetForegroundWindow;

def postRecord():
    global record
    if (record != ""): 
        record = setEndTime();
        postSqlRecord();

def resetRecord():
    global record
    resetSqlRecord();
    record = setStartTime();

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
def winMain():
    initSql();
    initListeners();
    while 1:
        checkActiveWindow();
    closeSqlConnection();
