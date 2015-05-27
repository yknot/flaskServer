# import render_template for the static index page
from flask import render_template, jsonify

# import the app, the database, and the api manager
from flaskApp import app, db, manager
# import the models
from flaskApp.models import Container, Item

import simplejson

###### api functions #######
# list of tasks that the api can do
# this is hardcoded since it to add tasks needs more coding
@app.route('/api', methods=['GET'])
def list_tasks():
    return jsonify({'tasks':['inventory']})


# list inventories
@app.route('/api/inventory', methods=['GET'])
def list_inventories():
    return jsonify(inventories =
                [i.serialize() for i in Container.query.all()])


# modify/add inventory

# delete inventory



# list items in named inventory
@app.route('/api/inventory/<name>', methods=['GET'])
def get_items(name):
    return jsonify(items =
                [i.serialize() for i in
                        Container.query.filter_by(name = name).first().items])

# get specific item

# modify/add item

# delete item




######## Static pages ############
# splash page
@app.route('/')
def index():
    return render_template('index.html')
