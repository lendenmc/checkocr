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

    def extract_content(self, scanned_pages=1, length=1):
        print("--------------------------------------------------------------")
        cmd = ['pdftotext', '-q', '-l', str(scanned_pages), self.pathname,
               '/dev/stdout']
        content = subprocess.check_output(cmd)[:length]
        print("Name : {} \nContent: {}\n".format(self.name, repr(content)))
        ### This condition is for python 3 portability reasons, as python 3
        ### check_ouput returns bytes instead of a string. The 'ignore'
        ### option is then used to prevent the UnicodeDecodeError  might
        ### occur as the result of the 'content' bit-string being shortened
        ### at the wrong place with the 'length' parameter.
        content = content.decode('utf-8', 'ignore')
        return content

    def is_ocr(self, scanned_pages=15):
        warning = "\x0cPDF compression, OCR, web optimization using \
a watermarked evaluation copy of CVISION PDFCompressor\n\n"
        content = self.extract_content(scanned_pages=scanned_pages,
                                       length=len(warning))
        if content.startswith(warning):
            print(Fore.RED + warning + "\n")
            print("Not accepted" + Fore.RESET)
            return
        ### the re.UNICODE flag is needed for Python 2.7
        return re.search('\w{4}', content, re.UNICODE)

    def copy(self, output_dir):
        pdf_copy = os.path.join(output_dir, self.name)
        shutil.copyfile(self.pathname, pdf_copy)


class PDFScanner(object):

    def __init__(self, scanned_pages):
        self.scanned_pages = scanned_pages

    def scan(self, target_dir, output_dir):
        for root, dirs, files in os.walk(target_dir):
            for goodfile in fnmatch.filter(files, '*.pdf'):
                pdf = PDF(root, goodfile)
                if not pdf.is_ocr(scanned_pages=self.scanned_pages):
                    print(Fore.RED + "Not accepted" + Fore.RESET)
                    pdf.copy(output_dir)


if __name__ == '__main__':
    start_time = time.time()
    import sys
    target_dir, output_dir = sys.argv[1:]
    scanned_pages = 4
    scanner = PDFScanner(scanned_pages=scanned_pages)
    scanner.scan(target_dir, output_dir)
    print("--- {} seconds ---".format(time.time() - start_time))
