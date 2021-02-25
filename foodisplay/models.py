from foodisplay import db


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    ingredients = db.Column(db.String(1000))

    def __init__(self,name,ingredients):
        self.name = name
        self.ingredients = ingredients
