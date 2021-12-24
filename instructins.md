# Hello to the session one instructions

## Tools needed
    1. git bash
    2. python 3
## Environment Setup
```
$ sudo apt-get install python3-venv # ( for linux only to install venv as it isn't there by default)
$ python3 -m venv pyenv
$ source ./pyenv/scripts/activate # (to activat e the virtual environment from git bash)
$ ./pyenv/scripts/activate #(to activat e the virtual environment from powershell or cmd )
```
## Flask Installation
```
$ pip install flask
$ pip install psycopg2-binary
$ pip install flask-sqlalchemy
$ pip install Flask-Migrate


```
## Setup Database
### on windows
    * start pasql app
    * enter your credentials username, password, database
    * enter the following `\l`
    * now you should see the list of databases
    * enter the following `create database school;`
    * enter the following `\l` again
    * now you should see database school created
##  Migrating database 
0. pip install Flask-Migrate --> (requirement)
1. flask db init --> makes a migration folder
2. flask db migrate -m "inital migration" --> produces the migration file that will be later applied to the database
3. flask db upgrade --> applies the migration file from the previous step 


## running flask 
### on windows
```
set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run
```
### on Linux
```
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
```

### Connect to database
```
SQLALCHEMY_DATABASE_URI = 'postgresql://<user>:<password>@localhost:5432/<database_name>'
```

### tips
* If you want to view the app from mobile
    `flask run --host 0.0.0.0` makes the network interface card listen to connections from other computers
* 