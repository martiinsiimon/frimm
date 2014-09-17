#!/usr/bin/env python

import unittest
from frimm.filters import Filter, Filters
from frimm.config import Configuration
import tempfile
import os

class TestFilter(unittest.TestCase):
    def setUp(self):
        self.name = 'Name of Simple filter'
        self.author_name = 'Name Surname'
        self.author_mail = 'email@address.tld'
        self.lang = 'Python 3'
        self.source = 'print(\'Hello world\')'
        self.desc = 'Simple Hello world script'
        self.filter = Filter(name=self.name, lang=self.lang, source=self.source, desc=self.desc, author=self.author_name, mail=self.author_mail)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.filter.name, self.name)
        self.assertEqual(self.filter.lang, self.lang)
        self.assertEqual(self.filter.source, self.source)
        self.assertEqual(self.filter.description, self.desc)
        self.assertEqual(self.filter.author_name, self.author_name)
        self.assertEqual(self.filter.author_mail, self.author_mail)

    def test_dump(self):
        expected_dump = '%s (%s) - %s <%s>: %s\n' % (self.name, self.lang, self.author_name, self.author_mail, self.desc)
        self.assertEqual(self.filter.dump(), expected_dump)


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.config = Configuration(self.tmp_dir)
        self.filters = Filters(self.config)
        self.name1 = 'Filter AAA'
        self.lang1 = 'Python'
        self.auth1 = 'Name Surname'
        self.mail1 = 'mail@address.tld'
        self.src1 = 'print(\'Hello world\')'
        self.desc1 = 'Description of filter AAA'
        self.filter1 = Filter(name=self.name1, lang=self.lang1, source=self.src1, desc=self.desc1, author=self.auth1, mail=self.mail1)
        self.name2 = 'Filter BBB'
        self.lang2 = 'Python'
        self.auth2 = 'Name Surname'
        self.mail2 = 'mail@address.tld'
        self.src2 = 'print(\'Hello world\')'
        self.desc2 = 'Description of filter BBB'
        self.filter2 = Filter(name=self.name2, lang=self.lang2, source=self.src2, desc=self.desc2, author=self.auth2, mail=self.mail2)
        self.name3 = 'Filter CCC'
        self.lang3 = 'Python'
        self.auth3 = 'Name Surname'
        self.mail3 = 'mail@address.tld'
        self.src3 = 'print(\'Hello world\')'
        self.desc3 = 'Description of filter CCC'
        self.filter3 = Filter(name=self.name3, lang=self.lang3, source=self.src3, desc=self.desc3, author=self.auth3, mail=self.mail3)

    def tearDown(self):
        os.rmdir(self.tmp_dir)

    def test_dump(self):
        self.filters.add(self.filter1)
        self.filters.add(self.filter2)
        self.filters.add(self.filter3)
        expected_dump = '%s (%s) - %s <%s>: %s\n%s (%s) - %s <%s>: %s\n%s (%s) - %s <%s>: %s\n' % \
            (self.name1, self.lang1, self.auth1, self.mail1, self.desc1, self.name2, self.lang2, self.auth2, self.mail2, self.desc2, self.name3, self.lang3, self.auth3, self.mail3, self.desc3)
        self.assertEqual(self.filters.dump(), expected_dump)

    def test_setter1(self):
        self.filters['test5'] = self.filter1
        self.assertEqual(self.filters.filters['test5'].dump(), self.filter1.dump())

    def test_setter2(self):
        self.filters[self.filter1] = self.filter1
        self.assertEqual(self.filters.filters[self.filter1.name].dump(), self.filter1.dump())

    def test_getter1(self):
        self.filters.filters['test6'] = self.filter2
        self.assertEqual(self.filters['test6'].dump(), self.filter2.dump())

    def test_getter2(self):
        self.filters.filters[self.filter1.name] = self.filter1
        self.assertEqual(self.filters[self.filter1].dump(), self.filter1.dump())

    def test_add(self):
        self.filters.add(self.filter1)
        self.assertEqual(self.filters[self.filter1.name].dump(), self.filter1.dump())
        self.assertTrue(self.filters[self.filter1.name])
        self.assertEquals(len(self.filters), 1)

    def test_del1(self):
        self.filters.add(self.filter1)
        del self.filters[self.filter1.name]
        self.assertFalse(self.filters.filters.has_key(self.filter1.name))
        self.assertEquals(len(self.filters), 0)

    def test_del2(self):
        self.filters.add(self.filter2)
        del self.filters[self.filter2]
        self.assertFalse(self.filters.filters.has_key(self.filter2.name))
        self.assertEquals(len(self.filters), 0)

    def test_clear(self):
        self.filters.add(self.filter1)
        self.assertEquals(len(self.filters), 1)
        self.filters.clear()
        self.assertEquals(len(self.filters), 0)
