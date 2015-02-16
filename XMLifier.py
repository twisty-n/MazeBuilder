__author__ = 'tristan_dev'

from ObserverPattern import Observer
from Tkinter import Toplevel, Text, Scrollbar, DISABLED, END, NORMAL
import tkFileDialog, tkMessageBox
from Enumerations import Event, DESCRIPTOR_MAP
import lxml.etree as ET
import Debug
import Defaults

# Don't forget our magic number anti-pattern is 42!


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
        self.construct()
        self._xml_container = XMLContainer(subject)
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
        self._xml_container.create_skeleton(subject)

    def import_maze(self, filepath, datastore, canvas):
        self._xml_container.import_maze(filepath(), canvas, datastore)
        # We can use the canvas to manage all of the creation ops
        # If any of the coordinates are negative, we need to change the canvas scroll region
        outer_x_region = 0
        outer_y_region = 0

    def update(self):
        Debug.printi("The state of the datastore has been updated", Debug.Level.INFO)

        # Retrieve the update details from the datastore, and then dispatch the changes to
        # the XML container
        update_event = (self._subject._cache["EVENT"], self._subject._cache["ID"], self._subject._cache["DATA"])
        if update_event[0] == "Delete All":
            self._xml_container.create_skeleton(self._subject)
            return
        self._dispatch[update_event[0]](
            self._extract_xml_id(update_event[0], update_event[2]),
            update_event[2]
        )

        self._text_area.config(state=NORMAL)
        self._text_area.delete(1.0, END)
        self._text_area.insert(END, self._xml_container.to_string())
        self._text_area.config(state=DISABLED)

    def _extract_xml_id(self, event, data):
        if "Edge" in event:
            return (data["source"], data["target"])
        elif "Object" in event:
            return data["name"]
        elif "Node" in event:
            return data["node_id"]
        elif "Environment" in event:
            return "ENV"
        else:
            return "VR"

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

    def dump_file(self):

        # Validate, abort if invalid
        result, message = self._subject.export_finalize()
        if result  is False:
            # throw error, return
            tkMessageBox.showerror("Invalid Data", message)
            return

        # Obtain the file handle to print to
        handle = tkFileDialog.asksaveasfile(mode='w', defaultextension=".xml")
        if handle is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        handle.write(self._xml_container.to_string())
        handle.close()  # `()` was missing.
        Debug.printi("File " + handle.name + " has been saved")


class XMLContainer:

    def __init__(self, datastore):
        self._all_entries = {}

    def import_maze(self, filepath, canvas, datastore):
        """
        Imports a maze from an XML file

        This will overwrite any current information, you will lose the current work
        :param filepath:
        :return:
        """
        inputter = XMlInputer()
        self

        if filepath is '':
            Debug.printi("No input file to read", Debug.Level.INFO)
            return

        inputter.read_file(filepath)
        Debug.printi("Maze input file " + filepath + " has been read", Debug.Level.INFO)
        self._all_entries.clear()

        for node in inputter._root.iter("node"):
            original_id = node.attrib["id"]
            node.attrib["id"] = "n_" + node.attrib["id"]
            for edge in inputter._root.iter("edge"):
                if edge.attrib["source"] == original_id:
                    edge.attrib["source"] = node.attrib["id"]
                if edge.attrib["target"] == original_id:
                    edge.attrib["target"] = node.attrib["id"]

        i = 0
        for node in inputter._root.iter("node"):
            # Use an index to assign the id to the nodes
            i += 1
            self._all_entries[str(i)] = node
            attributes = node.attrib
            old_id = attributes["id"]
            attributes["id"] = str(i)
            pictures = {}
            for pic in node.getchildren():
                pictures[pic.attrib["name"]] = pic.attrib
            canvas.create_new_node(
                (
                    int(attributes["x"]),
                    int(attributes["y"])
                ),
                prog=True,
                data=(attributes, pictures)
            )
            Debug.printi("New Node Created from file ID:" + node.attrib["id"], Debug.Level.INFO)

            # Since we are changing the id's we need to update all of the edges that use them
            for edge in inputter._root.iter("edge"):
                if edge.attrib["source"] == old_id:
                    edge.attrib["source"] = str(i)
                if edge.attrib["target"] == old_id:
                    edge.attrib["target"] = str(i)

        for edge in inputter._root.iter("edge"):
            self._all_entries[(edge.attrib["source"], edge.attrib["target"])] = edge
            source_coords = int(self._all_entries[edge.attrib["source"]].attrib["x"]), \
                            int(self._all_entries[edge.attrib["source"]].attrib["y"])

            target_coords = int(self._all_entries[edge.attrib["target"]].attrib["x"]), \
                            int(self._all_entries[edge.attrib["target"]].attrib["y"])

            wall1_node = edge.find("Wall1")
            wall2_node = edge.find("Wall2")

            wall1 = {
                "height"    : wall1_node.attrib["height"] if len(wall1_node.attrib) > 0 else None,
                "textures"  : {}
            }

            wall2 = {
                "height": wall2_node.attrib["height"] if len(wall2_node.attrib) > 0 else None,
                "textures": {}
            }

            for texture in wall1_node.iter("Texture"):
                wall1["textures"]["path"] = {
                    "path"  : texture.attrib["path"],
                    "tile_x": texture.attrib["tileX"],
                    "tile_y": texture.attrib["tileY"]
                }

            for texture in wall2_node.iter("Texture"):
                wall2["textures"]["path"] = {
                    "path": texture.attrib["path"],
                    "tile_x": texture.attrib["tileX"],
                    "tile_y": texture.attrib["tileY"]
                }

            canvas._clear_cache(source_coords)
            canvas._begin_edge(source_coords)
            canvas._execute_edge(target_coords)
            canvas._end_edge(target_coords,
                               prog=True,
                               data={
                                       "source": edge.attrib["source"],
                                       "target": edge.attrib["target"],
                                       "height": None,
                                       "wall1": wall1,
                                       "wall2": wall2
                               })
            Debug.printi("New EDGE Created from file Source:" + edge.attrib["source"]
                         + " Target: " + edge.attrib["target"], Debug.Level.INFO)

        for object in inputter._root.iter("object"):
            self._all_entries[object.attrib["name"]] = object
            canvas._mark_object((int(object.attrib["x"]), int(object.attrib["y"])),
                                prog=True,
                                data={
                                        "x_coordinate": object.attrib["x"],
                                        "y_coordinate": object.attrib["y"],
                                        "name": object.attrib["name"],
                                        "mesh": object.attrib["mesh"],
                                        "scale": object.attrib["scale"]
                                })
            Debug.printi("New Object Created from file Name:" + object.attrib["name"], Debug.Level.INFO)

        self._floor_tex = ET.SubElement(self._root, "floorTexture")             if self._floor_tex is None else self._floor_tex
        self._wall_height = ET.SubElement(self._root, "wallHeight")             if self._wall_height is None else self._wall_height
        self._edge_width = ET.SubElement(self._root, "edgeWidth")               if self._edge_width is None else self._edge_width
        self._sky_texture = ET.SubElement(self._root, "skySphereTexture")       if self._sky_texture is None else self._sky_texture
        self._start_node = ET.SubElement(self._root, "startNode")               if self._start_node is None else self._start_node

        for floor_tex in inputter._root.iter("floorTexture"):
            self._floor_tex.attrib["val"] = floor_tex.attrib["val"]
        for wall_height in inputter._root.iter("wallHeight"):
            self._wall_height.attrib["val"] = wall_height.attrib["val"]
        for edge_width in inputter._root.iter("edgeWidth"):
            self._edge_width.attrib["val"] = edge_width.attrib["val"]
        for sky_tex in inputter._root.iter("skySphereTexture"):
            self._sky_texture.attrib["val"] = sky_tex.attrib["val"]
        for start_node in inputter._root.iter("startNode"):
            self._start_node.attrib["id"] = start_node.attrib["id"]

        datastore.inform("Environment Edit", data={
            "floor_texture": self._floor_tex.attrib["val"],
            "wall_height": self._wall_height.attrib["val"],
            "edge_width": self._edge_width.attrib["val"],
            "sky_texture": self._sky_texture.attrib["val"],
            "start_node": self._start_node.attrib["id"]
        })

        datastore.inform("VR Edit", data={\
                "frame_angle"           : inputter._root.attrib["frameAngle"],
                "distortion"            : inputter._root.attrib["distortion"],
                "windowed"              : inputter._root.attrib["windowed"],
                "eye_height"            : inputter._root.attrib["eye"],
                "minimum_dist_to_wall"  : inputter._root.attrib["minDistToWall"]
        })
        self._root.attrib["takeOffAfter"] = "20"
        self._root.attrib["displays"] = "3,4,1,2,5,6"

    def create_skeleton(self, datastore):

        self._root = ET.Element("graph")

        # Environment params
        self._floor_tex = ET.SubElement(self._root, "floorTexture")
        self._wall_height = ET.SubElement(self._root, "wallHeight")
        self._edge_width = ET.SubElement(self._root, "edgeWidth")
        self._sky_texture = ET.SubElement(self._root, "skySphereTexture")
        self._start_node = ET.SubElement(self._root, "startNode")
        self._root.attrib["takeOffAfter"]  = "20"
        self._root.attrib["displays"]      = "3,4,1,2,5,6"

        datastore.inform("Environment Edit", data={
            "floor_texture":    Defaults.Environment.FLOOR_TEXTURE,
            "wall_height":      Defaults.Environment.WALL_HEIGHT,
            "edge_width":       Defaults.Environment.EDGE_WIDTH,
            "sky_texture":      Defaults.Environment.SKY_TEXTURE,
            "start_node":       Defaults.Environment.START_NODE,
        })

        datastore.inform("VR Edit", data={ \
            "frame_angle"           :Defaults.VR.FRAME_ANGLE,
            "distortion"            :Defaults.VR.DISTORTION,
            "windowed"              :Defaults.VR.WINDOWED,
            "eye_height"            :Defaults.VR.EYE_HEIGHT,
            "minimum_dist_to_wall"  :Defaults.VR.MIN_DIST_TO_WALL
        })
        self._root.attrib["takeOffAfter"] = "20"
        self._root.attrib["displays"] = "3,4,1,2,5,6"

    def add_node_entry(self, entry_id, data):

        node = ET.SubElement(self._root, "node")

        node.attrib["id"]        = str(data["node_id"])
        node.attrib["x"]         = str(data["x_coordinate"])
        node.attrib["y" ]        = str(data["y_coordinate"])
        if data["room_texture"] is None:
            data["room_texture"] = "Data/default.jpg"
        node.attrib["texture"]   = str((data["room_texture"].split("/"))[1]) if "Data" in data["room_texture"] else data["room_texture"]
        node.attrib["accessible"] = "true"

        if data["wall_pictures"] is not None:
            for index, (pic_id, pic) in enumerate(data["wall_pictures"].iteritems()):
                pic_node = ET.SubElement(node, "w"+str(index+1)+"Img")
                pic_node.attrib["name"]     = str(pic["name"])
                pic_node.attrib["visible"]  = str(pic["visible"]).lower()
                if "Data\\" in pic["texture"]:
                    pic_node.attib["texture"] = pic["texture"].replace("Data\\", "")
                else:
                    pic_node.attrib["texture"]  = str(pic["texture"])
        self._all_entries[entry_id] = node

    def edit_node_entry(self, entry_id, data):
        self._root.remove(self._all_entries[entry_id])
        self.add_node_entry(entry_id, data)

    def add_object_entry(self, entry_id, data):

        node = ET.SubElement(self._root, "object")

        node.attrib["x"]        = str(data["x_coordinate"])
        node.attrib["y"]        = str(data["y_coordinate"])
        node.attrib["name"]     = str(data["name"])
        if data["mesh"] == "No mesh loaded":
            data["mesh"] = "default.x"
        node.attrib["mesh"]     = str(data["mesh"]) if "Data" not in data["mesh"] else str(data["mesh"].split("/")[1])
        node.attrib["scale"]    = str(data["scale"])

        self._all_entries[entry_id] = node

    def edit_object_entry(self, entry_id, data):
        self._root.remove(self._all_entries[entry_id])
        self.add_object_entry(entry_id, data)

    def add_edge_entry(self, entry_id, data):

        node = ET.SubElement(self._root, "edge")
        node.attrib["source"] = str(data["source"])
        node.attrib["target"] = str(data["target"])

        if data["wall1"] is not None:
            wall1 = ET.SubElement(node, "Wall1")
            wall1.attrib["height"] = str(data["wall1"]["height"])
            for key, val in data["wall1"]["textures"].iteritems():
                tex_node = ET.SubElement(wall1, "Texture")
                tex_node.attrib["path"] = val["path"] if "Data" not in val["path"] else str(val["path"].split("/")[1])
                tex_node.attrib["tileX"] = val["tile_x"]
                tex_node.attrib["tileY"] = val["tile_y"]

        if data["wall2"] is not None:
            wall2 = ET.SubElement(node, "Wall2")
            wall2.attrib["height"] = str(data["wall2"]["height"])
            for key, val in data["wall2"]["textures"].iteritems():
                tex_node = ET.SubElement(wall2, "Texture")
                tex_node.attrib["path"] = val["path"] if "Data" not in val["path"] else str(val["path"].split("/")[1])
                tex_node.attrib["tileX"] = val["tile_x"]
                tex_node.attrib["tileY"] = val["tile_y"]

        self._all_entries[entry_id] = node

    def edit_edge_entry(self, entry_id, data):
        self._root.remove(self._all_entries[entry_id])
        self.add_edge_entry(entry_id, data)

    def remove_entry(self, entry_id, data):
        self._root.remove(self._all_entries[entry_id])
        del self._all_entries[entry_id]

    def edit_environment(self, entry_id, data):
        self._floor_tex.attrib["val"]   = str(data["floor_texture"])
        self._wall_height.attrib["val"] = str(data["wall_height"])
        self._edge_width.attrib["val"]  = str(data["edge_width"])
        self._sky_texture.attrib["val"] = str(data["sky_texture"])
        self._start_node.attrib["id"]  = str(data["start_node"])

    def edit_vr(self, entry_id, data):
        attribs = self._root.attrib

        attribs["frameAngle"]           = str(data["frame_angle"])
        attribs["distortion"]           = str(data["distortion"]).lower()
        attribs["windowed"]             = str(data["windowed"]).lower()
        attribs["eye"]                  = str(data["eye_height"])
        attribs["minDistToWall"]        = str(data["minimum_dist_to_wall"])

    def to_string(self):
        return ET.tostring(self._root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

class XMlInputer:

    def __init__(self):
        self._root = None

    def read_file(self, file):
        tree = ET.ElementTree(file=file)
        self._root = root = tree.getroot()



if __name__ == "__main__":

    con = XMLContainer()
    con.read_file("Data/AngleTest.xml")
    print(con.to_string())
