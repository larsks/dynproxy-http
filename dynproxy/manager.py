#!/usr/bin/python -u

import os
import sys

import yaml
import bottle
from bottle import route, post, put, hook, request, response, abort, delete

import config
from model import *

@hook('before_request')
def setup_request():
    config.loadconfig()
    initmodel(config.config['dburi'])
    request.db = Session()

@hook('after_request')
def finish_request():
    request.db.commit()
    response.content_type='text/plain'

@put('/proxy/:name')
def new_proxy(name):
    proxy = Backend(
            name=name,
            ipaddr=request.remote_addr)
    request.db.add(proxy)
    return yaml.dump({
        'status': 0,
        'message': 'created',
        'proxy': proxy.as_dict(),
        })

@post('/proxy/:name')
def update_proxy(name):
    proxy = request.db.query(Backend).get(name)
    if proxy is None:
        abort(404, 'No proxy named %s' % name)

    proxy.ipaddr=request.remote_addr
    return yaml.dump({
        'status': 0,
        'message': 'updated',
        'proxy': proxy.as_dict(),
        })

@route('/proxy/:name')
def show_proxy(name):
    proxy = request.db.query(Backend).get(name)
    if proxy is None:
        abort(404, 'No proxy named %s' % name)

    return yaml.dump({
        'status': 0,
        'message': 'present',
        'proxy': proxy.as_dict(),
        })

@delete('/proxy/:name')
def delete_proxy(name):
    proxy = request.db.query(Backend).get(name)
    if proxy is None:
        abort(404, 'No proxy named %s' % name)

    request.db.delete(proxy)
    return yaml.dump({
        'status': 0,
        'message': 'deleted',
        })

app = bottle.default_app()

if __name__ == '__main__':
    bottle.run()

