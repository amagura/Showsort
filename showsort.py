#!/usr/bin/python3

import argparse
import errno
import re
# import ctypes
# import pywikibot
# import requests
# import urllib
# import wikipedia

from os import walk, getcwd, path, symlink, mkdir, chdir, rename
from sys import argv
# from os import listdir
# from os.path import isfile, join

class Sorter:

    def __init__(self, args):
        # self.show = show
        # self.args = args
        self.src = args.show
        self.dest = getcwd()
        self.seasons = args.season

    def get_eplist(self):
        pass
        # tvdb = tvdb_v4_official.TVDB("APIKEY")
        # NOTE should search for show + TV Series; if not present, go with first result

        # Attempt No. 1
        # query = wikipedia.search(self.show)[0]
        # page = wikipedia.search(f'List of {query} episodes')[0]
        # wiki = pywikibot.Site('en', 'wikipedia')
        # page = pywikibot.Page(wiki, page)

        # TODO now we need to parse the output
        # print(page.get())
        # site = pywikibot.Site('en', 'wikipedia')
        # query = wikipedia.search(f'List of {self.show} episodes')
        # page = pywikibot.Page(site, query[0])
        # print(page)
        # print(query)
        # pg = wikipedia.page(query[0])
        # print(pg.content)

    def _find(self, dir=None):
        if dir == None:
            dir = self.src
        files = next(walk(dir), (None, None, []))[2]
        return files


    def linker(self):
        ii = len(self.seasons)
        files = self._find()
        for season in self.seasons:
            mkdir('./Season %.2d' % ii)
            chdir('Season %.2d' % ii)
            ## Link files
            for ep in files:
                # print(path.realpath(ep))
                try:
                    symlink(path.realpath(ep), f'./{ep}')
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        pass
            ## Rename files
            files = self._find(getcwd())
            jj = 1
            for episode in files:
                if not path.islink(episode):
                    # Don't rename files that aren't symlinks
                    continue
                elif re.match(r'S\d+E\d+', episode):
                    # Don't rename files that already have been renamed
                    continue
                tmp = "S%.2dE%.2d %s" % (ii, jj, episode)
                rename(episode, tmp)
                # print(f'`{episode}` -> `{tmp}`')
                jj += 1
            chdir('../')
            ii -= 1



def dirp(s):
    return True if path.exists(path.dirname(path.abspath(s))) else False


#
parser = argparse.ArgumentParser(description='Sorts shows in a torrent friendly manner')
parser.add_argument('show', type=str, help='directory containing episodes')
parser.add_argument('-s', '--season', action='append', nargs='+', help="split show into seasons")
args = parser.parse_args()

srt = Sorter(args)
srt.linker()

# show = argv[1]
# # TODO if no arg is given, get the current directory
# if dirp(show):
#     show = path.basename(path.abspath(show))
# print(show)
#
# srt = Sorter(show)
# print(srt.get_eplist())
# print(srt.find())


# TODO cli options:
# -m, --movie (assume show is a film)
# -t, --tv (default)
# -i, --install DIR (install show into directory)
# -n, --dry-run


# pr = MyHTMLParser()
# pr.feed
