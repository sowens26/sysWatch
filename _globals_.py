from time import time, localtime;

sql_conn = sql_ctrl = None;
sql_record = {"record":""};
ignore_titles = [ "", "Task Switching" ];
active_window_title = active_pid = record = "";
key_listener = mouse_listener = None;

