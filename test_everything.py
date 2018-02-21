from app import app, views, models, db
from app.models import Total
from app.views import *
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
