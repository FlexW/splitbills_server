import json

from app.models.user import User, insert_user
from app.models.group import get_group_by_id


def test_add_group(app, test_client, api_headers_auth):
    group_data = {
        "name": "Muster"
    }

    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)

    user = insert_user(user)

    response = test_client.post("/groups",
                                headers=api_headers_auth(user.email, password),
                                data=json.dumps(group_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert json_respone["message"] == "Created new group."
    assert json_respone["group"]["id"] == 1
    assert json_respone["group"]["name"] == group_data["name"]

    group = get_group_by_id(json_respone["group"]["id"])

    assert group is not None
    assert len(group.members) == 1
