"""
Graphics module. Consists of object which represent graphic objects.
"""
import cairo
import array


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
        self.width = data.get_width()
        self.height = data.get_height()
        self.data = self._from_cairo_to_internal(data)
        self.color_format = data.get_format()
        self.pixel_width = COLOR_MODEL[self.color_format]['pixel_width']

        self.r_offset = COLOR_MODEL[self.color_format]['r']
        self.g_offset = COLOR_MODEL[self.color_format]['g']
        self.b_offset = COLOR_MODEL[self.color_format]['b']

        self.dirty = False

    @staticmethod
    def _from_cairo_to_internal(input_data):
        """
        Convert given cairo data to internal data
        :param input_data: input cairo buffer
        """
        data = input_data.get_data()
        return array.array('B', data.__str__())

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
        open()
        getFrame()
        getCameraInformation() -- or more methods
    """

    def __init__(self):
        pass


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
