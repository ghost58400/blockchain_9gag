#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify


app = Flask(__name__)
api = Api(app)
CORS(app)

import web.models
import web.controllers
