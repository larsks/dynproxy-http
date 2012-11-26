#!/usr/bin/python -u

import os
import sys

import yaml
import bottle
from bottle import route, post, put, hook, request, response, abort, delete

import config
from model import *

def asyaml (f):
    def _ (*args, **kwargs):
        res = f(*args, **kwargs)
        if isinstance(res, dict):
            response.content_type = 'text/yaml'
            return yaml.dump(res, default_flow_style=False)
        else:
            return res

    return _

@hook('before_request')
def setup_request():
    config.loadconfig()
    initmodel(config.config['dburi'])
    request.db = Session()

@hook('after_request')
def finish_request():
    request.db.commit()

@put('/backend/:name')
@asyaml
def new_backend(name):
    backend = Backend(
            name=name,
            ipaddr=request.remote_addr)
    request.db.add(backend)
    return {
        'status': 0,
        'action': 'create',
        'backend': backend.as_dict(),
        }

@post('/backend/:name')
@asyaml
def update_backend(name):
    backend = request.db.query(Backend).get(name)
    if backend is None:
        return new_backend(name)

    backend.ipaddr=request.remote_addr
    return {
        'status': 0,
        'action': 'update',
        'backend': backend.as_dict(),
        }

@route('/backend/:name/enable')
@asyaml
def enable_backend(name):
    backend = request.db.query(Backend).get(name)
    if backend is None:
        abort(404, 'No backend named %s' % name)

    backend.enabled = True

    return {
        'status': 0,
        'action': 'enable',
        'backend': backend.as_dict(),
        }

@route('/backend/:name/disable')
@asyaml
def disable_backend(name):
    backend = request.db.query(Backend).get(name)
    if backend is None:
        abort(404, 'No backend named %s' % name)

    backend.enabled = False

    return {
        'status': 0,
        'action': 'disable',
        'backend': backend.as_dict(),
        }

@route('/backend/:name')
@asyaml
def show_backend(name):
    backend = request.db.query(Backend).get(name)
    if backend is None:
        abort(404, 'No backend named %s' % name)

    return {
        'status': 0,
        'action': 'show',
        'backend': backend.as_dict(),
        }

@delete('/backend/:name')
@asyaml
def delete_backend(name):
    backend = request.db.query(Backend).get(name)
    if backend is None:
        abort(404, 'No backend named %s' % name)

    request.db.delete(backend)
    return {
        'status': 0,
        'action': 'delete',
        }

@route('/backend')
@asyaml
def list_backend():
    backend = request.db.query(Backend)
    return {
        'status': 0,
        'action': 'list',
        'backends': [x.as_dict() for x in backend],
        }

app = bottle.default_app()

if __name__ == '__main__':
    bottle.run(reloader=True)

