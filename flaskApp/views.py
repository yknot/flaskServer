# import render_template for the static index page
# jsonify for creating responses
# abort for calling 404
# request for POST methods
from flask import render_template, jsonify, abort, request
# import the app, the database, and the api manager
from flaskApp import app, db, manager
# import the models
from flaskApp.models import Container, Item

###### api functions #######
# list of tasks that the api can do
@app.route('/api', methods=['GET'])
def list_tasks():
    # this is hardcoded since it to add tasks needs more coding
    return jsonify({'tasks':['inventory']})



###### inventories ###########
# list inventories
@app.route('/api/inventory', methods=['GET'])
def list_inventories():
    # get all inventories and call serialize on each
    inventories = [i.serialize() for i in Container.query.all()]
    # return as json
    return jsonify(inventories = inventories)


# modify/add inventory
@app.route('/api/inventory', methods=['POST'])
def add_inventory():
    # if input is not correct error
    if not request.json or 'name' not in request.json:
        abort(400)
    name = request.json['name']
    # if container already exists
    if len(Container.query.filter_by(name = name).all()) > 0:
        abort(400)
    # create new container
    temp = Container(name)
    # add and commit
    db.session.add(temp)
    db.session.commit()
    # return name of new container
    return jsonify({'created_inventory' : name})


# delete inventory
@app.route('/api/inventory/<name>', methods=['DELETE'])
def delete_inventory(name):
    # check to make sure 1 and only one record
    if Container.query.filter_by(name = name).delete() == 1:
        # if one record commit transaction
        db.session.commit()
        # return name of deleted container
        return jsonify(deleted = {'name' : name})
    else:
        abort(404)



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



######## Static pages ############
# splash page
@app.route('/')
def index():
    return render_template('index.html')
