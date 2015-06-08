# import render_template for the static index page
# jsonify for creating responses
# abort for calling 404
# request for POST methods
from flask import render_template, jsonify, abort, request
# import the app, the database, and the api manager
from flaskApp import app, db, manager
# import the models
from flaskApp.models import Inventory, Item


def get_inventory(name):
    """Get the inventory object given a name"""
    i = Inventory.query.filter_by(name = name).first()
    if i == None:
        abort(404)
    else:
        return i


##### items ###########

# list items in named inventory
@app.route('/api/inventory/<name>', methods=['GET'])
def get_items(name):
    # query for the specific inveontory
    qryresult = get_inventory(name)

    # get and serialize items from inveontory
    items = [i.serialize() for i in qryresult.items]

    # return as json
    return jsonify(items = items)




# get specific item
@app.route('/api/inventory/<name>/<int:item_id>', methods=['GET'])
def get_item(name, item_id):
    # get inventory id
    cid = get_inventory(name).id

    # get items within inventoryId
    qryresult = Item.query.filter_by(id = item_id, inventoryId = cid).first()
    if qryresult == None:
        abort(404)

    # return the one item serialized
    return jsonify(qryresult.serialize())





# modify/add item
@app.route('/api/inventory/<cName>', methods=['POST'])
def add_item(cName):
    # get inventory id
    cid = get_inventory(cName).id

    # if input is not correct error
    if not request.json or 'name' not in request.json:
        abort(400)

    name = request.json['name']

    items = Item.query.filter_by(name = name, inventoryId = cid).all()

    # if item already exists
    if len(items) == 1:
        # update item
        i = items[0]

        if 'quantity' in request.json:
            i.quantity = request.json['quantity']
        if 'purchaseDate' in request.json:
            i.purchaseDate = request.json['purchaseDate']
        if 'expirationDate' in request.json:
            i.expirationDate = request.json['expirationDate']
        if 'purchasePrice' in request.json:
            i.purchasePrice = request.json['purchasePrice']

        db.session.commit()
        return jsonify({'updated_item' : i.serialize()})

    elif len(items) > 1:
        # delete items because can't determine
        # this shouldn't happen because there shouldn't be dup names
        Item.query.filter_by(name = name, inventoryId = cid).delete()

    # create new item
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
    # return the new item
    return jsonify({'created_item' : temp.serialize()})






# delete item
@app.route('/api/inventory/<name>/<int:item_id>', methods=['DELETE'])
def delete_item(name, item_id):
    # get inventory  id
    cid = get_inventory(name).id

    # check to make sure 1 and only one record
    if Item.query.filter_by(id = item_id, inventoryId = cid).delete() == 1:
        # if one record commit transaction
        db.session.commit()
        # return name of deleted inventory
        return jsonify(deleted = { 'item_id' : item_id,
                'inventory_name' : name})
    else:
        abort(404)
