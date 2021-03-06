import Debug

__author__ = 'tristan_dev'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: UtilWidgets.py
Classes based on those listed in
http://effbot.org/tkinterbook/tkinter-application-windows.htm

Contains a custom, but generalised widgets library -.-
"""

from Tkinter import SUNKEN, W, Label, X, Frame, Toplevel, \
    ACTIVE, Button, LEFT, E, Canvas, Listbox, SINGLE, END, \
    ANCHOR, Menu, StringVar, TclError, DISABLED
import tkFileDialog
from PIL import Image, ImageTk
import shutil, os, sys
from DataStore import DataStore
from Debug import OutputPipe

from Exceptions import DuplicateListHeapItemException, DuplicateCommandException, MaxItemLimitReachedException

class SubMenu():
    """
    Defines a generic Sub menu class that may be used as part of a larger menu
    """
    def __init__(self, parent_menu, label):
        """
        Construct the SubMenu instance
        :param parent_menu:             The menu in which this submenu will be accessed from
        :param label:                   The label to give the submenu, this is what the user will see
        :return:                        An instance of SubMenu
        """
        self._parent_menu = parent_menu
        self._options = {}
        self._label = label
        self._menu = Menu(parent_menu)
        self._key_underline = 0

    def add_option(self, label, action, type_func, shortcut):
        """
        Adds a menu item to the submenu

        Adds a menu item to the tk representation of the menu, as well as the underlying
        dictionary that defines the menu. This method also allows the addition of a keyboard
        shortcut to be defined for a particular menu option
        :param label:
        :param action:
        :param type_func:
        :param shortcut:
        :return:
        """
        pass

    def add_option(self, label, action, type_func):
        """
        Adds a menu item to the submenu

        Adds a menu item to the dictionary of menu items that make up this
        submenu. Also adds the command to actual Tk menu structure,
        Function will fail if the menu item already exists
        :param label(string):           The label of the option to add
        :param action(function):        The action callback to be executed
        :param type_func(string):       The menu entry function for the type of item to add to the menu
        """
        _type = \
            {          "command"        : self._menu.add_command,
                       "checkbutton"    : self._menu.add_checkbutton,
                       "radiobutton"    : self._menu.add_radiobutton
            }

        if label in self._options:
            raise DuplicateCommandException(label)

        self._options[label] = action
        _type[type_func](label=label, command=action)

    def remove_option(self, label):
        """
        Remove a menu option from this submenu

        Removes a menu option from this submenu
        Will fail silently if the menu item does not exist

        :param label:       The label of the menu item that needs to be removed
        """
        del self._options[label]
        index = self._menu.index(label)
        self._menu.delete(index, index)

class ImagePicker(Frame):
    """
    A custom widget that allows for the selection and preview of a picture
    Note that in the current format, the image picker is specific to the
    maze builder project
    """
    def __init__(self, parent, label, default="No File Selected", auto_move=False, move_fold=None):
        """
        Construct the image picker instance

        :param default:     Use to set the image path and inital data loaded
        :param auto_move:   If this is set to true, the image picker will automatically
                            move the image into a defined relative folder in the same
                            relative location
        """
        Frame.__init__(self, parent)
        self._image_ref = None
        self._file_name = default if not default == "No File Selected" else None
        self._file_path = self._file_name
        self._parent = parent

        self._auto_move = auto_move
        if auto_move is True:
            self._folder = "/" + move_fold + "/"

        # Text label
        self._label = Label(self, text=label, anchor=W)
        self._label.grid(row=0, column=0, sticky=W, padx=2)
        self._label.config(width=10)

        # The label that displays the name of the selected file
        self._img_label = Label(self, text=default)
        self._img_label.config(width=15)
        self._img_label.grid(row=0, column=1, sticky=W)

        # Button that enables the previewing of the loaded picture
        self._pButton = Button(self, text="Preview", command=self._display_img, padx=5)
        self._pButton.config(width=8)
        self._pButton.grid(row=0, column=3, sticky=W)

        # Button that enables the loading of files
        self._fButton = Button(self, text="|...|", command=self._load_img_label, padx=5)
        self._fButton.config(width=4)
        self._fButton.grid(row=0, column=2)

    def _display_img(self):
        """
        Display a loaded image in a dialog
        """
        if self._file_path is None:
            Debug.printi("No picture has been loaded to preview", Debug.Level.ERROR)
            return
        photo = self._open_img(self._file_path)
        ImageViewDialog(self._parent, self._file_name, photo)


    def _open_img(self, img_name):
        """
        Open an image from its location on disk

        Retrieves an image in ImageTk form from a given file path
        and loads it for application use

        :img_name: The path/name (?) of the image to open
        """
        try:
            img = Image.open(img_name)
            photo = ImageTk.PhotoImage(img)
            return photo
        except IOError:
            Debug.printi("Unable to find image " + img_name, Debug.Level.ERROR)

    def _launch_file_b(self):
        """
        Launch a file selector dialog
        """
        types = [
            ("JPG", "*.jpg"),
            ("Bitmap", "*.bmp"),
            ("PNG", "*.png"),
            ("GIF", "*.gif"),
            ("All files", "*")]
        dialog = tkFileDialog.Open(self, filetypes = types)
        self._file_path = dialog.show()

        self._file_name = self._scrub_name(self._file_path)
        self._move_img()
        return self._file_name

    def _move_img(self):
        if self._auto_move is False:
            return
        # Else, move the image to the given folder that is in the same dir as this module
        try:
            src = self._file_path
            dest = os.path.dirname(os.path.realpath(__file__)) +"/" + self._file_name
            shutil.copy(src, dest)
            Debug.printi("Moving file " + self._file_path + " to location "
                         + os.path.dirname(os.path.realpath(__file__))
                         + self._file_name, Debug.Level.INFO)
        # eg. src and dest are the same file
        except shutil.Error as e:
            print('Error: %s' % e + " " +dest)
        # eg. source or destination doesn't exist
        except IOError as e:
            print('Error: %s' % e.strerror +" "+ dest)

    def _scrub_name(self, file_path):
        """
        Override: Parse and clean the filename
        """
        split = self._file_path.split("/")
        if self._auto_move is True:
            f_name = self._folder[1:] + split[-1]
        else:
            f_name = split[-1]
        return f_name

    def _load_img_label(self):
        """
        Changes the text in the widget label to the (adjusted) filepath of the image
        """
        name = self._launch_file_b()
        self._img_label.configure(text=name)

    def get(self):
        return self._file_name

    def set(self, val):
        self._file_name = val
        self._img_label.config(text=val)

class StatusBar(Frame, OutputPipe):
    """
    A basic definition for a statusBar style widget that can be updated
    during runtime
    This class has been derived from the link at the header of this file
    """

    def __init__(self, parent, text_link=None):
        """
        Construct the status bar instance

        :parent:        The parent tk widget that the taskbar should sit in
        :text_link:     Allows the user to supply there own undoable text value
        """
        Frame.__init__(self, parent)
        if text_link is None:
            text_link = StringVar(value="Running")
        self._text = text_link
        self._label = Label(self, bd=1, relief=SUNKEN, anchor=W, textvariable=self._text)
        self._label.pack(fill=X)

    def set_text_f(self, format, *args):
        """
        Set the text of the status bar with formatting

        :format: The formatting string to use
        """
        self._text.set(format % args)
        self.change_bg("green")
        self._label.update_idletasks()

    def set_text(self, text):
        """
        Set the text of the status bar
        """
        self.set_text_f("%s", text)

    def alert(self, msg, level):
        """
        Posts text to the status bar, and colours the background based on an alert level
        """
        self.set_text(msg)
        if level is Debug.Level.INFO:
            self.change_bg("green")
        elif level is Debug.Level.ERROR:
            self.change_bg("yellow")
        else:
            self.change_bg("red")


    def clear(self):
        self.set_text("%s", "")

    def change_bg(self, colour):
        self._label.config(bg=colour)

class Dialog(Toplevel):
    """
    A definition for a dialog style widget
    This class has been derived from the link at the header of this file
    """
    def __init__(self, parent, title="MazeBuilder Dialog", lock_focus=True, x=None, y=None, populator=None, manager=None):
        """
        Construct the instance of the dialog

        :parent:                The parent widget that spawns the dialog
        :title:                 The title of the dialog that will be used in the header bar
        :lock_focus:            Bind the focus of the mouse to this window until it is dismissed
        :x:                     The x coord to launch the dialog at
        :y:                     The y coords to launch the dialog at
        :populator:             THe population parameters for the dialog
        :type manager: DataStore
        """
        Toplevel.__init__(self, parent)
        self.title(title)
        self.transient(parent)
        self._manager = manager
        if title:
            self._title = title
        self.parent = parent
        self.result = None
        body = Frame(self)
        if populator is not None:
            self.populate(populator)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()

        # Needed to grab the window on Linux machines
        while True:
            try:
                self.grab_set()
            except TclError:
                continue
            else:
                break

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", lambda: Debug.printi("Window Close Disabled", Debug.Level.ERROR))
        if x is None and y is None:
            self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        else:
            self.geometry("+%d+%d" % (x + 1,
                                      y + 1))
        self.initial_focus.focus_set()

        if lock_focus:
            self.wait_window(self)


    """
    Construction Hooks
    """

    def body(self, parent):
        """
        Override: Create the dialogue body with this function
        :param parent:
        :return:
        """
        pass

    def populate(self, manager):
        """
        Override: Define a population plan to fill all of the required entries for this widget
        :param manager:               The population parameters for the widget
        """
        pass

    def buttonbox(self):
        """
        Defines the standard button box.
        Override if you want a custom one
        :return:
        """

        box = Frame(self)
        b = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        b.pack(side=LEFT, padx=5, pady=5)
        #w = Button(box, text="Cancel", width=10, command=self.cancel)
        a= Button(box, text="Autofill", width=10, command=self.auto_populate, default=ACTIVE)
        a.pack(side=LEFT, padx=5, pady=5)
        #w.pack(side=LEFT, padx=5, pady=5)
        #w["state"] = DISABLED


        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    """
    Button Semantics
    """

    def ok(self, event=None):
        """
        Callback function to be launched when the (OK) button is pressed
        """
        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    """
    Command Hooks
    """

    def validate(self):
        """
        Override: Create validation paramaters for the information gathered by the dialog
        """
        return 1

    def apply(self):
        """
        Apply the results, information gathered by the dialog
        """
        pass

    def auto_populate(self):
        """
        Autopopulate the fields in the dialog
        This function is activated with the spacebar when in a dialog
        """
        Debug.printi("Call to autopopulater registered")

class ImageViewDialog(Dialog):
    """
    A basic dialog that displays some image
    """
    def __init__(self, parent, f_name, photo):
        """
        Construct the instance of the image viewer

        :f_name:    The file name of the image, to be used as the dialog title
        :photo:     The image that is to be displayed
        """
        self._photo = photo
        Dialog.__init__(self, parent, f_name, True)

    def body(self, parent):
        """
        Overridden, defines the construction of the meat of the ImageViewingDIalog
        """
        img = Label(parent, image = self._photo, text="Unable to display image")
        img.pack()


class ListHeap(Frame):
    """
    A widget that encapsulates a list box, allow adding and delete and contextual interaction
        with a set of items in a list box
    """

    def __init__(self, parent, populator, max_limit=sys.maxint):
        """

        :param parent:          The parent tk item
        :param max_limit:       The maximum number of items allowed to be added to the listheap
        :return:
        """
        Frame.__init__(self, parent)
        self._items = {}
        self._parent = parent
        self._max_limit = max_limit
        self._listbox = Listbox(self, selectmode=SINGLE)
        self._listbox.grid(row=0, column=0)

        # Bind mouse events
        self._listbox.bind("<Double-Button-1>", self._handle_db_click)
        self._listbox.bind("<Button-2>", self._handle_r_click)

        # Populate the widget with custom params if they are available
        if populator is not None:
            self.populate(populator)

    def populate(self, populator):
        """
        Override to define the population paramaters for this widget
        This allows default values to be provided
        """
        pass

    def add_new(self, item, key):
        """
        Add new item to the list heap

        Adds a new item to the list box and the data structure that defines the heap

        :param item:            The item to be added to the ListHeap
        :param key:             The key that is to be used to identify the item, must be unique
        :throws:                DuplicateListHeapItemException  - duplicate key attempted to add to the heap
        :throws:                MaxItemLimitReachedException    - Attempted item addition when max sized already reached
        """
        if key in self._items:
            raise DuplicateListHeapItemException(key)
        if len(self._items) >= self._max_limit:
            raise MaxItemLimitReachedException()
        self._items[key] = item
        self._listbox.insert(END, key)

    def _remove(self, key):
        """
        Remove an item from the ListHeap
        :param key:             The key of the item that is to be removed
        """
        del self._items[key]
        self._listbox.delete(ANCHOR)

    def _remove_all(self):
        """
        Removes all of the items from the ListHeap
        """
        self._items.clear()
        self._listbox.delete(0, END)

    def _handle_db_click(self, event):
        """
        Override: define a handler for the doubleclick event on the ListHeap
        :param event:           The tk event generated by user input
        """
        pass

    def _handle_r_click(self, event):
        """
        Override: Define a handler for the rightclick event on the ListHeap
        :param event:           The tk event generated by user input
        """
        pass