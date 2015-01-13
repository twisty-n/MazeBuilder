__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: MazeCanvas.py


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
            Event.DRAG_M2       : self._execute_edge,
            Event.RETURN        : self._launch_menu,
            Event.D_CLICK_M1    : self._node_operation
        }
        self._edge_cache = \
            {
                "x_start"       : None,
                "y_start"       : None,
                "x_end"         : None,
                "y_end"         : None,
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
        self._edge_bindings = {}
        self._node_listing = {}
        self._construct(parent)

    def _construct(self, parent):
        """
        Construct all of the event bindings and callbacks for mouse events
        """
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
        """
        Callback function to handle movement of the mouse

        Function updates the mouse location status bar as well as setting cache values to the current location
        of the mouse

        :m_event:           The specifier for the type of event that has been generated
        :event:             The tk provided event object
        """
        self._status.set_text("Mouse X:" + str(event.x) + "\tMouse Y:" + str(event.y))
        self._cache["x"] = event.x
        self._cache["y"] = event.y

    def _handle_mouse_events(self, m_event, event):
        """
        Function that routes mouse events to the appropriate handlers

        Prints logging and UI information about the state of the mouse and then routes
        the mouse event to the appropriate handler

        :m_event:           The specifier for the tupe of event that has been generated
        :event:             The tk provided event object
        """
        self._status.set_text("Mouse X:" + str(self._cache["x"]) + "\tMouse Y:" + str(self._cache["y"]))
        Debug.printet(event, m_event, Debug.Level.INFO)
        self._cache["event"] = event
        self._commands[m_event]((event.x, event.y))
        self._command_cache = m_event


    def _begin_node_drag(self, coords):
        """
        Handles starting operations for dragging a node

        Updates the cache information regarding a node drag event, we will used this cache value
        as the handle on which node to update the information for

        :coords:            The mouse coordinates associated with this event
        """
        # Determine which node has been selected, cache this information
        item = self._get_current_item(coords)
        if item in self._node_listing:
            self._update_cache(item, coords)

    def _end_node_drag(self, coords):
        """
        Performs actions to complete a node drag operation

        Validates node location, and other associated object information and updates the cache
        when a node drag is completed

        :coords:            The coordinates associated with this event
        """

        # TODO add in local object manager information
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
        """
        Updates object position on canvas when user is dragging a node

        :param coords:          The coordinates associated with this event
        """
        # Update the drawing information
        delta_x = coords[0] - self._cache["x"]
        delta_y = coords[1] - self._cache["y"]
        # move the object the appropriate amount
        self._canvas.move(self._cache["item"], delta_x, delta_y)
        # record the new position
        self._cache["x"] = coords[0]
        self._cache["y"] = coords[1]
        # TODO: make sure that any attached edges are update
        self._update_attached_edges(self._cache["item"], coords)

    def _update_attached_edges(self, node, coords):
        """
        Updates all associated edges related to a node drag event

        :param node:            The node that has been dragged
        :param coords:          The mouse coordinates which are the new coordinates of the node
        """

        # Go through dictionary and gather list of all attached edge bindings for a node
        start_bindings = []
        for n in self._edge_bindings:
            if self._edge_bindings[n].item_start == node:
                start_bindings.append(self._edge_bindings[n])
        end_bindings = []
        for n in self._edge_bindings:
            if self._edge_bindings[n].item_end == node:
                end_bindings.append(self._edge_bindings[n])

        #  Adjust the bindings with this node as the starting edge
        for binding in start_bindings:
            self._canvas.delete(binding.edge)
            binding.edge = self._canvas.create_line( \
                coords[0], coords[1],
                binding.x_end, binding.y_end, tags="edge")
            binding.x_start = coords[0]
            binding.y_start = coords[1]

        # Adjust the bindings with this node as the ending edge
        for binding in end_bindings:
            self._canvas.delete(binding.edge)
            binding.edge = self._canvas.create_line( binding.x_start, binding.y_start, coords[0], coords[1], tags="edge")
            binding.x_end = coords[0]
            binding.y_end = coords[1]

        # Remeber to adjust all of the edges so that they sit under the node images
        self._canvas.tag_lower("edge")

    def _launch_menu(self, coords):
        """
        Callback function in response to the pressing of the Return key

        Launches a context menu based on the location of the mouse
        :param coords:
        :return:
        """
        # Launch a context menu based on the coords of the mouse
        item = self._get_current_item((self._cache["x"], self._cache["y"]))
        p_menu = Menu(self._canvas)

        if item is ():
            # No node is currently selected, create the general menu
            p_menu.add_command(label="Place Node", command=lambda coords: self._node_operation(coords))
            p_menu.add_command(label="Delete All", command=lambda: Debug.printi("Delete all nodes", Debug.Level.INFO))
        else:
            # Create the node specific menu
            p_menu.add_command(label="Place Object", command=lambda: Debug.printi("Place object", Debug.Level.INFO))
            p_menu.add_command(label="Edit Node", command=lambda: Debug.printi("Edit node", Debug.Level.INFO))
            p_menu.add_command(label="Delete  Node", command=lambda: Debug.printi("Delete node", Debug.Level.INFO))
            p_menu.add_command(label="Mark as start", command=lambda: Debug.printi("New starting node", Debug.Level.INFO))

        updated_coords = self._canvas_to_screen((self._cache["x"], self._cache["y"]))
        p_menu.tk_popup(updated_coords[0], updated_coords[1])

    def _valid_edge_cache(self):
        """
        Return true if the edge cache contains a valid edge descriptor

        A valid edge descriptor is when the edge has a valid starting node, if the
        edge does not contain a valid starting node, this means that the edge was not
        created in the proper manner and should thus be ignored by any edge operations
        :return:
        """
        return self._edge_cache["item_start"] is not (None,)

    def _canvas_to_screen(self, coords):
        """
        Convert canvas coordinates into screen coordinates

        :param coords:              The current canvas coordinates
        :return:
        """
        # upper left corner of the visible region
        x0 = self._canvas.winfo_rootx()
        y0 = self._canvas.winfo_rooty()

        # given a canvas coordinate cx/cy, convert it to window coordinates:
        wx0 = x0 + coords[0]
        wy0 = y0 + coords[1]
        return (int(wx0), int(wy0))

    def _begin_edge(self, coords):
        """
        Begin recording information regarding the placement of an edge

        :param coords:               The coordinates associated with this event
        """
        # Record the starting node
        self._edge_cache["item_start"] = self._get_current_item((self._cache["x"], self._cache["y"]))
        if self._edge_cache["item_start"] is None or self._edge_cache["item_start"] not in self._node_listing:
            self._clear_edge_cache()
            return
        self._edge_cache["x_start"] = self._cache["x"]
        self._edge_cache["y_start"] = self._cache["y"]

    def _end_edge(self, coords):
        """
        Perform the operations required to complete an edge creation operation
        :param coords:
        :return:
        """
        # Record the ending node\
        # Check if the cursor is over a node, if so continue, else abort

        curr = self._get_current_item((coords[0], coords[1]))
        if curr is None or not self._valid_edge_cache() or curr not in self._node_listing:
            # Abort the edge creation process
            self._canvas.delete(self._edge_cache["edge"])
            self._clear_edge_cache()
            return
        # Post the edge information to the object manager
        # Clear the current edge from the edge drawing cache
        # Need to use the coord values as the cache values aren't updated during a drag apparently
        self._canvas.tag_lower("edge")
        self._edge_cache["x_end"] = coords[0]
        self._edge_cache["y_end"] = coords[1]
        self._edge_cache["item_end"] = curr
        self._edge_bindings[self._edge_cache["edge"]] = EdgeBind(self._edge_cache)
        self._clear_edge_cache()

    def _execute_edge(self, coords):
        """
        Perform the operations that occur during the motion of an edge drag

        :param coords:
        :return:
        """
        # Update the line position
        # We will update the line position by deleting and redrawing
        if not self._valid_edge_cache():
            return
        self._canvas.delete(self._edge_cache["edge"])
        self._edge_cache["edge"] = self._canvas.create_line( \
            self._edge_cache["x_start"], self._edge_cache["y_start"],
            coords[0]-1, coords[1]-1, tags="edge")

    def _update_cache(self, item, coords):
        """
        Update the local cache with the item id and coordinates of the mouse

        :param item:                The item with which to update the cache
        :param coords:              The current event coordinates
        """
        self._cache["item"] = item
        self._cache["x"] = coords[0]
        self._cache["y"] = coords[1]

    def _clear_cache(self, coords):
        """
        Clear the cache

        Set the cache values to the current mouse position and None the item
        :param coords:              The coordinates of the mouse at that event time
        """
        self._cache["item"] = None
        self._cache["x"] = coords[0]
        self._cache["y"] = coords[1]

    def _clear_edge_cache(self):
        """
        Clear the edge cache to None for all values
        :return:
        """
        self._edge_cache["x_start"]       = None,
        self._edge_cache["y_start"]       = None,
        self._edge_cache["x_end"]         = None,
        self._edge_cache["y_end"]         = None,
        self._edge_cache["item_start"]    = None,
        self._edge_cache["item_end"]      = None,
        self._edge_cache["edge"]          = None


    def _get_current_item(self, coords):
        """
        Return the item(if any) that the mouse is currently over
        :param coords:                  The current coordinates of the mouse
        :return:
        """
        Debug.printi("X:"+ str(self._cache["x"]) + " Y:" + str(self._cache["y"]), Debug.Level.INFO)
        item =  self._canvas.find_overlapping(coords[0],coords[1], coords[0], coords[1])
        if item is ():
            return None
        return item[0]

    def _node_operation(self, coords):
        """
        Contextually create or edit a node
        :param coords:
        :return:
        """
        # Determine if they are double click on the canvas, or on a node
        item = self._get_current_item(coords)
        self._cache["item"] = item
        if item is not None and item in self._node_listing:
            # Make request from object manager using the tag assigned
            NodeDialog(self, self._cache["event"].x_root+50, self._cache["event"].y_root+50)
            # post information to object manager, or let the dialog handle it, or whatever
            return
        # if its the canvas, plot a new node and show the editing dialog
        self._cache["item"] = self._canvas.create_rectangle(coords[0], coords[1], coords[0]+25, coords[1]+25,
                                outline="red", fill="black", activeoutline="black", activefill="red")
        # TODO: flesh out the information that is stored here
        self._node_listing[self._cache["item"]] = self._cache["item"]
        # then open the dialog
        NodeDialog(self, self._cache["event"].x_root+50, self._cache["event"].y_root+50)

    def delete_all(self):
        """
        Delete all nodes and associated edges and objects from the canvas
        """
        # Iterate over each node in the node listing and delete it using delete node
        pass

    def delete_node(self, node_id):
        """
        Delete a node and all its associated edges and object from the canvas

        :param node_id:             The tkinter id of the node to be deleted
        """
        # Delete from our internal representations
        # Delete from the canvas
        # Iterate through the edge bindings and delete all of those
        # Inform the object manager that a node as been deleted
        pass


class EdgeBind():

    def __init__(self, dict):
        self.x_start = dict["x_start"]
        self.y_start = dict["y_start"]
        self.x_end = dict["x_end"]
        self.y_end = dict["y_end"]
        self.item_start = dict["item_start"]
        self.item_end = dict["item_end"]
        self.edge = dict["edge"]        # Use the tkinter canvas id as the specifier