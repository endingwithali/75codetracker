from flask import Flask
from flask import render_template
from flask import request
from flask import Response
import sqlite3
import datetime
# from markupsafe import escape


current_date = datetime.datetime.now().date()

app = Flask(__name__)

task_list = [{
        "task": "task1",
        "status": False,
        "id": "t1"
    },    {
        "task": "task2",
        "status": False,
        "id": "t2"
    },    {
        "task": "task3",
        "status": False,
        "id": "t3"
    },    {
        "task": "task4",
        "status": False,
        "id": "t4"
    },    {
        "task": "task5",
        "status": False,
        "id": "t5"
    },    
]

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


user_id = 0

@app.route('/')
def hello():
    """
    1 - pull from db - (check if date exists ) - if not, return unfilled
    2 - quick run through exist, to modify task list
    """
    conn = get_db_connection()
    return_statement = conn.execute('SELECT * FROM tasks WHERE user_id="%s" AND day="%s"' % (user_id, current_date)).fetchone()
    if return_statement == None:
        conn.execute("INSERT INTO tasks (user_id, day, task1, task2, task3, task4, task5) VALUES (%s, %s, False, False, False, False, False);" % (user_id, ))
        return render_template('hello.html', tasks=task_list)
    else:
        ## if user doesnt exist, insert row, and then return task lit
        pass

    return render_template('hello.html', tasks=task_list)


"""
expects:
body to contain - 
json object body
{
    "task_id": "__text1__",
    "status": False,
    "user_id": "beans"
}
"""
@app.put('/update')
def update():
    """
    - take current task (value) + day, and change status in DB from false to true 
    """
    print(request.get_json())
    body = request.get_json()
    ##sql query to db to update status 
    conn = get_db_connection()

    # update taskId where user_id = userid and date=date 
    return_statement = conn.execute('SELECT * FROM tasks WHERE user_id="%s" AND day="%s"' % (user_id, current_date)).fetchone()
    if return_statement == None:
        return render_template('hello.html', tasks=task_list)
    else:
        pass

    return Response(status=200)
