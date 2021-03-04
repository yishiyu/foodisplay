from foodisplay import db, app
from flask import current_app
# 密码加密
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Food(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    FoodName = db.Column(db.String(200), nullable=False)
    Url = db.Column(db.String(500), nullable=False)
    Ingredients = db.Column(db.String(1000), nullable=False)
    MainPicture = db.Column(db.String(1000), nullable=True)
    Steps = db.Column(db.String(3000), nullable=True)
    StepPicture = db.Column(db.String(5000), nullable=True)


class Page:
    def __init__(self, index):
        self.index = index


class FlavorRC:
    def __init__(self, flavors):
        # 存放顺序:酸甜苦辣咸
        self.flavors = []
        assert(isinstance(flavors, str))
        for f in flavors:
            self.flavors.append(
                min(max(int(f), 0), 5)
            )

    def __str__(self):
        return ''.join(
            map(str, self.flavors)
        )


class User(db.Model, UserMixin):
    UID = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(20), nullable=False)
    Passwd = db.Column(db.String(100), nullable=False)
    Region = db.Column(db.String(100), nullable=False)
    Flavor = db.Column(db.String(100), nullable=True)
    History = db.Column(db.String(200), nullable=True)

    def set_password(self, raw_password):
        self.Passwd = generate_password_hash(raw_password)

    def validate_password(self, raw_password):
        return check_password_hash(self.Passwd, raw_password)

    def get_id(self):
        return self.UID

    @property
    def FlavorRC(self):
        return FlavorRC(str(self.Flavor))

    @FlavorRC.setter
    def FlavorRC(self, flavors):
        current_app.logger.info('set user:{}\'s Flavor to{}'.format(self.UID, flavors))
        self.Flavor = str(flavors)
