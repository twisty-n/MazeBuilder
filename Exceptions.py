__author__ = 'tristan_dev'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Exceptions.py
"""

class CommandException(Exception):
    """
    Base class for command related exceptions
    """
    pass

class DuplicateCommandException(CommandException):
    """
    Raised when a duplicate command item is added to a menu

    Attributes:
        _label:     The label that caused the excpetion
        _msg:       The msg to be reported
    """
    def __init__(self, label="UNDEFINED", msg="Duplicate command exception. Command label already exists in menu"):
        self._label = label
        self._msg = msg

class DuplicateListHeapItemException(Exception):
    """
    Raised when a duplicate item is added to a ListHeap
    """
    def  __init__(self, item):
        Exception.__init__(self, "Item" + str(item) + "already exists in ListHeap")

class MaxItemLimitReachedException(Exception):
    """
    Raised when an attempt to add an item to a ListHeap is made when the ListHeap is at maximum capacity
    """
    def __init__(self):
        Exception.__init__(self, "Maximum number of items reached for this ListHeap")

class ContainerFillException(Exception):
    """
    Raised when the incorrect dictionary has been provided to fill a given container
    """
    def __init__(self, container_type, provided_dict):
        Exception.__init__(self, "Improper dictionary provided to container of type "
                           + container_type + "|| Values provided: " + str(provided_dict))

class InvalidDataException(Exception):
    """
    Raised when data provided is invalid
    """
    def __init__(self, event, data):
        Exception.__init__("Invalid data provided for event" + str(event) + "\tData: " + str(data))