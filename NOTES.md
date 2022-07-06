# Notes from the study

- cursor object is the client instance to interact with the database
    - in python, a cursor object is a class that you can instantiate and call various cursor methods on 
- 


Tutorials That I followed to help me:
- https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
- https://python-adv-web-apps.readthedocs.io/en/latest/flask_db1.html
- https://flask.palletsprojects.com/en/2.1.x/quickstart/
- https://stackoverflow.com/questions/5476065/how-to-truncate-the-time-on-a-datetime-object
- https://mnzel.medium.com/how-to-activate-python-venv-on-a-mac-a8fa1c3cb511


## How init sqlite3 db
```

$ python init_db.py
```

## How to check if the database is running
1. run `$ sqlite3`
2. `.open database.db`
3. `select * from tasks`
that should work

## How to run flask server 
```
$ export FLASK_APP=hello    
$ flask run 
```

## Run flask with debugger
```
$ export FLASK_ENV=development
$ flask run --debugger
```


## How to start using the VENV 
https://mnzel.medium.com/how-to-activate-python-venv-on-a-mac-a8fa1c3cb511




## Concepts:

use bootstrap multicolored progressbar to count how many days and tasks are done :
https://getbootstrap.com/docs/5.0/components/progress/#multiple-bars

-- to be done on the bottom of the screen under the to do list 
-- a specific color maps to current number of tasks done for that day 


- if we have 75 days 


- command shift p to open up sqlite reader