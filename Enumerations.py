__author__ = 'tristan_dev'


class Event:

    NODE_CREATE = "Node Creation"
    NODE_EDIT = "Node Edit"
    NODE_DELETE = "Node Delete"

    OBJECT_CREATE = "Object Creation"
    OBJECT_EDIT = "Object Edit"
    OBJECT_DELETE = "Object Delete"

    EDGE_CREATE = "Edge Create"
    EDGE_EDIT = "Edge Edit"
    EDGE_DELETE = "Edge Delete"

    ENVIRONMENT_EDIT = "Environment Edit"
    VR_EDIT = "VR Edit"

class Input_Event:
    """
    A stand in enumeration that encapsulates the different main events
    """
    CLICK_M1 = "CLICK_M1"
    CLICK_M2 = "CLICK_M2"
    CLICK_M3 = "CLICK_M3"
    D_CLICK_M1 = "D_CLICK_M1"
    D_CLICK_M2 = "D_CLICK_M2"
    D_CLICK_M3 = "D_CLICK_M3"
    DRAG_M1 = "DRAG_M1"
    DRAG_M2 = "DRAG_M2"
    DRAG_M3 = "DRAG_M3"
    RELEASE_M1 = "RELEASE_M1"
    RELEASE_M2 = "RELEASE_M2"
    RELEASE_M3 = "RELEASE_M3"
    RETURN = "RETURN"
    SPACE = "SPACE"

class ContainerDescriptor:
    ENVIRONMENT_CONTAINER = "Environment_Container"
    VR_CONTAINER = "VR_Container"
    NODE_CONTAINER = "Node_Container"
    OBJECT_CONTAINER = "Object_Container"
    EDGE_CONTAINER = "Edge_Container"
    WALL_CONTAINER = "Wall_Container"
    WALL_TEXTURE_CONTAINER = "Wall_Texture_Container"
    NODE_PICTURE_CONTAINER = "Node_Picture_Container"

class EditableObject:
    """
    An enumeration capturing the types of objects that can appear on the canvas
    """
    NODE                = "NODE"
    EDGE                = "EDGE"
    OBJECT              = "OBJECT"

    ENVIRONMENT         = "ENVIRONMENT"
    VR_CONFIG           = "VR_CONFIG"
=======
>>>>>>> 1d551f30ca7926ca356951ac63d25e107f1fd387
