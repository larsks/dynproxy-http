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

@put('/backend/:name')
def new_backend(name):
    backend = Backend(
            name=name,
            ipaddr=request.remote_addr)
    request.db.add(backend)
    return yaml.dump({
        'status': 0,
        'action': 'create',
        'backend': backend.as_dict(),
        })

@post('/backend/:name')
def update_backend(name):
    backend = request.db.query(Backend).get(name)
    if backend is None:
        return new_backend(name)

    backend.ipaddr=request.remote_addr
    return yaml.dump({
        'status': 0,
        'action': 'update',
        'backend': backend.as_dict(),
        })

@route('/backend/:name')
def show_backend(name):
    backend = request.db.query(Backend).get(name)
    if backend is None:
        abort(404, 'No backend named %s' % name)

    return yaml.dump({
        'status': 0,
        'action': 'show',
        'backend': backend.as_dict(),
        })

@delete('/backend/:name')
def delete_backend(name):
    backend = request.db.query(Backend).get(name)
    if res is None:
        abort(404, 'No backend named %s' % name)

    request.db.delete(backend)
    return yaml.dump({
        'status': 0,
        'action': 'delete',
        })

@route('/backend')
def list_backend():
    backend = request.db.query(Backend)
    return yaml.dump({
        'status': 0,
        'action': 'list',
        'backends': [x.as_dict() for x in backend],
        })

app = bottle.default_app()

if __name__ == '__main__':
    bottle.run()

