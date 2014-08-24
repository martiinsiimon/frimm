"""
"""

from graphics import Graphics

class Image(Graphics):
    """
    Image object. This class is meant to perform store and load file operations of image files.
    TODO:
        setData() -- inherited
        getData() -- inherited
        setColorModel() -- inherited
        getColorModel() -- inherited
        convertColorModel() -- inherited
        dumpImageInformation() -- inherited
        storeImage()
        loadImage()
    """

    def __init__(self):
        pass


class Camera(Graphics):
    """
    Camera object. This object provides operation needed to get data from inbuild or other attached real-time camera.
    TODO:
        setData() -- inherited
        getData() -- inherited
        setColorModel() -- inherited
        getColorModel() -- inherited
        convertColorModel() -- inherited
        dumpImageInformation() -- inherited
        getFrame()
        getCameraInformation() -- or more methods
    """

    def __init__(self):
        pass

class Video(Graphics):
    """
    Video object. This class is similar to Image object, but handles video files. Rather than store and load images provides functions to load and store videos, get next frame and so on.
    TODO:
        setData() -- inherited
        getData() -- inherited
        setColorModel() -- inherited
        getColorModel() -- inherited
        convertColorModel() -- inherited
        dumpImageInformation() -- inherited
        loadVideo()
        modifyFrame()
        getFrame()
        getNextFrame()
        getVideoInformation() -- or more methods
    """
    
    def __init__(self):
        pass
