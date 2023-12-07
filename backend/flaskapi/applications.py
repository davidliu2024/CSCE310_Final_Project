from flask import Flask, Blueprint, request, g, abort, Response, jsonify, session
import psycopg
from db_interface.users import User
from toolkit.application_tools import create_application, fetch_user_applications, update_application, delete_application

bp = Blueprint("applications", __name__, url_prefix="/applications")


@bp.route("", methods=["POST"])
def submit_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    good_request = request.json is not None
    good_request &= all(field in request.json for field in ['program_num', 'uncom_cert', 'com_cert', 'purpose_statement'])
    if not good_request:
        abort(400)

    application_response = create_application(g.userobj.uin, request.json)
    return jsonify({"response": application_response})

@bp.route("", methods=["GET"])
def get_user_applications() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    applications = fetch_user_applications(g.userobj.uin)
    return jsonify(applications)

@bp.route("", methods=["PATCH"])
def update_user_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    good_request = request.json is not None
    good_request &= all(field in request.json for field in ['app_num', 'program_num', 'uncom_cert', 'com_cert', 'purpose_statement'])
    if not good_request:
        abort(400)

    application_response = update_application(request.json)
    return jsonify({"response": application_response})

@bp.route("", methods=["DELETE"])
def delete_user_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    good_request = request.json is not None
    good_request &= 'app_num' in request.json
    if not good_request:
        abort(400)

    application_response = delete_application(request.json['app_num'])
    return jsonify({"response": application_response})

if __name__ == "__main__":
    bp.run(debug=True)
