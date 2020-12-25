#!/usr/bin/env python

import os
import sys
import json
import requests


CONFIG_FILE_NAME = ".config.json"


def print_error(message):
    print("ERROR: {}".format(message))


def read_json_file(filename):
    with open(filename) as f:
        return json.load(f)


def read_config_file():
    return read_json_file(CONFIG_FILE_NAME)


def print_response(response):
    print("Status code:\n{}".format(response.status_code))

    print("\nHeaders:", end="")
    for header_key in response.headers:
        print("\n{}: {}".format(header_key, response.headers[header_key]),
              end="")
    print("\n", end="")

    print("\nData:\n{}".format(response.text))


class SplitBillsClient:
    def setup(self):
        self.config = read_config_file()

    def _get_headers(self, authorized):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if authorized is True:
            token = self.config["access_token"]["token"]
            headers["Authorization"] = "Bearer {}".format(token)

        return headers

    def _send_request(self, method, route, data={}, authorized=True):
        host = self.config["host"]
        port = self.config["port"]
        url = "{}:{}{}".format(host, port, route)

        headers = self._get_headers(authorized)

        if method == "GET":
            return requests.get(url, headers=headers)
        elif method == "POST":
            return requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            return requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            return requests.delete(url, headers=headers, json=data)
        else:
            print_error("Method {} is not supported".format(method))
            exit(1)

    def register_user(self, first_name, last_name, email, password):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }

        response = self._send_request("POST", "/users", data, authorized=False)
        print_response(response)

    def obtain_tokens(self, email, password):
        data = {
            "email": email,
            "password": password
        }

        response = self._send_request("POST", "/tokens", data, authorized=False)
        print_response(response)

    def get_user(self, id):
        response = self._send_request("GET", "/users/{}".format(id))
        print_response(response)


if __name__ == "__main__":
    client = SplitBillsClient()
    client.setup()

    if len(sys.argv) == 1:
        print_error("Provide a action")
        exit(1)

    action = sys.argv[1]

    try:
        # Show help or execute action
        if len(sys.argv) >= 3 and sys.argv[2] == "help":
            help(getattr(client, action))
        else:
            args = tuple(sys.argv[2:])
            getattr(client, action)(*args)
    except AttributeError:
        print_error("Invalid action {}".format(action))
    except TypeError as error:
        print_error(error)
