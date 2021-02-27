from foodisplay import db


class Food(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    FoodName = db.Column(db.String(200))
    Url = db.Column(db.String(500))
    Ingredients = db.Column(db.String(1000))
    MainPicture = db.Column(db.String(1000), nullable=True)
    Steps = db.Column(db.String(3000), nullable=True)
    StepPicture = db.Column(db.String(5000), nullable=True)

class Page:
    def __init__(self,index):
        self.index = index