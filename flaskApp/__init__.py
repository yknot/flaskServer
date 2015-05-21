# import flask
from flask import Flask

# SQLAlchemy connection
from flask.ext.sqlalchemy import SQLAlchemy

# import manager to create apis
from flask.ext.restless import APIManager

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


# startup db connection
db = SQLAlchemy(app)

# create api manager
manager = APIManager(app, flask_sqlalchemy_db=db)


# import all the views
import flaskApp.views
