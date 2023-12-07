
import psycopg
from flask import Blueprint, request, g, abort, Response, jsonify
from toolkit.user_tools import authenticate  # Assuming you have authentication tools
from toolkit.application_tools import ApplicationTools
from db_interface.applications import Application  # Import the Application class

bp = Blueprint("applications", __name__, url_prefix="/applications")

<<<<<<< HEAD:backend/flaskapi/application.py
=======

>>>>>>> 167d5b42fc45524e0daba6a67ab17025e0dab609:backend/flaskapi/applications.py
@bp.route("", methods=["POST"])
@authenticate
def create_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    data = request.json

    required_fields = ['program_num', 'uin']
    if not all(field in data for field in required_fields):
        abort(400)

    response = ApplicationTools.create_application(**data)
    return jsonify({"response": response})

@bp.route("", methods=["GET"])
@authenticate
def fetch_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    data = request.args

    response = ApplicationTools.fetch_application(**data)
    return jsonify(response)

@bp.route("", methods=["PUT"])
@authenticate
def auto_fill_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    data = request.args

    response = ApplicationTools.auto_fill_application(**data)
    return jsonify({"response": response})

@bp.route("/<int:app_num>", methods=["PATCH"])
@authenticate
def update_application(app_num) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    data = request.json

    response = ApplicationTools.update_application(app_num=app_num, **data)
    return jsonify({"response": response})

@bp.route("", methods=["DELETE"])
@authenticate
def delete_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    data = request.args

    response = ApplicationTools.delete_application(**data)
    return jsonify({"response": response})

@bp.route("/between_dates", methods=["GET"])
@authenticate
def fetch_applications_between_dates() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    response = ApplicationTools.fetch_applications_between_dates(start_date, end_date)
    return jsonify(response)

