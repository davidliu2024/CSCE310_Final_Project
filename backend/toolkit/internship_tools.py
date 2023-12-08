from sys import intern
from flask import g, jsonify
import psycopg
from db_interface.internships import Internship

def create_internship(internJSON):
    '''
    Create a new internship and return the program with internJSON
    '''
    internship = Internship(
        intern_id=internJSON.get('intern_id'),
        internship_name=internJSON.get('internship_name'),
        internship_description=internJSON.ge('internship_description'),
        is_gov = internJSON.get('is_gov')
    )

    response = internship.create()
    return response

def fetch_all_internships():
    '''
    Fetch all internships and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM internship
                '''
            )
            internship_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            internship_list = [
                {
                    'intern_id': record[0],
                    'internship_name': record[1],
                    'internship_description': record[2],
                    'is_gov': record[3]
                }
                for record in internship_records
            ]

            return jsonify(internship_list)

        except Exception as e:
            g.conn.rollback()
            return {"response": f"Error fetching all internships: {e}"}

def patch_internship( internJSON ):
    '''
    Update an existing internship and return the internship with internJSON
    '''
    internship = Internship(
        intern_id=internJSON.get('intern_id'),
        internship_name=internJSON.get('internship_name'),
        internship_description=internJSON.ge('internship_description'),
        is_gov = internJSON.get('is_gov')
    )

    return {"response": internship.update()}

def remove_internship(id):
    internship = Internship(intern_id=id)
    return internship.delete()
