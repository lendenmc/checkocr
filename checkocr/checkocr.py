#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import fnmatch
import subprocess
import re
import shutil

from colorama import Fore

scanned_pages = 8
extensions = ['pdf',
              'djvu',
              ]


class File(object):

    def __init__(self, directory, name, extension):
        self.name = name
        self.directory = directory
        self.extension = extension
        self.pathname = os.path.join(directory, name)
        self.content = self.make_content()

    def extract_content(self, first_page, last_page):
        if self.extension == "pdf":
            cmd = ['pdftotext', '-q',
                   '-f', str(first_page),
                   '-l', str(last_page),
                   self.pathname, '/dev/stdout']
        if self.extension == "djvu":
            cmd = ['djvutxt',
                   '--page=' + str(first_page) + "-" + str(last_page),
                   self.pathname]
        bytes_content = subprocess.check_output(cmd)
        content = bytes_content.decode('utf-8', 'ignore')
        # The use of decode is for python 3 portability reasons, as python 3
        # check_ouput returns bytes instead of a string. The 'ignore'
        # option is then used to prevent the UnicodeDecodeError that might
        # occur as the result of the 'content' bit-string being shortened
        # at the wrong place.
        return content

    def make_content(self):
        warning = "PDF compression, OCR, web optimization using \
a watermarked evaluation copy of CVISION PDFCompressor\n\n"
        treshold = scanned_pages // 2
        min_treshold = scanned_pages // 4
        for i in reversed(range(treshold)):
            try:
                content = self.extract_content(first_page=i*scanned_pages+1,
                                               last_page=(i+1)*scanned_pages)
            except subprocess.CalledProcessError:
                print((i*scanned_pages+1, (i+1)*scanned_pages))
                print(Fore.RED + "Too small !" + Fore.RESET)
                continue
            if self.extension == "djvu":
                return content
            if content.endswith(min_treshold*"\x0c"):
                if content.endswith(treshold*"\x0c"):
                    print(Fore.RED + "Clear Cut !" + Fore.RESET)
                    return
                print(Fore.RED + "Too small !" + Fore.RESET)
                continue
            if content.startswith(warning):
                print(Fore.RED + warning[:-2] + Fore.RESET)
                return
            break
        try:
            return content
        except UnboundLocalError:
            return
        # This try-except block fix UnboundLocalError in case
        # subprocess.CalledProcessErroor is raised on each and every iteration.

    def make_words_number(self):
        if self.content:
            words_list = re.findall('[^\W\d_]{6}', self.content, re.UNICODE)
            # the re.UNICODE flag is needed for Python 2.7
            return len(words_list)

    def make_junk_number(self):
        junks = [u"&", u"+{", u"{>", u"+[", u"@", u"±", u" %",
                 u" $", u"#", u"¿"]
        if self.content:
            junk_number = sum([self.content.count(junk) for junk in junks])
            return junk_number

    def is_wordy(self):
        words_number = self.make_words_number()
        words_limit = 15 * scanned_pages

        if words_number is not None:
            return words_number > words_limit
        else:
            return False

    def is_junky(self):
        junk_number = self.make_junk_number()
        upper_limit = 25 * scanned_pages
        lower_limit = 5 * scanned_pages

        if junk_number is not None:
            first_test = (junk_number > upper_limit)
            if first_test:
                return True

            second_test = (junk_number > lower_limit and not self.is_wordy())
            return second_test
        else:
            return True

    def is_ocr(self):
        if not self.content:
            return
        if self.is_junky():
            print(Fore.RED + "Too junky !" + Fore.RESET)
            return
        return re.search('[^\W\d_]{6}', self.content, re.UNICODE)

    def copy(self, output_dir):
        pdf_copy = os.path.join(output_dir, self.name)
        shutil.copyfile(self.pathname, pdf_copy)


def scan(target_dir, output_dir):
    for root, dirs, files in os.walk(target_dir):
        for extension in extensions:
            for goodfile in fnmatch.filter(files, '*.' + extension):
                print("-----------------------------------------------")
                print("Name : {}".format(goodfile))
                scanned_file = File(directory=root,
                                    name=goodfile,
                                    extension=extension)
                if not scanned_file.is_ocr():
                    print(Fore.RED + "Not accepted !" + Fore.RESET)
                    scanned_file.copy(output_dir)


if __name__ == '__main__':
    import time
    start_time = time.time()

    import sys
    target_dir, output_dir = sys.argv[1:]
    scan(target_dir, output_dir)

    print("--- {} seconds ---".format(time.time() - start_time))
