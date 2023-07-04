"""Script to download the movie review dataset"""


import os
import tarfile
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen


URL = ("http://www.cs.cornell.edu/people/pabo/"
       "movie-review-data/review_polarity.tar.gz")

ARCHIVE_NAME = URL.rsplit('/', 1)[1]
DATA_FOLDER = "txt_sentoken"


if not os.path.exists(DATA_FOLDER):

    if not os.path.exists(ARCHIVE_NAME):
        print(f"Downloading dataset from {URL} (3 MB)")
        opener = urlopen(URL)
        open(ARCHIVE_NAME, 'wb').write(opener.read())

    print(f"Decompressing {ARCHIVE_NAME}")
    tarfile.open(ARCHIVE_NAME, "r:gz").extractall(path='.')
    os.remove(ARCHIVE_NAME)
