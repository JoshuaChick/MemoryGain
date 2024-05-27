import urllib.request
import os
import sys


def update_available():
    """
    Returns True if a newer version is available at https://joshuachick.github.io/MemoryGain/.
    """
    try:
        html = urllib.request.urlopen("https://joshuachick.github.io/MemoryGain/")
        html = str(html.read())
        if ("Version 1.0.7" not in html) and ("MemoryGain" in html):
            return True

    except urllib.error.URLError as e:
        print(e)

    except urllib.error.HTTPError as e:
        print(e)

    return False


def go_to_memorygain_site():
    """
    Opens https://joshuachick.github.io/MemoryGain/ and exits.
    """
    os.system("START https://joshuachick.github.io/MemoryGain/")
    sys.exit()
