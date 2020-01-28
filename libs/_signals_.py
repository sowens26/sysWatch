from signal import signal, SIGINT, SIGTERM
from _sql_functions_ import *
from _cv_ import *
def interrupt(signal, frame) -> None:
    closeSqlConnection();
    closeCV();
    exit();
def terminate(signal, frame) -> None:
    print("aa");
    closeSqlConnection();
    closeCV();
    exit();
signal(SIGINT, interrupt)
signal(SIGTERM, terminate)

