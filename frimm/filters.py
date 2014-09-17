"""
Filters module. Consists of two main classes, Filter itself, containing
filter information, and Filters, the container fo filters providing
loading, storing and executing of filters.
"""

import sys
import os
import re
import time

from config import Configuration


class Filter(object):
    """
    Filter object. Contains filter name (displayed), filter language,
    filter source file (for execution) and filter description (to show
    details, if provided)
    """

    def __init__(self, name='', lang='', source='', desc='', author='', \
                 mail=''):
        self.name = name
        self.lang = lang
        self.source = source
        self.description = desc
        self.author_name = author
        self.author_mail = mail

    def dump(self):
        """
        Dump information about object in a single string
        """
        return "%s (%s) - %s <%s>: %s\n" % \
            (self.name, self.lang, self.author_name, \
             self.author_mail, self.description)


class Filters(object):
    """
    Container for filter objects. Provides function to automatically load
    filters from predefined location, create list of them, provide
    information of specific filter and execute code of specific filter.
    TODO:
        execute_active()
        test_refresh() -- tests
        test_execute_active() -- tests
    """

    def __init__(self, config):
        assert isinstance(config, Configuration)
        self.config = config
        self.filters = {}
        self.active = None

    def dump(self):
        """
        Dump informatio about filters in container as a single string
        """
        res = ''
        keys = self.filters.keys()
        keys.sort()
        for key in keys:
            res += self.filters[key].dump()
        return res

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.filters[key]
        elif isinstance(key, Filter):
            return self.filters[key.name]
        else:
            assert RuntimeError, 'Key type must be str or Filter!'

    def __setitem__(self, key, value):
        if not isinstance(value, Filter):
            assert RuntimeError, 'Type of value must be Filter!'
        if isinstance(key, str):
            self.filters[key] = value
        elif isinstance(key, Filter):
            self.filters[key.name] = value
        else:
            assert RuntimeError, 'Key type must be str or Filter!'

    def add(self, filt):
        """
        Add a new filter. Filter can be added in container using standard
        setter or via this method
        """
        if isinstance(filt, Filter):
            self.filters[filt.name] = filt
        else:
            assert RuntimeError, 'Only items of type Filter can be added!'

    def __delitem__(self, filt):
        if isinstance(filt, str):
            key = filt
        elif isinstance(filt, Filter):
            key = filt.name
        else:
            return

        try:
            del self.filters[key]
        except KeyError:
            pass

    def __len__(self):
        return len(self.filters)

    def __iter__(self):
        return iter(self.filters)

    def clear(self):
        """
        Clear container
        """
        self.filters = {}

    def refresh(self):
        """
        Refresh list of filters from given folder. The folder is set in
        configuration, given in object initialization. Parses filters
        one by one and adding all correct filters to the list
        """
        def add_python_filters(self, path, files):
            """
            Parse and add Python filters.
            """
            py_files = [f for f in files if re.match(r'.*\.py$', f)]

            sys.path.append(path)
            for filee in py_files:
                try:
                    module = __import__(filee.strip('.py'))
                    reload(module)
                    self.add(
                        Filter(name=module.__filter_name__,\
                        lang='Python', source=module.process,\
                        desc=module.__filter_description__,\
                        author=module.__author_name__,\
                        mail=module.__author_mail__))
                except ImportError:
                    pass
            del sys.path[-1]

        path = self.config['filter_path']
        files = [f for f in os.listdir(path) if\
            os.path.isfile(os.path.join(path, f))\
            and not re.match('^template', f)]

        # parse Python files
        add_python_filters(self, path, files)

    def execute_active(self, input_img, output_img):
        """
        Execute active filter. It also measures time between filter call
        and its end, if requested.
        """
        if self.active:
            if self.config['measure']:
                start_time = time.time()
            self.active.source(input_img, output_img)
            if self.config['measure']:
                end_time = time.time()
            return end_time - start_time
        else:
            return -1.0
