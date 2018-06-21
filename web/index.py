#! /usr/bin/python


from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return "Welcome to out reddit style app based on the multichain !"


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=8080)


