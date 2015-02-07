#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_checkocr
----------------------------------

Tests for `checkocr` module.
"""
from __future__ import print_function

import unittest
import os
import fnmatch

from checkocr import checkocr


class TestIsNotJunky(unittest.TestCase):

    def setUp(self):
        self.directory = os.path.join(os.getcwd(),
                                      'tests/pdf_files/non_junky_files')
        self.non_junky_files = fnmatch.filter(os.listdir(self.directory),
                                              '*.pdf')
        self.scanned_pages = checkocr.scanned_pages

    def test_is_not_junky(self):
        for filename in self.non_junky_files:
            scanned_file = checkocr.File(directory=self.directory,
                                         name=filename,
                                         extension='pdf',
                                         pages=self.scanned_pages)
            self.assertFalse(scanned_file.is_junky())

    def tearDown(self):
        pass


class TestIsJunky(unittest.TestCase):

    def setUp(self):
        self.directory = os.path.join(os.getcwd(),
                                      'tests/pdf_files/junky_files')
        self.junky_files = fnmatch.filter(os.listdir(self.directory),
                                          '*.pdf')
        self.scanned_pages = checkocr.scanned_pages

    def test_is_junky(self):
        for filename in self.junky_files:
            scanned_file = checkocr.File(directory=self.directory,
                                         name=filename,
                                         extension='pdf',
                                         pages=self.scanned_pages)
            self.assertTrue(scanned_file.is_junky())

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
