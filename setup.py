#!/usr/bin/env python2
from distutils.core import setup
from distutils.command.bdist_rpm import bdist_rpm

def tests():
    import os
    exList = os.listdir(os.curdir + '/tests/')
    result = []
    for ex in exList:
        if ex.split('.')[-1] == 'py':
            result = result + ['tests/' + ex]
    return result

def icons(ext_tuple):
    import os
    list = os.listdir(os.curdir + '/data/icons/')
    result = []
    for file in list:
        if file.split('.')[-1] in ext_tuple:
            result = result + ['data/icons/' + file]
    return result

setup (
        name = 'frimm',
        version = '0.1-alpha1',
        description = """FRIMM - Framework for Image Manipulation is a easy to use tool which provides clean API to develop own image filter and see results in real time. It also show some measurements of filter operation..""",
        author = 'Martin Simon',
		author_email = 'martiin.siimon@gmail.com',
        url = 'http://github.com/martiinsiimon/frimm',
        packages = ['frimm'],
		scripts = ['scripts/frimm'],
        data_files = [
        #                        ('share/doc/waktu/tests',
        #                                tests() ),
                                ('share/frimm/ui', ['data/window.ui']),
								('share/frimm/data', ['data/logo.png']),
                                ('share/applications', ['data/frimm.desktop']),
                                ('share/icons/hicolor/48x48/apps', icons('png')),
                                ('share/icons/hicolor/scalable/apps', icons('svg'))
                                ],
        cmdclass = {
                'bdist_rpm': bdist_rpm
                }
)

# vim: sw=4 ts=4 sts=4 noet ai
