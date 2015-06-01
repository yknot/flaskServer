# import render_template for the static index page
# jsonify for creating responses
# abort for calling 404
# request for POST methods
from flask import render_template, jsonify, abort, request
# import the app, the database, and the api manager
from flaskApp import app, db, manager
# import the models
from flaskApp.models import Container, Item


##### items ###########

# list items in named inventory
@app.route('/api/inventory/<name>', methods=['GET'])
def get_items(name):
    # query for the specific inveontory
    qryresult = Container.query.filter_by(name = name).first()
    if qryresult == None:
        abort(404)
    # get and serialize items from inveontory
    items = [i.serialize() for i in qryresult.items]
    # return as json
    return jsonify(items = items)

# get specific item
@app.route('/api/inventory/<name>/<int:item_id>', methods=['GET'])
def get_item(name, item_id):
    # get container if exists
    c = Container.query.filter_by(name = name).first()
    if c == None:
        abort(404)
    # get containerId from result
    cid = c.id
    # get items within containerId
    qryresult = Item.query.filter_by(id = item_id, containerId = cid).first()
    if qryresult == None:
        abort(404)
    # return the one item serialized
    return jsonify(qryresult.serialize())


# modify/add item
@app.route('/api/inventory/<cName>', methods=['POST'])
def add_item(cName):
    # get container if exists
    c = Container.query.filter_by(name = cName).first()
    if c == None:
        abort(404)
    # get containerId from result
    cid = c.id

    # if input is not correct error
    if not request.json or 'name' not in request.json:
        abort(400)

    name = request.json['name']
    # if item already exists
    if len(Item.query.filter_by(name = name, containerId = cid).all()) > 0:
        # delete item
        Item.query.filter_by(name = name, containerId = cid).delete()

    # create new container
    temp = Item(cid, name)

    if 'quantity' in request.json:
        temp.quantity = request.json['quantity']
    if 'purchaseDate' in request.json:
        temp.purchaseDate = request.json['purchaseDate']
    if 'expirationDate' in request.json:
        temp.expirationDate = request.json['expirationDate']
    if 'purchasePrice' in request.json:
        temp.purchasePrice = request.json['purchasePrice']

    # add and commit
    db.session.add(temp)
    db.session.commit()
    # return name of new container
    return jsonify({'created_item' : name})


# delete item
@app.route('/api/inventory/<name>/<int:item_id>', methods=['DELETE'])
def delete_item(name, item_id):
    # get container if exists
    c = Container.query.filter_by(name = name).first()
    if c == None:
        abort(404)
    # get containerId from result
    cid = c.id
    # check to make sure 1 and only one record
    if Item.query.filter_by(id = item_id, containerId = cid).delete() == 1:
        # if one record commit transaction
        db.session.commit()
        # return name of deleted container
        return jsonify(deleted = { 'item_id' : item_id,
                'inventory_name' : name})
    else:
        abort(404)
