#!/usr/bin/python3
from _sql_functions_ import *
from _listener_functions_ import *
from _globals_ import *
import os

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
    pid = os.popen('xdotool getactivewindow getwindowpid').read();
    if (active_pid != pid):
        active_pid = pid;
        sqlSetWindowPid(active_pid);
        title = os.popen('xdotool getactivewindow getwindowname').read();
        if active_window_title != title:
            active_window_title = title;
            sqlSetWindowTitle(active_window_title);
            if (active_window_title not in ignore_titles):
                postRecord();
                resetRecord();


def linuxMain():
    initSql();
    initListeners();
    while 1:
        checkActiveWindow();
    closeSqlConnection();
