__author__ = 'tristan_dev'

from ObserverPattern import Observer
from Tkinter import Toplevel, Text, Scrollbar, DISABLED, END, NORMAL
from Enumerations import EditableObject
import xml.dom.minidom as minidom
import lxml.etree as ET
import Debug


class XMLObserver(Observer):

    def __init__(self, subject):
        """

        :param subject:         The data store that the XMLObserver will be watching
        :type subject:          DataStore.DataStore
        :return:
        """
        Observer.__init__(self, subject)
        self._pane = None
        self._text_area = None
        self._active = False
        self._xml_container = XMLContainer(None, None)
        self.construct()

    def update(self):
        Debug.printi("\nThe state of the datastore has been updated", Debug.Level.INFO)

        # Retrieve the update details from the datastore, and then dispatch the changes to
        # the XML container
        

        self._text_area.config(state=NORMAL)
        self._text_area.delete(1.0, END)
        self._text_area.insert(END, self._xml_container.to_string())
        self._text_area.config(state=DISABLED)

    def construct(self):
        """
        Construct the window and the frame used to display the XML
        :return:
        """
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
        """
        Toggle the XML window on or offs
        :return:
        """
        self._pane.withdraw() if self._active else self._pane.deiconify()
        self._active = not self._active



class XMLContainer:

    XML_LOOKUP = {

    }

    def __init__(self, environment=None, vr_config=None):
        self.environment_dict = environment
        self.vr_config_dict = vr_config
        self.create_skeleton()

    def create_skeleton(self):

        self._root = ET.Element("graph")
        self._floor_tex = ET.SubElement(self._root, "floorTexture")
        self._wall_height = ET.SubElement(self._root, "wallHeight")
        self._edge_width = ET.SubElement(self._root, "edgeWidth")
        self._sky_texture = ET.SubElement(self._root, "skySphereTexture")
        self._start_node = ET.SubElement(self._root, "startNode")

    def read_file(self, file):
        tree = ET.ElementTree(file=file)
        root = tree.getroot()
        return ET.tostring(root, encoding="utf8", method='xml')

    def add_entry(self, type, data):
        """
        Adds a new entry to the XML representation

        :param type:                The type of data to be added
        :param data:        A dict containing the entries to be added
        :return:
        """
        pass

    def edit_entry(self, type, entry_id, data):
        """
        Edit an existing XML node

        :param type:                The type of entry that is being edited
        :param entry_id:            The id of the entry
        :param data:                The dict representing the new data
        """
        pass

    def to_string(self):
        return ET.tostring(self._root, pretty_print=True)



if __name__ == "__main__":

    con = XMLContainer()
    con.read_file("Data/AngleTest.xml")
    print(con.to_string())
