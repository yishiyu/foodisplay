from foodisplay import app, db
from flask import render_template
from foodisplay.models import Food

@app.route('/')
def index():
    food_lists = Food.query.all()
    return render_template("index.html",food_lists = food_lists)
