# import render_template for the static index page
# jsonify for creating responses
# abort for calling 404
# request for POST methods
from flask import render_template, jsonify, abort, request
# import the app, the database, and the api manager
from flaskApp import app, db, manager
# import the models
from flaskApp.models import Inventory, Item


###### inventories ###########
# list inventories
@app.route('/api/inventory', methods=['GET'])
def list_inventories():
    # get all inventories and call serialize on each
    inventories = [i.serialize() for i in Inventory.query.all()]
    # return as json
    return jsonify(inventories = inventories)


# modify/add inventory
@app.route('/api/inventory', methods=['POST'])
def add_inventory():
    # if input is not correct error
    if not request.json or 'name' not in request.json:
        abort(400)
    name = request.json['name']
    # if inventory already exists
    if len(Inventory.query.filter_by(name = name).all()) > 0:
        abort(400)
    # create new inventory
    temp = Inventory(name)
    # add and commit
    db.session.add(temp)
    db.session.commit()
    # return name of new inventory
    return jsonify({'created_inventory' : name})


# delete inventory
@app.route('/api/inventory/<name>', methods=['DELETE'])
def delete_inventory(name):
    # check to make sure 1 and only one record
    if Inventory.query.filter_by(name = name).delete() == 1:
        # if one record commit transaction
        db.session.commit()
        # return name of deleted inventory
        return jsonify(deleted = {'name' : name})
    else:
        abort(404)
