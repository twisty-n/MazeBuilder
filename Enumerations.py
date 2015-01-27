__author__ = 'tristan_dev'

# Using "Enum" style contructs to give stuff more semantic meaning
class Event:

    NODE_CREATE         = "Node Creation"
    NODE_EDIT           = "Node Edit"
    NODE_DELETE         = "Node Delete"

    OBJECT_CREATE       = "Object Creation"
    OBJECT_EDIT         = "Object Edit"
    OBJECT_DELETE       = "Object Delete"

    EDGE_CREATE         = "Edge Create"
    EDGE_EDIT           = "Edge Edit"
    EDGE_DELETE         = "Edge Delete"

    ENVIRONMENT_EDIT    = "Environment Edit"
    VR_EDIT             = "VR Edit"

    DELETE_ALL          = "Delete All"

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

class ControlSpecifier:

    DRAG_NODE   = "DRAG_NODE"
    CREATE_NODE = "CREATE_NODE"
    CREATE_EDGE = "CREATE_EDGE"
    MENU        = "MENU"

class ExecutionStage:

    START   = "_START"           # Indicates the start of some user action
    EXECUTE = "_EXECUTE"         # Indicates that a user action is currently executing
    END     = "_END"             # Indicates the end of a user action