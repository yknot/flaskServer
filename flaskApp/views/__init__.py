# import render_template for the static index page
# jsonify for creating responses
# abort for calling 404
# request for POST methods
from flask import render_template, jsonify, abort, request
# import the app, the database, and the api manager
from flaskApp import app, db
# import the models
from flaskApp.models import Inventory, Item

from item import *
from inventory import *

###### api functions #######
# list of tasks that the api can do
@app.route('/api', methods=['GET'])
def list_tasks():
    # this is hardcoded since it to add tasks needs more coding
    return jsonify({'tasks':[{'title':'Inventory', 'description':'Inventories of pantry, freezer, etc.'}]})



######## Static pages ############
# splash page
@app.route('/')
def index():
    return render_template('index.html')
