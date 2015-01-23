__author__ = 'tristan_dev'

import Debug, sys
from Enumerations import Input_Event

CONTROL_MAP = {
    "BUTTON_1_CLICK"    :   Input_Event.CLICK_M1,
    "BUTTON_2_CLICK"    :   Input_Event.CLICK_M2,
    "BUTTON_3_CLICK"    :   Input_Event.CLICK_M3,
    "DOUBLE_BUTTON_1"   :   Input_Event.D_CLICK_M1,
    "DOUBLE_BUTTON_2"   :   Input_Event.D_CLICK_M2,
    "DOUBLE_BUTTON_3"   :   Input_Event.D_CLICK_M3,
    "SPACE"             :   Input_Event.SPACE,
    "ENTER"             :   Input_Event.RETURN
}

def  _load_control_file(file_path):
    try:
        control_file = open(file_path)
        Debug.printi("Control file " + file_path + " successfully loaded", Debug.Level.INFO)
        return control_file
    except IOError as e:
        Debug.printi(e.message, Debug.Level.FATAL)


def load_controls(file_path="Data/def-controls.mb"):
    file = _load_control_file(file_path)
    control_map = _generate_control_map(file)

def _parse_controls(control_action_map):
    pass

def _generate_control_map(file):
    """
    Generate a control map that can be parsed
    :param file:        The file to parse the controls
    :return:
    """
    try:
        line_list = file.readlines()
        con_map = []
        for line in line_list:
            str = line.split(":")
            str[0] = ''.join(str[0].strip())
            str[1] = ''.join(str[1].strip())
            con_map.append((str[0], str[1]))
    except (IOError, EOFError) as e:
        file.close()
        Debug.printi(e, Debug.Level.FATAL)
    else:
        file.close()
        Debug.printi("Control file successfully parsed", Debug.Level.INFO)
        return con_map



if __name__ == "__main__":
    load_controls()