import json
import os


class Configuration(object):
    """
    Configuration class managing  FRIMM's configuration, its storing and
    restoring.
    """

    def __init__(self, config_dir=os.path.expanduser('~/.config/frimm/')):
        self.configuration = {}
        self.config_dir = config_dir
        self.config_file = self.config_dir + 'config.json'

        if not os.path.isdir(self.config_dir):
            os.mkdir(self.config_dir)

    def __getitem__(self, key):
        return self.configuration[key]

    def __setitem__(self, key, value):
        self.configuration[key] = value

    def set_defaults(self):
        self['print_results'] = 0
        self['measure'] = 0
        self['filter_path'] = os.path.expanduser('~/frimm/')
        if not os.path.isdir(self['filter_path']):
            os.mkdir(self['filter_path'])
        self.store()

    def restore(self):
        if os.path.exists(self.config_file):
            with open(self.config_file) as f:
                file_content = f.read()
            if not file_content:
                self.set_defaults()
            else:
                file_json = json.loads(file_content)
                for key, value in file_json.iteritems():
                    self.configuration[key] = value
        else:
            self.set_defaults()

    def store(self):
        if len(self.configuration) > 0:
            with open(self.config_file, 'w+') as f:
                json.dump(self.configuration, f, indent=2)
