# import flask
from flask import Flask
from flask.ext import restful

# create app
app = Flask(__name__)
# create api
api = restful.Api(app)

# list all of the resorts
class SkiResorts(restful.Resource):
    def get(self):
        return 'Work in progress!'

# add SkiResorts resource
api.add_resource(SkiResorts, '/SkiResorts')

# run the app
if __name__ == '__main__':
    app.run()



