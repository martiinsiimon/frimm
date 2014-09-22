"""
Module containing configuration relevant classes and methods.
"""

import json
import os


class Configuration(object):
    """
    Configuration class managing  FRIMM's configuration, its storing and
    restoring.
    """

    def __init__(self, config_dir=os.path.expanduser('~/.config/frimm/'),
                 filters_dir=os.path.expanduser('~/FRIMM Filters')):
        self.configuration = {}
        self.config_dir = config_dir
        self.config_file = self.config_dir + 'config.json'
        self['filter_path'] = filters_dir

        if not os.path.isdir(self.config_dir):
            os.mkdir(self.config_dir)
            self.set_defaults()

        if not os.path.isdir(self['filter_path']):
            os.mkdir(self['filter_path'])

    def __getitem__(self, key):
        return self.configuration[key]

    def __setitem__(self, key, value):
        self.configuration[key] = value

    def dump(self):
        """
        Dump configuration as a single string
        """
        return self.configuration

    def set_defaults(self):
        """
        Method to set default values for configuration. This method is
        called after application very first run.
        """
        self['print_results'] = 0
        self['measure'] = 0

        self.store()

    def restore(self):
        """
        Restore configuration if exist. Otherwise, set defaults and store.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file) as conf_file:
                file_content = conf_file.read()
            if not file_content:
                self.set_defaults()
            else:
                file_json = json.loads(file_content)
                for key, value in file_json.iteritems():
                    self.configuration[key] = value
        else:
            self.set_defaults()

    def store(self):
        """
        Store configuration if any.
        """
        if len(self.configuration) > 0:
            with open(self.config_file, 'w+') as conf_file:
                json.dump(self.configuration, conf_file, indent=2)
