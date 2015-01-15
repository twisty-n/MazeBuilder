__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Containers.py

Module contains the data containers that will be passed around the application
"""

# Imports
from Exceptions import ContainerFillException

# Enumerations and Functions

class ContainerDescriptor:
    ENVIRONMENT_CONTAINER = "Environment_Container"


# Classes

class Container:
    def __init__(self, key_val=None):
        if key_val is not None:
            self.fill_container(key_val)

    def fill_container(self, key_val):
        """
        Fill the container with values from the key_val pair
        :param key_val:                 The values with which to fill the container
        :return:
        """

    def empty_container(self):
        """
        Override::
        Returns a dictionary containing each container entry
        :return:
        """
        pass

    @staticmethod
    def manufacture_container():
        # TODO, define better what we want the container to be able to do
        pass

class EnvironmentContainer(Container):
    def __init__(self):
        self.floor_texture  = None
        self.wall_height    = None
        self.edge_width     = None
        self.sky_texture    = None
        self.start_node     = None

    def fill_container(self, key_val):

            # Test to see that all of the expected values have been supplied
            if "floor_texture" not in key_val   \
            or "wall_height" not in key_val     \
            or "edge_width" not in key_val      \
            or "sky_texture" not in key_val     \
            or "start_node" not in key_val:
                raise ContainerFillException(ContainerDescriptor.ENVIRONMENT_CONTAINER, key_val)

            self.floor_texture = key_val["floor_texture"]
            self.wall_height = key_val["wall_height"]
            self.edge_width = key_val["edge_width"]
            self.sky_texture = key_val["sky_texture"]
            self.start_node = key_val["start_node"]

    def empty_container(self):
        return  \
            {
                "floor_texture" : self.floor_texture,
                "wall_height"   : self.wall_height,
                "edge_width"    : self.edge_width,
                "sky_texture"   : self.sky_texture,
                "start_node"    : self.start_node
            }

class VRContainer(Container):
    def __init__(self):
        self.frame_angle                = None
        self.distortion                 = None
        self.windowed                   = None
        self.eye_height                 = None
        self.minimum_dist_to_wall       = None

    def fill_container(self, key_val):

        # Test to see that all of the expected values have been supplied
        if "frame_angle" not in key_val \
                or "distortion" not in key_val \
                or "windowed" not in key_val \
                or "eye_height" not in key_val \
                or "minimum_dist_to_wall" not in key_val:
            raise ContainerFillException(ContainerDescriptor.ENVIRONMENT_CONTAINER, key_val)

        self.frame_angle = key_val["frame_angle"]
        self.distortion = key_val["distortion"]
        self.windowed = key_val["windowed"]
        self.eye_height = key_val["eye_height"]
        self.minimum_dist_to_wall = key_val["minimum_dist_to_wall"]

    def empty_container(self):
        return \
            {
                "frame_angle"           : self.frame_angle,
                "distortion"            : self.distortion,
                "windowed"              : self.windowed,
                "eye_height"            : self.eye_height,
                "minimum_dist_to_wall"  : self.minimum_dist_to_wall
            }

    class NodeContainer(Container):
        def __init__(self):
            self.node_id  = None
            self.x_coordinate    = None
            self.y_coordinate     = None
            self.room_texture    = None
            self.wall_pictures     = None

    def fill_container(self, key_val):

        # Test to see that all of the expected values have been supplied
        if "node_id" not in key_val \
                or "x_coordinate" not in key_val \
                or "y_coordinate" not in key_val \
                or "room_texture" not in key_val \
                or "wall_pictures" not in key_val:
            raise ContainerFillException(ContainerDescriptor.ENVIRONMENT_CONTAINER, key_val)

        self.node_id = key_val["node_id"]
        self.x_coordinate = key_val["x_coordinate"]
        self.y_coordinate = key_val["y_coordinate"]
        self.room_texture = key_val["room_texture"]
        self.wall_pictures = key_val["wall_pictures"]

    def empty_container(self):
        return \
            {
                "node_id" : self.node_id,
                "x_coordinate"  : self.x_coordinate,
                "y_coordinate"  : self.y_coordinate,
                "room_texture"  : self.room_texture,
                "wall_pictures" : self.wall_pictures
            }

class ObjectContainer(Container):
    def __init__(self):
        self.x_coordinate   = None
        self.y_coordinate   = None
        self.name           = None
        self.mesh           = None
        self.scale          = None

    def fill_container(self, key_val):

        # Test to see that all of the expected values have been supplied
        if "x_coordinate" not in key_val \
                or "y_coordinate" not in key_val \
                or "name" not in key_val \
                or "mesh" not in key_val \
                or "scale" not in key_val:
            raise ContainerFillException(ContainerDescriptor.ENVIRONMENT_CONTAINER, key_val)

        self.x_coordinate = key_val["x_coordinate"]
        self.y_coordinate = key_val["y_coordinate"]
        self.name = key_val["name"]
        self.mesh = key_val["mesh"]
        self.scale = key_val["scale"]

    def empty_container(self):
        return \
            {
                "x_coordinate" : self.x_coordinate,
                "y_coordinate"   : self.y_coordinate,
                "name"    : self.name,
                "mesh"   : self.mesh,
                "scale"    : self.scale
            }

class EdgeContainer(Container):
    def __init__(self):
        self.source = None
        self.target = None
        self.height = None
        self.wall1 = None
        self.wall2 = None

    def fill_container(self, key_val):

        # Test to see that all of the expected values have been supplied
        if "floor_texture" not in key_val \
                or "wall_height" not in key_val \
                or "edge_width" not in key_val \
                or "sky_texture" not in key_val \
                or "start_node" not in key_val:
            raise ContainerFillException(ContainerDescriptor.ENVIRONMENT_CONTAINER, key_val)

        self.floor_texture = key_val["floor_texture"]
        self.wall_height = key_val["wall_height"]
        self.edge_width = key_val["edge_width"]
        self.sky_texture = key_val["sky_texture"]
        self.start_node = key_val["start_node"]

    def empty_container(self):
        return \
            {
                "floor_texture" : self.floor_texture,
                "wall_height"   : self.wall_height,
                "edge_width"    : self.edge_width,
                "sky_texture"   : self.sky_texture,
                "start_node"    : self.start_node
            }