#!/usr/bin/python

import os
import sys
import yaml

DEFAULT_CFG_FILE = os.environ.get('CLOUDPROXY_CONFIG',
        '/etc/cloudproxy.yml')

config = {}

def loadconfig(path=DEFAULT_CFG_FILE):
    global config
    config = yaml.load(open(path))

