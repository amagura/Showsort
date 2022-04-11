#!/usr/bin/python3

import pywikibot
import requests
import urllib
import wikipedia

from os import walk, getcwd, path
from sys import argv
# from os import listdir
# from os.path import isfile, join

class Sorter:

    def __init__(self, show):
        self.show = show

    def get_eplist(self):
        # tvdb = tvdb_v4_official.TVDB("APIKEY")
        # NOTE should search for show + TV Series; if not present, go with first result

        # Attempt No. 1
        query = wikipedia.search(self.show)[0]
        page = wikipedia.search(f'List of {query} episodes')[0]
        wiki = pywikibot.Site('en', 'wikipedia')
        page = pywikibot.Page(wiki, page)

        # TODO now we need to parse the output
        print(page.get())
        # site = pywikibot.Site('en', 'wikipedia')
        # query = wikipedia.search(f'List of {self.show} episodes')
        # page = pywikibot.Page(site, query[0])
        # print(page)
        # print(query)
        # pg = wikipedia.page(query[0])
        # print(pg.content)


    def find(self):
        files = next(walk("."), (None, None, []))[2]
        return files


def dirp(s):
    return True if path.exists(path.dirname(path.abspath(s))) else False


show = argv[1]
# TODO if no arg is given, get the current directory
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
