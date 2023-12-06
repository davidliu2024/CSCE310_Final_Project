from flask import g, jsonify
import psycopg
from db_interface.classes import Application

def submit_application(applicationJSON) -> jsonify:
    assert isinstance(g.conn, psycopg.Connection)

    # Validate the JSON data
    valid_request = applicationJSON is not None
    valid_request &= all(field in applicationJSON for field in ['program_num', 'uin', 'purpose_statement'])
    if not valid_request:
        return jsonify({"response": "Invalid application data. Required fields: program_num, uin, purpose_statement"}), 400

    application = Application(
        program_num=applicationJSON['program_num'],
        uin=applicationJSON['uin'],
        uncom_cert=applicationJSON.get('uncom_cert'),
        com_cert=applicationJSON.get('com_cert'),
        purpose_statement=applicationJSON['purpose_statement']
    )

    response = application.create()
    return jsonify({"response": response})

def update_application(applicationJSON) -> jsonify:
    assert isinstance(g.conn, psycopg.Connection)

    # Validate the JSON data
    valid_request = applicationJSON is not None
    valid_request &= all(field in applicationJSON for field in ['app_num', 'program_num', 'uin', 'purpose_statement'])
    if not valid_request:
        return jsonify({"response": "Invalid application data. Required fields: app_num, program_num, uin, purpose_statement"}), 400

    application = Application(
        app_num=applicationJSON['app_num'],
        program_num=applicationJSON['program_num'],
        uin=applicationJSON['uin'],
        uncom_cert=applicationJSON.get('uncom_cert'),
        com_cert=applicationJSON.get('com_cert'),
        purpose_statement=applicationJSON['purpose_statement']
    )

    response = application.update()
    return jsonify({"response": response})

def get_own_application(uin) -> jsonify:
    assert isinstance(g.conn, psycopg.Connection)

    # Validate the user's UIN
    if not isinstance(uin, int):
        return jsonify({"response": "Invalid UIN"}), 400

    application = Application(uin=uin)
    application_records = application.fetch()

    if not application_records:
        return jsonify({"response": "Error fetching application information"}), 500

    # Convert the result to a list of dictionaries
    applications_list = [
        {
            'app_num': record[0],
            'program_num': record[1],
            'uin': record[2],
            'uncom_cert': record[3],
            'com_cert': record[4],
            'purpose_statement': record[5],
            'app_date': record[6].isoformat() if record[6] else None
        }
        for record in application_records
    ]

    return jsonify(applications_list)

def remove_application(app_num) -> jsonify:
    assert isinstance(g.conn, psycopg.Connection)

    # Validate the application number
    if not isinstance(app_num, int):
        return jsonify({"response": "Invalid application number"}), 400

    application = Application(app_num=app_num)
    response = application.delete()

    return jsonify({"response": response})
