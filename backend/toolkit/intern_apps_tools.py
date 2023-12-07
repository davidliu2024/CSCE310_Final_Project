from sys import intern
from flask import g, jsonify
import psycopg
from db_interface.intern_apps import InternApplication
from db_interface.users import User

def create_intern_application(internAppJSON):
    '''
    Create a new intern application and return the event with internAppJSON
    '''
    assert isinstance(g.userobj,User)
    intern_app = InternApplication(
        uin=g.userobj.uin,
        intern_id=internAppJSON.get('intern_id'),
        app_status=internAppJSON.get('app_status'),
        app_year=internAppJSON.get('year')
    )

    intern_app.create()
    return intern_app.get_json()


def fetch_intern_applications():
    '''
    Fetch all intern applications and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM intern_app
                WHERE uin = %s
                ''',
                (g.userobj.uin,)
            )
            intern_app_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            intern_app_list = [
                {
                    'ia_num': record[0],
                    'uin': record[1],
                    'intern_id': record[2],
                    'app_status': record[3],
                    'app_year': str(record[4]),
                }
                for record in intern_app_records
            ]

            return jsonify(intern_app_list)

        except Exception as e:
            g.conn.rollback()
            return {"response" : f"Error fetching all intern applications: {e}"}


def fetch_all_intern_applications():
    '''
    Fetch all intern applications and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM intern_app
                '''
            )
            intern_app_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            intern_app_list = [
                {
                    'ia_num': record[0],
                    'uin': record[1],
                    'intern_id': record[2],
                    'app_status': record[3],
                    'app_year': str(record[4]),
                }
                for record in intern_app_records
            ]

            return jsonify(intern_app_list)

        except Exception as e:
            g.conn.rollback()
            return {"response" : f"Error fetching all intern applications: {e}"}



def patch_intern_application(internAppJSON):
    '''
    Create a new event and return the event with eventJSON
    '''
    intern_app = InternApplication(
        ia_num=internAppJSON.get('ia_num'),
        uin=internAppJSON.get('uin'),
        intern_id=internAppJSON.get('intern_id'),
        app_status=internAppJSON.get('app_status'),
        app_year=internAppJSON.get('app_year'),
    )
    is_owner = intern_app.uin == g.userobj.uin or g.userobj.isAdmin()
    if is_owner:
        response = intern_app.update()
    else:
        response = "User is not authorized"

    return response


def delete_intern_application(ia_num):
    assert isinstance(g.userobj, User)
    intern_app = InternApplication(
        ia_num = ia_num
    )
    intern_app.auto_fill()
    is_owner = intern_app.uin == g.userobj.uin or g.userobj.isAdmin()
    if is_owner:
        response = intern_app.delete()
    else:
        response = "User not allowed to delete"
    return { "response": response }
