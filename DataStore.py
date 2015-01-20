__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: DataStore.py
"""

# Imports

import Containers
from EditableObject import EditableObject

# Enumerations and Functions

class Event:

    # Node Creation
    NODE_CREATE = "Node Creation"
    # Node Edit
    NODE_EDIT = "Node Edit"
    # Node Delete
    NODE_DELETE = "Node Delete"

    # Object creation
    OBJECT_CREATE = "Object Creation"
    # Object edit
    OBJECT_EDIT = "Object Edit"
    # Object deletion
    OBJECT_DELETE = "Object Delete"

    # Edge Creation
    EDGE_CREATE = "Edge Create"
    # Edge Edit
    EDGE_EDIT = "Edge Edit"
    # Edge Deletion
    EDGE_DELETE = "Edge Delete"

    # Environment Edit
    ENVIRONMENT_EDIT = "Environment Edit"
    # VR Edit
    VR_EDIT = "VR Edit"

# Classes

# TODO: Extend with Observer pattern extensions

class DataStore:

    def __init__(self):
        self._node_store = {}                   # Will hold hashmap of Containers
        self._edge_store = {}                   # Will hold hashmap of Containers
        self._object_store = {}                 # Will hold hashmap of Containers
        self._environment_store = None          # Will hold the raw container
        self._vr_store = None                   # Will hold the raw container
        self._dispatch = \
            {
                Event.NODE_CREATE       :   self._node_store,
                Event.NODE_EDIT         :   self._node_store,
                Event.NODE_DELETE       :   self._node_store,

                Event.EDGE_CREATE       :   self._edge_store,
                Event.EDGE_EDIT         :   self._edge_store,
                Event.EDGE_DELETE       :   self._edge_store,

                Event.OBJECT_CREATE     :   self._object_store,
                Event.OBJECT_DELETE     :   self._object_store,
                Event.OBJECT_EDIT       :   self._object_store,

                Event.ENVIRONMENT_EDIT  :   self._environment_store,
                Event.VR_EDIT           :   self._vr_store
            }

        self._heap_map = \
            {
                EditableObject.NODE     :   self._node_store,
                EditableObject.EDGE     :   self._edge_store,
                EditableObject.OBJECT   :   self._object_store,
                EditableObject.ENVIRONMENT  :   self._environment_store,
                EditableObject.VR_CONFIG    :   self._vr_store
            }
        self._validator = DataValidator()
        pass

    def attempt_validation(self, event, data):
        return self._validator.validate(event, data)

    def inform(self, event, data):
        pass

    def request(self, datatype, data_id):
        """
        Return a data container containing all of the available informaiton
        about the object with the provided ID

        If the data requested is of environment or VR_config type, then provide a
        data_id of None. For all of the other required datatypes, provided the valid data
        id. The data id's that are being used are the tkinter canvas ID's that are supplied

        :param datatype:        The datatype of information that has been requested
        :param data_id:         The id of the data
        :return:                A data container matching the corresponding datatype
        """
        if data_id is None:
            # Tpo return the environment or vr_config container
            return self._heap_map[datatype]

        return self._heap_map[datatype][data_id]


class DataValidator:

    def __init__(self):
        pass

    def validate(self, event, data):
        # TODO:  actual validation of the data
        return True