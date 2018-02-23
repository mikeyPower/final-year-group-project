from app import app, views, models, db, menu_views
from app.models import Total
from app.views import *
from app.menu_views import *
import pytest

def test_total_raised():
    x = get_total_raised_tester()
    add_to_total_raised(4000)
    y = get_total_raised_tester()
    add_to_total_raised(-4000)
    assert y-x == 4000
    x = get_total_raised_tester()
    add_to_total_raised(6000)
    y = get_total_raised_tester()
    add_to_total_raised(-4000)
    assert y-x != 4000


def test_menu_added():
    title_data = "Brunch Test5"
    body_data = "Eggs and Toast Test5"
    add_menu(title_data,body_data)
    menu = Menu.query.filter_by(title=title_data).first()
    db.session.delete(menu)
    db.session.commit()
    assert body_data == menu.body
