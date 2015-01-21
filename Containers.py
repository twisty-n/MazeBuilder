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
from Enumerations import ContainerDescriptor
# Classes

class Container:

    DESCRIPTOR = ContainerDescriptor

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
    def manufacture_container(descriptor, key_val=None):
        # TODO: move this to be a static variable
        dispatch = \
            {
                ContainerDescriptor.NODE_CONTAINER          :       NodeContainer,
                ContainerDescriptor.EDGE_CONTAINER          :       EdgeContainer,
                ContainerDescriptor.OBJECT_CONTAINER        :       ObjectContainer,
                ContainerDescriptor.ENVIRONMENT_CONTAINER   :       EnvironmentContainer,
                ContainerDescriptor.VR_CONTAINER            :       VRContainer,
                ContainerDescriptor.WALL_CONTAINER          :       WallContainer,
                ContainerDescriptor.WALL_TEXTURE_CONTAINER  :       WallTextureContainer,
                ContainerDescriptor.NODE_PICTURE_CONTAINER  :       NodePictureContainer
            }
        return dispatch[descriptor](key_val)


class EnvironmentContainer(Container):
    def __init__(self, key_val=None):
        self.floor_texture  = None
        self.wall_height    = None
        self.edge_width     = None
        self.sky_texture    = None
        self.start_node     = None
        Container.__init__(self, key_val)

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
    def __init__(self, key_val=None):
        self.frame_angle                = None
        self.distortion                 = None
        self.windowed                   = None
        self.eye_height                 = None
        self.minimum_dist_to_wall       = None
        Container.__init__(self, key_val)


    def fill_container(self, key_val):

        # Test to see that all of the expected values have been supplied
        if "frame_angle" not in key_val \
                or "distortion" not in key_val \
                or "windowed" not in key_val \
                or "eye_height" not in key_val \
                or "minimum_dist_to_wall" not in key_val:
            raise ContainerFillException(ContainerDescriptor.VR_CONTAINER, key_val)

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
    def __init__(self, key_val=None):
        self.node_id  = None
        self.x_coordinate    = None
        self.y_coordinate     = None
        self.room_texture    = None
        self.wall_pictures     = None
        Container.__init__(self, key_val)

    def fill_container(self, key_val):

        # Test to see that all of the expected values have been supplied
        if "node_id" not in key_val \
                or "x_coordinate" not in key_val \
                or "y_coordinate" not in key_val \
                or "room_texture" not in key_val \
                or "wall_pictures" not in key_val:
            raise ContainerFillException(ContainerDescriptor.NODE_CONTAINER, key_val)

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
    def __init__(self, key_val=None):
        self.x_coordinate   = None
        self.y_coordinate   = None
        self.name           = None
        self.mesh           = None
        self.scale          = None
        Container.__init__(self, key_val)

    def fill_container(self, key_val):

        # Test to see that all of the expected values have been supplied
        if "x_coordinate" not in key_val \
                or "y_coordinate" not in key_val \
                or "name" not in key_val \
                or "mesh" not in key_val \
                or "scale" not in key_val:
            raise ContainerFillException(ContainerDescriptor.OBJECT_CONTAINER, key_val)

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
    def __init__(self, key_val=None):
        self.source = None
        self.target = None
        self.height = None
        self.wall1 = None
        self.wall2 = None
        Container.__init__(self, key_val)

    def fill_container(self, key_val):

        # Test to see that all of the expected values have been supplied
        if "source" not in key_val.keys() \
                or "target" not in key_val.keys() \
                or "height" not in key_val.keys() \
                or "wall1" not in key_val.keys() \
                or "wall2" not in key_val.keys():
            raise ContainerFillException(ContainerDescriptor.EDGE_CONTAINER, key_val)

        self.source = key_val["source"]
        self.target = key_val["target"]
        self.height = key_val["height"]
        self.wall1 = key_val["wall1"]
        self.wall2 = key_val["wall2"]

    def empty_container(self):
        return \
            {
                "source" : self.source,
                "target"   : self.target,
                "height"    : self.height,
                "wall1"   : self.wall1,
                "wall2"    : self.wall2
            }

class WallContainer(Container):
    def __init__(self, key_val):
        self.height = None
        self.textures = None
        Container.__init__(self, key_val)

    def fill_container(self, key_val):

        # Test to see that the dict that has been provided is valid
        if "height" not in key_val  \
        or "textures" not in key_val:
            raise ContainerFillException(ContainerDescriptor.WALL_CONTAINER, key_val)

        self.height = key_val["height"]
        self.textures = key_val["textures"]

    def empty_container(self):
        return \
            {
                "height"    : self.height,
                "textures"  : self.textures
            }

class WallTextureContainer(Container):
    def __init__(self, key_val=None):
        self.path= None
        self.tile_x = None
        self.tile_y = None
        self.height = None
        Container.__init__(self, key_val)

    def fill_container(self, key_val):

        # Check to see that we have the required dictionary to fill the container
        if "path" not in key_val    \
        or "tile_x" not in key_val  \
        or "tile_y" not in key_val  \
        or "height" not in key_val:
            raise ContainerFillException(ContainerDescriptor.WALL_TEXTURE_CONTAINER, key_val)

        self.path = key_val["path"]
        self.tile_x = key_val["tile_x"]
        self.tile_y = key_val["tile_y"]
        self.height = key_val["height"]

    def empty_container(self):
        return \
            {
                "path"      : self.path,
                "tile_x"    : self.tile_x,
                "tile_y"   : self.tile_y,
                "height"    : self.height,
            }

class NodePictureContainer(Container):
    def __init__(self, key_val=None):
        self.name = None
        self.visible = None
        self.texture = None
        Container.__init__(self, key_val)

    def fill_container(self, key_val):

        # Check to see that we have the required dictionary to fill the container
        if "name" not in key_val \
                or "visible" not in key_val \
                or "texture" not in key_val:
            raise ContainerFillException(ContainerDescriptor.NODE_PICTURE_CONTAINER, key_val)

        self.name = key_val["name"]
        self.visible = key_val["visible"]
        self.texture = key_val["texture"]

    def empty_container(self):
        return \
            {
                "name"      : self.name,
                "visible"    : self.visible,
                "texture"   : self.texture
            }

