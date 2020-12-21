import datetime

from app.util.converter import datetime_to_string
from app.api.resources.common import string_to_datetime


def test_parse_datetime():
    now = datetime.datetime.utcnow()

    date = string_to_datetime(datetime_to_string(now))

    assert date == now
