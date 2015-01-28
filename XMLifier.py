__author__ = 'tristan_dev'

from ObserverPattern import Observer
import Debug


class XMLObserver(Observer):

    def __init__(self, subject):
        Observer.__init__(self, subject)

    def update(self):
        Debug.printi("The state of the datastore has been updated", Debug.Level.INFO)