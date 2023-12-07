from flask import Blueprint, request, g, abort, Response
import psycopg
import sys
sys.path.insert(1, "/home/david-liu/david_liu/TAMU/FALL2023/CSCE310/final_project/CSCE310_Final_Project/backend")
from db_interface.college_students import CollegeStudent
from toolkit.user_tools import *
from toolkit.college_student_tools import *

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("", methods=["POST"])
@authenticate
def create_new_user() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    if request.json is None:
        abort(415)
    if not isinstance(request.json, dict):
        abort(400)
    if "username" not in request.json or "password" not in request.json or "uin" not in request.json:
        abort(400)
    if not isinstance(request.json["uin"], int):
        abort(400)
    if not isinstance(request.json["username"], str) or not isinstance(request.json["password"], str):
        abort(400)
    
    new_user = create_user(request.json)
    return new_user.getJSON()

@bp.route("", methods=["GET"])
@authenticate
def get_all_users() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    return fetch_all_users()

@bp.route("/<int:uin>", methods=["GET"])
@authenticate
def get_user_by_uin(uin) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(uin, int):
        abort(400)
    current_user = User(uin=uin)
    if (len(current_user.fetch()) == 0):
        abort(404, f"no user with uin: {uin}")
    current_user.autoFill()
    return current_user.getJSON()

@bp.route("/<int:uin>", methods=["DELETE"])
@authenticate
@check_if_admin
def delete_user_by_uin(uin) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(uin, int):
        abort(400)
    current_user = User(uin=uin)
    response = current_user.delete()
    return {"response": response}

@bp.route("/<int:uin>/deactivate", methods=["PUT"])
@authenticate
@check_if_admin
def deactivate_user_by_uin(uin):
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(uin, int):
        abort(400)
    
    current_user = User(uin=uin)
    response = current_user.deactivate_user()
    return {"response": response}

@bp.route("/<int:uin>/activate", methods=["PUT"])
@authenticate
@check_if_admin
def activate_user_by_uin(uin):
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(uin, int):
        abort(400)
    
    current_user = User(uin=uin)
    response = current_user.activate_user()
    return {"response": response}

@bp.route("/<int:uin>/set-admin", methods=["PUT"])
@authenticate
@check_if_admin
def set_admin_by_uin(uin):
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(uin, int):
        abort(400)
    
    current_user = User(uin=uin)
    response = current_user.makeAdmin()
    return {"response": response}

@bp.route("/<int:uin>/set-user", methods=["PUT"])
@authenticate
@check_if_admin
def set_user_by_uin(uin):
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(uin, int):
        abort(400)
    
    current_user = User(uin=uin)
    response = current_user.removeAdmin()
    return {"response": response}

@bp.route("/student", methods=["POST"])
@authenticate
@check_if_admin
def create_new_student():
    assert isinstance(g.conn, psycopg.Connection)
    bad_request = ~isinstance(request.json, dict)
    bad_request |= 'uin' not in request.json
    bad_request |= ~isinstance(request.json['uin'], int)
    bad_request |= len(User(uin = request.json['uin']).fetch()) == 0
    if bad_request:
        abort(400, "Make sure uin exists as a user!")

    new_student = create_college_student(request.json)
    return jsonify(new_student.getJSON())

@bp.route("", methods=["PATCH"])
@authenticate
def patch_user():
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    bad_request = ~isinstance(request.json, dict)
    bad_request |= 'uin' not in request.json
    bad_request |= ~isinstance(request.json['uin'], int)
    bad_request |= len(User(uin = request.json['uin']).fetch()) == 0
    if bad_request:
        abort(400, "Make sure uin exists as a user!")
    if g.userobj.uin != request.json['uin'] and g.userobj.user_type != 'ADMIN':
        abort(401, "Not an admin, can only update your own account")
    
    return update_user(request.json)

@bp.route("/student", methods=["PATCH"])
@authenticate
def patch_student():
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    bad_request = ~isinstance(request.json, dict)
    bad_request |= 'uin' not in request.json
    bad_request |= ~isinstance(request.json['uin'], int)
    bad_request |= len(User(uin = request.json['uin']).fetch()) == 0
    if bad_request:
        abort(400, "Make sure uin exists as a user!")
    if g.userobj.uin != request.json['uin'] and g.userobj.user_type != 'ADMIN':
        abort(401, "Not an admin, can only update your own account")
    
    return update_college_student(request.json)