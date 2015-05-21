
from flask import jsonify, render_template

from flaskApp import app, db, manager
from flaskApp.models import Container, Item, ContainerItemRel






###### api functions #######


manager.create_api(Container
                    , collection_name='inventory'
                    , methods=['GET', 'POST', 'DELETE'])



######## Static pages ############


# splash page
@app.route('/')
def index():
    return render_template('index.html')
