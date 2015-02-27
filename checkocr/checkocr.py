#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import fnmatch
import re
import shutil

from colorama import Fore

import pdf
import djvu


_EXTENSIONS = ['pdf',
               # 'djvu',
               ]


class ScannedFile(object):

    SCANNED_PAGES = 8

    def __init__(self, fullname):
        self.fullname = fullname
        self.name = os.path.basename(fullname)
        self.dirname = os.path.dirname(fullname)
        self.extension = os.path.splitext(fullname)[1][1:]

        self.sample = self.make_sample()

    def make_sample(self):
        if self.extension == 'pdf':
            return pdf.make_sample(self.fullname, pages=self.SCANNED_PAGES)
        elif self.extension == 'djvu':
            return djvu.make_sample(self.fullname, pages=self.SCANNED_PAGES)

    def has_prohibited(self):
        prohibited = ["PDF compression, OCR, web optimization using \
a watermarked evaluation copy of CVISION PDFCompressor\n\n",
                      4*'\x0c',
                      ]
        if self.sample:
            return any(self.sample.startswith(msg) for msg in prohibited)
        else:
            return False

    def make_words_number(self):
        if self.sample:
            words_list = re.findall('[^\W\d_]{6}', self.sample, re.UNICODE)
            # the re.UNICODE flag is needed for Python 2.7
            return len(words_list)

    def make_junk_number(self):
        junks = [u'&', u'+{', u'{>', u'+[', u'@', u'±', u' %',
                 u' $', u'#', u'¿']
        if self.sample:
            junk_number = sum([self.sample.count(junk) for junk in junks])
            return junk_number

    def is_wordy(self):
        words_number = self.make_words_number()
        words_limit = 15 * self.SCANNED_PAGES

        if words_number is not None:
            return words_number > words_limit
        else:
            return False

    def is_junky(self):
        junk_number = self.make_junk_number()
        upper_limit = 25 * self.SCANNED_PAGES
        lower_limit = 5 * self.SCANNED_PAGES

        if junk_number is not None:
            first_test = (junk_number > upper_limit)
            if first_test:
                return True

            second_test = (junk_number > lower_limit and not self.is_wordy())
            return second_test
        else:
            return False

    def is_ocr(self):
        if not self.sample or self.has_prohibited():
            print(Fore.RED + 'Weird !' + Fore.RESET)
            return
        if self.is_junky():
            print(Fore.RED + 'Too junky !' + Fore.RESET)
            return
        return re.search('[^\W\d_]{6}', self.sample, re.UNICODE)

    def copy(self, output_dir):
        file_copy = os.path.join(output_dir, self.name)
        try:
            shutil.copyfile(self.fullname, file_copy)
        except OSError as e:
            print("{}\nDestionation folder is not writable.\n\
Please change destionation folder.".format(e))


def scan(target_dir, output_dir):
    for root, dirs, files in os.walk(target_dir):
        for extension in _EXTENSIONS:
            for goodfile in fnmatch.filter(files, '*.' + extension):
                print('-----------------------------------------------')
                print("Name : {}".format(goodfile))
                fullname = os.path.join(root, goodfile)
                scanned_file = ScannedFile(fullname)
                if not scanned_file.is_ocr():
                    print(Fore.RED + 'Not accepted !' + Fore.RESET)
                    scanned_file.copy(output_dir)


if __name__ == '__main__':
    import time
    start_time = time.time()

    import sys
    target_dir, output_dir = sys.argv[1:]
    scan(target_dir, output_dir)

    print('--- {} seconds ---'.format(time.time() - start_time))
