#!/usr/bin/python3

import argparse
import errno
import glob
import mimetypes
import os
import re
# import ctypes
# import pywikibot
# import requests
# import urllib
# import wikipedia

from os import walk, getcwd, path, symlink, mkdir, chdir, rename, listdir
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
        # self.seasons = self._flatten(self.seasons)
        self.seasons = self._flatten(self.seasons)
        print(self.seasons)

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

        dir = path.realpath(dir)
        # for root, dirs, files in walk(dir):
        #     for file in files:
        files = next(walk(dir), (None, None, []))[2]
        #
        files.sort()
        #
        # for idx in range(len(files)):
        #     tmp = path.join(self.src, files[idx])
        #     files[idx] = path.realpath(tmp)
        videos = filter(lambda zz: mimetypes.guess_type(os.fsdecode(zz)) != (None, None) \
                        and mimetypes.guess_type(os.fsdecode(zz))[0].startswith('video'), files)
        videos = map(lambda xx: path.realpath(path.join(self.src, xx)), videos)
        videos = list(videos)
        # print(list(videos))
        #
        # files = [mimetypes.guess_type(os.fsdecode(item)) for item in os.listdir(dir)]
        # print(files)
        # videos = filter(lambda xx: xx != (None, None), files)
        # print(videos)

        # for file in os.listdir(dir):
        #     print(file)
        #     filename = os.fsdecode(file)
        #     print (mimetypes.guess_type(filename))
            # if mimetypes.guess_type(filename)[0].startswith('video'):
            #     print(file)


        # print(files)
        return videos

        # return files

    def _flatten(self, *n):
        '''Flattens lists of lists, even deeply nested ones'''
        return list((e for a in n
                for e in (self._flatten(*a) if isinstance(a, (tuple, list)) else (a,))))
    # OG Code:
    # Written by samplebias: https://stackoverflow.com/users/538718/samplebias
    # flatten = lambda *n: (e for a in n
    #    for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

    def linker(self):
        ii = 1
        episodes = self._find()
        print(episodes)
        for season in self.seasons:
            try:
                mkdir('./Season %.2d' % ii)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    pass
                else:
                    raise e
            chdir('Season %.2d' % ii)
            ## Link files
            limit = int(season)
            for ep in episodes:
                if limit == 0:
                    break
                # print(path.realpath(ep))
                try:
                    symlink(ep, path.basename(ep))
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        pass
                    else:
                        raise e
                episodes.pop(0) # consume each episode as we link it
                limit -= 1
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
            ii += 1



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
