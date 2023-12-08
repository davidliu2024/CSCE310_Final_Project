from db_interface.class_enrollments import ClassEnrollment
from flask import Response, jsonify


def create_enrollment(enrollmentJSON) -> Response:
    enrollment = ClassEnrollment(
        uin=enrollmentJSON.get('uin'),
        class_id=enrollmentJSON.get('class_id'),
        class_status=enrollmentJSON.get('class_status'),
        semester=enrollmentJSON.get('semester'),
        class_year=enrollmentJSON.get('class_year'),
    )

    result = enrollment.create()

    if result == "success":
        return jsonify(enrollment.get_json())
    else:
        return jsonify({"response": result})

def delete_enrollment(enrollmentJSON) -> Response:
    ce_num = enrollmentJSON.get('ce_num')
    uin = enrollmentJSON.get('uin')
    class_id = enrollmentJSON.get('class_id')

    enrollment = ClassEnrollment(ce_num=ce_num, uin=uin, class_id=class_id)
    result = enrollment.delete()
    return jsonify({ "response": result })

def update_enrollment(enrollmentJSON):
    enrollment = ClassEnrollment(
        uin=enrollmentJSON.get('uin'),
        class_id=enrollmentJSON.get('class_id'),
        class_status=enrollmentJSON.get('class_status'),
        semester=enrollmentJSON.get('semester'),
        class_year=enrollmentJSON.get('class_year'),
    )

    result = enrollment.update()
    return jsonify({ "response": result })