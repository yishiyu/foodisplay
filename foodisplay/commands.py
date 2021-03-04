import click

from foodisplay import app, db
from foodisplay.models import Food, User


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    food_lists = [
        Food("foodname1","ingredients1,ingredients2,ingredients3"),
        Food("foodname2","ingredients1,ingredients2,ingredients3"),
        Food("foodname3","ingredients1,ingredients2,ingredients3"),
        Food("foodname4","ingredients1,ingredients2,ingredients3"),
        Food("foodname5","ingredients1,ingredients2,ingredients3"),
        Food("foodname6","ingredients1,ingredients2,ingredients3")
    ]

    for food in food_lists:
        db.session.add(food)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.Name = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(Name=username,Region='somewhere')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')