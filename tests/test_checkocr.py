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

TESTS = {
        'TestIsNotJunky': {
                           'files': 'tests/pdf_files/non_junky_files/*.pdf',
                           'method': 'is_junky',
                           'test_fct': 'assertFalse',
                          },
        'TestIsJunky': {
                        'files': 'tests/pdf_files/junky_files/*.pdf',
                        'method': 'is_junky',
                        'test_fct': 'assertTrue',
                       },
         }


class TestScannedFileMethod(object):

    def __init__(self, testcase):
        self.testcase = testcase
        self.name = self.testcase.__class__.__name__
        self.params = TESTS[self.name]

    def get_test_params(self):
        files = glob.glob(self.params['files'])
        method = self.params['method']
        test_fct = getattr(self.testcase, self.params['test_fct'])

        return files, method, test_fct

    def run_test(self):
        files, method, test_fct = self.get_test_params()

        for scanned_file in files:
            scanned_file = ScannedFile(scanned_file)
            test_fct(getattr(scanned_file, method)())


class TestIsNotJunky(unittest.TestCase):

    def setUp(self):
        self.test = TestScannedFileMethod(self)

    def test_is_not_junky(self):
        self.test.run_test()

    def tearDown(self):
        pass


class TestIsJunky(unittest.TestCase):

    def setUp(self):
        self.test = TestScannedFileMethod(self)

    def test_is_junky(self):
        self.test.run_test()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
