#!/usr/bin/python

import sys
import os
import site

appdir = os.path.dirname(__file__)
sys.path.append(appdir)
os.chdir(appdir)

if os.path.exists('virtenv'):
    site.addsitedir('virtenv/lib/python%d.%d/site-packages' % (
        sys.version_info[0], sys.version_info[1]))

import dynproxy.manager
application = dynproxy.manager.app

