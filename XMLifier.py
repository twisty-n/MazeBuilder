__author__ = 'tristan_dev'

from ObserverPattern import Observer
from Tkinter import Toplevel, Text, Scrollbar, DISABLED, END, NORMAL
import xml.dom.minidom as minidom
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import Debug


class XMLObserver(Observer):

    def __init__(self, subject):
        Observer.__init__(self, subject)
        self._pane = None
        self._text_area = None
        self._active = False
        self.construct()

    def update(self):
        Debug.printi("The state of the datastore has been updated", Debug.Level.INFO)
        self._text_area.config(state=NORMAL)
        self._text_area.insert(END, "\nThe state of the datastore has been updated")
        self._text_area.config(state=DISABLED)
        # Update the relevant portion of the XML with the changed information from
        # the datastore

    def construct(self):
        top = Toplevel()
        top.withdraw()
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        top.title("XML Preview")
        self._pane = top

        xml_area = Text(top, borderwidth=2, relief="sunken")
        xml_area.config(font=("consolas", 12), undo=True, wrap='word', state=DISABLED)
        xml_area.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scrollbar = Scrollbar(top, command=xml_area.yview)
        scrollbar.grid(row=0, column=1, sticky='nsew')
        xml_area['yscrollcommand'] = scrollbar.set

        self._text_area = xml_area


    def view_xml_pane(self):

        self._pane.withdraw() if self._active else self._pane.deiconify()

        self._active = not self._active
        # Launch a top level dialog

        # insert all of the needed text into the dialog


class XMLContainer:

    def __init__(self):
        pass

    def read_file(self, file):
        tree = ET.ElementTree(file=file)
        root = tree.getroot()
        return ET.tostring(root, encoding="utf8", method='xml')



if __name__ == "__main__":

    con = XMLContainer()
    con.read_file("Data/AngleTest.xml")
