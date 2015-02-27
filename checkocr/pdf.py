import subprocess


def get_content(pdffile, first_page, last_page):
    command = ['pdftotext', '-q',
               '-f', str(first_page),
               '-l', str(last_page),
               pdffile, '/dev/stdout']

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
