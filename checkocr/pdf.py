#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import get_subprocess_output


def get_content(pdffile, first_page, last_page):
    command = ['pdftotext', '-q',
               '-f', str(first_page),
               '-l', str(last_page),
               pdffile, '/dev/stdout']

    return get_subprocess_output(command)


def make_sample(pdffile, pages=8, max_iterations=4):

    for i in reversed(range(max_iterations)):

        first_page, last_page = i*pages+1, (i+1)*pages
        content = get_content(pdffile, first_page, last_page)

        if content in [None, '\x0c']:
            # try a more representative sample
            continue
        elif content.endswith(2*'\x0c') and not content.endswith(4*'\x0c'):
            # try a more representative sample
            continue
        else:
            break

    return content
