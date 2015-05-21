
from flask import jsonify, render_template

from flaskApp import app
from flaskApp.models import db, Container






###### api functions #######
# api GET all items
@app.route('/api/inventory', methods=['GET'])
def get_items():
    # return all items as json
    # return jsonify({'items' : items})
    return Container.query.all()










######## Static pages ############


# splash page
@app.route('/')
def index():
    return render_template('index.html')
