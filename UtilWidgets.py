__author__ = 'tristan_dev'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: MazeBuilder.py
Classes based on those listed in
http://effbot.org/tkinterbook/tkinter-application-windows.htm
"""

from Tkinter import SUNKEN, W, Label, X, Frame, Toplevel, \
    ACTIVE, Button, LEFT, E, Canvas
import tkFileDialog
from PIL import Image, ImageTk
import Debug


#TODO add in a populate method which fills dialogues from the
#database

class ImagePicker(Frame):
    """
    A custom widget that allows for the selection and preview of a picture
    """
    def __init__(self, parent, label, default="No File Selected"):
        Frame.__init__(self, parent)
        self._image_ref = None
        self._file_name = None
        self._file_path = None
        self._parent = parent

        #Text label
        self._label = Label(self, text=label)
        self._label.grid(row=0, column=0, sticky=E, padx=2)
        self._label.config(width=10)

        #The label that displays the name of the selected file
        self._img_label = Label(self, text=default)
        self._img_label.config(width=15)
        self._img_label.grid(row=0, column=1, sticky=W)

        #Button that enables the previewing of the loaded picture
        self._pButton = Button(self, text="Preview", command=self._display_img, padx=5)
        self._pButton.config(width=8)
        self._pButton.grid(row=0, column=3, sticky=W)

        #Button that enables the loading of files
        self._fButton = Button(self, text="|...|", command=self._load_img_label, padx=5)
        self._fButton.config(width=4)
        self._fButton.grid(row=0, column=2)



    def _display_img(self):
        if self._file_path is None:
            Debug.printi("No picture has been loaded to preview", Debug.Level.ERROR)
            return
        photo = self._open_img(self._file_path)
        view = ImageViewDialog(self._parent, self._file_name, photo)


    def _open_img(self, img_name):
        try:
            img = Image.open(img_name)
            photo = ImageTk.PhotoImage(img)
            return photo
        except IOError:
            Debug.printi("Unable to find image " + img_name, Debug.Level.ERROR)

    def _launch_file_b(self):
        types = [
            ("JPG", "*.jpg"),
            ("Bitmap", "*.bmp"),
            ("PNG", "*.png"),
            ("GIF", "*.gif"),
            ("All files", "*")]
        dialog = tkFileDialog.Open(self, filetypes = types)
        self._file_path = dialog.show()

        #Now we clean the file name
        split = self._file_path.split("/")
        self._file_name = "Data/" + split[-1]
        return self._file_name

    def _load_img_label(self):
        name = self._launch_file_b()
        self._img_label.configure(text=name)

class StatusBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self._label.pack(fill=X)

    def set_text_f(self, format, *args):
        self._label.config(text=format % args)
        self._label.update_idletasks()

    def set_text(self, text):
        self.set_text_f("%s", text)

    def clear(self):
        self.set_text("%s", "")

class Dialog(Toplevel):
    def __init__(self, parent, title="MazeBuilder Dialog", lock_focus=True):
        Toplevel.__init__(self, parent)
        self.title(title)
        self.transient(parent)

        if title:
            self._title = title
        self.parent = parent
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
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

    def buttonbox(self):
        """
        Defines the standard button box.
        Override if you want a custom one
        :return:
        """

        box = Frame(self)
        b = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        b.pack(side=LEFT, padx=5, pady=5)
        w=Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    """
    Button Semantics
    """

    def ok(self, event=None):

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
        return 1

    def apply(self):
        pass

class ImageViewDialog(Dialog):

    def __init__(self, parent, f_name, photo):
        self._photo = photo
        Dialog.__init__(self, parent, f_name, True)

    def body(self, parent):
        img = Label(parent, image = self._photo, text="Unable to display image")
        img.pack()