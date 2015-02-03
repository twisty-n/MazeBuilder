__author__ = 'tristan_dev'

from ObserverPattern import Observer
from Tkinter import Toplevel, Text, Scrollbar, DISABLED, END, NORMAL
from Enumerations import Event, DESCRIPTOR_MAP
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

        self._dispatch = {
            Event.EDGE_CREATE       :   self._xml_container.add_edge_entry,
            Event.NODE_CREATE       :   self._xml_container.add_node_entry,
            Event.OBJECT_CREATE     :   self._xml_container.add_object_entry,
            Event.OBJECT_EDIT       :   self._xml_container.edit_object_entry,
            Event.NODE_EDIT         :   self._xml_container.edit_node_entry,
            Event.EDGE_EDIT         :   self._xml_container.edit_edge_entry,
            Event.EDGE_DELETE       :   self._xml_container.remove_entry,
            Event.NODE_DELETE       :   self._xml_container.remove_entry,
            Event.OBJECT_DELETE     :   self._xml_container.remove_entry,
            Event.ENVIRONMENT_EDIT  :   self._xml_container.edit_environment,
            Event.VR_EDIT           :   self._xml_container.edit_vr
        }

    def update(self):
        Debug.printi("\nThe state of the datastore has been updated", Debug.Level.INFO)

        # Retrieve the update details from the datastore, and then dispatch the changes to
        # the XML container
        update_event = (self._subject._cache["EVENT"], self._subject._cache["ID"], self._subject._cache["DATA"])
        self._dispatch[update_event[0]](
            update_event[1],
            update_event[2]
        )

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
        top.protocol("WM_DELETE_WINDOW", self.view_xml_pane)
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
        self._all_entries = {}
        self.create_skeleton()

    def create_skeleton(self):

        self._root = ET.Element("graph")

        # Environment params
        self._floor_tex = ET.SubElement(self._root, "floorTexture")
        self._wall_height = ET.SubElement(self._root, "wallHeight")
        self._edge_width = ET.SubElement(self._root, "edgeWidth")
        self._sky_texture = ET.SubElement(self._root, "skySphereTexture")
        self._start_node = ET.SubElement(self._root, "startNode")

    def read_file(self, file):
        tree = ET.ElementTree(file=file)
        root = tree.getroot()
        return ET.tostring(root, encoding="utf8", method='xml')

    def add_node_entry(self, entry_id, data):

        node = ET.SubElement(self._root, "node")

        node.attrib["id"]        = str(data["node_id"])
        node.attrib["x"]         = str(data["x_coordinate"])
        node.attrib["y" ]        = str(data["y_coordinate"])
        if data["room_texture"] is None:
            data["room_texture"] = "Data/default.jpg"
        node.attrib["texture"]   = str((data["room_texture"].split("/"))[1])

        if data["wall_pictures"] is not None:
            # TODO: put the pics as an attribute
            pass

        self._all_entries[entry_id] = node

    def edit_node_entry(self, entry_id, data):
        self._root.remove(self._all_entries[entry_id])
        self.add_node_entry(entry_id, data)

    def add_object_entry(self, entry_id, data):
        pass

    def edit_object_entry(self, entry_id, data):
        pass

    def add_edge_entry(self, entry_id, data):

        node = ET.SubElement(self._root, "edge")
        node.attrib["source"] = str(data["source"])
        node.attrib["target"] = str(data["target"])

        if data["wall1"] is not None:
            # TODO: implement
            pass

        if data["wall2"] is not None:
            # TODO implement
            pass

        self._all_entries[entry_id] = node

    def edit_edge_entry(self, entry_id, data):
        self._root.remove(self._all_entries[entry_id])
        self.add_edge_entry(entry_id, data)

    def remove_entry(self, entry_id, data):
        self._root.remove(self._all_entries[entry_id])
        del self._all_entries[entry_id]

    def edit_environment(self, entry_id, data):
        pass

    def edit_vr(self, entry_id, data):
        pass

    def to_string(self):
        return ET.tostring(self._root, pretty_print=True)



if __name__ == "__main__":

    con = XMLContainer()
    con.read_file("Data/AngleTest.xml")
    print(con.to_string())
