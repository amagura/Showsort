#!/usr/bin/python3

import requests
import wikipedia

from html.parser import HTMLParser
from os import walk, getcwd, path
from sys import argv
# from os import listdir
# from os.path import isfile, join


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


class Sorter:

    def __init__(self, show):
        self.show = show

    def get_eplist(self):
        # tvdb = tvdb_v4_official.TVDB("APIKEY")
        # NOTE should search for show + TV Series; if not present, go with first result

        # Attempt No. 1
        query = wikipedia.search(f'{self.show} (TV series)')
        pg = wikipedia.page(query[0])
        print(pg.content)

        print(query)

    def find(self):
        files = next(walk("."), (None, None, []))[2]
        return files


def dirp(s):
    return True if path.exists(path.dirname(path.abspath(s))) else False


show = argv[1]
if dirp(show):
    show = path.basename(path.abspath(show))
print(show)

srt = Sorter(show)
print(srt.get_eplist())
print(srt.find())


# TODO cli options:
# -m, --movie (assume show is a film)
# -t, --tv (default)
# -i, --install DIR (install show into directory)
# -n, --dry-run


# pr = MyHTMLParser()
# pr.feed
