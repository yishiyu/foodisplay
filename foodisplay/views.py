from foodisplay import app, db
from flask import render_template
from foodisplay.models import Food

@app.route('/')
def index():
    food_list = Food.query.limit(30)
    for food in food_list:
        food.Ingredients = food.Ingredients.replace("|||||",'、')
        food.Ingredients = food.Ingredients.replace('|',' ')
    return render_template("index.html",food_list=food_list)
