#!/bin/python
# Simple GTK selector with filters similar to dmenu
# A. Schlemmer, 11/2020

import gi
gi.require_version("Gtk", "3.0")  # noqa: E402
from gi.repository import Gtk
from gi.repository import Gdk

import os
import sys


class Application(object):

    def __init__(self):
        """
        Initialize the application by loading the objects from the glade file,
        setting up the event handlers and initializing some application-wide
        variables.

        Finally show the window and run the gtk main loop.
        """
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialog.glade"))

        store = builder.get_object("store")
        for g in sys.stdin.readlines():
            store.append((g.strip(),))
        self.tree = builder.get_object("tree")

        handlers = {
            "close_application": self.close_application,
            "set_filter": self.set_filter,
            "row_activated": self.row_activated,
            "ok_application": self.ok_application,
            "key_pressed": self.key_pressed
        }
        builder.connect_signals(handlers)

        self.treefilter = builder.get_object("treemodelfilter1")
        self.treefilter.set_visible_func(self.list_filter)

        self.filtertext = ""
        self.selected = ""

        self.main_window = builder.get_object("window")
        self.main_window.connect("destroy", Gtk.main_quit)
        self.main_window.show_all()
        Gtk.main()

    def close_application(self, widget):
        Gtk.main_quit()

    def ok_application(self, widget):
        """
        Action run for the OK button:
        - If nothing is selected, select the first shown entry.
        - Print the selected entry to stdout.
        - Quit the application and close the dialog.
        """
        if len(self.selected) == 0:
            el_first = self.treefilter.get_iter_first()
            if el_first is not None:
                self.selected = self.treefilter.get_value(el_first, 0)
        print(self.selected)
        Gtk.main_quit()

    def key_pressed(self, widget, ev, data=None):
        """
        Handlers for some keys:
        - ENTER: press the OK button
        - ESCAPE: press the CANCEL button
        """
        if ev.keyval == Gdk.KEY_Escape:
            self.close_application(widget)
        elif ev.keyval == Gdk.KEY_Return:
            self.ok_application(widget)

    def set_filter(self, widget):
        """
        Set the tree filter to the text in the entry box.
        Afterwards do a refiltering.
        """
        self.filtertext = widget.get_text()
        self.treefilter.refilter()

    def list_filter(self, model, iter, data):
        """
        Definition of the filter.

        Currently set to case insensitive text filtering.
        """
        if self.filtertext.lower() not in model[iter][0].lower():
            return False
        return True

    def row_activated(self, widget):
        """
        Set the selection.
        """
        (model, node) = self.tree.get_selection().get_selected()
        self.selected = model.get_value(node, 0)


if __name__ == "__main__":
    Application()
