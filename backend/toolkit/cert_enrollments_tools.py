from flask import g, jsonify
import psycopg
from db_interface.cert_enrollments import CertEnrollment

def create_cert_enrollment(cert_enrollment_json) -> CertEnrollment:
    '''
    Create a new class and return the class with class_json
    '''
    cert_enrollment_instance = CertEnrollment(
        certe_num=cert_enrollment_json.get('certe_num'),
        uin=cert_enrollment_json.get('uin'),
        cert_id=cert_enrollment_json.get('cert_id'),
        cert_status=cert_enrollment_json.get('cert_status'),
        training_status=cert_enrollment_json.get('training_status'),
        program_num=cert_enrollment_json.get('program_num'),
        semester = cert_enrollment_json.get('semester'),
        cert_year=cert_enrollment_json.get('cert_year'),

    )

    cert_enrollment_instance.create()
    return cert_enrollment_instance

def fetch_all_cert_enrollments():
    '''
    Fetch all classes and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM cert_enrollment
                '''
            )
            cert_enrollment_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            classes_list = [
                {
                    'certe_num': record[0],
                    'uin': record[1],
                    'cert_id': record[2],
                    'cert_status': record[3],
                    'training_status': record[4],
                    'program_num': record[5],
                    'semester': record[6],
                    'cert_year': record[7]
                }
                for record in cert_enrollment_records
            ]

            return jsonify(classes_list)

        except Exception as e:
            g.conn.rollback()
            return {"response": f"Error fetching all cert enrollments: {e}"}

def patch_cert_enrollment(cert_enrollment_json):
    '''
    Update an existing class and return the class with class_json
    '''
    cert_enrollment_instance = CertEnrollment(
        certe_num=cert_enrollment_json.get('certe_num'),
        uin=cert_enrollment_json.get('uin'),
        cert_id=cert_enrollment_json.get('cert_id'),
        cert_status=cert_enrollment_json.get('cert_status'),
        training_status=cert_enrollment_json.get('training_status'),
        program_num=cert_enrollment_json.get('program_num'),
        semester = cert_enrollment_json.get('semester'),
        cert_year=cert_enrollment_json.get('cert_year'),

    )

    return {"response": cert_enrollment_instance.update()}




def delete_cert_enrollment( certEnrollmentJSON):
    cert_enrollment = CertEnrollment(
        certe_num = certEnrollmentJSON.get('cert_num')
    )

    cert_enrollment.delete()

    