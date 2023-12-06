from flask import Blueprint, request, g, abort, Response, jsonify
import psycopg
import sys
sys.path.insert(1, "/home/david-liu/david_liu/TAMU/FALL2023/CSCE310/final_project/CSCE310_Final_Project/backend")
from toolkit.user_tools import authenticate, check_if_admin
from toolkit.class_tools import *
from db_interface.classes import CourseClass

bp = Blueprint("classes", __name__, url_prefix="/classes")

@bp.route("", methods=["POST"])
@authenticate
@check_if_admin
def create_new_class() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    good_request &= all(field in request.json for field in ['class_name', 'class_description', 'class_type'])
    if not good_request:
        abort(400)

    new_class = create_class(request.json)
    return new_class.get_json()

@bp.route("", methods=["GET"])
@authenticate
def get_all_classes() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    return fetch_all_classes()

@bp.route("/<int:class_id>", methods=["GET"])
@authenticate
def get_class_by_id(class_id) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(class_id, int):
        abort(400)
    current_class = CourseClass(class_id=class_id)
    if len(current_class.fetch()) == 0:
        abort(404, f"no class with class_id: {class_id}")
    current_class.auto_fill()
    return current_class.get_json()

@bp.route("/<int:class_id>", methods=["DELETE"])
@authenticate
@check_if_admin
def delete_class_by_id(class_id) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(class_id, int):
        abort(400)
    current_class = CourseClass(class_id=class_id)
    response = current_class()
    return response

@bp.route("/<int:class_id>", methods=["PATCH"])
@authenticate
@check_if_admin
def update_class(class_id) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    good_request &= all(field in request.json for field in ['class_name', 'class_description', 'class_type'])
    response = patch_class(class_id, request.json)
    return response