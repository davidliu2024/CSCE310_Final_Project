from flask import Blueprint, request, g, abort, jsonify, Response
import psycopg
from toolkit.user_tools import authenticate
from toolkit.application_tools import *

bp = Blueprint("applications", __name__, url_prefix="/applications")

@bp.route("", methods=["POST"])
@authenticate
def submit_new_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    good_request &= all(field in request.json for field in ['program_num', 'uncompleted_certificate', 'completed_certificate', 'purpose_statement'])
    if not good_request:
        abort(400)

    new_application = submit_application(request.json)
    return new_application.getJSON()

@bp.route("", methods=["PUT"])
@authenticate
def edit_application_details() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    updated_data = request.json.get('updated_data', {})

    if not good_request or not updated_data:
        abort(400)

    application_id = updated_data.get('application_id')
    if application_id is None:
        abort(400)

    updated_application = edit_application(application_id, updated_data)
    return updated_application.getJSON()

@bp.route("", methods=["GET"])
@authenticate
def view_application_info() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    application_id = request.args.get('application_id')

    if application_id is None:
        abort(400)

    return jsonify(view_application_info(application_id))

@bp.route("", methods=["DELETE"])
@authenticate
def delete_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    application_id = request.args.get('application_id')

    if application_id is None:
        abort(400)

    response = delete_application(application_id)
    return jsonify(response)
