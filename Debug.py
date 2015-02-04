__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Debug.py

Module contains debugging output utility class
"""


# Imports

# Enumerations and Functions


# Classes

class OutputPipe:
    def __init__(self):
        pass

    def alert(self, msg, level):
        pass

class Level():
    """
    Defines a basic logging level enumeration

    Attributes:
        _verbose (bool): A flag indicating if the logging level is general or verbose
    """

    ERROR = "ERROR"
    INFO = "INFO"
    FATAL = "FATAL"

    def __init__(self):
        """
        Constructs the "static" instance of level
        """
        self._verbose = True        #Todo: Change to false for release
        self.message_pad = OutputPipe()

    def toggle(self):
        """
        Toggle the verbosity level
        """
        self._verbose = not self._verbose

    def set_message_pad(self, pad):
        """
        Set an additional output area to send messages to
        :param pad:
        :type pad: OutputPipe
        :return:
        """
        self.message_pad = pad

# "Static" instance of level that is used in determining the debugging output
d_level = Level()

def printi(mssg, level=Level.INFO, org=None):
    """
    Print a debug message based on the current verbosity filter

    :param mssg:        The message to be printed
    :param level:       The level the message is to be printed at
    """

    # Will not print the debug info if the level is not verbose
    if org is not "event":
        d_level.message_pad.alert(mssg, level)
    if d_level._verbose is False and level is Level.INFO:
        return
    print(level + ": " + mssg)

def printe(event, level=Level.INFO):
    """
    Print a debug message based on a user input event

    :param event:       The event that cause the message
    :param level:       The level the message is to be printed at
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
    printi(mssg, level, "event")

def printet(event, event_type, level=Level.INFO):
    """
    Print a debug message based on a user input event

    :param event:       The event that cause the message
    :param level:       The level the message is to be printed at
    """
    printi("Event Recorded || " + str(event_type) + " || x=" + str(event.x) + " y=" + str(event.y), level, "event")