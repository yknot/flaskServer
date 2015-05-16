# import flask
from flask import Flask, render_template, jsonify, abort, make_response, request

# create app
app = Flask(__name__)

# splash page
@app.route('/')
def index():
    return render_template('index.html')


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
def get_items():
    return jsonify({'items' : items})


# api GET specific items
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'item' : item[0]})


# api POST add item
@app.route('/api/items', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        abort(400)
    item = {
        'id': items[-1]['id'] + 1,
        'name': request.json['name']
    }
    items.append(item)
    return jsonify({'item': item}), 201


# api PUT update item
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    elif not request.json:
        abort(400)
    elif 'name' not in request.json:
        abort(400)
    item[0]['name'] = request.json.get('name', item[0]['name'])
    return jsonify({'item': item[0]})


# api DELETE delete item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(400)

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
    # reload on change of file
    app.debug = True
    app.run()
