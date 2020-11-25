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
pip install -r requirements_lock.txt
```

## Run tests
Run all tests with
```
./scripts/run_tests
```

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

## Api Description

| Resource                         | URI                                  | Method |
|:---------------------------------|:-------------------------------------|:-------|
| Get list of all groups from user | /groups                              | GET    |
| Create new group                 | /groups                              | POST   |
| Change group detail              | /groups/{group_id}                   | PUT    |
| Add group member                 | /groups/{group_id}/members           | POST   |
| Delete group member              | /groups/{group_id}/members/{user_id} | DELETE |
| Create new bill                  | /bills                               | POST   |
| Get list of all bills from user  | /bills                               | GET    |
| Create new user                  | /users                               | POST   |
| Get user detail                  | /users/{id}                          | GET    |
