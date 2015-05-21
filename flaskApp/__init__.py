# import flask
# render_template for template folder
# jsonify for json returns
# abort for error handling
# make_response for adding in response values
# request for using post, put and delete
from flask import Flask, render_template#, jsonify, abort, make_response, request
# to authorize users
# from flask.ext.httpauth import HTTPBasicAuth
# SQLAlchemy connection
from flask.ext.sqlalchemy import SQLAlchemy
import os


# create app
app = Flask(__name__, instance_relative_config=True)

# read standard production config file
app.config.from_object('config')

# if not on Heroku read the instance config file
# means you are on dev
if not (os.environ.get('IS_HEROKU', None)):
    app.config.from_pyfile('config.py')

# set database uri based on environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://andrewyale@localhost/testdb'

#os.environ.get('DATABASE_URL')

# startup db connection
db = SQLAlchemy(app)


import flaskApp.views
#
# # splash page
# @app.route('/')
# def index():
#     return render_template('index.html')
