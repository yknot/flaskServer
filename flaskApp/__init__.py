# import flask
from flask import Flask, make_response, jsonify

# SQLAlchemy connection
from flask.ext.sqlalchemy import SQLAlchemy

# import manager to create apis
from flask.ext.restless import APIManager

import os


# create app
app = Flask(__name__, instance_relative_config=True)

# read standard production config file
app.config.from_pyfile('config.py')

# if not on Heroku read the instance config file
# means you are on dev
if (os.environ.get('IS_HEROKU', None)):
    app.config.from_object('config')


# startup db connection
db = SQLAlchemy(app)

# create api manager
manager = APIManager(app, flask_sqlalchemy_db=db)


# import all the views
import flaskApp.views



###### error handling  #######
# 404 error
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

# 400 error
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error' : 'Bad request'}), 400)
