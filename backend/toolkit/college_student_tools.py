from flask import Blueprint, request, g, abort, Response, jsonify
from db_interface.college_students import CollegeStudent
from toolkit.user_tools import *

def create_college_student(studentJSON) -> CollegeStudent:
    student = CollegeStudent(
        uin=studentJSON['uin'],
        gender=studentJSON['gender'],
        hispanic_latino=studentJSON.get('hispanic_latino'),
        race=studentJSON.get('race'),
        us_citizen=studentJSON.get('us_citizen'),
        first_generation=studentJSON.get('first_generation'),
        dob=studentJSON['dob'],
        gpa=studentJSON.get('gpa'),
        major=studentJSON['major'],
        minor1=studentJSON.get('minor1'),
        minor2=studentJSON.get('minor2'),
        expected_graduation=studentJSON.get('expected_graduation'),
        school=studentJSON['school'],
        classification=studentJSON['classification'],
        phone=studentJSON['phone'],
        student_type=studentJSON.get('student_type')
    )

    student.create()
    return student

def update_college_student(studentJSON) -> str:
    student = CollegeStudent(
        uin=studentJSON['uin'],
        gender=studentJSON['gender'],
        hispanic_latino=studentJSON.get('hispanic_latino'),
        race=studentJSON.get('race'),
        us_citizen=studentJSON.get('us_citizen'),
        first_generation=studentJSON.get('first_generation'),
        dob=studentJSON['dob'],
        gpa=studentJSON.get('gpa'),
        major=studentJSON['major'],
        minor1=studentJSON.get('minor1'),
        minor2=studentJSON.get('minor2'),
        expected_graduation=studentJSON.get('expected_graduation'),
        school=studentJSON['school'],
        classification=studentJSON['classification'],
        phone=studentJSON['phone'],
        student_type=studentJSON.get('student_type')
    )

    return {"response": student.update()}