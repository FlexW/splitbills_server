![Tests](https://github.com/FlexW/splitbills_server/workflows/Tests/badge.svg)
[![Coverage](https://codecov.io/gh/FlexW/splitbills_server/branch/main/graph/badge.svg?token=DODRY5LAPK)](https://codecov.io/gh/FlexW/splitbills_server)


![Dev Tests](https://github.com/FlexW/splitbills_server/workflows/Dev%20Tests/badge.svg)
[![Coverage](https://codecov.io/gh/FlexW/splitbills_server/branch/dev/graph/badge.svg?token=DODRY5LAPK)](https://codecov.io/gh/FlexW/splitbills_server)

![Deploy](https://github.com/FlexW/splitbills_server/workflows/Deploy/badge.svg)

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

### Build with Nix
If you have the [Nix](https://nixos.org/) package manager installed,
you can simply run `nix-shell` and everything will be setup
automatically. If you don't have Nix, read on.

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
