from flaskApp import db


class Container(db.Model):
    """docstring for Container"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


    def __init__(self, name):
        self.name = name



class Item(db.Model):
    """docstring for Item"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)


    def __init__(self, name):
        self.name = name



class ContainerItemRel(db.Model):
    """docstring for ContainerItemRel"""
    containerId = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    purchaseDate = db.Column(db.Date)
    expirationDate = db.Column(db.Date)
    purchasePrice = db.Column(db.Float)


    def __init__(self, ):
        self.containerId = containerId
        self.itemId = itemId
        self.quantity = quantity
        self.purchaseDate = purchaseDate
        self.expirationDate = expirationDate
        self.purchasePrice = purchasePrice
