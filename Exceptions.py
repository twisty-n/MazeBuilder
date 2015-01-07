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
    def  __init__(self, item):
        Exception.__init__("Item" + str(item) + "already exists in ListHeap")

class MaxItemLimitReachedException(Exception):
    def __init__(self):
        Exception.__init__("Maximum number of items reached for this ListHeap")
