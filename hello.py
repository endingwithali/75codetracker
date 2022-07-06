from os import stat
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
        "id": "task1"
    },    {
        "task": "task2",
        "status": False,
        "id": "task2"
    },    {
        "task": "task3",
        "status": False,
        "id": "task3"
    },    {
        "task": "task4",
        "status": False,
        "id": "task4"
    },    {
        "task": "task5",
        "status": False,
        "id": "task5"
    },    
]

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


user_id = 1

@app.route('/')
def hello():
    """
    1 - pull from db - (check if date exists ) - if not, return unfilled
    2 - quick run through exist, to modify task list
    """
    try:
        conn = get_db_connection()
        return_statement = conn.execute('SELECT * FROM tasks WHERE user_id="%s" AND day="%s"' % (user_id, current_date)).fetchone()
        if return_statement == None:
            attempt = False
            while not attempt:
                try: 
                    conn.execute("INSERT INTO tasks (user_id, day, task1, task2, task3, task4, task5) VALUES (%s, '%s', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE');" % (user_id, current_date))
                    conn.commit()
                    attempt = True
                except:
                    attempt = False
            return render_template('hello.html', tasks=task_list)
        else:
            for i in range(2,len(return_statement)):
                task_list[i-2]["status"]=return_statement[i]
            ## if user doesnt exist, insert row, and then return task lit
            print(task_list)
        return render_template('hello.html', tasks=task_list)
    except Exception as e:
        print(e)
        return Response(status=400)

"""
expects:
body to contain - 
json object body
{
    "task_id": "task#",
    "status": boolean,
    "user_id": "beans"
}
"""
@app.put('/update')
def update():
    try:
        body = request.json
        conn = get_db_connection()
        return_statement = conn.execute("UPDATE tasks SET %s='%s' WHERE user_id='%s' AND day='%s'" % (body['task_id'], str(body['status']).upper(), user_id, current_date))
        conn.commit()
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=400)


@app.get('/teapot')
def teapot():
    return Response(status=418)