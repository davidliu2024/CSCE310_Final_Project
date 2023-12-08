from flask import g, jsonify, Response
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
        app_year=internAppJSON.get('app_year')
    )

    return Response(intern_app.create(),200)


def fetch_intern_applications():
    '''
    Fetch all intern applications and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    applications = InternApplication(uin=g.userobj.uin).fetch()
    return jsonify(applications)



def fetch_all_intern_applications():
    '''
    Fetch all intern applications and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)
    applications = InternApplication().fetch_all()
    return jsonify(applications)



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
