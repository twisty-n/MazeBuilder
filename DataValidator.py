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
        result = True
        message = ""
        if len(data["wall1"]["textures"]) < 1 or len(data["wall2"]["textures"]) < 1:
            result = False
            message = "Walls must have at least 1 texture. Please input a texture for each wall\n"
        if data["wall1"]["height"] is "" or data["wall2"]["height"] is "":
            result = False
            message = "You must specify a height for each wall"

        return result, message

    def _validate_object(data):
        # object must have a name
        # the name must be individual --> this should be checked as part of tghe export check
        result = True
        message = ""
        if data["name"] is "":
            result = False
            message = "The object must be given a unique name\n"
        if data["mesh"] is "":
            result = False
            message = "You must select a mesh to use for the object"

        return result, message

    VALIDATE_MAP = {
        Event.ENVIRONMENT_EDIT  : _validate_environment,
        Event.VR_EDIT           : _validate_vr,
        Event.NODE_EDIT         : _validate_node,
        Event.EDGE_EDIT         : _validate_edge,
        Event.OBJECT_EDIT       : _validate_object,
        Event.NODE_CREATE       : _validate_node,
        Event.EDGE_CREATE       : lambda data: (True, ""),
        Event.OBJECT_CREATE     : _validate_object
    }

