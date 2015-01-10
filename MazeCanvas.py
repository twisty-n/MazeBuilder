__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Debug.py

Module contains the implementation
"""

# Imports
import Debug
from Tkinter import Canvas, Frame, BOTH, Menu
from DiaDoges import NodeDialog


# Enumerations and Functions

class Event:
    """
    A stand in enumeration that encapsulates the different main events
    """
    CLICK_M1        = "CLICK_M1"
    CLICK_M2        = "CLICK_M2"
    CLICK_M3        = "CLICK_M3"
    D_CLICK_M1      = "D_CLICK_M1"
    D_CLICK_M2      = "D_CLICK_M2"
    D_CLICK_M3      = "D_CLICK_M3"
    DRAG_M1         = "DRAG_M1"
    DRAG_M2         = "DRAG_M2"
    DRAG_M3         = "DRAG_M3"
    RELEASE_M1      = "RELEASE_M1"
    RELEASE_M2      = "RELEASE_M2"
    RELEASE_M3      = "RELEASE_M3"
    RETURN          = "RETURN"


# Classes

class MazePlannerCanvas(Frame):

    def __init__(self, parent, status=None):
        Frame.__init__(self, parent)
        self._canvas = Canvas(self, bg="grey", cursor="tcross")
        self._canvas.pack(fill=BOTH, expand=1)
        self._commands = {
            Event.CLICK_M1      : self._begin_node_drag,
            Event.CLICK_M2      : self._begin_edge,
            Event.RELEASE_M1    : self._end_node_drag,
            Event.RELEASE_M2    : self._end_edge,
            Event.DRAG_M1       : self._execute_drag,
            Event.RETURN        : self._launch_menu,
            Event.D_CLICK_M1    : self._node_operation
        }
        self._current_node_drag = { "x":None,
                                    "y":None  }
        self._command_cache = None
        self._cache = {
            "item"  : None,
            "x"     : None,
            "y"     : None,
            "event" : None
        }
        self._status = status
        self._construct(parent)

    def _construct(self, parent):
        self._canvas.focus_set()
        self._canvas.bind("<B1-Motion>", lambda event, m_event=Event.DRAG_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonPress-2>", lambda event, m_event=Event.CLICK_M2: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonRelease-2>", lambda event, m_event=Event.RELEASE_M2: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonPress-1>", lambda event, m_event=Event.CLICK_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonRelease-1>", lambda event, m_event=Event.RELEASE_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<Return>", lambda event, m_event=Event.RETURN: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<Double-Button-1>", lambda event, m_event=Event.D_CLICK_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<Motion>", lambda event, m_event=None : self._handle_mot(m_event, event))
        self._canvas.bind("<Enter>", lambda event: self._canvas.focus_set())

    def _handle_mot(self, m_event, event):
        self._status.set_text("Mouse X:" + str(event.x) + "\tMouse Y:" + str(event.y))
        self._cache["x"] = event.x
        self._cache["y"] = event.y

    def _handle_mouse_events(self, m_event, event):
        self._status.set_text("Mouse X:" + str(self._cache["x"]) + "\tMouse Y:" + str(self._cache["y"]))
        Debug.printet(event, m_event, Debug.Level.INFO)
        self._cache["event"] = event
        self._commands[m_event]((event.x, event.y))
        self._command_cache = m_event


    def _begin_node_drag(self, coords):
        # Determine which node has been selected, cache this information
        item = self._get_current_item(coords)
        self._update_cache(item, coords)

    def _end_node_drag(self, coords):
        if self._command_cache is Event.D_CLICK_M1 or None:
            # Don't dispatch if its the result of a double click
            return
        # Obtain the final points
        x = coords[0]
        y = coords[1]
        item = self._cache["item"]
        # TODO Check that the final points are within a valid range
        """
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self._canvas.winfo_width():
            x = self._canvas.winfo_width()-25
        if y > self._canvas.winfo_height():
            y = self._canvas.winfo_height()-25
        self._canvas.move(item, x, y)
        """
        # Clean the cache
        self._clear_cache()
        # TODO Post the information to the node manager

    def _execute_drag(self, coords):
        # Update the drawing information
        delta_x = coords[0] - self._cache["x"]
        delta_y = coords[1] - self._cache["y"]
        # move the object the appropriate amount
        self._canvas.move(self._cache["item"], delta_x, delta_y)
        # record the new position
        self._cache["x"] = coords[0]
        self._cache["y"] = coords[1]

    def _launch_menu(self, coords):
        # Launch a context menu based on the coords of the mouse
        item = self._get_current_item((self._cache["x"], self._cache["y"]))
        p_menu = Menu(self._canvas)

        if item is ():
            # No node is currently selected, create the general menu
            p_menu.add_command(label="Place Node", command=lambda: Debug.printi("Place node", Debug.Level.INFO))
            p_menu.add_command(label="Delete All", command=lambda: Debug.printi("Delete all nodes", Debug.Level.INFO))
        else:
            # Create the node specific menu
            p_menu.add_command(label="Place Object", command=lambda: Debug.printi("Place object", Debug.Level.INFO))
            p_menu.add_command(label="Edit Node", command=lambda: Debug.printi("Edit node", Debug.Level.INFO))
            p_menu.add_command(label="Delete  Node", command=lambda: Debug.printi("Delete node", Debug.Level.INFO))
            p_menu.add_command(label="Mark as start", command=lambda: Debug.printi("New starting node", Debug.Level.INFO))

        p_menu.post(self._cache["x"], self._cache["y"])

    def _begin_edge(self, coords):
        pass

    def _end_edge(self, coords):
        pass

    def _execute_edge(self, coords):
        pass

    def _update_cache(self, item, coords):
        self._cache["item"] = item
        self._cache["x"] = coords[0]
        self._cache["y"] = coords[1]

    def _clear_cache(self):
        self._cache["item"] = None
        self._cache["x"] = None
        self._cache["y"] = None

    def _get_current_item(self, coords):
        return self._canvas.find_overlapping(coords[0], coords[1], coords[0], coords[1])

    def _node_operation(self, coords):
        # Determine if they are double click on the canvas, or on a node
        item = self._get_current_item(coords)
        self._cache["item"] = item
        if item is not ():
            # Make request from object manager using the tag assigned
            NodeDialog(self, self._cache["event"].x_root+50, self._cache["event"].y_root+50)
            # post information to object manager, or let the dialog handle it, or whatever
            return
        # if its the canvas, plot a new node and show the editing dialog
        self._cache["item"] = self._canvas.create_rectangle(coords[0], coords[1], coords[0]+25, coords[1]+25,
                                outline="red", fill="black", activeoutline="black", activefill="red")
        # then open the dialog
        NodeDialog(self, self._cache["event"].x_root+50, self._cache["event"].y_root+50)



"""
data={"one":1,"two":2}
widget.bind("<ButtonPress-1>",
    lambda event, arg=data: self.OnMouseDown(event, arg))
"""

"""

import Tkinter as tk

class SampleApp(tk.Tk):
    '''Illustrate how to drag items on a Tkinter canvas'''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # create a canvas
        self.canvas = tk.Canvas(width=400, height=400)
        self.canvas.pack(fill="both", expand=True)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple movable objects
        self._create_token((100, 100), "white")
        self._create_token((200, 100), "black")

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.canvas.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)

    def _create_token(self, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        self.canvas.create_oval(x-25, y-25, x+25, y+25,
                                outline=color, fill=color, tags="token")

    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def OnTokenMotion(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

"""