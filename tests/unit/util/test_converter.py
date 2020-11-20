import datetime

from app.util.converter import datetime_to_string, string_to_datetime

def test_datetime_to_string():
    now = datetime.datetime.utcnow()

    result = datetime_to_string(now)

    assert result == now.isoformat()

def test_string_to_datetime():
    now = datetime.datetime.utcnow()
    now_str = now.isoformat()

    result = string_to_datetime(now_str)

    assert result == now
