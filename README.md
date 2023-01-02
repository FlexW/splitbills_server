![Tests](https://github.com/FlexW/splitbills_server/workflows/Tests/badge.svg)
[![Coverage](https://codecov.io/gh/FlexW/splitbills_server/branch/main/graph/badge.svg?token=DODRY5LAPK)](https://codecov.io/gh/FlexW/splitbills_server)


![Dev Tests](https://github.com/FlexW/splitbills_server/workflows/Dev%20Tests/badge.svg)
[![Coverage](https://codecov.io/gh/FlexW/splitbills_server/branch/dev/graph/badge.svg?token=DODRY5LAPK)](https://codecov.io/gh/FlexW/splitbills_server)

# SplitBills Server

Server for [SplitBills](https://gitlab.com/flexw/splitbills).

## Build
Clone the repository
```
git clone https://github.com/FlexW/splitbills_server
```
Change into the cloned repository
```
cd splitbills_server
```

### Virtual environment with Python
Create a virtual environment for python
```
python -m venv env
```
Activate the environment. If you are using a other shell interpreter
than bash, search for an correct activate file. Example for fish:
`env/bin/activate.fish`.
```
source env/bin/activate
```
Now install the dependencies.
```
pip install -r requirements.txt
```

### Docker
It's also possible to run the server in a Docker container. In the
root of the project you can find the `Dockerfile`. A docker-compose
file that starts the server with a postgresql database can be found in
`docker/splitbills_server/docker-compose.yml`.

To start the docker containers execute:
```
cd docker/splitbills_server
docker-compose up
```
After you did changes to the source code make sure to rebuild the docker
container with
```
docker-compose up --build
```

## Run tests
Run all tests with
```
./scripts/run_tests
```
This will also generate the coverage.

To just run unit tests without coverage, you can execute `pytest` in the root of the project.

## Run
Tell flask which app it shoud run
```
export FLASK_APP=splitbills_server.py
```
If you want to do development then export this environment variable
too
```
export FLASK_ENV=development
```
Then run it
```
flask run
```
This will start a debug server on `http://127.0.0.1:5000`. If you want
the debug server to be visible for other operating systems too, run
instead
```
flask run --host=0.0.0.0
```
There is a script in the `script` directory called `run_debug_server`
which runs all the previous commands automatically.

## Run development server
Change into the directory `docker` with `cd docker`. Start the server
with `sudo docker-compose up --build`. If you are finished and want to
delete all data run `sudo docker-compose down --volumes`. If you want
to keep the volumes but want to remove the server simply run `sudo
docker-compose down`.

## Api Description

To get a rough overview, below are the routes listed that the server
can handle. To learn how to use these routes have a look at the unit
tests
[here](https://github.com/FlexW/splitbills_server/tree/dev/tests/unit/api/resources).
Every route has it's own test file. For example, the test for the
`/groups` route are in `test_groups.py`.

### Groups

| Resource                         | URI                                  | Method |
|:---------------------------------|:-------------------------------------|:-------|
| Create new group                 | /groups                              | POST   |
| Delete group                     | /groups/{group_id}                   | DELETE |
| Get list of all groups from user | /groups                              | GET    |
| Change group detail              | /groups/{group_id}                   | PUT    |
| Add group member                 | /groups/{group_id}/members           | POST   |
| Delete group member              | /groups/{group_id}/members/{user_id} | DELETE |
| Get all bills from group         | /groups/{group_id}/bills             | GET    |

### Bills

| Resource                        | URI              | Method |
|:--------------------------------|:-----------------|:-------|
| Create new bill                 | /bills           | POST   |
| Delete bill                     | /bills/{bill_id} | DELETE |
| Change bill detail              | /bills/{bill_id} | PUT    |
| Get list of all bills from user | /bills           | GET    |

### Users

| Resource        | URI              | Method |
|:----------------|:-----------------|:-------|
| Create new user | /users           | POST   |
| Get user detail | /users/{user_id} | GET    |

### Friends

| Resource        | URI      | Method |
|:----------------|:---------|:-------|
| Get all friends | /friends | GET    |


### Authentication
| Resource                 | URI                | Method |
|:-------------------------|:-------------------|:-------|
| Authenticate             | /tokens            | POST   |
| Revoke or unrevoke token | /tokens/{token_id} | PUT    |
| Refresh token            | /tokens/refresh    | POST   |

## Usage Example
These examples demonstrate how to control the server with `curl`. Keep in mind,
that on your computer depeding on your setup the server will not run on 
`localhost:5000` but on a different address.

For convinience set the server address as variable
```
export HOST=http://localhost:5000
```

### Create a user

First, check if the server is running
```sh
curl -X GET -H 'Content-Type: application/json' $HOST
```
Which will be answered, in case the server is running, by
```json
{
    "message": "Welcome to the SplitBills Api. More Information can be found on https://github.com/FlexW/splitbills_server"
}
```

Now register a new user with
```sh
curl \
    -X POST \
    -H 'Content-Type: application/json' \
    -d '{"first_name": "Tim", "last_name": "Muster", "email": "tim@mail.de", "password": "securepassword"}' \
    $HOST/users
```
Which should be answered by
```json
{
    "message": "Created new user",
    "user": {
        "id": 2,
        "first_name": "Tim",
        "last_name": "Muster",
        "email": "tim@mail.de"
    }
}
```
Create another user
```sh
curl \
    -X POST \
    -H 'Content-Type: application/json' \
    -d '{"first_name": "Felix", "last_name": "Muster", "email": "felix@mail.de", "password": "securepassword"}' \
    $HOST/users
```

### Get a token
A token is needed for authentication of the user. The access token needs to be
send with every API request.

Obtain the token for a user with
```sh
curl \
    -X POST \
    -H 'Content-Type: application/json' \
    -d '{"email": "tim@mail.de", "password": "securepassword"}' \
    $HOST/tokens
```
From the response
```json
{
    "message": "Created access and refresh token",
    "access_token": {
        "id": 1,
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3MjY2NDI5MCwianRpIjoiNzY3NjUwOWQtOGQ5Mi00YjdiLTliMzAtMGJiNDY5ZWU1Mzg2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRpbUBtYWlsLmRlIiwibmJmIjoxNjcyNjY0MjkwLCJleHAiOjE2NzI2NjUxOTB9.E4mJP5ka8BEKZzPCDGvSrasEU0u0AqyWVcPSyRPp7Sc"
    },
    "refresh_token": {
        "id": 2,
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3MjY2NDI5MCwianRpIjoiNjdlYmU2NTgtOTk1ZS00NDZiLWEzOTYtMjc1NWFhMjAxZWM1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJ0aW1AbWFpbC5kZSIsIm5iZiI6MTY3MjY2NDI5MCwiZXhwIjoxNjc1MjU2MjkwfQ.IlG8aBp__7k3F2pNE8TVlb_XgmiTHcTKgD4dXJD3ago"
    }
}
```
the access token can be obtained. Save the access token in a variable with:
```sh
export TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3MjY2NDI5MCwianRpIjoiNzY3NjUwOWQtOGQ5Mi00YjdiLTliMzAtMGJiNDY5ZWU1Mzg2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRpbUBtYWlsLmRlIiwibmJmIjoxNjcyNjY0MjkwLCJleHAiOjE2NzI2NjUxOTB9.E4mJP5ka8BEKZzPCDGvSrasEU0u0AqyWVcPSyRPp7Sc
```

### Create a new bill 

A new bill can now be created with
```sh
curl \
    -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' \
    -d '{"description": "Important bill", "date": "2023-01-01T13:06:44.492993", "date_created": "2023-01-01T13:06:44.492993", "members": [{"user_id": 1, "amount": 200}, {"user_id": 2, "amount": -200}]}' \
    $HOST/bills
```
Which should be answered in the case of success by
```json
{
    "message": "Created new bill",
    "bill": {
        "id": 1,
        "description": "Important bill",
        "date": "2023-01-01T13:06:44.492993",
        "date_created": "2023-01-01T13:06:44.492993"
    }
}
```

Bills can also be created in groups. For this a group needs to be created first.
For more examples on how to use the API look at the test cases. 
