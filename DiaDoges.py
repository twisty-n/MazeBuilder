__author__ = 'tristan_dev'

from UtilWidgets import Dialog, ImagePicker
from Tkinter import Scale, Label, Entry, HORIZONTAL, E, W, Checkbutton, S, SW
import Debug

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

    #TODO populate the handler methods

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

        #Define all of the labels for our options
        Label(parent, text="Frame Angle:", padx=3, anchor=SW, height=2).grid(row=0, column=0, sticky=W)
        Label(parent, text="Eye Height:", padx=3, anchor=SW, height=2).grid(row=1, column=0, pady=2, sticky=W )
        Label(parent, text="MinDistToWall:", padx=3, anchor=SW, height=2).grid(row=2, column=0, pady=2,  sticky=W)
        Label(parent, text="Distortion:", padx=3).grid(row=3, column=0, pady=2, sticky=W)
        Label(parent, text="Windowed:", padx=3).grid(row=4, column=0, pady=2, sticky=W)

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

