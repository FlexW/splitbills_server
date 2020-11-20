import datetime
import pytest

from app.util.json_data_encoder import json_data_encoder


def test_json_data_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        json_data_encoder(None)


def test_json_data_encoder_convert_datetime():
    now = datetime.datetime.utcnow()

    result = json_data_encoder(now)

    assert result == now.isoformat()
