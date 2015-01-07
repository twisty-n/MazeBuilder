__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: CustomWidgets.py
Classes based on those listed in
http://effbot.org/tkinterbook/tkinter-application-windows.htm

Contains custom widgets for the mazebuilder project
"""

from UtilWidgets import ListHeap
from Tkinter import Menu
from Exceptions import DuplicateListHeapItemException, MaxItemLimitReachedException
import Debug

class PicConfigurator(ListHeap):

    def __init__(self, parent, max_entries):
        ListHeap.__init__(self, parent, max_entries)
        self.propagate(0)
        self.config(width=10, height=100)

    def _handle_db_click(self, event):
        Debug.printe(event, Debug.Level.INFO)
        # Open a room picture editing dialogue
        pass

    def _handle_r_click(self, event):
        Debug.printe(event, Debug.Level.INFO)
        # Create the menu to display
        p_menu = Menu(self._parent)
        p_menu.add_command(label="Add Picture", command=lambda: self._add_new_wall_pic())
        p_menu.add_command(label="Delete Picture", command=lambda: self._remove_wall_pic())
        p_menu.add_command(label="Delete All", command=lambda: self._remove_all())
        p_menu.post(event.x_root, event.y_root)

    def _add_new_wall_pic(self):
        # Display the dialogue
        item_id = None
        item = None
        # Extract the return values
        try:
            self._add_new(item, item_id)
        except DuplicateListHeapItemException:
            Debug.printi("Unable to add duplicate picture", Debug.Level.ERROR)
            return
        except MaxItemLimitReachedException:
            Debug.printi("Maximum number of pictures for this room reached")
            return
        # TODO COMPLETE
        # Post the dialogue information to the *manager

    def _remove_wall_pic(self):
        # Retrieve the item that was selected
        key = None
        # Post a delete notice to the manager
        self.remove(key)

    def _remove_all(self):
        # Post a delete all notice to the manager
        self._remove_all()