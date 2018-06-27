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

@app.route('/myetheraddr')
def myetheraddr():
    return get_ethaddr()

@app.route('/get_posts')
def get_posts():
    if get_chain_name() == '':
        return jsonify([])
    posts = get_all_posts(get_api())
    return jsonify(posts)


@app.route('/new_post', methods=['POST'])
def new_post():
    a = request.form
    f = request.files
    if len(f) ==1 and a['type'] == 'Image':
        return create_post(a['title'], f['image'], a['type'])
    if len(f) == 0 and a['type'] == 'Text':
        return create_post(a['title'], a['content'], a['type'])
    return 'coherency problem'


@app.route('/log')
def log():
    return send_from_directory('/root/web', 'log.txt')


@app.route('/create_group/<group_tag>/<group_name>')
def create_group_handler(group_tag, group_name):
    create_group(group_tag, group_name)
    return 'ok'


@app.route('/join_group/<group_tag>')
def join_group_handler(group_tag):
    join_group(group_tag)
    return 'ok'


@app.route('/add_to_group/<address>/<group_tag>')
def add_to_group_handler(address, group_tag):
    add_to_group(address, group_tag)
    return 'ok'


@app.route('/post_to_group', methods=['POST'])
def post_to_group():
    a = request.form
    f = request.files
    if len(f) == 1 and a['type'] == 'Image':
        return post_group(a['title'], f['image'], a['type'], a['tag'])
    if len(f) == 0 and a['type'] == 'Text':
        return post_group(a['title'], a['content'], a['type'], a['tag'])
    return 'coherency problem'


@app.route('/get_pending_invites')
def invites():
    return jsonify(get_pending_invite(get_myaddr(), get_api()))


@app.route('/get_addresses')
def addresses():
    return jsonify(get_list_addresses(get_api()))


@app.route('/get_posts/<group_tag>')
def posts_group(group_tag):
    return jsonify(get_all_posts(get_api(), group_tag))


@app.route('/get_my_groups')
def my_groups():
    return jsonify(get_list_group(get_myaddr(), get_api(), True))


if __name__ == '__main__':
    kill_old_daemon()
    set_state('Not connected')
    name = get_chain_name()
    #createEtherAddr()
    if name != '':
        call("multichaind " + name + " -daemon -autosubscribe=streams", shell=True)
        set_state('Connected to ' + name)
    app.run(host='0.0.0.0', port=80, debug=False)
