from flask import abort


def load_request_data_as_json(request):
    json_data = request.get_json()

    if not json_data:
        abort({"message": "No input data provided."})

    return json_data
