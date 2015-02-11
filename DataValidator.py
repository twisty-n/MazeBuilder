__author__ = 'tristan_dev'

from Enumerations import Event
import Debug

DEBUG = False

class DataValidator:

    def __init__(self):
        pass

    @staticmethod
    def validate(event, data):

        if DEBUG:
            return True, ""
        try:
            return DataValidator().VALIDATE_MAP[event](data)
        except KeyError as error:
            Debug.printi(error.message, Debug.Level.FATAL)

    def export_validation(self, databank):

        # Don't bother validateing while im debugging
        if DEBUG:
            return True, ""

        messages = ""
        valid = True

        if  databank["vr_config_store"]["minimum_dist_to_wall"] is not None and  \
            databank["environment_store"]["edge_width"] is not None:
            if 2*int(databank["vr_config_store"]["minimum_dist_to_wall"]) >= \
                int(databank["environment_store"]["edge_width"]):
                valid = False
                messages += "2 x Minimum Distance to Wall MUST be lower then the specified edge width\n"
        # Check that all of the stuff has been filled in for the VRConfig and the environment
        for key, item in databank["environment_store"].iteritems():
            if item is None:
                valid = False
                messages += "You must provide a value for " + str(key) + "\n"
        for key, item in databank["vr_config_store"].iteritems():
            if item is None:
                valid = False
                messages += "You must provide a value for " + str(key) + "\n"

        if databank["environment_store"]["start_node"] not in databank["node_store"].keys():
            valid = False
            messages += "The starting node selected is invalid, please select a new starting node\n"

        for key, edge in databank["edge_store"].iteritems():
            if edge.wall1 == {} or edge.wall1 == None \
                or edge.wall2 == {} or edge.wall2 == None:
                valid = False
                messages += "Wall textures must be defined for each corridor\n"
                break

        return valid, messages

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
            messages += "Room Texture must be defined\n"
        return result, messages

    def _validate_edge(data):
        result = True
        message = ""
        if len(data["wall1"]["textures"]) < 1 or len(data["wall2"]["textures"]) < 1:
            result = False
            message += "Walls must have at least 1 texture. Please input a texture for each wall\n"
        if data["wall1"]["height"] is "" or data["wall2"]["height"] is "":
            result = False
            message += "You must specify a height for each wall"

        return result, message

    def _validate_object(data):
        # object must have a name
        # the name must be individual --> this should be checked as part of tghe export check
        result = True
        message = ""
        if data["name"] is "":
            result = False
            message += "The object must be given a unique name\n"
        if data["mesh"] is "":
            result = False
            message += "You must select a mesh to use for the object"

        return result, message

    VALIDATE_MAP = {
        Event.ENVIRONMENT_EDIT  : _validate_environment,
        Event.VR_EDIT           : _validate_vr,
        Event.NODE_EDIT         : _validate_node,
        Event.EDGE_EDIT         : _validate_edge,
        Event.OBJECT_EDIT       : _validate_object,
        Event.NODE_CREATE       : _validate_node,
        # HaX0R ergh
        Event.EDGE_CREATE       : lambda data: (True, ""),
        Event.OBJECT_CREATE     : _validate_object
    }

