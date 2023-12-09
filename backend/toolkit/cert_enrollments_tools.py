from flask import g, jsonify
import psycopg
from db_interface.cert_enrollments import CertEnrollment
from db_interface.users import User

def create_cert_enrollment(cert_enrollment_json):
    '''
    Create a new class and return the class with class_json
    '''
    assert isinstance(g.userobj, User)
    cert_enrollment_instance = CertEnrollment(
        cert_en_num=cert_enrollment_json.get('cert_en_num'),
        uin=g.userobj.uin,
        cert_id=cert_enrollment_json.get('cert_id'),
        cert_status=cert_enrollment_json.get('cert_status'),
        training_status=cert_enrollment_json.get('training_status'),
        program_num=cert_enrollment_json.get('program_num'),
        semester = cert_enrollment_json.get('semester'),
        cert_year=cert_enrollment_json.get('cert_year'),

    )

    return cert_enrollment_instance.create()

def fetch_all_cert_enrollments():
    '''
    Fetch all classes and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)
    enrollments = CertEnrollment().fetch_all()
    return jsonify(enrollments)

def fetch_user_cert_enrollment():
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    enrollments = CertEnrollment(uin=g.userobj.uin).fetch()
    return jsonify(enrollments)

def patch_cert_enrollment(cert_enrollment_json):
    '''
    Update an existing class and return the class with class_json
    '''
    assert isinstance(g.userobj, User)
    cert_enrollment_instance = CertEnrollment(
        cert_en_num=cert_enrollment_json.get('cert_en_num'),
        uin=g.userobj.uin,
        cert_id=cert_enrollment_json.get('cert_id'),
        cert_status=cert_enrollment_json.get('cert_status'),
        training_status=cert_enrollment_json.get('training_status'),
        program_num=cert_enrollment_json.get('program_num'),
        semester = cert_enrollment_json.get('semester'),
        cert_year=cert_enrollment_json.get('cert_year'),

    )

    return cert_enrollment_instance.update()

def delete_cert_enrollment(cert_en_num):
    cert_enrollment = CertEnrollment(
        cert_en_num = cert_en_num
    )
    return cert_enrollment.delete()