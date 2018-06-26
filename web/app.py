#! /usr/bin/python
# -*- coding:utf-8 -*-
from threading import Thread

from flask import Flask, send_from_directory, jsonify, request
from chain_utils import *

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/chain_name')
def chain_name():
    return get_chain_name()


@app.route('/connect_blockchain/<chain_name>/<ip>/<port>/<nickname>')
def connect_blockchain(chain_name, ip, port, nickname):
    Thread(target=connect_chain, args=[ip, port, chain_name, nickname]).start()
    return 'ok'


@app.route('/create_blockchain/<chain_name>/<nickname>')
def create_blockchain(chain_name, nickname):
    Thread(target=create_chain, args=[chain_name, nickname]).start()
    return 'ok'


@app.route('/state')
def state():
    return get_state()


@app.route('/get_posts')
def get_posts():
    if get_chain_name() == '':
        return 'pas de chaine configuree'
    posts = get_all_posts(get_api())
    return jsonify(posts)


@app.route('/new_post', methods=['POST'])
def new_post():
    a = request.form
    f = request.files
    if len(f) ==1 and a['type'] == 'Image':
        create_post(a['title'], f['image'], a['type'])
        return 'ok'
    if len(f) == 0 and a['type'] == 'Text':
        create_post(a['title'], a['content'], a['type'])
        return 'ok'
    return 'coherency problem'


@app.route('/log')
def log():
    return send_from_directory('/root/web', 'log.txt')









@app.route('/show_post/<num_stream>', methods=['GET'])
def show_post(num_stream):
    return "Post : {}".format(num_stream)
# stream = récupération stream
# return jsonify(stream)


if __name__ == '__main__':
    set_state('Not connected')
    name = get_chain_name()
    if name != '':
        call("nohup multichaind " + name + " -daemon", shell=True)
    app.run(host='0.0.0.0', port=80, debug=False)
