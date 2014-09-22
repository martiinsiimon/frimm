"""
Graphics module. Consists of object which represent graphic objects.
"""
import cairo

ARGB=0
RGB24=1
COLOR_MODEL = \
    {0: {'name' : 'ARGB', 'pixel_width' : 4, 'a' : 3, 'r' : 2, 'g' : 1, 'b' : 0},\
     1: {'name' : 'RGB24', 'pixel_width' : 4, 'a' : 3, 'r' : 2, 'g' : 1, 'b' : 0}}

OUTPUT_COLOR_MODEL=RGB24

class Pixel(object):
    '''
    '''
    def __init__(self, r=0, g=0, b=0, a=0, v=0):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = v
        self.value = v
    
    @property
    def r(self):
        return self.red

    @r.setter
    def r(self, value):
        self.red = int(round(value))

    @property
    def g(self):
        return self.green

    @g.setter
    def g(self, value):
        self.green = int(round(value))

    @property
    def b(self):
        return self.blue

    @b.setter
    def b(self, value):
        self.blue = int(round(value))

    @property
    def a(self):
        return self.alpha

    @a.setter
    def a(self, value):
        self.alpha = int(round(value))

    @property
    def v(self):
        return self.value
        
    @v.setter
    def v(self, value):
        self.value = int(round(value))
        self.r = int(round(value))
        self.g = int(round(value))
        self.b = int(round(value))
        self.a = int(round(value))
        

class Frame(object):
    '''
    '''
    def __init__(self, data=None):
        if data:
            self.width = data.get_width()
            self.height = data.get_height()
            self.data = self._from_cairo_to_internal(data)
        else:
            self.data = []
            self.width = 0
            self.height = 0
            
        self.dirty = False
        

    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        self.data.insert(index, value)
        self.dirty = True

    def _from_cairo_to_internal(self, input_data):
        '''
        Convert given cairo data to internal data
        '''
        data = input_data.get_data()
        color_format = input_data.get_format()
        pixel_width = COLOR_MODEL[color_format]['pixel_width']
        output = []

        total_width = self.width * pixel_width
        
        if color_format  == ARGB:
            for y in range(0, self.height):
                for x in range(0, total_width, pixel_width):
                    pix = Pixel()
                    pix.r = ord(data[y * total_width + x + COLOR_MODEL[color_format]['r']])
                    pix.g = ord(data[y * total_width + x + COLOR_MODEL[color_format]['g']])
                    pix.b = ord(data[y * total_width + x + COLOR_MODEL[color_format]['b']])
                    pix.a = ord(data[y * total_width + x + COLOR_MODEL[color_format]['a']])
                    output.insert(y * self.width + x/pixel_width, pix)
        elif color_format == RGB24:
            for y in range(0, self.height):
                for x in range(0, total_width, pixel_width):
                    pix = Pixel()
                    pix.r = ord(data[y * total_width + x + COLOR_MODEL[color_format]['r']])
                    pix.g = ord(data[y * total_width + x + COLOR_MODEL[color_format]['g']])
                    pix.b = ord(data[y * total_width + x + COLOR_MODEL[color_format]['b']])
                    output.insert(y * self.width + x/pixel_width, pix)
        else:
            assert RuntimeError, 'No other color format is supported!'
        
        return output

    def update_cairo(self, data_pointer, format_pointer):
        '''
        Update cairo data from internal buffer to the given pointer
        '''
        pixel_width = COLOR_MODEL[OUTPUT_COLOR_MODEL]['pixel_width']
        
        for y in range(0, self.height):
            for x in range(0, self.width):
                pix = self[y * self.width + x]

                data_pointer[y * self.width * pixel_width + x * pixel_width + COLOR_MODEL[OUTPUT_COLOR_MODEL]['r']] = chr(pix.r)
                data_pointer[y * self.width * pixel_width + x * pixel_width + COLOR_MODEL[OUTPUT_COLOR_MODEL]['g']] = chr(pix.g)
                data_pointer[y * self.width * pixel_width + x * pixel_width + COLOR_MODEL[OUTPUT_COLOR_MODEL]['b']] = chr(pix.b)
                data_pointer[y * self.width * pixel_width + x * pixel_width + COLOR_MODEL[OUTPUT_COLOR_MODEL]['a']] = chr(255) #  unused
        
        self.dirty = False

        format_pointer = OUTPUT_COLOR_MODEL

    def get_cairo_data(self, color_format):
        '''
        Return converted data to cairo format
        '''
        return self._from_internal_to_cairo(self.data, color_format)


class Image(object):
    """
    Image object. This class is meant to perform store and load file
    operations of image files.
    TODO:
        convertColorModel()
        dumpImageInformation()
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
        if self.data.dirty:
            self.data.update_cairo(self.cairo_image_surface.get_data(), self.cairo_image_surface.get_format())
        return self.cairo_image_surface
    
    @cairo_data.setter
    def cairo_data(self, value):
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
