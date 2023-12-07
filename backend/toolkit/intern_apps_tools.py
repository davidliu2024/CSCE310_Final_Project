from flask import g, jsonify
import psycopg
from datetime import datetime
from db_interface.intern_apps import InternApplication

def create_intern_application( internAppJSON) -> InternApplication:
    '''
    Create a new intern application and return the event with internAppJSON
    '''
    intern_app = InternApplication(
        ia_num=internAppJSON.get('ia_num'),
        uin=internAppJSON.get('uin'),
        intern_id=internAppJSON.get('intern_id'),
        app_status=internAppJSON.get('app_status'),
        app_year=internAppJSON.get('app_year'),
    )

    intern_app.create()
    return intern_app


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

    return { "response": intern_app.update() }


def delete_intern_application(uin, internAppJSON):
    intern_app = InternApplication(
        uin=uin,
        ia_num = internAppJSON.get('ia_num')
    )

    response = intern_app.delete()
    return { "response": response }


