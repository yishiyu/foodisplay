from foodisplay import app
from flask import render_template
from foodisplay.models import Food

@app.route('/')
def index():
    food_lists = [
        Food("foodname1","ingredients1,ingredients2,ingredients3"),
        Food("foodname2","ingredients1,ingredients2,ingredients3")
    ]
    return render_template("index.html",food_lists = food_lists)
