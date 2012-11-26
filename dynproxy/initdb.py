#!/usr/bin/python

import os
import sys

from model import *
import config

def main():
    config.loadconfig()
    initmodel(config.config['dburi'])
    print 'Initialized database (%s).' % config.config['dburi']

if __name__ == '__main__':
    main()

