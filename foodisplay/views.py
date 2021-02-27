from foodisplay import app, db
from flask import render_template
from foodisplay.models import Food, Page

PAGE_SIZE = 20


@app.route('/')
@app.route('/index/<page_index>')
def index(page_index=1):
    page_index = int(page_index)
    current_page = Page(page_index)
    previous_pages = [
        Page(i)
        for i in range(max(1,page_index-3),page_index)
    ]
    next_pages = [
        Page(i)
        for i in range(page_index+1,page_index+4)
    ]

    food_list = Food.query.limit(PAGE_SIZE).offset((page_index-1)*PAGE_SIZE)
    for food in food_list:
        food.Ingredients = food.Ingredients.replace("|||||", '、')
        food.Ingredients = food.Ingredients.replace('|', ' ')
    return render_template("index.html",
                           food_list=food_list,
                           current_page=current_page,
                           previous_pages=previous_pages,
                           next_pages=next_pages)
