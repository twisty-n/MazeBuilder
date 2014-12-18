__author__ = 'tristan_dev'

from UtilWidgets import Dialog, ImagePicker
from Tkinter import Scale, Label, Entry, HORIZONTAL, E, W

class EnviroDialog(Dialog):
    def __init__(self, parent):
        Dialog.__init__(self, parent, "Environment Configuration")
        entries = {
            "floorTexVal": None,
            "wallHeight": None,
            "edgeWidth": None,
            "skyTexVal": None,
            "stateNode": None
        }

    def body(self, parent):
        self._floorSel = ImagePicker(parent, "Floor Texture").grid(row=0, columnspan=5)
        self._skySel = ImagePicker(parent, "Sky Texture").grid(row=1, columnspan=5)

        Label(parent, text="Wall Height", width=10).grid(row=2, column=0, sticky=W)
        Label(parent, text="Edge Width", width=10).grid(row=3, column=0, sticky=W)

        self._wallScale = Scale(parent, from_=10, to=1000, orient=HORIZONTAL).grid(row=2, column=1)
        self._edgeScale = Scale(parent, from_=10, to=1000, orient=HORIZONTAL).grid(row=3, column=1)

        Label(parent, text="Starting Node").grid(row=4, column=0, sticky=W)
        self._sNode = Entry(parent, width=10)
        self._sNode.grid(row=4, column=1)

    #TODO populate the handler methods


