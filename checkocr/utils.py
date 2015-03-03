#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output, CalledProcessError


def get_subprocess_output(command):
    try:
        bytes_content = check_output(command)
    except CalledProcessError:
        return

    content = bytes_content.decode('utf-8')
    # The use of decode is for python 3 portability reasons, as python 3
    # check_ouput returns bytes instead of a string.
    return content
