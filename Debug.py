__author__ = 'tristan_dev'

class Level():

    ERROR = "ERROR"
    INFO = "INFO"
    FATAL = "FATAL"
    def __init__(self):
        pass

def printi(mssg, level):
    print(level + ": " + mssg)