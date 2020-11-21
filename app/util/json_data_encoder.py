import datetime
import decimal

from app.util.converter import datetime_to_string


def json_data_encoder(data):

    if isinstance(data, datetime.datetime):
        return datetime_to_string(data)

    raise NotImplementedError("Implement an encoder for this type")
