import json


def test_show_welcome_banner(test_client, api_headers):
    response = test_client.get("/", headers=api_headers)
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Welcome to the SplitBills Api. More Information can be found on https://github.com/FlexW/splitbills_server"
