from flaskApp import db


class Container(db.Model):
    """docstring for Container"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "{'id': " + str(self.id) + ", 'name': '" + self.name + "'    }"

    # def __repr__(self):
    #     return "{Container : %r" % self.name
