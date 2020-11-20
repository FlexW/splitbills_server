import json
import datetime

from app.models.user import User, insert_user
from app.models.bill import Bill, insert_bill
from app.models.bill_member import BillMember
from app.util.json_data_encoder import json_data_encoder
from app.util.converter import datetime_to_string


def test_add_bill(app, test_client, api_headers_auth):
    now = datetime.datetime.utcnow()

    bill_data = {
        "description": "Important bill",
        "date": now,
        "date_created": now
    }

    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)

    response = test_client.post("/bills",
                                headers=api_headers_auth(user.email, password),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Created new bill."
    assert json_response["bill"]["id"] == 1
    assert json_response["bill"]["description"] == bill_data["description"]
    assert json_response["bill"]["date"] == datetime_to_string(bill_data["date"])
    assert (json_response["bill"]["date_created"]
            == datetime_to_string(bill_data["date_created"]))


def test_get_bills_from_user(app, test_client, api_headers_auth):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)

    bill_member1 = BillMember(user_id=user.id, amount="1.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now)
    insert_bill(bill1)
    bill_member1.bill = bill1
    bill1.members.append(bill_member1)

    bill_member2 = BillMember(user_id=user.id, amount="1.00")

    bill2 = Bill(description="Bill2",
                 date=now,
                 date_created=now)
    insert_bill(bill2)
    bill_member2.bill = bill2

    response = test_client.get("/bills",
                               headers=api_headers_auth(user.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 2
    assert json_response["bills"][0]["description"] == bill1.description
    assert json_response["bills"][1]["description"] == bill2.description


def test_get_just_bills_from_user(app, test_client, api_headers_auth):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_member1 = BillMember(user_id=user1.id, amount="1.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now)
    insert_bill(bill1)
    bill_member1.bill = bill1
    bill1.members.append(bill_member1)

    bill_member2 = BillMember(user_id=user2.id, amount="1.00")

    bill2 = Bill(description="Bill2",
                 date=now,
                 date_created=now)
    insert_bill(bill2)
    bill_member2.bill = bill2

    response = test_client.get("/bills",
                               headers=api_headers_auth(user1.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["description"] == bill1.description
