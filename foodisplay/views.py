from foodisplay import app, db
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request, url_for, redirect, flash
from foodisplay.models import Food, Page, User

PAGE_SIZE = 20


@app.route('/')
@app.route('/index/<page_index>')
def index(page_index=1):
    page_index = int(page_index)
    current_page = Page(page_index)
    previous_pages = [
        Page(i)
        for i in range(max(1, page_index-3), page_index)
    ]
    next_pages = [
        Page(i)
        for i in range(page_index+1, page_index+4)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 阻止重复登陆
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']

        if not account or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.get(int(account))
        # 验证用户名和密码是否一致
        if user is not None and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid account or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页
