#Special import
from __future__ import print_function
import MazeCanvas
import Debug

__author__ = 'tristan_dev'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: MazeBuilder.py
"""

#Imports

from Tkinter import Frame, Tk, Menu, BOTTOM, X, BOTH
from UtilWidgets import StatusBar
from DiaDoges import EnviroDialog, VRConfigDialog, NodeDialog, ObjectDialog
from UtilWidgets import SubMenu
from DataStore import DataStore
from XMLifier import XMLObserver


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
    mazeBuilder.pack(fill=BOTH, expand=1)
    return root

def launch():
    """
    Launch the application
    """
    build().mainloop()


class MainMBMenuBar():
    """
    Encapsulates all of the functions required of the MazeBuilder menu bar

    The Menubar class contains all of the menu options and submenus to
    provide all of the tools needed to view load and build mazes
    Menu entries are cascades which form submenus. These may or may not be chained

    Attributes:
        _root(Tk):          The root of the application to hook the menus into
        _root_menu(Menu):   The main menubar of the application
    """
    def __init__(self, root, manager=None):
        """
        Initializes all of the requisite class members to their initial state
        """
        self._root = root
        self._entries = {}
        self._root_menu = Menu(self._root)
        root.config(menu=self._root_menu)
        self._manager = manager
        self.construct()

    def construct(self):
        #TODO: remap all hardcoded calls to the Command Manager
        """
        Construct the default menu bar with all of the default options

        Constructs the default menu bar with its associated submodules
        While at the moment this is hardcoded, there my be some scope in the future to
        allow it all to be configurable
        """
        file_sub = SubMenu(self._root_menu, "File")
        file_sub.add_option("Load Environment", (lambda: print("File:Load_Environment Undefined")), "command")
        file_sub.add_option("Save Environment", (lambda: print("File:Save_Environment Undefined")), "command")
        file_sub.add_option("Export Environment", (lambda: print("File: Load_Environment Undefined")), "command")
        file_sub.add_option("Quit", quit, "command")
        self.addEntry(file_sub._label, file_sub)

        configure_sub = SubMenu(self._root_menu, "Configure")
        configure_sub.add_option("Environment", (lambda: EnviroDialog(self._root,
                                                                        manager=self._manager,
                                                                        populator=self._manager.request(DataStore.DATATYPE.ENVIRONMENT))), "command")
        configure_sub.add_option("VR Settings", (lambda: VRConfigDialog(self._root,
                                                                        manager=self._manager,
                                                                        populator=self._manager.request(DataStore.DATATYPE.VR_CONFIG))), "command")
        self.addEntry(configure_sub._label, configure_sub)

        tools_sub = SubMenu(self._root_menu, "Tools")
        tools_sub.add_option("Debug", (lambda: Debug.d_level.toggle()), "checkbutton")
        tools_sub.add_option("View XML", (lambda: print("Tools:View_XML Undefined")), "checkbutton")
        # TODO: Write a control parser that reads in control configs
        tools_sub.add_option("Configure Controls", (lambda: print("Tools:Configure Controls")), "command")
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
        self._parent = parent
        self.manager = DataStore()
        self.xml = XMLObserver(self.manager)
        self._menubar = MainMBMenuBar(self._parent, manager=self.manager)
        self.pack(fill=BOTH, expand=1)
        self.construct()

    def construct(self):
        status = Frame(self)
        self._update_bar = StatusBar(status)
        self._drawer = MazeCanvas.MazePlannerCanvas(self, self._update_bar, manager=self.manager)
        self._drawer.pack(fill=BOTH, expand=1)
        self._status_bar = StatusBar(status)
        status.pack(side=BOTTOM, fill=X)

        self._status_bar.pack(side=BOTTOM, fill=X)
        self._update_bar.pack(side=BOTTOM, fill=X)

