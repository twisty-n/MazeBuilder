__author__ = 'tristan_dev'



class Level():

    ERROR = "ERROR"
    INFO = "INFO"
    FATAL = "FATAL"
    def __init__(self):
        self._verbose = True        #Todo: Change to false for release

    def toggle(self):
        self._verbose = not self._verbose

d_level = Level()

def printi(mssg, level):
    """
    Print a debug message based on the current verbosity filter

    :param mssg:        The message to be printed
    :param level:       The level the message is to be printed at
    :return:            No return
    """

    # Will not print the debug info if the level is not verbose
    if d_level._verbose is False and level is Level.INFO:
        return
    print(level + ": " + mssg)

def printe(event, level):
    """

    :param event:
    :param level:
    :return:
    """
    # Extract all of the needed event information, could optimize, wont :P
    mssg = ""
    if event.type == 4 or 5:
        # We have some kind of mouse event
        mssg = mssg + "Mouse Event || Button: " + str(event.num) + " || x="+str(event.x) + " y="+str(event.y) + " ||"
    else:
        # We have a key event
        mssg = mssg + "Key Event || Button: " + str(event.keysym) + " ||"
    # Dispatch to the normal print method
    printi(mssg, level)