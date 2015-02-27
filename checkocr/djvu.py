import subprocess


def get_content(djvufile, first_page, last_page):
    command = ['djvutxt',
               '--page=' + str(first_page) + "-" + str(last_page),
               djvufile]

    try:
        bytes_content = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        return

    content = bytes_content.decode('utf-8', 'ignore')
    # The use of decode is for python 3 portability reasons, as python 3
    # check_ouput returns bytes instead of a string. The 'ignore'
    # option is then used to prevent the UnicodeDecodeError that might
    # occur as the result of the 'content' bit-string being shortened
    # at the wrong place.
    return content


def make_sample(djvufile, pages=8, max_iterations=4):

    for i in reversed(range(max_iterations)):

        first_page, last_page = i*pages+1, (i+1)*pages
        content = get_content(djvufile, first_page, last_page)

        if content is not None:
            break

    return content
