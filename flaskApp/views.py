# import render_template for the static index page
from flask import render_template

# import the app, the database, and the api manager
from flaskApp import app, db, manager
# import the models
from flaskApp.models import Container, Item




###### api functions #######
# container api aka inventory
manager.create_api(Container
                    , primary_key='name'
                    , collection_name='inventory'
                    , methods=['GET', 'POST', 'DELETE'])

manager.create_api(Item
                    , methods=['GET', 'POST', 'DELETE'])


######## Static pages ############
# splash page
@app.route('/')
def index():
    return render_template('index.html')
