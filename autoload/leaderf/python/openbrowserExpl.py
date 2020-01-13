#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import vim
import sys
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *


# *****************************************************
# OpenbrowserExplorer
# *****************************************************
class OpenbrowserExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        # g:openbrowser_search_engines
        engins = vim.vars.get("openbrowser_search_engines", {})
        # g:Lf_openbrowser_bookmarks
        bookmarks = vim.vars.get("Lf_openbrowser_bookmarks", {})

        # Use lfBytes2Str because return value is bytes
        sources = []
        sources.extend(
            [[lfBytes2Str(name), lfBytes2Str(url)] for name, url in engins.items()]
        )
        sources.extend(
            [[lfBytes2Str(name), lfBytes2Str(url)] for name, url in bookmarks.items()]
        )

        if len(sources) == 0:
            return []

        max_name_len = max(
            map(lambda x: int(lfEval("strdisplaywidth('{}')".format(x[0]))), sources)
        )

        lines = []
        for source in sources:
            name, url = source
            if sys.version_info >= (3, 0):
                import urllib.parse
                url = urllib.parse.unquote(url)
            width = int(lfEval("strdisplaywidth('{}')".format(name)))
            space_num = max_name_len - width
            lines.append('{}{} "{}"'.format(name, " " * space_num, url))

        return lines

    def getStlCategory(self):
        return "OpenBrowser"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def supportsNameOnly(self):
        return True

# *****************************************************
# OpenbrowserExplManager
# *****************************************************
class OpenbrowserExplManager(Manager):
    def __init__(self):
        super(OpenbrowserExplManager, self).__init__()

    def _getExplClass(self):
        return OpenbrowserExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#OpenBrowser#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]

        name = self._getDigest(line, 1)
        url = self._getDigest(line, 2)

        if "{query}" in url:
            lfCmd("call feedkeys(':OpenBrowserSmartSearch -{} ', 'n')".format(name))
        else:
            if sys.version_info >= (3, 0):
                import urllib.parse
                url = urllib.parse.quote(url, safe=':/')
            lfCmd("call openbrowser#open('{}')".format(url))

    def _getDigest(self, line, mode):
        """
        mode: 0, return the full path
              1, return the name only
              2, return the directory name
        """
        if not line:
            return ""

        if mode == 0:
            return line
        elif mode == 1:
            start_pos = line.find(' "')
            return line[:start_pos].rstrip()
        else:
            start_pos = line.find(' "')
            return line[start_pos+2:-1]

    def _getDigestStartPos(self, line, mode):
        if not line:
            return 0

        if mode == 2:
            start_pos = line.find(' "')
            return lfBytesLen(line[:start_pos+2])
        else:
            return 0

    def _afterEnter(self):
        super(OpenbrowserExplManager, self)._afterEnter()
        if self._getInstance().getWinPos() == "popup":
            lfCmd(
                """call win_execute(%d, 'let matchid = matchadd(''Lf_hl_openbrowserUrl'', ''\s\+\zs".\+'')')"""
                % self._getInstance().getPopupWinId()
            )
            id = int(lfEval("matchid"))
            self._match_ids.append(id)
        else:
            id = int(lfEval("matchadd('Lf_hl_openbrowserUrl', '\s\+\zs" ".\+')"))
            self._match_ids.append(id)

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help


# *****************************************************
# openbrowserExplManager is a singleton
# *****************************************************
openbrowserExplManager = OpenbrowserExplManager()

__all__ = ["openbrowserExplManager"]
