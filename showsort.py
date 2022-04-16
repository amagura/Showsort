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

from os import walk, getcwd, path, symlink, mkdir, chdir, rename, listdir, rmdir
from pathlib import Path
from sys import argv, exit
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
        self.one = args.one
        # self.episodes = self._find()
        # print(self.seasons)
        # print(self.episodes[0])

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

    def _find(self, shows=None):
        if shows == None:
            shows = self.src


        if type(shows) is not list:
            shows = [shows]
            # for show in shows:
            #     print(show)
            #     exit(0)

        shows = map(lambda x: path.realpath(x), shows)

        videos = []

        for show in shows:
            files = next(walk(show), (None, None, []))[2]
            files.sort()

            known = filter(lambda x: mimetypes.guess_type(os.fsdecode(x)) != (None, None), files)
            vids = filter(lambda x: mimetypes.guess_type(os.fsdecode(x))[0].startswith('video'), known)
            real_vids = map(lambda x: path.join(show, x), vids)
            vids = list(real_vids)
            videos.append(vids)


        videos = self._flatten(videos)
        # self.episodes = videos
        # print(videos)
        # exit(0)
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

    def sort(self):
        self.episodes = self._find()
        # print(self.episodes)
        # exit(0)
        self._linker()

    def _link(self, episode):
        try:
            glob = next(Path('.').glob(f'S*E* {path.basename(episode)}'))
            print(f'glob: {glob}')
        except StopIteration as e:
            pass
            try:
                symlink(episode, path.basename(episode))
            except OSError as e:
                if e.errno == errno.EEXIST:
                    pass
                else:
                    raise e

    def _linker(self):
        ii = 1
        # print(self.episodes)
        for season in self.seasons:
            if self.one:
                ii = 1
            try:
                # FIXME if there are more than 99 seasons, the seasons won't
                # all have the same number of digits
                mkdir('./Season %.2d' % ii)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    pass
                else:
                    raise e
            chdir('Season %.2d' % ii)
            ## Link files
            # print(f'season: {season}')
            for epint in range(int(season)):
                # print(f'epint: {epint}')
                # if limit == 0:
                #     break
                # print(path.realpath(ep))
                try:
                    ep = self.episodes.pop(0)
                except IndexError as e:
                    left = 1 if len(self.seasons) - ii == 0 else len(self.seasons) - ii
                    right = 'season' if left == 1 else 'seasons'
                    print(f'error: out of episodes, but {left} {right} left')
                    print('listdir: %s' % os.listdir('..'))
                    chdir('..')
                    rmdir('Season %.2d' % ii)
                    # print(f'* ii: {ii}\n* len(self.seasons): {len(self.seasons)}')
                    # for kdx in range(ii, len(self.seasons)):
                    #     chdir('..')
                    #     print(f'self.seasons: {self.seasons}')
                    #     print(f'Season %d: Season {kdx}')
                    #     rmdir('Season %.2d' % kdx)
                    return
                self._link(ep)
                # episodes.pop(0) # consume each episode as we link it
                # limit -= 1
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
                prefix = 'S%.2dE%.2d ' % (ii, jj)
                episode = re.sub(r'/S\d+E\d+ ', '/', episode)
                nn, _ = re.subn(r'^(S\d*E\d* )?', prefix, path.basename(episode))
                #tmp = "S%.2dE%.2d %s" % (ii, jj, path.basename(episode))
                rename(episode, nn)
                # print(f'`{episode}` -> `{nn}`')
                jj += 1
            chdir('../')
            ii += 1
        if ii == 1:
            for ep in self.episodes:
                self._link(ep)


def dirp(s):
    return True if path.exists(path.dirname(path.abspath(s))) else False


#
parser = argparse.ArgumentParser(description='Sorts shows in a non-destructive manner')
parser.add_argument('show', type=str, nargs='+', help='directory containing episodes')
parser.add_argument('-s', '--season', action='append', nargs='+', help="split show into seasons")
parser.add_argument('-1', '--one', action='store_true', help='show only contains one season: for when you have multiple copies of the same show')
args = parser.parse_args()

srt = Sorter(args)
srt.sort()

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
