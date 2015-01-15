__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Containers.py

Module contains the data containers that will be passed around the application
"""

# Imports


# Enumerations and Functions

class ContainerDescriptor:
    ENVIRONMENT_CONTAINER = "Environment_Container"


# Classes

class Container:
    def __init__(self):
        pass

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
        pass