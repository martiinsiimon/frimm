#-*- coding: UTF-8 -*-
"""
TODO:
    finish signal handlers
"""
import os
import sys
from gi.repository import Gtk

class MainWindow(object):
    def __init__(self):
        if os.path.exists('../data/window.ui'):
            self.gladefile = '../data/window.ui'
        else:
            path = os.path.abspath(
                os.path.join(__file__, os.path.pardir, os.path.pardir))
            if path is '/': # in case the path is /bin/frimm
                path = '/usr'
            self.gladefile = path + '/share/frimm/ui/window.ui'

        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('mainwindow')

        if os.path.exists('../data/icons/frimm.png'):
            self.window.set_icon_from_file('../data/icons/frimm.png')
        else:
            path = os.path.abspath(
                os.path.join(__file__, os.path.pardir, os.path.pardir))
            if path is '/':
                path = '/usr'
            self.window.set_icon_from_file(os.path.join(path,
                'share/icons/hicolor/48x48/apps/frimm.png'))

        self.window.show_all()

    def on_main_window_destroy(self, object, data=None):
        print("DBG: on_main_window_destroy")
        sys.exit()
    
    def on_result_area_draw(self, object, data=None):
        print("DBG: on_result_area_draw")
    
    def on_original_area_button_press_event(self, object, data=None):
        print("DBG: on_original_area_button_press_event")
    
    def on_original_area_draw(self, object, data=None):
        print("DBG: on_original_area_draw")
    
    def on_quit_button_clicked(self, object, data=None):
        print("DBG: on_quit_button_clicked")
        sys.exit()
    
    def on_proceed_button_clicked(self, object, data=None):
        print("DBG: on_proceed_button_clicked")
    
    def on_export_button_clicked(self, object, data=None):
        print("DBG: on_export_button_clicked")
    
    def on_load_button_clicked(self, object, data=None):
        print("DBG: on_load_button_clicked")
    
    
