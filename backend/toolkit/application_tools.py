from flask import g, jsonify, abort, Response
from db_interface.applications import Application
import psycopg
from toolkit.user_tools import User

def create_application(uin, application_json):
    '''
    Create a new application and return the application with application_json
    '''
    assert isinstance(g.conn, psycopg.Connection)

    application_instance = Application(
        program_num=application_json['program_num'],
        uin=uin,
        uncom_cert=application_json.get('uncom_cert'),
        com_cert=application_json.get('com_cert'),
        purpose_statement=application_json.get('purpose_statement')
    )

    response = application_instance.create()
    if response == "success":
        return Response(response, 202)
    else:
        abort(400, response)

def fetch_all_applications():
    '''
    Fetch all applications for a user and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM applications
                '''
            )
            application_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            applications_list = [
                {
                    'app_num': record[0],
                    'program_num': record[1],
                    'uin': record[2],
                    'uncom_cert': record[3],
                    'com_cert': record[4],
                    'purpose_statement': record[5],
                    'app_date': record[6]
                }
                for record in application_records
            ]

            return jsonify(applications_list)

        except Exception as e:
            g.conn.rollback()
            return {"response": f"Error fetching user applications: {e}"} 

def fetch_user_applications(uin):
    '''
    Fetch all applications for a user and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM applications
                WHERE uin = %s
                ''',
                (uin,)
            )
            application_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            applications_list = [
                {
                    'app_num': record[0],
                    'program_num': record[1],
                    'uin': record[2],
                    'uncom_cert': record[3],
                    'com_cert': record[4],
                    'purpose_statement': record[5],
                    'app_date': record[6]
                }
                for record in application_records
            ]

            return applications_list

        except Exception as e:
            g.conn.rollback()
            return {"response": f"Error fetching user applications: {e}"}

def update_application(application_json):
    '''
    Update an existing application and return the application with application_json
    '''
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    application_instance = Application(
        app_num=application_json['app_num'],
        program_num=application_json['program_num'],
        uin=g.userobj.uin,
        uncom_cert=application_json.get('uncom_cert'),
        com_cert=application_json.get('com_cert'),
        purpose_statement=application_json.get('purpose_statement')
    )

    return application_instance.update()

def delete_application(uin, app_num):
    '''
    Delete an existing application
    '''
    assert isinstance(g.conn, psycopg.Connection)

    application_instance = Application(app_num=app_num)
    application_instance.auto_fill()
    is_owner = application_instance.uin == uin
    if is_owner:
        response = application_instance.delete()
    else:
        abort(401)
    return response
