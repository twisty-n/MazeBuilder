__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Debug.py

Module contains the custom user interface dialoges
"""

# Imports
from UtilWidgets import Dialog, ImagePicker
from CustomWidgets import PicConfigurator
from Tkinter import Scale, Label, Entry, HORIZONTAL, E, W, Checkbutton, S, SW
import Debug


# Enumerations and Functions


# Classes

class EnviroDialog(Dialog):
    def __init__(self, parent):
        self._entries = {
            "floorTexVal": None,
            "wallHeight": None,
            "edgeWidth": None,
            "skyTexVal": None,
            "stateNode": None
        }
        Dialog.__init__(self, parent, "Environment Configuration")

    def body(self, parent):

        self._floorSel = ImagePicker(parent, "Floor Texture:").grid(row=0, columnspan=4)
        self._skySel = ImagePicker(parent, "Sky Texture:").grid(row=1, columnspan=4)

        Label(parent, text="Wall Height:", width=10, anchor=W).grid(row=2, column=0, sticky=W)
        Label(parent, text="Edge Width:", width=10, anchor=W).grid(row=3, column=0, sticky=W)

        self._wallScale = Scale(parent, from_=10, to=1000, orient=HORIZONTAL)
        self._wallScale.grid(row=2, column=1, columnspan=2, sticky=W)
        self._edgeScale = Scale(parent, from_=10, to=1000, orient=HORIZONTAL)
        self._edgeScale.grid(row=3, column=1, columnspan=2, sticky=W)

        Label(parent, text="Starting Node:", anchor=W).grid(row=4, column=0, sticky=W)
        self._sNode = Entry(parent, width=12)
        self._sNode.grid(row=4, column=1, columnspan=2, sticky=W)

    # TODO populate the handler methods

class VRConfigDialog(Dialog):
    def __init__(self, parent):
        self._entries = {
            "frameAngle"    : None,
            "distortion"     : False,
            "windowed"      : False,
            "eyeHeight"     : None,
            "minDisToWall"  : None

        }
        Dialog.__init__(self, parent, "VR Configuration")

    def body(self, parent):

        # Define all of the labels for our options
        Label(parent, text="Frame Angle:", padx=3, anchor=SW, height=2).grid(row=0, column=0, sticky=W)
        Label(parent, text="Eye Height:", padx=3, anchor=SW, height=2).grid(row=1, column=0, pady=2, sticky=W )
        Label(parent, text="MinDistToWall:", padx=3, anchor=SW, height=2).grid(row=2, column=0, pady=2,  sticky=W)
        Label(parent, text="Distortion:", padx=3).grid(row=3, column=0, pady=2, sticky=W)
        Label(parent, text="Windowed:", padx=3).grid(row=4, column=0, pady=2, sticky=W)

        # Define the sub-widgets that the labels are referring to
        self._frameAngle = Scale(parent, from_=-20, to=20, orient=HORIZONTAL)
        self._frameAngle.set(-5)
        self._frameAngle.grid(row=0, column=1, padx=3)

        self._eyeHeight = Scale(parent, from_=0, to=500, orient=HORIZONTAL)
        self._eyeHeight.set(50)
        self._eyeHeight.grid(row=1, column=1, padx=3)

        self._minDistToWall = Scale(parent, from_=1, to=300, orient=HORIZONTAL)
        self._minDistToWall.set(20)
        self._minDistToWall.grid(row=2, column=1, padx=3)

        self._distortion = Checkbutton(parent, text="Enable", command=self._toggle_distortion)
        self._distortion.grid(row=3, column=1, padx=3)

        self._windowed = Checkbutton(parent, text="Enable", command=self._toggle_windowed)
        self._windowed.grid(row=4, column=1, padx=3)

    def _toggle_distortion(self):
        val = self._entries["distortion"]
        self._entries["distortion"] = not val
        Debug.printi("Distortion toggled to " + (str(not val)), Debug.Level.INFO)

    def _toggle_windowed(self):
        val = self._entries["windowed"]
        self._entries["windowed"] = not val
        Debug.printi("Windowing toggled to " + (str(not val)), Debug.Level.INFO)

class NodeDialog(Dialog):

    def __init__(self, parent):
        self._entries = {

        }
        Dialog.__init__(self, parent, "Node Builder")

    def body(self, parent):

        # Define the labels of all of the widgets that are to be used
        Label(parent, text="Node ID:", anchor=SW).grid(row=0, column=0, sticky=W)
        Label(parent, text="x-Coord:", anchor=SW).grid(row=1, column=0, sticky=W)
        Label(parent, text="y-Coord:", anchor=SW).grid(row=2, column=0, sticky=W)

        self._node_id = Entry(parent, width=5)
        self._node_id.grid(column=1, row=0)
        self._x_coord = Entry(parent, width=5)
        self._x_coord.grid(column=1, row=1)
        self._y_coord = Entry(parent, width=5)
        self._y_coord.grid(column=1, row=2)

        # The text entry areas, these will have to be autofilled for some part
        # TODO: write auto-population utility for things

        # Image picker dialog for texture
        self._texture_selector = ImagePicker(parent, "Room Tex:")
        self._texture_selector.grid(row=3, columnspan=4)
        # New widget that allows configuration of multiple things -- to allow picking pictures for the walls
        self._wall_pics = PicConfigurator(parent, 6)
        self._wall_pics.grid(row=0, rowspan=3, column=2, sticky=E)


