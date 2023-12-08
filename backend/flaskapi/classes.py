from flask import Blueprint, request, g, abort, Response, jsonify
import psycopg
from toolkit.class_enrollment_tools import create_enrollment
from toolkit.user_tools import authenticate, check_if_admin
from toolkit.class_tools import *
from toolkit.class_enrollment_tools import *
from db_interface.classes import CourseClass
from db_interface.users import User

bp = Blueprint("classes", __name__, url_prefix="/classes")

@bp.route("", methods=["POST"])
@authenticate
@check_if_admin
def create_new_class():
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    assert isinstance(request.json, dict)
    good_request &= all(field in request.json for field in ['class_name', 'class_description', 'class_type'])
    if not good_request:
        abort(400)

    new_class = create_class(request.json)
    return new_class.get_json()

@bp.route("", methods=["GET"])
@authenticate
def get_all_classes():
    assert isinstance(g.conn, psycopg.Connection)
    return fetch_all_classes()

@bp.route("/<int:class_id>", methods=["GET"])
@authenticate
def get_class_by_id(class_id):
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
def delete_class_by_id(class_id):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(class_id, int):
        abort(400)
    current_class = CourseClass(class_id=class_id)
    response = current_class.delete()
    return response

@bp.route("/<int:class_id>", methods=["PUT"])
@authenticate
@check_if_admin
def update_class(class_id) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    assert isinstance(request.json, dict)
    good_request &= all(field in request.json for field in ['class_name', 'class_description', 'class_type'])
    response = patch_class(class_id, request.json)
    return Response(response, 200)

@bp.route("/fetch-enrollments", methods=["GET"])
@authenticate
def fetch_user_classes()->Response:
    assert isinstance(g.conn, psycopg.Connection)
    response = fetch_enrollments()
    return response

@bp.route("/add-enrollment", methods=["POST"])
@authenticate
def add_user_to_class() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    if request.json is None:
        abort(400)
    assert isinstance(request.json, dict)
    is_owner = request.json.get("uin") == g.userobj.uin
    if is_owner:
        return create_enrollment(request.json)
    else:
        abort(401, "Cannot enroll for this person")

@bp.route("/remove-enrollment", methods=["DELETE"])
@authenticate
def remove_user_from_class() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    if request.json is None:
        abort(400)
    assert isinstance(request.json, dict)
    is_owner = request.json.get("uin") == g.userobj.uin
    if is_owner:
        return delete_enrollment(request.json)
    else:
        abort(401, "Cannot update enrollment for this person")

@bp.route("/update-enrollment", methods=["PUT"])
@authenticate
def update_user_in_class() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    if request.json is None:
        abort(400)
    assert isinstance(request.json, dict)
    is_owner = request.json.get("uin") == g.userobj.uin
    if is_owner:
        return update_enrollment(request.json)
    else:
        abort(401, "Cannot delete enrollment for this person")