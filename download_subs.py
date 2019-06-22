# The core code was stolen from https://github.com/manojmj92/subtitle-downloader/

import os
import hashlib
import urllib.request

# set some variables
loc = '/home/jochenater/Videos/'
vid_extensions = ['mp4', 'mpeg', 'avi', 'mkv']

# Define some functions
def get_hash(file_path):
    """Return the hash of the video file."""
    read_size = 64 * 1024
    with open(file_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()

def get_from_subdb(file_path, language_code='en', verbose=False):
    """Download subtitles from subdb."""
    try:
        root, extension = os.path.splitext(file_path)
        filename = root + language_code + ".srt"

        if not os.path.exists(filename):
            headers = {'User-Agent': 'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)'}
            url = "http://api.thesubdb.com/?action=download&hash=" + get_hash(file_path) + "&language=" + language_code
            req = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(req).read()

            with open(filename, "wb") as subtitle:
                subtitle.write(response)
                if verbose:
                    print(language_code + " subtitles successfully downloaded for " + file_path)

    except:
        if verbose:
            print(language_code + " subtitles not found for " + file_path + " in subdb")


# Actually downloading the subs
for d in [x[0] for x in os.walk(loc)]:          # all directories and subdirectories in Videos
    for f in os.listdir(d):                     # for all files in the dir
        if f.endswith(tuple(vid_extensions)):   # if it's a video:
            file = d + '/' + f
            get_from_subdb(file, 'en', verbose=True)

