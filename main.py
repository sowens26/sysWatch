#!/usr/bin/python3
import sys
if __name__ == "__main__":
    platform = sys.platform;
    sys.path.append('./libs/');
    if (platform == "win32"):
        from _windows_ import winMain;
        winMain();
    elif (platform == "linux"):
        from _linux_ import linuxMain;
        linuxMain();
    else:
        print("unsupported os");
