#!/usr/bin/python -u

import os
import sys

from model import *
import config

def main():
    config.loadconfig()

    initmodel(config.config['dburi'])
    s = Session()

    while True:
        req = sys.stdin.readline()
        res = s.query(Backend).order_by(func.random()).first()
        if res is None:
            print 'NULL'
        else:
            print res.ipaddr

if __name__ == '__main__':
    main()

