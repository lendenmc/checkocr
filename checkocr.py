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
        bytes_content = subprocess.check_output(cmd)
        content = bytes_content.decode('utf-8', 'ignore')
        ## The use of decode is for python 3 portability reasons, as python 3
        ### check_ouput returns bytes instead of a string. The 'ignore'
        ### option is then used to prevent the UnicodeDecodeError that might
        ### occur as the result of the 'content' bit-string being shortened
        ### at the wrong place.
        return content

    def is_ocr(self, scanned_pages):
        print("-----------------------------------------------")
        print("Name : {}".format(self.name))
        warning = "PDF compression, OCR, web optimization using \
a watermarked evaluation copy of CVISION PDFCompressor\n\n"
        treshold = scanned_pages // 2
        for i in reversed(range(treshold)):
            try:
                content = self.extract_content(first_page=i*scanned_pages+1,
                                               last_page=(i+1)*scanned_pages)
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
                print(Fore.RED + warning + Fore.RESET)
                return
            break
        junks = ["&", "+{", "{>", "+[", "@", "±", "%", "#", "¿"]
        junk_upper_limit = 25 * scanned_pages
        junk_lower_limit = 5 * scanned_pages
        min_words = 15 * scanned_pages
        junk_number = sum([content.count(junk) for junk in junks])
        if junk_number > junk_upper_limit:
            print(Fore.RED + "Too junky !" + Fore.RESET)
            return
        y = re.findall('[^\W\d_]{6}', content, re.UNICODE)
        if (junk_number > junk_lower_limit) and (len(y) < min_words):
            print(Fore.RED + "Too junky !" + Fore.RESET)
            return
        return re.search('[^\W\d_]{6}', content, re.UNICODE)

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
                    print(Fore.RED + "Not accepted !" + Fore.RESET)
                    pdf.copy(output_dir)


if __name__ == '__main__':
    start_time = time.time()
    import sys
    target_dir, output_dir = sys.argv[1:]
    scanned_pages = 8
    scanner = PDFScanner(scanned_pages=scanned_pages)
    scanner.scan(target_dir, output_dir)
    print("--- {} seconds ---".format(time.time() - start_time))
