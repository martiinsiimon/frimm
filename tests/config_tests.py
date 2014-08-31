#!/usr/bin/env python

import unittest
from frimm.config import Configuration
import tempfile
import os


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.config_dir = tempfile.mkdtemp()
        self.config = Configuration(self.config_dir)

    def tearDown(self):
        try:
            os.rmdir(self.config_dir)
        except:
            pass

    def test_setter(self):
        self.config['test1'] = 10
        self.assertEqual(self.config.configuration['test1'], 10)

    def test_getter(self):
        self.config.configuration['test2'] = 20
        self.assertEqual(self.config['test2'], 20)

    def test_store_restore(self):
        self.config['print_results'] = 1
        self.config['measure'] = 1
        self.config.store()
        self.assertEqual(self.config['print_results'], 1)
        self.assertEqual(self.config['measure'], 1)
        self.config['print_results'] = 0
        self.config.restore()
        self.assertEqual(self.config['print_results'], 1)
        self.assertEqual(self.config['measure'], 1)

    def test_set_defaults1(self):
        self.config.set_defaults()
        self.assertEqual(self.config['print_results'], 0)
        self.assertEqual(self.config['measure'], 0)

    def test_set_defaults2(self):
        self.config.set_defaults()
        self.config['print_results'] = 1
        self.config.restore()
        self.assertEqual(self.config['print_results'], 0)
        self.assertEqual(self.config['measure'], 0)

    def test_restore(self):
        os.rmdir(self.config_dir)
        self.config.restore()
        self.assertEqual(self.config['print_results'], 0)
        self.assertEqual(self.config['measure'], 0)
