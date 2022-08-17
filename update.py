import urllib.request
import os


def update_available():
    """
    Returns True if a newer version is available at https://memorygain.app.
    """
    try:
        html = urllib.request.urlopen("https://memorygain.app")
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
    Opens https://memorygain.app and exits.
    """
    os.system("START https://memorygain.app")
    sys.exit()
