# -*- coding: UTF-8 -*-
"""
FRIMM module containing main window class
"""
import os

from gi.repository import Gtk
from graphics import Image
from config import Configuration
from filters import Filters
import time


class MainWindow(object):
    """
    MainWindow class handles GUI of FRIMM. It does not contain any functional
    parts
    """

    def __init__(self, exe_path):
        if os.path.exists('../data/window.ui'):
            self.gladefile = '../data/window.ui'
        elif os.path.exists('data/window.ui'):
            self.gladefile = 'data/window.ui'
        else:
            path = os.path.abspath(
                os.path.join(exe_path, os.path.pardir, os.path.pardir))
            if path is '/':  # in case the path is /bin/frimm
                path = '/usr'
            self.gladefile = path + '/share/frimm/ui/window.ui'

        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('mainwindow')

        if os.path.exists('../data/icons/frimm.png'):
            self.window.set_icon_from_file('../data/icons/frimm.png')
        elif os.path.exists('data/icons/frimm.png'):
            self.window.set_icon_from_file('data/icons/frimm.png')
        else:
            path = os.path.abspath(
                os.path.join(exe_path, os.path.pardir, os.path.pardir))
            if path is '/':
                path = '/usr'
            self.window.set_icon_from_file(
                os.path.join(path,
                             'share/icons/hicolor/48x48/apps/frimm.png'))

        self.original_image = None
        self.result_image = None

        self.config = Configuration()
        self.config.restore()
        self.filters = Filters(self.config)

        self.filter_author_label = \
            self.builder.get_object('filter_author_label')
        self.filter_description_textview = \
            self.builder.get_object('filter_description_textview')
        self.filter_details_box = \
            self.builder.get_object('filter_details_box')
        self.statusbar = \
            self.builder.get_object('statusbar')
        self.statusbar_context_id = \
            self.statusbar.get_context_id('statusbar_note')
        self.comboboxfilter = \
            self.builder.get_object('comboboxfilter')
        self.filters_liststore = None

        self.update_filters_combobox()

        self.window.show_all()

    @staticmethod
    def on_main_window_destroy(window):
        Gtk.main_quit()

    def on_comboboxfilter_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            selected_name, selected_key = model[tree_iter]
            if selected_key == 'no_filter':
                self.filters.active = None
                self.filter_details_box.set_visible(False)
            else:
                self.filters.active = self.filters[selected_name]
                self.filter_author_label.set_text(
                    self.filters.active.author_name)
                textbuffer = Gtk.TextBuffer()
                textbuffer.set_text(self.filters.active.description)
                self.filter_description_textview.set_buffer(textbuffer)
                self.filter_details_box.set_visible(True)

    def on_result_area_draw(self, screen, cairo_context):
        if not self.result_image:
            return

        win_w = screen.get_allocated_width()
        win_h = screen.get_allocated_height()

        img_w = self.result_image.width
        img_h = self.result_image.height

        win_ratio = win_w / float(win_h)
        img_ratio = img_w / float(img_h)

        if img_ratio > win_ratio:
            scale = win_w / float(img_w)
        else:
            scale = win_h / float(img_h)

        cairo_context.translate(
            (win_w / 2.0) - ((img_w * scale) / 2.0),
            (win_h / 2.0) - ((img_h * scale) / 2.0))
        cairo_context.scale(scale, scale)

        cairo_context.set_source_surface(self.result_image.cairo_data, 0, 0)
        cairo_context.paint()

    def on_original_area_press_event(self, drawing_area, button):
        if not self.original_image:
            return

    def on_original_area_draw(self, screen, cairo_context):
        if not self.original_image:
            return

        win_w = screen.get_allocated_width()
        win_h = screen.get_allocated_height()

        img_w = self.original_image.width
        img_h = self.original_image.height

        win_ratio = win_w / float(win_h)
        img_ratio = img_w / float(img_h)

        if img_ratio > win_ratio:
            scale = win_w / float(img_w)
        else:
            scale = win_h / float(img_h)

        cairo_context.translate(
            (win_w / 2.0) - ((img_w * scale) / 2.0),
            (win_h / 2.0) - ((img_h * scale) / 2.0))
        cairo_context.scale(scale, scale)

        cairo_context.set_source_surface(self.original_image.cairo_data, 0, 0)
        cairo_context.paint()

    def on_quit_button_clicked(self, button):
        Gtk.main_quit()

    def on_proceed_button_clicked(self, button):
        if not self.original_image:
            self.update_statusbar(
                'You need to load a source before filter execution!')
            return

        if not self.filters.active:
            self.update_statusbar('You need to set filter first!')
            return

        self.result_image = \
            Image(filename=self.original_image.filename, filetype='png')

        self.result_image.cairo_image_surface.flush()

        total_time = self.filters.execute_active(self.original_image.data,
                                                 self.result_image.data)
        self.result_image.data.dirty = True

        self.result_image.cairo_image_surface.mark_dirty()
        win = self.builder.get_object('result_area').get_window()
        win.invalidate_rect(None, False)

        msg = 'Filter \'%s\' executed.' % self.filters.active.name
        if self.config['measure']:
            msg += ' Total time: %f' % total_time
        self.update_statusbar(msg)

    def on_export_button_clicked(self, button):
        if not self.result_image:
            self.update_statusbar(
                'You need to execute filtering before exporting results!')
            return

        dialog = Gtk.FileChooserDialog(
            'Save file', self.window,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filter_png = Gtk.FileFilter()
        filter_png.set_name('PNG Image')
        filter_png.add_mime_type('image/png')
        dialog.add_filter(filter_png)

        res = dialog.run()
        if res == Gtk.ResponseType.OK:
            if dialog.get_filter().get_name() == 'PNG Image':
                filename = dialog.get_filename()
                if not filename.endswith('.png'):
                    filename = "%s.png" % filename
                self.result_image.store(filename)
            else:
                pass

        dialog.destroy()

    def on_load_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            'Open file', self.window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter_png = Gtk.FileFilter()
        filter_png.set_name('PNG Image')
        filter_png.add_mime_type('image/png')
        dialog.add_filter(filter_png)

        res = dialog.run()
        if res == Gtk.ResponseType.OK:
            if dialog.get_filter().get_name() == 'PNG Image':
                start_time = time.time()
                self.original_image = \
                    Image(filename=dialog.get_filename(), filetype='png')
                end_time = time.time()
                self.update_statusbar(
                    "Total time to load: %f" % (end_time - start_time))
            else:
                pass

        dialog.destroy()

    def update_statusbar(self, text):
        """
`       Set given text to statusbar
        :param text: statusbar message
        """
        self.statusbar.remove_all(self.statusbar_context_id)
        self.statusbar.push(self.statusbar_context_id, text)

    def update_filters_combobox(self):
        self.filters.refresh()
        self.filters_liststore = Gtk.ListStore(str, str)
        if len(self.filters) > 0:
            self.filters_liststore.append(['Select filter', 'no_filter'])
            for filtname in self.filters:
                self.filters_liststore.append([filtname, filtname])
        else:
            self.filters_liststore.append(['No filter found!', 'no_filter'])
        self.comboboxfilter.set_model(self.filters_liststore)
        self.comboboxfilter.set_active(0)
