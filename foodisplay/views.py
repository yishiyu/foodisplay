from foodisplay import app, db
from flask import render_template
from foodisplay.models import Food

@app.route('/')
def index():
    food_list = Food.query.limit(10)
    return render_template("index.html",food_list=food_list)
