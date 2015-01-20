import Debug

__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: MazeCanvas.py


Module contains the implementation
"""

# Imports
from Tkinter import Canvas, Frame, BOTH, Menu
from DiaDoges import NodeDialog, EdgeDialog, ObjectDialog
from EditableObject import EditableObject


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
    SPACE           = "SPACE"

# Classes

class MazePlannerCanvas(Frame):
    """
    The main workhorse fot the GUI
    """
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
            Event.D_CLICK_M1    : self._selection_operation,
            Event.SPACE         : self._launch_menu
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
        self._object_listing = {}
        self._curr_start = None
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
        self._canvas.bind("<space>", lambda event, m_event=Event.SPACE: self._handle_mouse_events(m_event, event))

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
        # Abort drag if the item is not a node
        if self._cache["item"] not in self._node_listing:
            return
        # Update the drawing information
        delta_x = coords[0] - self._cache["x"]
        delta_y = coords[1] - self._cache["y"]

        # move the object the appropriate amount as long as the drag event has not been done on the empty canvas
        if not self._cache["item"] is None:
            self._canvas.move(self._cache["item"], delta_x, delta_y)

        # record the new position
        self._cache["x"] = coords[0]
        self._cache["y"] = coords[1]

        self._update_attached_edges(self._cache["item"], coords)

    def _update_attached_edges(self, node, coords):
        """
        Updates all associated edges related to a node drag event

        :param node:            The node that has been dragged
        :param coords:          The mouse coordinates which are the new coordinates of the node
        """
        # Go through dictionary and gather list of all attached edge bindings for a node
        start_bindings = []
        for key, binding in self._edge_bindings.iteritems():
            if binding.item_start == node:
                start_bindings.append(binding)

        end_bindings = []
        for key, binding in self._edge_bindings.iteritems():
            if binding.item_end == node:
                end_bindings.append(binding)

        #  Adjust the bindings with this node as the starting edge
        for binding in start_bindings:
            self._canvas.delete(binding.edge)
            del self._edge_bindings[binding.edge]
            binding.edge = self._canvas.create_line(coords[0], coords[1], binding.x_end,
                                                    binding.y_end, tags="edge", activefill="RoyalBlue1", tag="edge")
            self._edge_bindings[binding.edge] = binding
            binding.x_start = coords[0]
            binding.y_start = coords[1]

        # Adjust the bindings with this node as the ending edge
        for binding in end_bindings:
            self._canvas.delete(binding.edge)
            del self._edge_bindings[binding.edge]
            binding.edge = self._canvas.create_line(binding.x_start, binding.y_start,
                                                    coords[0], coords[1], tags="edge", activefill="RoyalBlue1", tag="edge")
            self._edge_bindings[binding.edge] = binding
            binding.x_end = coords[0]
            binding.y_end = coords[1]

        # Remember to adjust all of the edges so that they sit under the node images
        self._canvas.tag_lower("edge")

    def _launch_menu(self, coords):
        """
        Callback function in response to the pressing of the Return key

        Launches a context menu based on the location of the mouse
        :param coords:
        :return:
        """
        # Configure the "static" menu entries -- they can't be static without seriously destroying readability
        # due to the Python version that is being used -.- so now it has to be not optimal until I find a better
        # solution
        p_menu = Menu(self._canvas)
        item = self._get_current_item((self._cache["x"], self._cache["y"]))
        updated_coords = self._canvas_to_screen((self._cache["x"], self._cache["y"]))

        # TODO: when specifiying that an object be added to a node, make it so that the node as a stipple pattern

        if item is None:
            # No node is currently selected, create the general menu
            p_menu.add_command(label="Place Node", command=lambda: self._selection_operation((self._cache["x"], self._cache["y"])))
            p_menu.add_command(label="Delete All", command=lambda: self.delete_all())
            p_menu.tk_popup(updated_coords[0], updated_coords[1])
            return

        if self._is_node(item):
            # Create the node specific menu
            p_menu.add_command(label="Place Object", command=lambda: Debug.printi("Place object", Debug.Level.INFO))
            p_menu.add_command(label="Edit Node", command=lambda: self._selection_operation((self._cache["x"], self._cache["y"])))
            p_menu.add_command(label="Delete Node", command=lambda: self.delete_node(self._get_current_item((self._cache["x"], self._cache["y"]))))
            p_menu.add_command(label="Mark as start", command=lambda: self._mark_start_node(self._get_current_item((self._cache["x"], self._cache["y"]))))
            p_menu.tk_popup(updated_coords[0], updated_coords[1])
            return

        if self._is_edge(item):
            p_menu.add_command(label="Edit Edge", command=lambda: self._selection_operation((self._cache["x"], self._cache["y"])))
            p_menu.add_command(label="Delete Edge", command=lambda: self.delete_edge(self._get_current_item((self._cache["x"], self._cache["y"]))))
            p_menu.tk_popup(updated_coords[0], updated_coords[1])
            return

        if self._is_object(item):
            # Todo, define
            pass


    def _valid_edge_cache(self):
        """
        Return true if the edge cache contains a valid edge descriptor

        A valid edge descriptor is when the edge has a valid starting node, if the
        edge does not contain a valid starting node, this means that the edge was not
        created in the proper manner and should thus be ignored by any edge operations
        """
        valid = not self._edge_cache["item_start"] == (None,)
        return valid

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

        # Abort the operation if the item was not a valid node to be selecting
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
        # Check if the cursor is over a node, if so continue, else abort
        curr = self._get_current_item((coords[0], coords[1]))
        if curr is None or not self._valid_edge_cache() or curr not in self._node_listing:
            # Abort the edge creation process
            self._canvas.delete(self._edge_cache["edge"])
            self._clear_edge_cache()
            return

        # Check if this edge already exists in the program
        if self._check_duplicate_edges(self._edge_cache["item_start"], curr):
            self.delete_edge(self._edge_cache["edge"])
            return

        # Post the edge information to the object manager
        # Clear the current edge from the edge drawing cache
        # Need to use the coord values as the cache values aren't updated during a drag apparently
        self._canvas.tag_lower("edge")
        self._edge_cache["x_end"] = coords[0]
        self._edge_cache["y_end"] = coords[1]
        self._edge_cache["item_end"] = curr
        self._edge_bindings[self._edge_cache["edge"]] = EdgeBind(self._edge_cache)  #Note that we use the edge ID as the key
        self._clear_edge_cache()
        self._clear_cache(coords)

    def _check_duplicate_edges(self, start_node, end_node):
        for binding in self._edge_bindings.itervalues():
            if ( start_node == binding.item_start and end_node == binding.item_end )\
            or ( start_node == binding.item_end and end_node == binding.item_start):
                return True
        return False

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
            coords[0]-1, coords[1]-1, tags="edge", activefill = "RoyalBlue1", tag="edge")

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
        Debug.printi("X:" + str(self._cache["x"]) + " Y:" + str(self._cache["y"]), Debug.Level.INFO)
        item = self._canvas.find_overlapping(coords[0]-1, coords[1]-1, coords[0]+1, coords[1]+1)

        if item is ():
            return None

        # Hacky solution for now TODO make it better!
        # Return the first node that we come across, since they seem to be returned by tkinter
        # in reverse order to their visual positioning, we'll go through the list backwards
        for val in item[::-1]:
            if val in self._node_listing:
                return val

        # Else, just return the first item and be done with it
        return item[0]

    def _is_node(self, obj):
        """
        Returns true if the supplied object is a node
        :param obj:             The object id to id
        :return:
        """
        return obj in self._node_listing

    def _is_edge(self, obj):
        """
        Returns true if the supplied object is an edge

        :param obj:             The object id to id
        :return:
        """
        return obj in self._edge_bindings

    def _is_object(self, obj):
        """
        Returns true if the supplied object is an object

        :param obj:             The object id to id
        :return:
        """
        return obj in self._object_listing

    def _get_obj_type(self, obj):
        """
        Returns the Object type of the supplied object

        :param obj:             The object to identify
        :return:
        """
        if self._is_node(obj):
            return EditableObject.NODE
        if self._is_edge(obj):
            return EditableObject.EDGE
        if self._is_object(obj):
            return EditableObject.OBJECT
        return None

    def _selection_operation(self, coords):
        """
        Contextually create or edit a node
        :param coords:
        :return:
        """
        # Determine the item ID
        item = self._get_current_item(coords)
        self._cache["item"] = item
        true_coords = self._canvas_to_screen((self._cache["x"], self._cache["y"]))

        if self._is_node(item):
            Debug.printi("Node Selected : " + str(item) + " | Launching Editor", Debug.Level.INFO)
            # Make request from object manager using the tag assigned
            NodeDialog(self, true_coords[0] + 10, true_coords[1] + 10)
            # post information to object manager, or let the dialog handle it, or whatever
            return

        if self._is_edge(item):
            Debug.printi("Edge Selected : " + str(item) + " | Launching Editor", Debug.Level.INFO)
            # Make a request from the object manager to populate the dialog
            EdgeDialog(self, true_coords[0] + 10, true_coords[1] + 10)
            # Make sure that information is posted to the object manager
            return

        if self._is_object(item):
            Debug.printi("Object Selected : " + str(item) + " | Launching Editor", Debug.Level.INFO)
            # Make a request from the object manager to populate the dialog
            ObjectDialog(self, true_coords[0] + 10, true_coords[1] + 10)
            # Make sure that information is posted to the object manager
            return

        # its the canvas, plot a new node and show the editing dialog
        self._cache["item"] = self._canvas.create_rectangle(coords[0], coords[1], coords[0]+25, coords[1]+25,
                                outline="red", fill="black", activeoutline="black", activefill="red", tag="node")

        self._node_listing[self._cache["item"]] = self._cache["item"]

        # then open the dialog
        NodeDialog(self, true_coords[0]+25, true_coords[1]+25)

    def delete_all(self):
        """
        Delete all nodes and associated edges and objects from the canvas
        """
        # Iterate over each node in the node listing and delete it using delete node
        for key in self._node_listing.keys():
            self.delete_node(key)

        # Delete any rouge edge bindings that may exist
        for binding in self._edge_bindings:
            self.delete_edge(binding)

        # Delete any naughty objects that are left
        self._canvas.delete("all")

    def delete_node(self, node_id):
        """
        Delete a node and all its associated edges and object from the canvas

        :param node_id:             The tkinter id of the node to be deleted
        """
        # Delete from our internal representations
        if node_id not in self._node_listing:
            return

        del self._node_listing[node_id]
        # Delete from the canvas
        self._canvas.delete(node_id)

        # Iterate through the edge bindings and delete all of those
        for key in self._edge_bindings.keys():
            if self._edge_bindings[key].item_start == node_id or self._edge_bindings[key].item_end == node_id:
                self.delete_edge(key)
        # Inform the object manager that a node as been deleted
        pass

    def delete_edge(self, edge_id):
        """
        Delete the specified edge from the MazeCanvas

        :param edge_id:             The edge to be deleted
        :return:
        """
        # Go through the edge bindings and delete the appropriate edge
        try:
            # try to delete the edge binding if it exists
            del self._edge_bindings[edge_id]
        except KeyError:
            pass
        # Delete the edge from the canvas
        self._canvas.delete(edge_id)
        # Inform the object manager that an edge has been deleted
        pass

    def _mark_start_node(self, node_id):
        """
        Mark the passed in node as the starting node
        :param node_id:
        :return:
        """
        # Print the debug information
        # Mark as the new starting node on the canvas, first check that it is a node
        if node_id in self._node_listing:
            Debug.printi("Node:" + str(node_id) + " has been marked as the new starting node", Debug.Level.INFO)
            if self._curr_start is not None:
                # Return the old starting node to its normal colour
                self._canvas.itemconfig(self._curr_start, outline="red", fill="black", activeoutline="black", activefill="red")
            self._curr_start = node_id
            self._canvas.itemconfig(node_id, outline="black", fill="green", activeoutline="green", activefill="black")

        # Inform the object manager that there is a new starting node
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