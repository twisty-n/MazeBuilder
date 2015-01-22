import Debug

__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Debug.py

Module contains the custom user interface dialogs
"""


# Imports
from UtilWidgets import Dialog, ImagePicker
from CustomWidgets import PicConfigurator, TexturePicker
from Tkinter import Scale, Label, Entry, HORIZONTAL, E, W, Checkbutton, SW, Button, ACTIVE, END, StringVar, IntVar
import tkFileDialog


# Enumerations and Functions


# Classes

class EnviroDialog(Dialog):
    """
    Dialog for editing the simulation environment details
    """
    def __init__(self, parent, populator=None):
        """
        Construct the dialog
        :param parent:          The tk element that is the parent of the dialog
        :return:                An instance of EnviroDialog
        """
        self._entries = {
            "floor_texture": None,
            "wall_height": None,
            "edge_width": None,
            "sky_texture": None,
            "start_node": None
        }
        Dialog.__init__(self, parent=parent, title="EnvironmentConfiguration", populator=populator)

    def body(self, parent):
        """
        Overridden method defining the body of the dialog
        :param parent:
        :return:
        """
        # TODO: fix all of this up so that the references that I actually have are valid
        self._floorSel = ImagePicker(parent, "Floor Texture:",
                                     default=self._entries["floor_texture"])
        self._floorSel.grid(row=0, columnspan=4)
        self._skySel = ImagePicker(parent, "Sky Texture:", default=self._entries["sky_texture"])
        self._skySel.grid(row=1, columnspan=4)

        Label(parent, text="Wall Height:", width=10, anchor=W).grid(row=2, column=0, sticky=W)
        Label(parent, text="Edge Width:", width=10, anchor=W).grid(row=3, column=0, sticky=W)

        self._wallScale = Scale(parent, from_=10, to=1000, orient=HORIZONTAL)
        if self._entries["wall_height"] is not None:
            self._wallScale.set(self._entries["wall_height"])
        self._wallScale.grid(row=2, column=1, columnspan=2, sticky=W)

        self._edgeScale = Scale(parent, from_=10, to=1000, orient=HORIZONTAL)
        if self._entries["edge_width"] is not None:
            self._edgeScale.set(self._entries["edge_width"])
        self._edgeScale.grid(row=3, column=1, columnspan=2, sticky=W)

        Label(parent, text="Starting Node:", anchor=W).grid(row=4, column=0, sticky=W)
        self._sNode = Entry(parent, width=12, text=self._entries["start_node"])
        self._sNode.grid(row=4, column=1, columnspan=2, sticky=W)

    # TODO populate the handler methods
    def populate(self, populator):
        # I am against them just sharing a reference to a dict, as this is not robust
        # And this approach will not be taken with the other population schemes
        self._entries["floor_texture"]  = populator.floor_texture
        self._entries["edge_width"]     = populator.edge_width
        self._entries["sky_texture"]    = populator.sky_texture
        self._entries["start_node"]     = populator.start_node


class VRConfigDialog(Dialog):
    """
    Defines a custom dialog for editing the Virtual Reality params
    """
    def __init__(self, parent, populator=None):
        """
        Construct the dialog
        """
        self._entries = {
            "frame_angle"    : None,
            "distortion"     : False,
            "windowed"      : False,
            "eye_height"     : None,
            "minimum_dist_to_wall"  : None

        }
        self._dist_var = IntVar()
        self._win_var = IntVar()
        Dialog.__init__(self, parent=parent, title="VRConfiguration", populator=populator)

    def body(self, parent):
        """
        Overridden method defining the body of the dialog
        :param parent:
        :return:
        """

        # Define all of the labels for our options
        Label(parent, text="Frame Angle:", padx=3, anchor=SW, height=2).grid(row=0, column=0, sticky=W)
        Label(parent, text="Eye Height:", padx=3, anchor=SW, height=2).grid(row=1, column=0, pady=2, sticky=W )
        Label(parent, text="MinDistToWall:", padx=3, anchor=SW, height=2).grid(row=2, column=0, pady=2,  sticky=W)
        Label(parent, text="Distortion:", padx=3).grid(row=3, column=0, pady=2, sticky=W)
        Label(parent, text="Windowed:", padx=3).grid(row=4, column=0, pady=2, sticky=W)

        # Define the sub-widgets that the labels are referring to
        self._frameAngle = Scale(parent, from_=-20, to=20, orient=HORIZONTAL)
        if self._entries["frame_angle"] is not None:
            self._frameAngle.set(self._entries["frame_angle"])
        else:
            self._frameAngle.set(-5)
        self._frameAngle.grid(row=0, column=1, padx=3)

        self._eyeHeight = Scale(parent, from_=0, to=500, orient=HORIZONTAL)
        if self._entries["eye_height"] is not None:
            self._eyeHeight.set( self._entries["eye_height"] )
        else:
            self._eyeHeight.set(50)
        self._eyeHeight.grid(row=1, column=1, padx=3)

        self._minDistToWall = Scale(parent, from_=1, to=300, orient=HORIZONTAL)
        if self._entries["minimum_dist_to_wall"] is not None:
            self._eyeHeight.set( self._entries["minimum_dist_to_wall"] )
        else:
            self._minDistToWall.set(20)
        self._minDistToWall.grid(row=2, column=1, padx=3)

        self._distortion = Checkbutton(parent, text="Enable", command=self._toggle_distortion, var=self._dist_var)
        self._distortion.grid(row=3, column=1, padx=3)

        self._windowed = Checkbutton(parent, text="Enable", command=self._toggle_windowed, var=self._win_var)
        self._windowed.grid(row=4, column=1, padx=3)

    def _toggle_distortion(self):
        """
        Toggle the distortion flag
        :return:
        """
        val = self._entries["distortion"]
        self._entries["distortion"] = not val
        Debug.printi("Distortion toggled to " + (str(not val)), Debug.Level.INFO)

    def _toggle_windowed(self):
        """
        Toggle the windowed flag
        :return:
        """
        val = self._entries["windowed"]
        self._entries["windowed"] = not val
        Debug.printi("Windowing toggled to " + (str(not val)), Debug.Level.INFO)

    def populate(self, populator):
        self._entries["frame_angle"]            = populator.frame_angle
        self._entries["distortion"]             = populator.distortion
        self._entries["windowed"]               = populator.windowed
        self._entries["eye_height"]             = populator.eye_height
        self._entries["minimum_dist_to_wall"]   = populator.minimum_dist_to_wall
        self._dist_var = 1 if populator.distortion is True else 0
        self._win_var = 1 if populator.windowed is True else 0

class NodeDialog(Dialog):
    """
    Defines a custom dialog for node configuration
    """
    def __init__(self, parent, x=None, y=None, populator=None):
        """
        Construct the inital node dialog
        :param parent:          The tk parent instance to spawn the node from
        :return:                An instance of NodeDialog
        """
        self._entries = {
            "node_id"   : None,
            "x_coordinate"   : None,
            "y_coordinate"   : None,
            "room_texture" : None,
            "wall_pictures" : []
        }
        Dialog.__init__(self, parent, "NodeBuilder", True, x, y, populator)

    def body(self, parent):
        """
        Define the custom body of the dialog
        :param parent:          The parent instance of the dialog
        """

        # Define the labels of all of the widgets that are to be used
        Label(parent, text="Node ID:", anchor=SW).grid(row=0, column=0, sticky=W)
        Label(parent, text="x-Coord:", anchor=SW).grid(row=1, column=0, sticky=W)
        Label(parent, text="y-Coord:", anchor=SW).grid(row=2, column=0, sticky=W)

        self._node_id = Label(parent, text=self._entries["node_id"], anchor=SW).grid(row=0, column=1, sticky=W)
        self._x_coord = Label(parent, text=self._entries["x_coordinate"], anchor=SW).grid(row=1, column=1, sticky=W)
        self._y_coord = Label(parent, text=self._entries["y_coordinate"], anchor=SW).grid(row=2, column=1, sticky=W)

        # Image picker dialog for texture
        self._texture_selector = ImagePicker(parent, "Room Tex:", self._entries["room_texture"], auto_move=True, move_fold="Data")
        self._texture_selector.grid(row=3, columnspan=4)
        # New widget that allows configuration of multiple things -- to allow picking pictures for the walls
        self._wall_pics = PicConfigurator(parent, self._entries["wall_pictures"])
        self._wall_pics.grid(row=0, rowspan=3, column=2, sticky=E)

    def populate(self, populator):
        self._entries["node_id"]        = populator.node_id
        self._entries["x_coordinate"]   = populator.x_coordinate
        self._entries["y_coordinate"]   = populator.y_coordinate
        self._entries["room_texture"]   = populator.room_texture
        self._entries["wall_pictures"]  = populator.wall_pictures

    def validate(self):
        return True

    def apply(self):
        self._entries["room_texture"] = self._texture_selector.get()
        self._entries["wall_pictures"] = self._wall_pics.get()

class ObjectDialog(Dialog):
    """
    A custom dialog that allows the user to configure placing objects in the virtual environment
    """
    def __init__(self, parent, x=None, y=None, populator=None):
        """
        Construct the instance of the object dialog

        :param parent:          The parent tk instance that spawns the dialog
        """
        self._entries = {
            "x_coordinate"   : None,
            "y_coordinate"   : None,
            "name"      : None,
            "mesh"      : None,
            "scale"     : None
        }
        self._scale_text = StringVar()
        self._scale_text.set(str(1))

        Dialog.__init__(self, parent, "ObjectBuilder", True, x, y, populator)

    def body(self, parent):
        """
        Define the custom body of the dialog
        :param parent:          The parent instance of the dialog
        """
        # Define the labels of all of the sub widgets that are to be used
        Label(parent, text="Name:").grid(row=0, column=0, sticky=W)
        Label(parent, text="X Coord:").grid(row=1, column=0, sticky=W)
        Label(parent, text="Y Coord:").grid(row=1, column=2, sticky=W)
        Label(parent, text="Mesh:").grid(row=2, column=0, sticky=W)
        Label(parent, text="Scale:").grid(row=3, column=0, sticky=W)
        Label(parent, textvariable=self._scale_text, bg="grey").grid(row=3, column=1, sticky=W)

        #Define the text entry widgets
        self._object_name = Entry(parent, width=5, text=self._entries["name"])
        self._object_name.grid(column=1, row=0, sticky=W)
        self._x_coord = Entry(parent, width=5, text=self._entries["x_coordinate"])
        self._x_coord.grid(column=1, row=1, sticky=W)
        self._y_coord = Entry(parent, width=5, text=self._entries["y_coordinate"])
        self._y_coord.grid(column=3, row=1, stick=W)
        self._mesh = Entry(parent, width=15, text=self._entries["mesh"])

        if self._entries["mesh"] is None:
            self._mesh.insert(0, "No mesh loaded")
        self._mesh.grid(column=1, row=2, columnspan=2, sticky=W)
        Button(parent, text="Load", width=5, command=self._load_mesh, default=ACTIVE).grid(column=3, row=2)

        self._scale = Scale(parent, from_=1, to=100, orient=HORIZONTAL, length=140, variable=self._scale_text, showvalue=0)
        if self._entries["scale"] is not None:
            self._scale.set(self._entries["scale"])
            self._scale_text.set(str(self._entries["scale"]))
        self._scale.grid(row=3, column=2, columnspan=2, sticky=W)

    def _load_mesh(self):
        """
        Open a file dialog to load a mesh filepath
        :return:
        """
        Debug.printi("Load Mesh called", Debug.Level.INFO)
        types = \
            [
                ("DirectX", "*.x"),
                ("Test", "*.txt")
            ]
        dialog = tkFileDialog.Open(self, filetypes=types)
        file_path = dialog.show()

        self._mesh.delete(0, END)
        self._mesh.insert(0, file_path)
        Debug.printi("Mesh Filepath:" + file_path, Debug.Level.INFO)

    def populate(self, populator):
        self._entries["x_coordinate"]   = populator.x_coordinate
        self._entries["y_coordinate"]   = populator.y_coordinate
        self._entries["name"]           = populator.name
        self._entries["mesh"]           = populator.mesh
        self._entries["scale"]          = populator.scale


class EdgeDialog(Dialog):
    def __init__(self, parent, x=None, y=None, populator=None):
        """
        Construct the instance of EdgeDialog

        :param parent:          The parent widget that spawns this dialog
        """
        self._entries = \
            {
                "source" : None,
                "target" : None,
                "height" : None,
                "wall1"  : {
                    "height" : None,
                    "textures": []
                },
                "wall2"  : {
                    "height" : None,
                    "textures": []
                }

            }
        Dialog.__init__(self, parent, "EdgeBuilder", True, x, y, populator)

    def body(self, parent):
        """
        Define the body of the dialog
        """
        Label(parent, text="Source:", bg="grey").grid(row=0, column=0, sticky=W)
        Label(parent, text="Target:", bg="grey").grid(row=0, column=2, sticky=W)
        Label(parent, text="Wall1:").grid(row=1, column=0, sticky=W+E, columnspan=2)
        Label(parent, text="Wall2:").grid(row=1, column=2, sticky=W+E, columnspan=2)

        # The edge options now
        self.source = Label(parent, width=9, text=self._entries["source"], bg="grey")
        self.target = Label(parent, width=9, text=self._entries["target"], bg="grey")
        self.source.grid(row=0, column=1, sticky=W)
        self.target.grid(row=0, column=3, sticky=W)

        # The wall options now
        Label(parent, text="Height:").grid(row=2, column=0, sticky=W)
        Label(parent, text="Height:").grid(row=2, column=2, sticky=W)
        self.wall1_tex_select = TexturePicker(parent, self._entries["wall1"]["textures"])
        self.wall2_tex_select = TexturePicker(parent, self._entries["wall2"]["textures"])
        self.wall1_tex_select.config(width=18)
        self.wall2_tex_select.config(width=18)
        self.wall1_tex_select.grid(row=3, columnspan=2, column=0)
        self.wall2_tex_select.grid(row=3, columnspan=2, column=2)
        self.wall1_height = Entry(parent, width=9, text=self._entries["wall1"]["height"])
        self.wall2_height = Entry(parent, width=9, text=self._entries["wall2"]["height"])
        self.wall1_height.grid(row=2, column=1)
        self.wall2_height.grid(row=2, column=3)

    def populate(self, populator):
        self._entries["source"]             = populator.source
        self._entries["target"]             = populator.target
        self._entries["height"]             = populator.height
        if populator.wall1 is not None:
            self._entries["wall1"]["height"]    = populator.wall1.height
            self._entries["wall1"]["textures"] = populator.wall1.textures
        # Note that we will store the textures in WallTextureContainers in the dialog
        # instead of in the standard raw format, this should make it easier to use if
        # even we are making is a little nasty :/
        if populator.wall2 is not None:
            self._entries["wall2"]["height"]    = populator.wall2.height
            self._entries["wall2"]["textures"] = populator.wall2.textures

    def apply(self):
        self._entries["wall1"]["height"] = self.wall1_height.get()
        self._entries["wall2"]["height"] = self.wall2_height.get()
        self._entries["wall1"]["textures"] = self.wall1_tex_select.get()
        self._entries["wall2"]["textures"] = self.wall2_tex_select.get()

    def validate(self):
        return True

