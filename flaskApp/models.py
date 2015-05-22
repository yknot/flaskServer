# import the database
from flaskApp import db


class Container(db.Model):
    """Containers are the groups in which the items are located"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship('Item')


    def __init__(self, name):
        self.name = name



class Item(db.Model):
    """Items are the objects stored in containers"""
    id = db.Column(db.Integer, primary_key=True)
    containerId = db.Column(db.Integer, db.ForeignKey('container.id'), primary_key=True)
    name = db.Column(db.String(200), unique=True)
    quantity = db.Column(db.Integer)
    purchaseDate = db.Column(db.Date)
    expirationDate = db.Column(db.Date)
    purchasePrice = db.Column(db.Float)

    container = db.relationship('Container')



    def __init__(self, name):
        self.containerId = containerId
        self.name = name
        self.quantity = quantity
        self.purchaseDate = purchaseDate
        self.expirationDate = expirationDate
        self.purchasePrice = purchasePrice
