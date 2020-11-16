![Tests](https://github.com/FlexW/splitbills_server/workflows/Tests/badge.svg)
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
