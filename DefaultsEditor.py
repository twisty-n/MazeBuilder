__author__ = 'Tristan Newmann'

"""
MazeBuilder, Stroke Recovery Project, HMRI
Author: Tristan Newmann
Developed with 2.7

File: Defaults.py

Specifies default values to be used for autopopulation
"""

import inspect, sys
import Defaults
import tkMessageBox
from Tkinter import Label, Entry, W, E, Frame, LEFT, SUNKEN, GROOVE
from UtilWidgets import Dialog
import Debug

class DefaultsEditorDialog(Dialog):

    def __init__(self, parent):
        self._entries = {}
        Dialog.__init__(self, parent, "Default Values Editor")

    def body(self, parent):

        tkMessageBox.showwarning("Edit Warning", "WARNING: For advanded users only.\nEntered values are not checked, "
                                                 "and may cause XML errors. Change at your own risk")

        try:
            params, self._class_names = load_defaults()
        except:
            tkMessageBox.showerror("Error", "Error loading default values. Aborting...")
            return

        Label(parent, text="Category", anchor=W, width=12).grid(row=0, column=0, stick=E)
        Label(parent, text="Variable", padx=5, anchor=W, width=20).grid(row=0, column=1, stick=E)
        Label(parent, text="Value", anchor=W).grid(row=0, column=2, sticky=W)
        i = 0
        for key, val in params.iteritems():
            i+=1
            for item in val:
                i+=1
                lab1=Label(parent, text=key, width=12, anchor=W, pady=0)
                lab1.grid(column=0, sticky=E, row=i)
                lab2=Label(parent, pady=0, text=item[0], padx=5, width=20, anchor=W)
                lab2.grid(column=1, sticky=E, row=i)
                self._entries[(key, item[0])] = Entry(parent, width=15, relief=GROOVE)
                self._entries[(key, item[0])].insert(0, str(item[1]))
                self._entries[(key, item[0])].grid(column=2, row=i, sticky=W)


    def apply(self):
        mappings = {}
        for name in self._class_names:
            mappings[name] = []
        for key, item in self._entries.iteritems():
            mappings[key[0]].append(str(key[1]) + "=" + ((str(item.get())) if "False" in item.get() or "True" in item.get() else "\"" + str(item.get()) + "\""))
        Debug.printi("Writing new default configurations")
        try:
            defaults_file = open("Defaults.py", "w")
            for key, item in mappings.iteritems():
                defaults_file.write(
                    "class " +key + ":" + "\n" + "".join(["\t" + str(set_p) + "\n" for set_p in item])
                )
            defaults_file.close()
        except IOError as e:
            Debug.printi(str(e) + "\n Please use backup file to restore Defaults.py", Debug.Level.FATAL)



    def validate(self):
        return True


def load_defaults():
    clsmembers = inspect.getmembers(Defaults, inspect.isclass)
    classes = {}
    names = []
    for cls in clsmembers:
        classes[cls[0]] = [val for val in cls[1].__dict__.iteritems() if "__" not in val[0]]

    return classes, [c[0] for c in clsmembers]


if __name__ == "__main__":
    load_defaults()