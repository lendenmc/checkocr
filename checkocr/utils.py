from subprocess import check_output, CalledProcessError


def get_subprocess_output(command):
    try:
        bytes_content = check_output(command)
    except CalledProcessError:
        return

    content = bytes_content.decode('utf-8', 'ignore')
    # The use of decode is for python 3 portability reasons, as python 3
    # check_ouput returns bytes instead of a string. The 'ignore'
    # option is then used to prevent the UnicodeDecodeError that might
    # occur as the result of the 'content' bit-string being shortened
    # at the wrong place.
    return content
