#!/usr/bin/python3
from sys import argv, platform, path as syspath
from os import path as ospath
BASE_DIR = ospath.dirname(ospath.abspath(__file__))
LIBS_DIR = BASE_DIR+"/libs/"
syspath.append(LIBS_DIR)

def mainWithCameraShown():
    initCV();
    initSql();
    initListeners();
    while 1:
        checkActiveWindow();
        getUsersInFrameAndShow();
    closeSql();
    closeCV();

def basicMain():
    initCV();
    initSql();
    initListeners();
    while 1:
        checkActiveWindow();
        getUsersInFrame();
    closeSql();
    closeCV();
if __name__ == "__main__":
    #verify OS is supported
    from sys import platform
    if (platform == "win32"):
        from _windows_ import *;
    elif (platform == "linux"):
        from _linux_ import *;
    else:
        print("unsupported operating system");
        exit();
    #######################
    #show help message if prompted
    if "--help" in argv or "-H" in argv or "-h" in argv:
        helpMessage();
        exit();
    ##############################
    #import local functions
    from _sql_functions_ import *
    from _listener_functions_ import *
    from _globals_ import *
    from _cv_ import *
    from _signals_ import *
    ######################
    #retrain FR model if prompted
    if "--train" in argv or "-T" in argv or "-t" in argv:
        trainModel();
    #############################
    #run the webserver on port 3000 if prompted
    if "--server" in argv or "-S" in argv or "-s" in argv:
        print("webserver")
    ###########################################
    #begin runtime : (with camera if prompted)
    if "--camera" in argv or "-C" in argv or "-c" in argv:
        mainWithCameraShown()
    else:
        basicMain();
    ##########################################
