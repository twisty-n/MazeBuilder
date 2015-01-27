__author__ = 'tristan_dev'

import Debug, sys
from Enumerations import Input_Event, ControlSpecifier, ExecutionStage

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

INPUT_MAP = {

    ("BUTTON_1_CLICK", ExecutionStage.START)    :   Input_Event.CLICK_M1,
    ("BUTTON_2_CLICK", ExecutionStage.START)    :   Input_Event.CLICK_M2,
    ("BUTTON_3_CLICK", ExecutionStage.START)    :   Input_Event.CLICK_M3,
    ("BUTTON_1_CLICK", ExecutionStage.END)      :   Input_Event.RELEASE_M1,
    ("BUTTON_1_CLICK", ExecutionStage.EXECUTE)  :   Input_Event.DRAG_M1,
    ("BUTTON_2_CLICK", ExecutionStage.END)      :   Input_Event.RELEASE_M2,
    ("BUTTON_2_CLICK", ExecutionStage.EXECUTE)  :   Input_Event.DRAG_M2,
    ("BUTTON_3_CLICK", ExecutionStage.END)      :   Input_Event.RELEASE_M3,
    ("BUTTON_3_CLICK", ExecutionStage.EXECUTE)  :   Input_Event.DRAG_M3,

}


def  _load_control_file(file_path):
    try:
        control_file = open(file_path)
        Debug.printi("Control file " + file_path + " successfully loaded", Debug.Level.INFO)
        return control_file
    except IOError as e:
        Debug.printi(e.message, Debug.Level.FATAL)


def load_controls(function_map, file_path="Data/def-controls.mb"):
    file = _load_control_file(file_path)
    control_map = _generate_control_map(file)
    return _parse_controls(control_map, function_map)

def _parse_controls(control_action_map, function_map):

    # First convert the input file into the keys represented by our tables
    for tuple in control_action_map:
        if tuple[0] == "BUTTON_1"   \
        or tuple[0] == "BUTTON_2"   \
        or tuple[0] == "BUTTON_3":
            tuple[0] = tuple[0] + "_CLICK"

    # Now expand the control specifiers to the three different specifiers if needed
    additionals = []
    for item in control_action_map:
        if item[1] == ControlSpecifier.CREATE_EDGE or item[1] == ControlSpecifier.DRAG_NODE:
            item.append(ExecutionStage.START)
            additionals.append(
                [
                    INPUT_MAP[(item[0], ExecutionStage.EXECUTE)],
                    item[1],
                    ExecutionStage.EXECUTE
                ]
            )
            additionals.append(
                [
                    INPUT_MAP[(item[0], ExecutionStage.END)],
                    item[1],
                    ExecutionStage.END
                ]
            )
            item[0] = CONTROL_MAP[item[0]]
        else:
            # Just remapp the specfier to its input event and add the appropriate executino flag
            item[0] = CONTROL_MAP[item[0]]
            item.append(ExecutionStage.EXECUTE)

    control_action_map.extend(additionals)

    # Now, using the function map, we can create the final control structure
    command_map = {}
    for control in control_action_map:
        command_map[control[0]] = function_map[(control[1], control[2])]

    return command_map

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
            con_map.append([str[0], str[1]])
    except (IOError, EOFError) as e:
        file.close()
        Debug.printi(e, Debug.Level.FATAL)
    else:
        file.close()
        Debug.printi("Control file successfully parsed", Debug.Level.INFO)
        return con_map



if __name__ == "__main__":
    load_controls(None)