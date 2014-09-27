"""
Graphics module. Consists of object which represent graphic objects.
"""
import cairo
import array
from pygame import camera
import pygame


ARGB = 0
RGB24 = 1
COLOR_MODEL = \
    {0: {'name': 'ARGB', 'pixel_width': 4, 'a': 3, 'r': 2, 'g': 1, 'b': 0},
     1: {'name': 'RGB24', 'pixel_width': 4, 'a': 3, 'r': 2, 'g': 1, 'b': 0}}

OUTPUT_COLOR_MODEL = RGB24


class Frame(object):
    """
    Object representing image frame. Its used in image, video and camera stream
    """

    def __init__(self, data):
        self.data, self.width, self.height = self._from_external_to_internal(data)
        self.color_format = data.get_format()
        self.pixel_width = COLOR_MODEL[self.color_format]['pixel_width']

        self.r_offset = COLOR_MODEL[self.color_format]['r']
        self.g_offset = COLOR_MODEL[self.color_format]['g']
        self.b_offset = COLOR_MODEL[self.color_format]['b']

        self.dirty = False

    def _from_external_to_internal(self, data):
        if isinstance(data, cairo.ImageSurface):
            return self._from_cairo_to_internal(data)
        elif isinstance(data, pygame.Surface):
            return self._from_pygame_to_internal(data)

    @staticmethod
    def _from_cairo_to_internal(input_data):
        """
        Convert given cairo data to internal data
        :param input_data: input cairo.ImageSurface
        """
        data = input_data.get_data()
        width = input_data.get_width()
        height = input_data.get_width()
        return array.array('B', data.__str__()), width, height

    @staticmethod
    def _from_pygame_to_internal(input_data):
        """
        Convert given pygame data to internal data
        :param input_data: input pygame.Surface
        """
        data = input_data.raw
        width, height = input_data.get_size()
        return array.array('B', data.__str__()), width, height

    def update_cairo(self, data_pointer):
        """
        Update cairo data from internal buffer to the given pointer
        :param data_pointer: pointer to cairo buffer
        """
        self.dirty = False

        data_pointer[:] = buffer(self.data)


class Image(object):
    """
    Image object. This class is meant to perform store and load file
    operations of image files.
    """

    def __init__(self, filename, filetype):
        self.filetype = filetype
        self.filename = filename
        self.cairo_image_surface = None
        self.data = None
        self.width = 0
        self.height = 0
        self.load()

    def load(self):
        """
        Load image from given. Currently, only PNG files are supported
        """
        if self.filetype == 'png':
            self.cairo_image_surface = \
                cairo.ImageSurface.create_from_png(self.filename)
            self.data = Frame(data=self.cairo_image_surface)
            self.width = self.data.width
            self.height = self.data.height
        else:
            raise TypeError('Not supported file type!')

    def store(self, new_filename=None):
        """
        Store this object as image of type PNG. If no new filename is
        provided, old filename extended with '_new' wil be used
        :param new_filename: name of output file
        """
        if self.cairo_image_surface:
            if not new_filename:
                new_filename = self.filename + '_new'

            if self.filetype == 'png':
                self.cairo_image_surface.write_to_png(new_filename)
            else:
                raise TypeError('Not supported file type!')

    @property
    def cairo_data(self):
        """
        Property returning updated cairo buffer
        """
        if self.data.dirty:
            self.data.update_cairo(self.cairo_image_surface.get_data())
        return self.cairo_image_surface

    @cairo_data.setter
    def cairo_data(self, value):
        """
        Property setter for cairo_data
        :param value: New cairo buffer to be set
        """
        self.cairo_image_surface = value


class Camera(object):
    """
    Camera object. This object provides operation needed to get data from
    built-in or any other attached real-time camera.
    TODO:
        convertColorModel()
        dumpImageInformation()
        getFrame()
        getCameraInformation() -- or more methods
    """

    def __init__(self, device):
        self.devicename = device
        self.data = None
        self.cairo_image_surface = None
        pygame.init()
        camera.init()
        self.camera = camera.Camera(self.devicename)
        self.width, self.height = self.camera.get_size()

        self.camera.start()

    def get_frame(self):
        self.cairo_image_surface = \
            cairo.ImageSurface.create_for_data(self.camera.get_buffer(), self.width, self.height, OUTPUT_COLOR_MODEL)
        self.data = Frame(data=self.cairo_image_surface)

    def stop(self):
        self.camera.stop()
        camera.quit()

    @property
    def cairo_data(self):
        """
        Property returning updated cairo buffer
        """
        if self.data.dirty:
            self.data.update_cairo(self.cairo_image_surface.get_data())
        return self.cairo_image_surface

    @cairo_data.setter
    def cairo_data(self, value):
        """
        Property setter for cairo_data
        :param value: New cairo buffer to be set
        """
        self.cairo_image_surface = value


def list_cameras():
    camera.init()
    return camera.list_cameras()


class Video(object):
    """
    Video object. This class is similar to Image object, but handles video
    files. Rather than store and load images provides functions to load
    and store videos, get next frame and so on.
    TODO:
        convertColorModel()
        dumpImageInformation()
        load()
        store()
        modifyFrame()
        getFrame()
        getNextFrame()
        getVideoInformation() -- or more methods
    """

    def __init__(self):
        pass
