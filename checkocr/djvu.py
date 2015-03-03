#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from checkocr.utils import get_subprocess_output


def get_content(djvufile, first_page, last_page):
    command = ['djvutxt',
               '--page=' + str(first_page) + "-" + str(last_page),
               djvufile]

    return get_subprocess_output(command)


def make_sample(djvufile, pages=8, max_iterations=4):

    for i in reversed(range(max_iterations)):

        first_page, last_page = i*pages+1, (i+1)*pages
        content = get_content(djvufile, first_page, last_page)

        if content is not None:
            break

    return content
