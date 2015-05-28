# import render_template for the static index page
from flask import render_template, jsonify

# import the app, the database, and the api manager
from flaskApp import app, db, manager
# import the models
from flaskApp.models import Container, Item

import simplejson

###### api functions #######
# list of tasks that the api can do
@app.route('/api', methods=['GET'])
def list_tasks():
    # this is hardcoded since it to add tasks needs more coding
    return jsonify({'tasks':['inventory']})


# list inventories
@app.route('/api/inventory', methods=['GET'])
def list_inventories():
    # get all inventories and call serialize on each
    inventories = [i.serialize() for i in Container.query.all()]
    # return as json
    return jsonify(inventories = inventories)


# modify/add inventory

# delete inventory
@app.route('/api/inventory/<name>', methods=['DELETE'])
def delete_inventory(name):
    # check to make sure 1 and only one record
    if Container.query.filter_by(name = name).delete() == 1:
        # if one record commit transaction
        db.session.commit()
        # return name of deleted container
        return jsonify(deleted = {'name' : name})


# list items in named inventory
@app.route('/api/inventory/<name>', methods=['GET'])
def get_items(name):
    # query for the specific inveontory
    qryresult = Container.query.filter_by(name = name).first()
    # get and serialize items from inveontory
    items = [i.serialize() for i in qryresult.items]
    # return as json
    return jsonify(items = items)

# get specific item
@app.route('/api/inventory/<name>/<int:item_id>', methods=['GET'])
def get_item(name, item_id):
    # get containerId from name
    cid = Container.query.filter_by(name = name).first().id
    # get items within containerId
    qryresult = Item.query.filter_by(id = item_id, containerId = cid).first()
    # return the one item serialized
    return jsonify(qryresult.serialize())

# modify/add item

# delete item
@app.route('/api/inventory/<name>/<int:item_id>', methods=['DELETE'])
def delete_item(name, item_id):
    # get containerId from name
    cid = Container.query.filter_by(name = name).first().id
    # check to make sure 1 and only one record
    if Item.query.filter_by(id = item_id, containerId = cid).delete() == 1:
        # if one record commit transaction
        db.session.commit()
        # return name of deleted container
        return jsonify(deleted = { 'item_id' : item_id,
                'inventory_name' : name})



######## Static pages ############
# splash page
@app.route('/')
def index():
    return render_template('index.html')
