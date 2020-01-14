#!/usr/bin/python3
import sys
if __name__ == "__main__":
    platform = sys.platform;
    if (platform == "win32"):
        from _windows_ import *;
        winMain();
    elif (platform == "linux"):
        from _linux_ import *;
        linuxMain();
    else:
        print("unsupported os");
