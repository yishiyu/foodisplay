import click

from foodisplay import app, db
from foodisplay.models import Food


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