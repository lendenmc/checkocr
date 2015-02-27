#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_checkocr
----------------------------------

Tests for `checkocr` module.
"""
from __future__ import print_function

import unittest
import glob

from checkocr.checkocr import ScannedFile


class TestIsNotJunky(unittest.TestCase):

    def setUp(self):
        non_junky_files = 'tests/pdf_files/non_junky_files/*.pdf'
        self.non_junky_files = glob.glob(non_junky_files)

    def test_is_not_junky(self):
        for scanned_file in self.non_junky_files:
            scanned_file = ScannedFile(scanned_file)
            self.assertFalse(scanned_file.is_junky())

    def tearDown(self):
        pass


class TestIsJunky(unittest.TestCase):

    def setUp(self):
        junky_files = 'tests/pdf_files/junky_files/*.pdf'
        self.junky_files = glob.glob(junky_files)

    def test_is_junky(self):
        for scanned_file in self.junky_files:
            scanned_file = ScannedFile(scanned_file)
            self.assertTrue(scanned_file.is_junky())

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
