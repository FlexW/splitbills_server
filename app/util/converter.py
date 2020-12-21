import dateutil.parser


def datetime_to_string(datetime):
    return datetime.isoformat()


def string_to_datetime(string):
    return dateutil.parser.parse(string)
