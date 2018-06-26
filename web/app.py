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
    create_post(a['title'], a['content'], a['type'], a['privkey'])
    return 'ok'








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
    app.config['UPLOAD_FOLDER'] = '/tmp/'
    app.run(host='0.0.0.0', port=80, debug=False)
