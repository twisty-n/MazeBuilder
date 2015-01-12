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
import math
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
            Event.DRAG_M2       : self._execute_edge,
            Event.RETURN        : self._launch_menu,
            Event.D_CLICK_M1    : self._node_operation
        }
        self._edge_cache = \
            {
                "x_start"       : None,
                "y_start"       : None,
                "item_start"    : None,
                "item_end"      : None,
                "edge"          : None
            }
        self._command_cache = None
        self._cache = \
            {
                "item"  : None,
                "x"     : 0,
                "y"     : 0,
                "event" : None
            }
        self._status = status
        self._construct(parent)

    def _construct(self, parent):
        self._canvas.focus_set()
        self._canvas.bind("<B1-Motion>", lambda event, m_event=Event.DRAG_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<B2-Motion>", lambda event, m_event=Event.DRAG_M2: self._handle_mouse_events(m_event, event))
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
        self._clear_cache(coords)
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

        updated_coords = self._canvas_to_screen((self._cache["x"], self._cache["y"]))
        p_menu.post(updated_coords[0], updated_coords[1])

    def _canvas_to_screen(self, coords):
        # upper left corner of the visible region
        x0 = self._canvas.winfo_rootx()
        y0 = self._canvas.winfo_rooty()

        # given a canvas coordinate cx/cy, convert it to window coordinates:
        wx0 = x0 + coords[0]
        wy0 = y0 + coords[1]
        return (int(wx0), int(wy0))

    def _begin_edge(self, coords):
        # Record the starting node
        self._edge_cache["item_start"] = self._get_current_item((self._cache["x"], self._cache["y"]))
        self._edge_cache["x_start"] = self._cache["x"]
        self._edge_cache["y_start"] = self._cache["y"]

    def _end_edge(self, coords):
        # Record the ending node\
        # Check if the cursor is over a node,
        # if it is, perform normally
        # else, cancel the edge creation by deleting the object
        # Post the edge information to the object manager
        # Clear the current edge from the edge drawing cache
        self._canvas.tag_lower("edge")
        self._clear_edge_cache()
        pass

    def _execute_edge(self, coords):
        # Update the line position
        # We will update the line position by deleting and redrawing
        self._canvas.delete(self._edge_cache["edge"])
        self._edge_cache["edge"] = self._canvas.create_line( \
            self._edge_cache["x_start"], self._edge_cache["y_start"],
            coords[0], coords[1], tags="edge")

    def _update_cache(self, item, coords):
        self._cache["item"] = item
        self._cache["x"] = coords[0]
        self._cache["y"] = coords[1]

    def _clear_cache(self, coords):
        self._cache["item"] = None
        self._cache["x"] = coords[0]
        self._cache["y"] = coords[1]

    def _clear_edge_cache(self):

        self._edge_cache["x_start"]       = None,
        self._edge_cache["y_start"]       = None,
        self._edge_cache["item_start"]    = None,
        self._edge_cache["item_end"]      = None,
        self._edge_cache["edge"]          = None


    def _get_current_item(self, coords):
        Debug.printi("X:"+ str(self._cache["x"]) + " Y:" + str(self._cache["y"]), Debug.Level.INFO)
        return self._canvas.find_overlapping(self._cache["x"], self._cache["y"], self._cache["x"], self._cache["y"])

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
