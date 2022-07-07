from os import stat
from flask import Flask, request, Response, render_template, redirect, session, url_for, render_template
import sqlite3
import datetime
import os 

from fusionauth.fusionauth_client import FusionAuthClient
from requests_oauthlib import OAuth2Session


# from markupsafe import escape

current_date = datetime.datetime.now().date()
app = Flask(__name__)
app.config.from_object('settings.Config')
app.secret_key = os.urandom(24)



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



@app.route('/')
def hello():
    """
    1 - pull from db - (check if date exists ) - if not, return unfilled
    2 - quick run through exist, to modify task list
    """
    """
    login mock up:
        1) check to see if user is logged in 
        2) if logged in - pull data from db, or create new row using insert
        3) if not logged in - create new user using FusionAuth! 
    """
    print('in study')
    user=None
    if session.get('user') != None:
        user = session['user']
        user_id = user['sub']
        try:
            print("WE ARE TRYING")
            conn = get_db_connection()
            return_statement = conn.execute('SELECT * FROM tasks WHERE user_id="%s" AND day="%s"' % (user_id, current_date)).fetchone()
            if return_statement == None:
                print(return_statement)
                attempt = False
                while not attempt:
                    try: 
                        print("we're trying")
                        cur = conn.cursor()
                        cur.execute("INSERT INTO tasks (user_id, day, task1, task2, task3, task4, task5) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (user_id, current_date, 'FALSE',  'FALSE',  'FALSE',  'FALSE',  'FALSE')
                                    )
                        conn.commit()
                        conn.close()
                        attempt = True
                    except:
                        attempt = False
                return render_template('taskboard.html', tasks=task_list)
            else:
                print("In else")
                for i in range(2,len(return_statement)):
                    task_list[i-2]["status"]=return_statement[i]
            return render_template('taskboard.html', tasks=task_list)
        except Exception as e:
            print(e)
            return Response(status=400)
    else:
        print("beeans")
        return render_template('login.html')
    print("hello world")
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

    """
    first get info about user that is logged in
    then update 
    """
    user=None
    if session.get('user') != None:
        user = session['user']
        user_id = user['sub']
        try:
            body = request.json
            conn = get_db_connection()
            return_statement = conn.execute("UPDATE tasks SET %s='%s' WHERE user_id='%s' AND day='%s'" % (body['task_id'], str(body['status']).upper(), user_id, current_date))
            conn.commit()
            return Response(status=200)
        except Exception as e:
            print(e)
            return Response(status=400)
    else:
        return Response(status=500)


@app.get('/teapot')
def teapot():
    return Response(status=418)



@app.route("/logout", methods=["GET"])
def logout():
  session.clear()
  return redirect(app.config['FA_URL']+'/oauth2/logout?client_id='+app.config['CLIENT_ID'])


@app.route("/login", methods=["GET"])
def login():
    fusionauth = OAuth2Session(app.config['CLIENT_ID'], redirect_uri=app.config['REDIRECT_URI'])
    print("in login")
    print(str(fusionauth))
    authorization_url, state = fusionauth.authorization_url(app.config['AUTHORIZATION_BASE_URL'])
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    # return Response(status=200)
    return redirect(authorization_url)



@app.route("/register", methods=["GET"])
def register():
    fusionauth = OAuth2Session(app.config['CLIENT_ID'], redirect_uri=app.config['REDIRECT_URI'])
    authorization_url, state = fusionauth.authorization_url(app.config['AUTHORIZATION_BASE_URL'])

    # registration lives under non standard url, but otherwise takes exactly the same parameters
    registration_url = authorization_url.replace("authorize","register", 1)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    return redirect(registration_url)

@app.route("/callback", methods=["GET"])
def callback():
    print("in callback")
    expected_state = session['oauth_state']
    state = request.args.get('state','')
    if state != expected_state:
        print("Error, state doesn't match, redirecting without getting token.")
        return redirect('/')
        
    fusionauth = OAuth2Session(app.config['CLIENT_ID'], redirect_uri=app.config['REDIRECT_URI'])
    print(str(fusionauth))
    print(fusionauth.redirect_uri)
    token = fusionauth.fetch_token(app.config['TOKEN_URL'], client_secret=app.config['CLIENT_SECRET'], authorization_response=request.url)

    session['oauth_token'] = token
    session['user'] = fusionauth.get(app.config['USERINFO_URL']).json()

    return redirect('/')