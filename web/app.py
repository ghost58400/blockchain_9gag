#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
import json

from web.utils import *

app = Flask(__name__)


@app.route('/')
def index():
    api = get_api('localhost', '1235', 'chain1')
    return get_all_posts(api)
    # return jsonify(streams)


@app.route('/new_post', methods=['POST'])
def new_post():
    return "Créer un post"


# return jsonify(stream)


@app.route('/show_post/<num_stream>', methods=['GET'])
def show_post(num_stream):
    return "Post : {}".format(num_stream)


# stream = récupération stream
# return jsonify(stream)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
