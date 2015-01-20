__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: DataStore.py
"""

# Imports
from Containers import Container
import Debug
from Exceptions import InvalidDataException
from Enumerations import Event, EditableObject

# Classes

# TODO: Extend with Observer pattern extensions

class DataStore:

    EVENT = Event
    DATATYPE = EditableObject

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
        self._descriptor_map = \
            {
                Event.NODE_CREATE       : Container.DESCRIPTOR.NODE_CONTAINER,
                Event.NODE_EDIT         : Container.DESCRIPTOR.NODE_CONTAINER,
                Event.EDGE_CREATE       : Container.DESCRIPTOR.EDGE_CONTAINER,
                Event.EDGE_EDIT         : Container.DESCRIPTOR.EDGE_CONTAINER,
                Event.OBJECT_CREATE     : Container.DESCRIPTOR.OBJECT_CONTAINER,
                Event.OBJECT_DELETE     : Container.DESCRIPTOR.OBJECT_CONTAINER
            }
        self._validator = DataValidator()
        pass

    def attempt_validation(self, event, data):
        """
        Call before passing data to the datastore through inform

        If the validation fails, it will throw an exception. To prevent this
        first attempt to validate the data through the this method, or the
        data validator

        :param event:           The event corresponding to the data to validate
        :param data:            The data to evaluate
        :return:
        """
        return self._validator.validate(event, data)

    def inform(self, event, data=None, data_id=None):
        """
        Inform the DataStore that a new event has happen, and provide and event type and data binding

        This method invokes an event manager to update the details of the datastore based on events that
        are defined. It expects a VALID data dictionary that corresponds to the event that has been provided

        :param event:           The event that has occured
        :param data:            The valid data binding that is related to the event, in dictionary form
        :param data_id:         The id of the data element that is to be used for identification
        :return:
        """
        # If the event is an object deletion, try to perform it
        if event == Event.EDGE_DELETE   \
        or event == Event.NODE_DELETE   \
        or event == Event.OBJECT_DELETE:
            try:
                del self._dispatch[event][data_id]
            except KeyError:
                Debug.printi("Deletion of data item failed, "
                             "key not in datastore. Key:" + data_id + " Event:" + event, Debug.Level.ERROR)
                KeyError("Deletion of data item failed, "
                         "key not in datastore. Key:" + data_id + " Event:" + event)

        # Else, its a creation or an edit, first validate
        if self.attempt_validation(event, data) is False:
            raise InvalidDataException(event, data)

        # We overwrite the container in the case of an edit at this point
        # TODO: make it so that containers are updated in place
        if event == Event.ENVIRONMENT_EDIT or event == Event.VR_EDIT:
            # TODO: implement
            pass
        self._dispatch[event][data_id] = Container.manufacture_container(self._descriptor_map[event], data)

    def request(self, datatype, data_id=None):
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