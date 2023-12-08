from flask import g, jsonify
import psycopg
from db_interface.certifications import Certification

def create_certification(certificationJSON):
    '''
    Create a new certification and return the certification with certificationJSON
    '''
    certification = Certification(
        cert_level=certificationJSON['cert_level'],
        cert_name=certificationJSON.get('cert_name'),
        cert_description=certificationJSON.get('cert_description')
    )

    return certification.create()

def fetch_all_certifications():
    '''
    Fetch all certifications and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM certification
                '''
            )
            certification_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            certifications_list = [
                {
                    'cert_id': record[0],
                    'cert_level': record[1],
                    'cert_name': record[2],
                    'cert_description': record[3]
                }
                for record in certification_records
            ]

            return jsonify(certifications_list)

        except Exception as e:
            g.conn.rollback()
            return {"response": f"Error fetching all certifications: {e}"}

def patch_certification(cert_id, certificationJSON):
    '''
    Update an existing certification and return the certification with certificationJSON
    '''
    certification = Certification(
        cert_id=cert_id,
        cert_level=certificationJSON['cert_level'],
        cert_name=certificationJSON.get('cert_name'),
        cert_description=certificationJSON.get('cert_description')
    )

    return {"response": certification.update()}
