#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, send_from_directory
import json

from chain_utils import *

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/chain_name')
def chain_name():
    return get_chain_name()


@app.route('/connect/<chain_name>/<ip>/<port>')
def connect(chain_name, ip, port):
    connect_chain(ip, port, chain_name)
    return 'ok'


@app.route('/create_blockchain/<chain_name>')
def create_blockchain(chain_name):
    create_chain(chain_name)
    return 'ok'


@app.route('/get_posts')
def get_posts():
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
    app.run(host='0.0.0.0', port=8081)
