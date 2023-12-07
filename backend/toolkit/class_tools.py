from flask import g, jsonify
import psycopg
from db_interface.classes import CourseClass

def create_class(class_json) -> CourseClass:
    '''
    Create a new class and return the class with class_json
    '''
    class_instance = CourseClass(
        class_name=class_json['class_name'],
        class_description=class_json.get('class_description'),
        class_type=class_json.get('class_type')
    )

    class_instance.create()
    return class_instance

def fetch_all_classes():
    '''
    Fetch all classes and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM classes
                '''
            )
            class_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            classes_list = [
                {
                    'class_id': record[0],
                    'class_name': record[1],
                    'class_description': record[2],
                    'class_type': record[3]
                }
                for record in class_records
            ]

            return jsonify(classes_list)

        except Exception as e:
            g.conn.rollback()
            return {"response": f"Error fetching all classes: {e}"}

def patch_class(class_id, class_json):
    '''
    Update an existing class and return the class with class_json
    '''
    class_instance = CourseClass(
        class_id=class_id,
        class_name=class_json['class_name'],
        class_description=class_json.get('class_description'),
        class_type=class_json.get('class_type')
    )

    return {"response": class_instance.update()}
