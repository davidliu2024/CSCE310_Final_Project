from flask import g, jsonify
import psycopg
from db_interface.class_enrollments import ClassEnrollment


def create_enrollment( enrollmentJSON ) -> ClassEnrollment:

    enrollment = ClassEnrollment(
        ce_num = enrollmentJSON.get('ce_num'),
        uin = enrollmentJSON.get('uin'),
        class_id = enrollmentJSON.get('class_id'),
        class_status = enrollmentJSON.get('class_status'),
        semester = enrollmentJSON.get('semester'),
        class_year = enrollmentJSON.get('class_year'),
    )

    enrollment.create()

    return enrollment

#TODO: FINISH THE REST OF THIS. -Hayden

