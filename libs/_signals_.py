from signal import signal, SIGINT, SIGTERM
from _sql_functions_ import *
from _cv_ import *
def signalHandler(signal, frame) -> None:
    closeSqlConnection();
    closeCV();
    exit();
signal(SIGINT, signalHandler)
signal(SIGTERM, signalHandler)

