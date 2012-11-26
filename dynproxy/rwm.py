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
        sys.stdout.write('%s\n' % (res.ipaddr if res else 'NULL'))
        sys.stdout.flush()

if __name__ == '__main__':
    main()

