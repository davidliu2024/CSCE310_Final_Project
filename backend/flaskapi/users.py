from flask import Blueprint, request, g, abort, Response
import psycopg
import sys
sys.path.insert(1, "/home/david-liu/david_liu/TAMU/FALL2023/CSCE310/final_project/CSCE310_Final_Project/backend")
from toolkit.user_tools import *

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("", methods=["POST"])
@authenticate
def create_new_user() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    if request.json is None:
        abort(415)
    if not isinstance(request.json, dict):
        abort(400)
    if "username" not in request.json or "password" not in request.json or "email" not in request.json:
        abort(400)
    if not isinstance(request.json["username"], str) or not isinstance(request.json["password"], str) \
        or not isinstance(request.json["email"], str) \
        or ("displayname" in request.json and not isinstance(request.json["displayname"], str)):
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
    current_user.delete()
    return {"status": "success"}

