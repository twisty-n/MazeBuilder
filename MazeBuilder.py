#Special import
from __future__ import print_function

__author__ = 'tristan_dev'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: MazeBuilder.py
"""

#Imports

from Tkinter import Frame, Tk, Menu, Image, BOTTOM, X, SW, SE
from Exceptions import DuplicateCommandException
from UtilWidgets import StatusBar, Dialog
from DiaDoges import EnviroDialog


WIN_X = 700         #Defines the window X width
WIN_Y = 500         #Defines the window Y width
POSITION = 200      #Defines the x, y window position

def build():
    """
    Constructs the application

    :return:    An instance of Tk to launch
    """
    root = Tk()
    #TODO, get the icon working
    root.title("MazeBuilder")
    root.geometry(str(WIN_X)+"x"+str(WIN_Y)+"+"+str(POSITION)+"+"+str(POSITION))
    mazeBuilder = MazeBuilder(root)
    return root

def launch():
    """
    Launch the application
    """
    build().mainloop()

class SubMenu():

    def __init__(self, parent_menu, label):
        """

        """
        self._parent_menu = parent_menu
        self._options = {}
        self._label = label
        self._menu = Menu(parent_menu)
        self._key_underline = 0

    def add_option(self, label, action, type_func, shortcut):
        #TODO implement
        pass

    def add_option(self, label, action, type_func):
        """
        Adds a menu item to the submenu

        Adds a menu item to the dictionary of menu items that make up this
        submenu. Also adds the command to actual Tk menu structure,
        Function will fail if the menu item already exists
        :param label(string):           The label of the option to add
        :param action(function):        The action callback to be executed
        :param type_func(string):       The menu entry function for the type of item to add to the menu
        """
        _type = \
        {          "command"        : self._menu.add_command,
                   "checkbutton"    : self._menu.add_checkbutton,
                   "radiobutton"    : self._menu.add_radiobutton
        }

        if label in self._options:
            raise DuplicateCommandException(label)

        self._options[label] = action
        _type[type_func](label=label, command=action)

    def remove_option(self, label):
        """
        Remove a menu option from this submenu

        Removes a menu option from this submenu
        Will fail silently if the menu item does not exist

        :param label:       The label of the menu item that needs to be removed
        """
        del self._options[label]
        index = self._menu.index(label)
        self._menu.delete(index, index)


class MenuBar():
    """
    Encapsulates all of the functions required of the MazeBuilder menu bar

    The Menubar class contains all of the menu options and submenus to
    provide all of the tools needed to view load and build mazes
    Menu entries are cascades which form submenus. These may or may not be chained

    Attributes:
        _root(Tk):          The root of the application to hook the menus into
        _root_menu(Menu):   The main menubar of the application
    """
    def __init__(self, root):
        """
        Initializes all of the requisite class members to their initial state
        """
        self._root = root
        self._root_menu = Menu(self._root)
        self._entries = {}
        root.config(menu=self._root_menu)
        self.construct()

    def construct(self):
        """
        Construct the default menu bar with all of the default options

        Constructs the default menu bar with its associated submodules
        While at the moment this is hardcoded, there my be some scope in the future to
        allow it all to be configurable
        """
        file_sub = SubMenu(self._root_menu, "File")
        file_sub.add_option("Load Environment", (lambda: print("File:Load_Environment Undefined")), "command")
        file_sub.add_option("Save Environment", (lambda: print("File:Save_Environment Undefined")), "command")
        file_sub.add_option("Quit", quit, "command")
        self.addEntry(file_sub._label, file_sub)

        place_sub = SubMenu(self._root_menu, "Place")
        place_sub.add_option("Place Node", (lambda: print("Place:Place_Node_Undefined")), "command")
        place_sub.add_option("Place Object", (lambda: print("Place:Place_Object_Undefined")), "command")
        self.addEntry(place_sub._label, place_sub)

        configure_sub = SubMenu(self._root_menu, "Configure")
        configure_sub.add_option("Environment", (lambda: EnviroDialog(self._root)), "command")
        configure_sub.add_option("VR Settings", (lambda: print("Configure:VR Settings_Undefined")), "command")
        self.addEntry(configure_sub._label, configure_sub)

        tools_sub = SubMenu(self._root_menu, "Tools")
        tools_sub.add_option("Debug", (lambda: print("Tools:Debug_Undefined")), "checkbutton")
        tools_sub.add_option("View XML", (lambda: print("Tools:View_XML Undefined")), "checkbutton")
        self.addEntry(tools_sub._label, tools_sub)

    def addEntry(self, label, submenu):
        """
        Add an entry to the menu bar

        Adds the provided submenu to the menu bar under the given lable
        using a cascading style
        """
        self._entries[label] = submenu
        self._root_menu.add_cascade(label=label, menu=submenu._menu)


class MazeBuilder(Frame):
    """
    Top level class containing the top level application constructs

    The Mazebuilder class captures all of the components and acts as a
    top level window containing the entirety of the application

    Attributes:
        _menuBar(MenuBar):  The menubar that contains all of the needed menu options
    """
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.menubar = MenuBar(self.parent)
        self.construct()

    def construct(self):
        #TODO, add in geometry management and layout management
        pass


