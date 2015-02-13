
__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Defaults.py

Specifies default values to be used for autopopulation
"""

class Environment:

    FLOOR_TEXTURE                           = "default_floor.png"
    WALL_HEIGHT                             = "500"
    EDGE_WIDTH                              = "100"
    SKY_TEXTURE                             = "default_sky.png"
    START_NODE                              = "1"

class VR:

    FRAME_ANGLE                             = "-5"
    DISTORTION                              = True
    WINDOWED                                = False
    EYE_HEIGHT                              = "10"
    MINIMUM_DISTANCE_TO_WALL                = "10"

class Node:

    ROOM_TEXTURE                            = "default_node.png"

class Object:

    MESH                                    = "default.x"
    SCALE                                   = "1"

class Edge:
    WALL_HEIGHT                             = "500"

class Wall:

    TILE_X                                  = "1"
    TILE_Y                                  = "1"
    PATH                                    = "default_wall.png"

class Picture:
    VISIBLE                                 = True
    TEXTURE                                 = "default_pic.png"

class Config:
    DEBUG                                   = True
    EASY_MAZE                               = True
