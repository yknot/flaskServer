# import flask
# render_template for template folder
# jsonify for json returns
# abort for error handling
# make_response for adding in response values
# request for using post, put and delete
from flask import Flask, render_template, jsonify, abort, make_response, request
# to authorize users
from flask.ext.httpauth import HTTPBasicAuth
import os


# create app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
if not (os.environ.get('IS_HEROKU', None)):
    app.config.from_pyfile('config.py')
auth = HTTPBasicAuth()

# splash page
@app.route('/')
def index():
    return render_template('index.html')

# user login info
@auth.get_password
def get_password(username):
    if username == 'yknot':
        return 'python'
    return None

# wrong login
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

##### create items ##### change to database
items = [
    {
        'id' : 1,
        'title' : 'testing this'
    },
    {
        'id' : 2,
        'title' : 'testing that'
    }
]
########################



###### api functions #######
# api GET all items
@app.route('/api/items', methods=['GET'])
@auth.login_required
def get_items():
    # return all items as json
    return jsonify({'items' : items})


# api GET specific items
@app.route('/api/items/<int:item_id>', methods=['GET'])
@auth.login_required
def get_item(item_id):
    # find item
    item = [item for item in items if item['id'] == item_id]
    # if not exists error
    if len(item) == 0:
        abort(404)
    return jsonify({'item' : item[0]})


# api POST add item
@app.route('/api/items', methods=['POST'])
@auth.login_required
def create_item():
    # if not right format
    if not request.json or not 'name' in request.json:
        abort(400)
    # create the item
    item = {
        'id': items[-1]['id'] + 1,
        'name': request.json['name']
    }
    # add to list of items
    items.append(item)
    return jsonify({'item': item}), 201


# api PUT update item
@app.route('/api/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(item_id):
    # find item to update
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    elif not request.json:
        abort(400)
    elif 'name' not in request.json:
        abort(400)
    # update
    item[0]['name'] = request.json.get('name', item[0]['name'])
    return jsonify({'item': item[0]})


# api DELETE delete item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(400)
    # delete item
    items.remove(item[0])
    return jsonify({'result': True})


##### error handling  #######
# 404 error
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

# 400 error
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error' : 'Bad request'}), 400)


# run the app
if __name__ == '__main__':
    # start app
    app.run()
