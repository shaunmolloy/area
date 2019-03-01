"""
Helpers
author: Shaun Molloy <shaunmolloy@gmail.com>
"""
import os
import requests
import subprocess
import shutil


def heading(text):
    print('')
    print('-' * 80)
    print(text.center(80) )
    print('-' * 80)
    print('')


def find_in_file(find, filename):
    p = subprocess.Popen(['grep', '-F', find, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        return None
    return result.decode('UTF-8').splitlines()


def download_file(filename, url):
    """
    Download an URL to a file.
    Creates and resumes adding to .part until done then renames to filename.

    :param filename
    :param url
    """
    block_size = 10240 * 1024 # 10 MB
    tmp_filename = filename + '.part'
    first_byte = os.path.getsize(tmp_filename) if os.path.exists(tmp_filename) else 0
    file_mode = 'ab' if first_byte else 'wb'
    file_size = int(requests.head(url).headers['Content-length'])
    headers = { "Range": "bytes=%s-" % first_byte }
    r = requests.get(url, headers=headers, stream=True)

    if os.path.getsize(filename) > file_size:
        return False

    print('Downloading: %s' % url)
    print('Starting download at %.0f MB' % (first_byte / 1e6))

    with open(tmp_filename, file_mode) as f:
        for chunk in r.iter_content(chunk_size=block_size):
            if chunk:
                # filter out keep-alive new chunks
                f.write(chunk)

    shutil.move(tmp_filename, filename)
    print("Saved: %s" % filename)
