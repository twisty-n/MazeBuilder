from DataValidator import DataValidator
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
from Enumerations import Input_Event, EditableObject, ControlSpecifier, ExecutionStage
from DataStore import DataStore
from Control import load_controls
import Containers


# Enumerations and Functions



# Classes

class MazePlannerCanvas(Frame):
    """
    MazePlannerCanvas contains the main frontend workhorse functionality of the entire
    application.
    it allows the user to graphically place nodes and define the edges between them
    """
    def __init__(self, parent, status=None, manager=DataStore()):
        """
        Contstruct an instance of the MazePlannerCanvas

        :param parent:              The parent widget that the mazePlannerCanvas will sit in
        :param status:              The statusbar that will receive mouse updates
        :type manager: DataStore
        :return:
        """
        Frame.__init__(self, parent)
        self._manager = manager
        self._canvas = Canvas(self, bg="grey", cursor="tcross")
        self._canvas.pack(fill=BOTH, expand=1)
        self._commands = {
            (ControlSpecifier.DRAG_NODE,    ExecutionStage.START)       : self._begin_node_drag,
            (ControlSpecifier.CREATE_EDGE,  ExecutionStage.START)       : self._begin_edge,
            (ControlSpecifier.DRAG_NODE,    ExecutionStage.END)         : self._end_node_drag,
            (ControlSpecifier.CREATE_EDGE,  ExecutionStage.END)         : self._end_edge,
            (ControlSpecifier.DRAG_NODE,    ExecutionStage.EXECUTE)     : self._execute_drag,
            (ControlSpecifier.CREATE_EDGE,  ExecutionStage.EXECUTE)     : self._execute_edge,
            (ControlSpecifier.MENU,         ExecutionStage.EXECUTE)     : self._launch_menu,
            (ControlSpecifier.CREATE_NODE,  ExecutionStage.EXECUTE)     : self.create_new_node,
        }
        self._commands = load_controls(self._commands)
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
        self._canvas.bind("<B1-Motion>", lambda event, m_event=Input_Event.DRAG_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<B2-Motion>", lambda event, m_event=Input_Event.DRAG_M2: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<B3-Motion>", lambda event, m_event=Input_Event.DRAG_M3: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonPress-2>", lambda event, m_event=Input_Event.CLICK_M2: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonRelease-2>", lambda event, m_event=Input_Event.RELEASE_M2: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonPress-1>", lambda event, m_event=Input_Event.CLICK_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonPress-3>", lambda event, m_event=Input_Event.CLICK_M3: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonRelease-1>", lambda event, m_event=Input_Event.RELEASE_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<ButtonRelease-3>", lambda event, m_event=Input_Event.RELEASE_M3: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<Return>", lambda event, m_event=Input_Event.RETURN: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<Double-Button-1>", lambda event, m_event=Input_Event.D_CLICK_M1: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<Double-Button-2>", lambda event, m_event=Input_Event.D_CLICK_M2: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<Double-Button-3>", lambda event, m_event=Input_Event.D_CLICK_M3: self._handle_mouse_events(m_event, event))
        self._canvas.bind("<Motion>", lambda event, m_event=None : self._handle_mot(m_event, event))
        self._canvas.bind("<Enter>", lambda event: self._canvas.focus_set())
        self._canvas.bind("<space>", lambda event, m_event=Input_Event.SPACE: self._handle_mouse_events(m_event, event))

    def _handle_mot(self, m_event, event):
        """
        Callback function to handle movement of the mouse

        Function updates the mouse location status bar as well as setting cache values to the current location
        of the mouse

        :m_event:           The specifier for the type of event that has been generated
        :event:             The tk provided event object
        """
        self._status.set_text("Mouse X:" + str(event.x) + "\tMouse Y:" + str(event.y))
        item = self._get_current_item((event.x, event.y))
        if self._is_node(item):
            Debug.printi("Node: " + str(item), Debug.Level.INFO)
        if self._is_edge(item):
            Debug.printi("Edge: " + str(item) + " | Source: " + str(self._edge_bindings[item].item_start)+ " | Target: " + str(self._edge_bindings[item].item_end)+ " | Length: ")
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
        try:
            self._commands[m_event]((event.x, event.y))
        except KeyError:
            Debug.printi("Warning, no control mapped to " + m_event, Debug.Level.ERROR)
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
        if self._cache["item"] is None:
            return

        # Obtain the final points
        x = coords[0]
        y = coords[1]
        item = self._cache["item"]
        self._validate_node_position(coords)

        container = self._manager.request(DataStore.DATATYPE.NODE, item)
        container.x_coordinate = x
        container.y_coordinate = y
        self._manager.inform(DataStore.EVENT.NODE_EDIT, container.empty_container(), self._cache["item"])
        Debug.printi("Node " + str(self._cache["item"]) + " has been moved", Debug.Level.INFO)
        # Clean the cache
        self._clear_cache(coords)

    def _validate_node_position(self, coords):
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
        pass

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
        self._update_attached_objects(self._cache["item"], coords)

    def _update_attached_objects(self, item, coords):
        if item not in self._object_listing:
            return
        container = self._manager.request(DataStore.DATATYPE.OBJECT, item)
        container.x_coordinate = coords[0]
        container.y_coordinate = coords[1]
        self._manager.inform(DataStore.EVENT.OBJECT_EDIT, container.empty_container(), item)

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
            old_edge = binding.edge
            binding.edge = self._canvas.create_line(coords[0], coords[1], binding.x_end,
                                                    binding.y_end, tags="edge", activefill="RoyalBlue1", tag="edge")
            self._edge_bindings[binding.edge] = binding
            self._manager.update_key(DataStore.EVENT.EDGE_EDIT, binding.edge, old_edge)
            binding.x_start = coords[0]
            binding.y_start = coords[1]

        # Adjust the bindings with this node as the ending edge
        for binding in end_bindings:
            self._canvas.delete(binding.edge)
            del self._edge_bindings[binding.edge]
            old_edge = binding.edge
            binding.edge = self._canvas.create_line(binding.x_start, binding.y_start,
                                                    coords[0], coords[1], tags="edge", activefill="RoyalBlue1", tag="edge")
            self._edge_bindings[binding.edge] = binding
            self._manager.update_key(DataStore.EVENT.EDGE_EDIT, binding.edge, old_edge)
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

        if item is None:
            # No node is currently selected, create the general menu
            p_menu.add_command(label="Place Node", command=lambda: self.create_new_node((self._cache["x"], self._cache["y"])))
            p_menu.add_command(label="Delete All", command=lambda: self.delete_all())
            p_menu.tk_popup(updated_coords[0], updated_coords[1])
            return

        if self._is_node(item):
            # Create the node specific menu
            p_menu.add_command(label="Place Object", command=lambda: self._mark_object((self._cache["x"], self._cache["y"])))
            p_menu.add_command(label="Edit Node", command=lambda: self._selection_operation((self._cache["x"], self._cache["y"])))
            p_menu.add_command(label="Delete Node", command=lambda: self.delete_node(self._get_current_item((self._cache["x"], self._cache["y"]))))
            p_menu.add_command(label="Mark as start", command=lambda: self._mark_start_node(self._get_current_item((self._cache["x"], self._cache["y"]))))

            if self._is_object(item):
                # Launch the node menu as well as an an added option for selecting stuff to edit an object
                p_menu.add_command(label="Edit Object", command=lambda: self._edit_object(coords))
                p_menu.add_command(label="Delete Object", command=lambda: self._delete_object(self._get_current_item((self._cache["x"], self._cache["y"]))))
                p_menu.delete(0)
            p_menu.tk_popup(updated_coords[0], updated_coords[1])
            return

        if self._is_edge(item):
            p_menu.add_command(label="Edit Edge", command=lambda: self._selection_operation((self._cache["x"], self._cache["y"])))
            p_menu.add_command(label="Delete Edge", command=lambda: self.delete_edge(self._get_current_item((self._cache["x"], self._cache["y"]))))
            p_menu.tk_popup(updated_coords[0], updated_coords[1])
            return

        self._clear_cache(coords)

    def _edit_object(self, coords):

        """
        Awkward moment when you find a threading related bug in the Tkinter library, caused by some
        Tcl issue or something like that.
        The below line must be left commented out otherwise the window_wait call in the dialog will crash
        out with a Tcl ponter based issue :/
        item = self._get_current_item((self._cache["x"], self._cache["y"]))
        This means that we can only use the mouse to edit objects
        """

        item = self._get_current_item(coords)

        if item not in self._object_listing:
            Debug.printi("Not a valid object to edit", Debug.Level.ERROR)
            return
        obj = ObjectDialog(self, coords[0] + 10, coords[1] + 10, populator=self._manager.request(DataStore.DATATYPE.OBJECT, item))
        Debug.printi("Editing object " + str(item), Debug.Level.INFO)
        self._manager.inform(DataStore.EVENT.OBJECT_EDIT, obj._entries, item)
        Debug.printi("Editing object " + str(item), Debug.Level.INFO)

    def _delete_object(self, item):
        if item not in self._object_listing:
            Debug.printi("Object does not exist to delete", Debug.Level.ERROR)
            return
        del self._object_listing[item]
        self._manager.inform(DataStore.EVENT.OBJECT_DELETE, data_id=item)
        self._canvas.itemconfig(item, outline="red", fill="black", activeoutline="black", activefill="red")

    def _mark_object(self, coords, prog=False, data=None):
        """
        Mark a node as containing an object
        :param coords:
        :return:
        """
        # Retrieve the item
        item = self._get_current_item(coords)

        if not prog:
            if item not in self._node_listing:
                Debug.printi("Invalid object placement selection", Debug.Level.ERROR)
                return

            if item in self._object_listing:
                Debug.printi("This room already has an object in it", Debug.Level.ERROR)
                return
            # Retrieve its coordinates
            # Launch the object maker dialog
            obj = ObjectDialog(self, coords[0] + 10, coords[1] + 10, populator=Containers.ObjectContainer(key_val={
                "x_coordinate"  :   coords[0],
                "y_coordinate"  :   coords[1],
                "name"          :   None,
                "mesh"          :   None,
                "scale"         :   None
            }))
            entries = obj._entries
        else:
            entries = {
                "x_coordinate": coords[0],
                "y_coordinate": coords[1],
                "name": data["name"],
                "mesh": data["mesh"],
                "scale": data["scale"]
            }
        # Save informatoin to the manager
        self._manager.inform(DataStore.EVENT.OBJECT_CREATE, entries, item)
        self._object_listing[item] = item
        self._canvas.itemconfig(item, fill="blue")
        Debug.printi("Object created in room " + str(item), Debug.Level.INFO)

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

    def _end_edge(self, coords, prog=False, data=None):
        """
        Perform the operations required to complete an edge creation operation
        :param coords:
        :return:
        """
        # Check if the cursor is over a node, if so continue, else abort
        curr = self._get_current_item((coords[0], coords[1]))
        if not prog:
            if curr is None or not self._valid_edge_cache() or curr not in self._node_listing:
                # Abort the edge creation process
                self._canvas.delete(self._edge_cache["edge"])
                self._clear_edge_cache()
                return

            # Check if this edge already exists in the program
            if self._check_duplicate_edges(self._edge_cache["item_start"], curr):
                self.delete_edge(self._edge_cache["edge"])
                Debug.printi("Multiple edges between rooms not permitted", Debug.Level.ERROR)
                return

        self._canvas.tag_lower("edge")
        self._edge_cache["item_end"] = curr

        # Note that we use the edge ID as the key
        self._edge_bindings[self._edge_cache["edge"]] = EdgeBind(self._edge_cache)
        self._edge_bindings[self._edge_cache["edge"]].x_end = coords[0]
        self._edge_bindings[self._edge_cache["edge"]].y_end = coords[1]
        # Inform the manager
        if not prog:
            self._manager.inform(
                DataStore.EVENT.EDGE_CREATE,
                    {
                        "source"    :   self._edge_cache["item_start"],
                        "target"    :   self._edge_cache["item_end"],
                        "height"    :   None,
                        "wall1"     :   None,
                        "wall2"     :   None,
                    },
                self._edge_cache["edge"])
        else:
            # We are programmatically adding the edges in
            self._manager.inform(
                DataStore.EVENT.EDGE_CREATE,
                {
                    "source": self._edge_cache["item_start"],
                    "target": self._edge_cache["item_end"],
                    "height": None,
                    "wall1": None,  # Todo: specify
                    "wall2": None, # Todo: specfiy
                },
                self._edge_cache["edge"])

        Debug.printi("Edge created between rooms "
                     + str(self._edge_cache["item_start"])
                     + " and "
                     + str(self._edge_cache["item_end"])
                     , Debug.Level.INFO)
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
            coords[0]-1, coords[1]-1, tags="edge", activefill="RoyalBlue1", tag="edge")

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
            populator = self._manager.request(DataStore.DATATYPE.NODE, item)
            updated_node = NodeDialog(self, true_coords[0] + 10, true_coords[1] + 10, populator=populator)
            # post information to object manager, or let the dialog handle it, or whatever
            self._manager.inform(DataStore.EVENT.NODE_EDIT, updated_node._entries, item)
            return

        if self._is_edge(item):
            Debug.printi("Edge Selected : " + str(item) + " | Launching Editor", Debug.Level.INFO)
            # Make a request from the object manager to populate the dialog
            populator = self._manager.request(DataStore.DATATYPE.EDGE, item)
            updated_edge = EdgeDialog(self, true_coords[0] + 10, true_coords[1] + 10, populator=populator)
            # Make sure that information is posted to the object manager
            self._manager.inform(DataStore.EVENT.EDGE_EDIT, updated_edge._entries, item)

            return

        if self._is_object(item):
            self._edit_object(coords)
            return

    def create_new_node(self, coords, prog = False, data=None):
        """
        Creates a new node on the Canvas and adds it to the datastore
        :param coords:
        :return:
        """
        # Create the node on Canvas
        self._cache["item"] = self._canvas.create_rectangle(coords[0], coords[1], coords[0]+25, coords[1]+25,
                                                            outline="red", fill="black", activeoutline="black", activefill="red", tag="node")

        self._node_listing[self._cache["item"]] = self._cache["item"]

        # then open the dialog
        if not prog:
            true_coords = self._canvas_to_screen((self._cache["x"], self._cache["y"]))
            new_node = NodeDialog(self, true_coords[0] + 25, true_coords[1] + 25,
                              populator=Containers.NodeContainer(
                                  {
                                      "node_id": self._cache["item"],
                                      "x_coordinate": self._cache["x"],
                                      "y_coordinate": self._cache["y"],
                                      "room_texture": None,
                                      "wall_pictures": None
                                  }))
            entries = new_node._entries
        else:
            entries = {
                "node_id": data["id"],
                "x_coordinate": data["x"],
                "y_coordinate": data["y"],
                "room_texture": data["texture"],
                "wall_pictures": {} # TODO: define
            }
        # Inform the datastore
        self._manager.inform(DataStore.EVENT.NODE_CREATE, entries, self._cache["item"])
        self._clear_cache(coords)

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
        self._manager.inform(DataStore.EVENT.DELETE_ALL)

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
        if node_id in self._object_listing:
            self._delete_object(node_id)
        self._manager.inform(DataStore.EVENT.NODE_DELETE, data_id=node_id)

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
            # Terrible I know, but I dont have the time to find the root cause
            pass
        # Delete the edge from the canvas
        self._canvas.delete(edge_id)
        # Inform the object manager that an edge has been deleted
        self._manager.inform(DataStore.EVENT.EDGE_DELETE, data_id=edge_id)

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
        environment_container = self._manager.request(DataStore.DATATYPE.ENVIRONMENT)
        environment_container.start_node = node_id
        self._manager.inform(DataStore.EVENT.ENVIRONMENT_EDIT, environment_container)


class EdgeBind():
    """
    Class that holds all of the informaiton needed to deal with edges between nodes
    """
    def __init__(self, dict):
        self.x_start = dict["x_start"]
        self.y_start = dict["y_start"]
        self.x_end = dict["x_end"]
        self.y_end = dict["y_end"]
        self.item_start = dict["item_start"]
        self.item_end = dict["item_end"]
        self.edge = dict["edge"]        # Use the tkinter canvas id as the specifier