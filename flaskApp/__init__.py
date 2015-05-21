# import flask; make_response and jsonify for error handl
from flask import Flask, make_response, jsonify
# SQLAlchemy connection
from flask.ext.sqlalchemy import SQLAlchemy
# import manager to create apis
from flask.ext.restless import APIManager
# for checking environment variables
import os


# create app with instance folder
app = Flask(__name__, instance_relative_config=True)



# if on heroku read production config
if (os.environ.get('IS_HEROKU', None)):
    app.config.from_object('config')

# else on developement so read instance config file
else:
    app.config.from_pyfile('config.py')


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
