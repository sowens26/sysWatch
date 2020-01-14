#!/usr/bin/python3
from _globals_ import *
import sqlite3 as sql
def initSqlConnection():
    global sql_conn
    sql_conn = sql.connect("usage.db");
def initSqlController():
    global sql_ctrl;
    sql_ctrl = sql_conn.cursor();
def closeSqlController():
    global sql_ctrl;
    sql_ctrl.close();
def closeSqlConnection():
    global sql_conn
    sql_conn.close();
def initSql():
    global sql_ctrl;
    initSqlConnection();
    initSqlController();
    sql_ctrl.execute("CREATE TABLE IF NOT EXISTS usage(year REAL, month REAL, day REAL, date TEXT,start_hour REAL, start_minutes REAL, start_seconds REAL, start_time TEXT, window_pid REAL, window_title TEXT, mouse_record TEXT, key_record TEXT, end_hour REAL, end_minutes REAL, end_seconds REAL, end_time TEXT)");
    sql_record = {"year":0, "month":0, "day":0, "date":"", "start_hour":0, "start_minutes":0, "start_seconds":0, "start_time":"", "window_pid":0, "window_title":"","mouse_record":"", "key_record":"", "end_hour":0, "end_minutes":0, "end_seconds":0, "end_time":""};
    sql_ctrl.close();


def postSqlRecord():
    global sql_comm, sql_ctrl;
    initSqlController();
    sql_insert_string = "INSERT INTO usage VALUES({},{},{},'{}',{},{},{},'{}',{},'{}','{}','{}',{},{},{},'{}')".format(\
                sql_record["year"], sql_record["month"], sql_record["day"], sql_record["date"],\
                sql_record["start_hour"],sql_record["start_minutes"], sql_record["start_seconds"], sql_record["start_time"],
                sql_record["window_pid"],sql_record["window_title"],sql_record["mouse_record"], sql_record["key_record"],\
                sql_record["end_hour"], sql_record["end_minutes"], sql_record["end_seconds"], sql_record["end_time"]);
    sql_ctrl.execute(sql_insert_string);	
    sql_conn.commit();
    closeSqlController();
def resetSqlRecord():
    global sql_record;
    sql_record = {};
    sql_record = {"year":0, "month":0, "day":0, "date":"", "start_hour":0, "start_minutes":0, "start_seconds":0, "start_time":"", "window_pid":0, "window_title":"", "mouse_record":"","key_record":"", "end_hour":0, "end_minutes":0, "end_seconds":0, "end_time":""};
def sqlSetWindowTitle(title):
    sql_record["window_title"] = title;
def sqlSetWindowPid(pid):
    sql_record["window_pid"] = pid;
def setStartTime():
    global sql_record;
    tm = localtime(time());
    timeString = "{}:{}:{} ".format( tm.tm_hour, tm.tm_min, tm.tm_sec);
    dateString = "{}/{}/{}".format(tm.tm_mon, tm.tm_mday, tm.tm_year);
    sql_record["date"] = dateString;
    sql_record["year"] = tm.tm_year;
    sql_record["month"] = tm.tm_mon;
    sql_record["day"] = tm.tm_mday;
    sql_record["start_time"] = timeString;
    sql_record["start_hour"] = tm.tm_hour;
    sql_record["start_minutes"] = tm.tm_min;
    sql_record["start_seconds"] = tm.tm_sec;
    return "<<<> {} {}\n".format( timeString, dateString);
def setEndTime():
    global sql_record;
    tm = localtime(time());
    timeString = "{}:{}:{} ".format( tm.tm_hour, tm.tm_min, tm.tm_sec);
    dateString = "{}/{}/{}".format(tm.tm_mon, tm.tm_mday, tm.tm_year);
    sql_record["end_time"] = timeString;
    sql_record["end_hour"] = tm.tm_hour;
    sql_record["end_minutes"] = tm.tm_min;
    sql_record["end_seconds"] = tm.tm_sec;
    return "\n>{} {} <>>>".format(timeString, dateString);
	

def sqlKeyRecordAppend( string ):
        global sql_record;
        sql_record["key_record"] += string;
def sqlMouseRecordAppend( string ):
        global sql_record;
        sql_record["mouse_record"] += string;

