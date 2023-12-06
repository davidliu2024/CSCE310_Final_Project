import datetime
from flask import Blueprint, request, g, abort, Response, jsonify
from db_interface.applications import Application

application_bp = Blueprint('application', __name__)

@application_bp.route('/application', methods=['POST'])
def create_application():
    applicationJSON = request.get_json()
    application = Application(
        program_num=applicationJSON['program_num'],
        uin=applicationJSON['uin'],
        uncom_cert=applicationJSON.get('uncom_cert'),
        com_cert=applicationJSON.get('com_cert'),
        purpose_statement=applicationJSON.get('purpose_statement')
    )
    response = application.create()
    return jsonify({"response": response})

@application_bp.route('/application', methods=['GET'])
def fetch_application():
    applicationJSON = request.get_json()
    application = Application(
        app_num=applicationJSON.get('app_num'),
        program_num=applicationJSON.get('program_num'),
        uin=applicationJSON.get('uin')
    )
    result = application.fetch()
    return jsonify(result)

@application_bp.route('/application/auto_fill', methods=['GET'])
def auto_fill_application():
    applicationJSON = request.get_json()
    application = Application(
        app_num=applicationJSON.get('app_num'),
        program_num=applicationJSON.get('program_num'),
        uin=applicationJSON.get('uin')
    )
    success = application.auto_fill()
    return jsonify({"success": success})

@application_bp.route('/application', methods=['PUT'])
def update_application():
    applicationJSON = request.get_json()
    application = Application(
        app_num=applicationJSON['app_num'],
        program_num=applicationJSON['program_num'],
        uin=applicationJSON['uin'],
        uncom_cert=applicationJSON.get('uncom_cert'),
        com_cert=applicationJSON.get('com_cert'),
        purpose_statement=applicationJSON.get('purpose_statement')
    )
    response = application.update()
    return jsonify({"response": response})

@application_bp.route('/application', methods=['DELETE'])
def delete_application():
    applicationJSON = request.get_json()
    application = Application(
        app_num=applicationJSON.get('app_num'),
        program_num=applicationJSON.get('program_num'),
        uin=applicationJSON.get('uin')
    )
    response = application.delete()
    return jsonify({"response": response})

@application_bp.route('/application/between_dates', methods=['GET'])
def fetch_applications_between_dates():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    result = Application().fetch_applications_between_dates(start_date, end_date)
    return jsonify(result)
