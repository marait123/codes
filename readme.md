# setup

```bash
# create virtual environment
python -m venv env
# activate virtual environment
source env/bin/activate # for linux
env\Scripts\activate # for windows

# install dependencies
pip install -r requirements.txt

# run flask with debug enabled
export FLASK_ENV=development
flask run
```

````

# Migration

```bash
flask db init
flask db migrate
flask db upgrade
````

# connect to database command

```bash
psql -U USERNAME -d DATABASE_NAME
```
