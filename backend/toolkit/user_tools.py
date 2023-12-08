from flask import Blueprint, request, g, abort, Response, jsonify
import psycopg
import os
from db_interface.users import User

def authenticate(func):
    """
    Requires HTTP Basic Authentication before a request is processed.
    On failure, returns a 401 status code.
    On success, sets `g.userid` to the authenticated user's ID.
    """
    def inner(*args, **kwargs):
        if request.authorization is None or request.authorization.type != "basic":
            abort(401)
        username = request.authorization.parameters["username"]
        password = request.authorization.parameters["password"]

        current_user = User(username = username)
        if (len(current_user.fetch()) == 0):
            abort(404)
        current_user.autoFill()
        correct_password = password == current_user.password
        if not correct_password:
            abort(401)
        g.useruin = current_user.uin
        g.userobj = current_user
        
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner

def check_if_admin(func):
    def inner(*args, **kwargs):
        assert isinstance(g.userobj, User)
        admin_status = g.userobj.isAdmin()
        if not admin_status:
            abort(401)
        return func(*args, **kwargs)
    inner.__name__=func.__name__
    return inner

def create_user(userJSON):
    user = User(
        uin=userJSON['uin'],
        first_name=userJSON['first_name'],
        m_initial=userJSON.get('m_initial'),
        last_name=userJSON['last_name'],
        username=userJSON['username'],
        password=userJSON['password'],
        user_type= "USER" if userJSON.get('user_type') == None else userJSON.get('user_type'),
        email=userJSON.get('email'),
        discord_name=userJSON.get('discord_name')
    )

    response = user.create()
    return response

@check_if_admin
def fetch_all_users():
    '''
    Fetch all users and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)
    print(os.getcwd())

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM users
                '''
            )
            user_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            users_list = [
                {
                    'uin': record[0],
                    'first_name': record[1],
                    'm_initial': record[2],
                    'last_name': record[3],
                    'username': record[4],
                    'password': record[5],
                    'user_type': record[6],
                    'email': record[7],
                    'discord_name': record[8]
                }
                for record in user_records
            ]

            return jsonify(users_list)

        except Exception as e:
            g.conn.rollback()
            return f"Error fetching all users: {e}"

def update_user(userJSON):
    user = User(
        uin=userJSON['uin'],
        first_name=userJSON['first_name'],
        m_initial=userJSON.get('m_initial'),
        last_name=userJSON['last_name'],
        username=userJSON['username'],
        password=userJSON['password'],
        user_type=userJSON['user_type'],
        email=userJSON.get('email'),
        discord_name=userJSON.get('discord_name')
    )
    response = user.update()

    return {"response": response}