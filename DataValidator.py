__author__ = 'tristan_dev'

from Enumerations import Event
import Debug


class DataValidator:

    def __init__(self):
        pass

    @staticmethod
    def validate(event, data):
        #return (True, "")
        try:
            return DataValidator().VALIDATE_MAP[event](data)
        except KeyError as error:
            Debug.printi(error.message, Debug.Level.FATAL)

    def _validate_environment(data):
        """
        Validate the environment configuration
        :param data:
        :return:    (result of validation, messages)
        """
        result = True
        messages = ""
        if data["sky_texture"] is None:
            result = False
            messages += "Sky texture must be defined\n"
        if data["floor_texture"] is None:
            result = False
            messages += "Floor texture must be defined\n"
        return result, messages

    def _validate_vr(data):
        return (True, "")

    def _validate_node(data):
        result = True
        messages = ""
        if data["room_texture"] is None:
            result = False
            messages = "Room Texture must be defined\n"
        return result, messages
    def _validate_edge(data):
        pass

    def _validate_object(data):
        pass

    VALIDATE_MAP = {
        Event.ENVIRONMENT_EDIT  : _validate_environment,
        Event.VR_EDIT           : _validate_vr,
        Event.NODE_EDIT         : _validate_node,
        Event.EDGE_EDIT         : _validate_edge,
        Event.OBJECT_EDIT       : _validate_object,
        Event.NODE_CREATE       : _validate_node,
        Event.EDGE_CREATE       : _validate_edge,
        Event.OBJECT_CREATE     : _validate_object
    }

