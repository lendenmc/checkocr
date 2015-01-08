# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import fnmatch
import subprocess
import re
import shutil

from colorama import Fore


class PDF(object):

    def __init__(self, directory, name, pages):
        self.name = name
        self.directory = directory
        self.pathname = os.path.join(directory, name)
        self.pages = pages
        self.content = self.make_content()

    def extract_content(self, first_page, last_page):
        cmd = ['pdftotext', '-q',
               '-f', str(first_page),
               '-l', str(last_page),
               self.pathname, '/dev/stdout']
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
        treshold = self.pages // 2
        for i in reversed(range(treshold)):
            try:
                content = self.extract_content(first_page=i*self.pages+1,
                                               last_page=(i+1)*self.pages)
            except subprocess.CalledProcessError:
                print(Fore.RED + "Too small !" + Fore.RESET)
                continue
            if content.startswith("\x0c"):
                if content.startswith(treshold*"\x0c"):
                    print(Fore.RED + "Clear Cut !" + Fore.RESET)
                    return
                print(Fore.RED + "Too small !" + Fore.RESET)
                continue
            if content.startswith(warning):
                print(Fore.RED + warning[:-2] + Fore.RESET)
                return
            break
        return content

    def make_words_number(self):
        if self.content:
            words_list = re.findall('[^\W\d_]{6}', self.content, re.UNICODE)
             # the re.UNICODE flag is needed for Python 2.7
            return len(words_list)

    def make_junk_number(self):
        junks = [u"&", u"+{", u"{>", u"+[", u"@", u"±", u"%", u"#", u"¿"]
        if self.content:
            junk_number = sum([self.content.count(junk) for junk in junks])
            return junk_number

    def is_wordy(self):
        words_number = self.make_words_number()
        words_limit = 15 * self.pages

        return words_number > words_limit

    def is_junky(self):
        junk_number = self.make_junk_number()
        upper_limit = 25 * self.pages
        lower_limit = 5 * self.pages

        first_test = (junk_number > upper_limit)
        if first_test:
            return True

        second_test = (junk_number > lower_limit and not self.is_wordy())
        return second_test

    def is_ocr(self):
        if self.content is None:
            return
        if self.is_junky():
            print(Fore.RED + "Too junky !" + Fore.RESET)
            return
        return re.search('[^\W\d_]{6}', self.content, re.UNICODE)

    def copy(self, output_dir):
        pdf_copy = os.path.join(output_dir, self.name)
        shutil.copyfile(self.pathname, pdf_copy)


class PDFScanner(object):

    def __init__(self, scanned_pages):
        self.scanned_pages = scanned_pages

    def scan(self, target_dir, output_dir):
        for root, dirs, files in os.walk(target_dir):
            for goodfile in fnmatch.filter(files, '*.pdf'):
                print("-----------------------------------------------")
                print("Name : {}".format(goodfile))
                pdf = PDF(directory=root,
                          name=goodfile,
                          pages=self.scanned_pages)
                if not pdf.is_ocr():
                    print(Fore.RED + "Not accepted !" + Fore.RESET)
                    pdf.copy(output_dir)


if __name__ == '__main__':
    import time
    start_time = time.time()

    import sys
    target_dir, output_dir = sys.argv[1:]
    scanned_pages = 8

    scanner = PDFScanner(scanned_pages=scanned_pages)
    scanner.scan(target_dir, output_dir)

    print("--- {} seconds ---".format(time.time() - start_time))
