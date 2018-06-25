#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, send_from_directory, jsonify
from chain_utils import *

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/chain_name')
def chain_name():
    return get_chain_name()


@app.route('/connect/<chain_name>/<ip>/<port>/<nickname>')
def connect(chain_name, ip, port, nickname):
    connect_chain(ip, port, chain_name, nickname)
    return 'ok'


@app.route('/create_blockchain/<chain_name>')
def create_blockchain(chain_name):
    create_chain(chain_name)
    return 'ok'


@app.route('/get_posts')
def get_posts():
    if get_chain_name() == '':
        return 'pas de chaine configuree'
    posts = get_all_posts(get_api())
    return jsonify(posts)
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
    app.run(host='0.0.0.0', port=80)
