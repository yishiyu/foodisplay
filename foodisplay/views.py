from foodisplay import app, db, photos, UploadForm
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request, url_for, redirect, flash, current_app
from foodisplay.models import Food, Page, User
from .recongnize import FoodNameSearch
from foodisplay import LOCALPHOTODIR
from collections import Counter

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


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        if 'name' in request.form and 'region' in request.form:
            name = request.form['name']
            region = request.form['region']

            if not name or len(name) > 20 or not region or len(region) > 20:
                flash('Invalid input.')
                return redirect(url_for('settings'))

            current_user.Name = name
            current_user.Region = region
            # current_user 会返回当前登录用户的数据库记录对象
            # 等同于下面的用法
            # user = User.query.first()
            # user.name = name
            db.session.commit()
            flash('Settings updated.')
            return redirect(url_for('index'))
        elif 'password' in request.form:
            password = request.form['password']
            if not password or len(password) > 20:
                flash('Invalid input.')
                return redirect(url_for('settings'))
            current_user.set_password(password)
            db.session.commit()
            flash('Settings updated.')
            return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


@app.route('/recongnition', methods=['GET', 'POST'])
@login_required
def recongnition():
    form = UploadForm()
    filename, foodname = None, None
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
    else:
        file_url = None
    current_app.logger.info("file:{}".format(file_url))

    foodnames = []
    foodlist = []
    if filename is not None:
        # 调用图片识别函数，返回食物名称
        foodnames = FoodNameSearch(LOCALPHOTODIR + filename)
        current_app.logger.info("foodnames:{}".format(foodnames))
        # 从所有名字中提取出频率最高的字
        counter = Counter()
        for name in foodnames:
            counter.update(name)
        foodnames = str(foodnames)[1:-2]
        current_app.logger.info(
            "counter.most_common():{}".format(counter.most_common()))

        foodlist = Food.query.filter(
            Food.FoodName.like(
                counter.most_common()[0][0]
            )
        ).limit(5).all()
        for food in foodlist:
            food.Ingredients = food.Ingredients.replace("|||||", '、')
            food.Ingredients = food.Ingredients.replace('|', ' ')

    return render_template('recongnition.html',
                           form=form,
                           file_url=file_url,
                           foodlist=foodlist,
                           foodnames=foodnames)
