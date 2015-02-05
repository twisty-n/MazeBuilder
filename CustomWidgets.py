import Debug

__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: CustomWidgets.py

Module contains custom widgets for the MazeBuilder project
"""


# Imports
from UtilWidgets import ListHeap, Dialog, ImagePicker
from Tkinter import Menu, Canvas, IntVar, Label, Entry, Checkbutton, W, ACTIVE
from Exceptions import DuplicateListHeapItemException, MaxItemLimitReachedException
from Containers import NodePictureContainer, WallTextureContainer


# Enumerations and Functions


# Classes


class NodePictureDialog(Dialog):
    """
    Dialog that allows the user to enter information to configue a Picture for a room in the maze
    """
    def __init__(self, parent, x=None, y=None, populator=None):
        # By default we will set the texture as visible
        self._entries = {
            "name"      : None,
            "visible"   : None,
            "texture"   : None
        }
        self._visi_var = IntVar(value=1)
        Dialog.__init__(self, parent, "PictureBuilder", True, x, y, populator)

    def body(self, parent):
        Label(parent, text="Name:").grid(row=0, column=0, sticky=W)
        Label(parent, text="Visible:").grid(row=1, column=0, sticky=W)
        self._texture = ImagePicker(parent, "Texture:", auto_move=True, move_fold="Data", default=self._entries["texture"])
        self._texture.grid(row=3, columnspan=3)

        self._name = Entry(parent, width=10)
        self._name.grid(row=0, column=1, sticky=W)
        if self._entries["name"] is not None:
            self._name.insert(0, self._entries["name"])

        if self._entries["visible"] is False:
            self._visi_var.set(0)
        else:
            self._visi_var.set(1)

        self._visible = Checkbutton(parent, command=self._toggle_visibility, var=self._visi_var)
        self._visible.grid(row=1, column=1, sticky=W)

    def _toggle_visibility(self):
        Debug.printi("Visibility changed to " + str(bool(self._visi_var)), Debug.Level.INFO)
        self._entries["visible"] = True

    def populate(self, manager):
        self._entries["name"]       =  manager.name
        self._entries["visible"]    =  manager.visible
        self._entries["texture"]    =  manager.texture

    def apply(self):
        self._entries["name"] = self._name.get()
        if self._entries["name"] is None:
            self._entries["name"] = "default"
        self._entries["texture"] = self._texture.get()
        self._entries["visible"] = self._visi_var.get()

    def validate(self):
        # TODO: inline validation
        return True

class WallTextureDialog(Dialog):
    """
    Dialog that allows the user to input configuration for the wall segments of the maze
    """
    def __init__(self, parent, x=None, y=None, populator=None):
        # By default we will set the texture as visible
        self._entries = {
            "path": None,
            "tile_x": None,
            "tile_y": None,
            "height": None
        }
        Dialog.__init__(self, parent, "WallBuilder", True, x, y, populator)

    def body(self, parent):
        self._texture = ImagePicker(parent, "Texture:", auto_move=True, move_fold="Data", default=self._entries["path"])
        self._texture.grid(row=0, columnspan=5)

        Label(parent, text="Height:").grid(row=1, column=0, sticky=W)
        Label(parent, text="Tile X:").grid(row=1, column=2, sticky=W)
        Label(parent, text="Tile Y:").grid(row=1, column=4, sticky=W)

        self._height = Entry(parent, width=5)
        self._height.grid(row=1, column=1, sticky=W)
        self._height.insert(0, self._entries["height"]) if self._entries["height"] is not None else self._height.insert(0,"")

        self._tile_x = Entry(parent, width=5)
        self._tile_x.grid(row=1, column=3, sticky=W)
        self._tile_x.insert(0, self._entries["tile_x"]) if self._entries["tile_x"] is not None else self._height.insert(0,"")

        self._tile_y = Entry(parent, width=5)
        self._tile_y.grid(row=1, column=5, sticky=W)
        self._tile_y.insert(0, self._entries["tile_y"]) if self._entries["tile_y"] is not None else self._height.insert(0,"")

    def populate(self, manager):
        self._entries["path"] = manager.path
        self._entries["tile_x"] = manager.tile_x
        self._entries["tile_y"] = manager.tile_y
        self._entries["height"] = manager.height


    def apply(self):
        self._entries["path"] = self._texture.get()
        self._entries["tile_x"] = self._tile_x.get()
        self._entries["tile_y"] = self._tile_y.get()
        self._entries["height"] = self._height.get()

    def validate(self):
        # TODO inline validation
        return True


class PicConfigurator(ListHeap):
    """
    Defines a custom widget to be used for selecting texture pictures

    The PicConfigurator is a widget that extends the ListHeap widget. It has been specifically
    designed to allow the user to select textures to be used as pictures for the walls
    of nodes in the mazes

    The remainder if this is yet to be implemented, and will be completed during the backend phase

    Attributes:

    """
    def __init__(self, parent, populator):
        """
        Construct and instance of PicConfigurator
        :param parent:      The parent tk item in which this widget will sit
        :return:            Instance of PicConfigurator
        """
        ListHeap.__init__(self, parent, populator, 6)
        self.propagate(0)
        self.config(width=10, height=100)

    def populate(self, populator):
        # Expects a list of wall pics with which to populate the widget
        for key, pic in populator.iteritems():
            self._add_new_wall_pic(pic)

    def _handle_db_click(self, event):
        """
        Handle mouse double click as a callback function

        Handles a mouse double click through the opening of an editing dialog
        for the picture item that was selected

        :param event:       The event generated by the window manager, automatically provided
        """
        Debug.printe(event, Debug.Level.INFO)
        item = self._listbox.get(ACTIVE)
        results = NodePictureDialog(self, populator=NodePictureContainer(self._items[item]))
        self._remove_wall_pic()
        self._add_new_wall_pic(results._entries)

    def _handle_r_click(self, event):
        """
        Handle mouse right click as a callback function

        Handle mouse right click by displaying a context menu for this widget,
        allow the addition and removal of window pics

        :param event:       The event generated by the window manager, automatically provided
        """
        Debug.printe(event, Debug.Level.INFO)

        # Create the menu to display
        p_menu = Menu(self._parent)
        p_menu.add_command(label="Add Picture", command=lambda: self._add_new_wall_pic())
        p_menu.add_command(label="Delete Picture", command=lambda: self._remove_wall_pic())
        p_menu.add_command(label="Delete All", command=lambda: self.remove_all())
        p_menu.post(event.x_root, event.y_root)

    def _add_new_wall_pic(self, pic=None):
        """
        Adds a new wall picture to the node definition

        Launches a dialog, and validates and posts the entered information
        to the repository for the creation of a new wall picture for the
        node that is being edited
        """
        # Display the dialogue
        results = pic
        if results is None:
            results = NodePictureDialog(self)
            results = results._entries

        item_id = results["name"]
        item = results
        # Extract the return values
        try:
            self.add_new(item, item_id)
        except DuplicateListHeapItemException:
            Debug.printi("Unable to add duplicate picture", Debug.Level.ERROR)
            return

        except MaxItemLimitReachedException:
            Debug.printi("Maximum number of pictures for this room reached", Debug.Level.ERROR)
            return

    def _remove_wall_pic(self):
        """
        Remove the wall picture that is currently selected
        """
        # Retrieve the item that was selected
        key = self._listbox.get(ACTIVE)
        # Post a delete notice to the manager
        self._remove(key)

    def remove_all(self):
        """
        Removes all of the wall pictures
        :return:
        """
        # Post a delete all notice to the manager
        self._remove_all()

    def get(self):
        """
        Return the information that has been gathered by this widget
        :return: [List] of WallPictureContainers
        """
        return self._items

class TexturePicker(ListHeap):
    def __init__(self, parent, populator):
        ListHeap.__init__(self, parent, populator)
        self.propagate(0)
        self.config(width=10, height=100)

    def populate(self, populator):
        for key, tex in populator.iteritems():
            self._add_new_texture(tex)


    def _handle_db_click(self, event):
        Debug.printe(event, Debug.Level.INFO)
        item = self._listbox.get(ACTIVE)
        results = WallTextureDialog(self, populator=WallTextureContainer(self._items[item]))
        self._remove_texture()
        self._add_new_texture(results._entries)
        pass

    def _handle_r_click(self, event):
        p_menu = Menu(self._parent)
        p_menu.add_command(label="Add Texture", command=lambda: self._add_new_texture())
        p_menu.add_command(label="Delete Texture", command=lambda: self._remove_texture())
        p_menu.add_command(label="Delete All", command=lambda: self.remove_all())
        p_menu.post(event.x_root, event.y_root)

    def _remove_texture(self):
        """
        Remove the wall picture that is currently selected
        """
        # Retrieve the item that was selected
        key = self._listbox.get(ACTIVE)
        # Post a delete notice to the manager
        self._remove(key)

    def remove_all(self):
        """
        Removes all of the wall pictures
        :return:
        """
        # Post a delete all notice to the manager
        self._remove_all()

    def get(self):
        """
        Return the information that has been gathered by this widget
        :return: [List] of WallPictureContainers
        """
        return self._items

    def _add_new_texture(self, tex=None):
        """
        Adds a new wall picture to the node definition

        Launches a dialog, and validates and posts the entered information
        to the repository for the creation of a new wall picture for the
        node that is being edited
        """
        # Display the dialogue
        results = tex
        if results is None:
            results = WallTextureDialog(self)
            results = results._entries

        item_id = results["path"]
        item = results
        # Extract the return values
        try:
            self.add_new(item, item_id)
        except DuplicateListHeapItemException:
            Debug.printi("Unable to add duplicate texture", Debug.Level.ERROR)
            return
