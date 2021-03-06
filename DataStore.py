from DataValidator import DataValidator

__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: DataStore.py

# Note that we are using 42 as the magic number that represents EVERYTHING
"""

# Imports
from Containers import Container, EnvironmentContainer, VRContainer
import Debug
from Exceptions import InvalidDataException
from Enumerations import Event, EditableObject, DESCRIPTOR_MAP, OBJECT_MAP
from ObserverPattern import Subject

# Classes

MAGIC_NUM = "42"

class DataStore(Subject):

    EVENT = Event
    DATATYPE = EditableObject

    def __init__(self):
        self._cache = {
            "EVENT" : None,
            "ID"    : None,
            "DATA"  : None
        }
        self._node_store = {}                               # Will hold hashmap of Containers
        self._edge_store = {}                               # Will hold hashmap of Containers
        self._object_store = {}                             # Will hold hashmap of Containers
        self._environment_store = {
            MAGIC_NUM  :   EnvironmentContainer()
        }                        # Will hold the raw container
        self._vr_store = {
            MAGIC_NUM  :   VRContainer()
        }                                 # Will hold the raw container
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
        self._descriptor_map = DESCRIPTOR_MAP
        self._validator = DataValidator()
        Subject.__init__(self)

    def export_finalize(self):
        """
        Finalizes the contents of the data store to be ready to be exported
        :return:
        """
        return self._validator.export_validation({
            "node_store"        : self._node_store,
            "edge_store"        : self._edge_store,
            "object_store"      : self._object_store,
            "environment_store" : self._environment_store[MAGIC_NUM].empty_container(),
            "vr_config_store"   : self._vr_store[MAGIC_NUM].empty_container()
        })

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
        return DataValidator.validate(event, data)[0]

    def inform(self, event, data=None, data_id=MAGIC_NUM):
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
                self._update_cache(event, data_id, self.request(OBJECT_MAP[event], data_id).empty_container())
                del self._dispatch[event][data_id]
                self.update_state()
                return
            except KeyError:
                error_msg = "Deletion of data item failed, "
                "key not in datastore. Key:" + str(data_id) + " Event:" + event
                Debug.printi(error_msg, Debug.Level.ERROR)

        if event == Event.DELETE_ALL:
            self._delete_all_vals()
            return

        if (event != Event.VR_EDIT and event != Event.ENVIRONMENT_EDIT) and data_id == MAGIC_NUM:
            return

        # To expand functionality we will first perform some type evaluations to make
        # certain that the type that we are using is correct
        if isinstance(data, Container):
            # if the data is a container type, extract the dict to use
            data = data.empty_container()

        # Else, its a creation or an edit, first validate
        if self.attempt_validation(event, data) is False:
            raise InvalidDataException(event, data)

        self._dispatch[event][data_id] = Container.manufacture_container(self._descriptor_map[event], data)
        self._update_cache(event, data_id, data)
        self.update_state()


    def _update_cache(self, event, data_id, data):
        self._cache["EVENT"]    = event
        self._cache["ID"]       = data_id
        self._cache["DATA"]     = data

    def request(self, datatype, data_id=MAGIC_NUM):
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
        try:
            return self._heap_map[datatype][data_id]
        except KeyError:
            Debug.printi("Data not in the datastore DataType:" + datatype + " Data ID: " + str(data_id), Debug.Level.ERROR)

    def _delete_all_vals(self):
        self._edge_store.clear()
        self._object_store.clear()
        self._node_store.clear()
        self._update_cache(Event.DELETE_ALL, None, None)
        self.update_state()


    def update_key(self, event, new_key, old_key):
        """
        Update the ID of an edge binding

        The event that is provided must be an EDGE_EDIT
        :param event:       The event that the data is bound to
        :param new_key:     The new key to be given to the edge data
        :param old_key:     The old key that is associated with that edge data
        :return:
        """
        if event is not self.EVENT.EDGE_EDIT:
            return
        self._edge_store[new_key] = self._edge_store.pop(old_key)

    def request_data(self, type, id):
        return self.request(type, id)