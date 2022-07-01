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


user_id = 0

@app.route('/')
def hello():
    """
    1 - pull from db - (check if date exists ) - if not, return unfilled
    2 - quick run through exist, to modify task list
    """
    conn = get_db_connection()
    print("INSERT INTO tasks (user_id, day, task1, task2, task3, task4, task5) VALUES (%s, %s, False, False, False, False, False);" % (user_id, current_date))
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

    # print("UPDATE tasks SET %s='%s' WHERE user_id='%s' AND day='%s'" % (body['task_id'], str(body['status']).upper(), user_id, current_date))
    return_statement = conn.execute("UPDATE tasks SET %s='%s' WHERE user_id='%s' AND day='%s'" % (body['task_id'], str(body['status']).upper(), user_id, current_date))
    conn.commit()
    print(return_statement.fetchall())
    if return_statement == None:
        return Response(status=400)
    else:
        pass
    return Response(status=200)


@app.get('/pupdate')
def pupdate():
    return Response(status=418)