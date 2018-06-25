#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
import json


app = Flask(__name__)


@app.route('/')
def index():
	return "Welcome to out reddit style app based on the multichain !"
	# streams = récupération streams
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


