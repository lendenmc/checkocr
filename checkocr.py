from __future__ import print_function
import os
import subprocess
import re
import shutil
import fnmatch
import time

from colorama import Fore


class PDF(object):

    def __init__(self, directory, name):
        self.name = name
        self.directory = directory
        self.pathname = os.path.join(directory, name)

    def extract_content(self, first_page, last_page):
        cmd = ['pdftotext', '-q',
               '-f', str(first_page),
               '-l', str(last_page),
               self.pathname, '/dev/stdout']
        content = subprocess.check_output(cmd)
        return content

    def is_ocr(self, max_scanned_pages, test_length):
        treshold = max_scanned_pages * 3
        ### This "treshold" (see bellow) is needed in order to get a content
        ### sample that is more representive of longer pdfs such as ebooks.
        ### Indeed, those pdfs might have ocr, but only after the first few
        ### pages, and the other way round. So it's better to start scanning
        #### longer pdfs from a more distant page number.
        try:
            content = self.extract_content(first_page=2*max_scanned_pages+1,
                                           last_page=treshold)
            self.is_large = True
        except subprocess.CalledProcessError:
            content = self.extract_content(first_page=1,
                                           last_page=max_scanned_pages)
            self.is_large = False
        print("------------------------------------------------------------")
        warning = "PDF compression, OCR, web optimization using \
a watermarked evaluation copy of CVISION PDFCompressor\n\n"
        if content.decode('utf-8', 'ignore').startswith(warning):
        ### This decoding is for python 3 portability reasons, as python 3
        ### check_ouput returns bytes instead of a string. The 'ignore'
        ### option is then used to prevent the UnicodeDecodeError that might
        ### occur as the result of the 'content' bit-string being shortened
        ### at the wrong place.
            print(Fore.RED + warning + "\n")
            return
        l = test_length
        if (len(content) <= 6*l or not self.is_large):
            ### Condition deals with the special case of small pdfs or pdfs
            ### whose content can't be split into 6 parts of length l (even
            ### though they might have a high number of pages, which is typical
            ### of non-ocr ebooks).
            content = content.decode('utf-8', 'ignore')
            print("Name : {}\n".format(self.name))
            print("Number of Pages : {}".format(self.is_large))
            return re.search('[^\W\d_]{5}', content, re.UNICODE)
            ### the re.UNICODE flag is needed for Python 2.7
        test_contents = [content[0:l],
                         content[l:2*l],
                         content[2*l:3*l],
                         content[-3*l:-2*l],
                         content[-2*l:-l],
                         content[-l:]]
        test_contents = (c.decode('utf-8', 'ignore') for c in test_contents)
        print("Name : {}\n".format(self.name))
        print("Number of Pages : {}".format(self.is_large))
        return all((re.search('[^\W\d_]{3}', c, re.UNICODE)
                    for c in test_contents))

    def copy(self, output_dir):
        pdf_copy = os.path.join(output_dir, self.name)
        shutil.copyfile(self.pathname, pdf_copy)


class PDFScanner(object):

    def __init__(self, max_scanned_pages, test_length):
        self.max_scanned_pages = max_scanned_pages
        self.test_length = test_length

    def scan(self, target_dir, output_dir):
        for root, dirs, files in os.walk(target_dir):
            for goodfile in fnmatch.filter(files, '*.pdf'):
                pdf = PDF(root, goodfile)
                if not pdf.is_ocr(max_scanned_pages=self.max_scanned_pages,
                                  test_length=self.test_length):
                    print(Fore.RED + "Not accepted" + Fore.RESET)
                    pdf.copy(output_dir)


if __name__ == '__main__':
    start_time = time.time()
    import sys
    target_dir, output_dir = sys.argv[1:]
    max_scanned_pages, test_length = 8, 50
    scanner = PDFScanner(max_scanned_pages=max_scanned_pages,
                         test_length=test_length)
    scanner.scan(target_dir, output_dir)
    print("--- {} seconds ---".format(time.time() - start_time))
