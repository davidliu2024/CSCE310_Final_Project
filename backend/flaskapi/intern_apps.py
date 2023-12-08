from flask import Blueprint, request
from toolkit.user_tools import *
from toolkit.intern_apps_tools import *

bp = Blueprint("intern-apps", __name__, url_prefix="/intern-apps")

@bp.route('', methods = ['POST'])
@authenticate
def create_intern_app():
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    return create_intern_application(request.json)

@bp.route('', methods = ['GET'])
@authenticate
def get_intern_applications():
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    if (g.userobj.isAdmin()):
        response = fetch_all_intern_applications()
    else:
        response = fetch_intern_applications()
    return response

@bp.route("", methods=["PUT"])
@authenticate
def update_internship_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(request.json, dict):
        abort(400)
    good_request = all(field in request.json for field in ['ia_num', 'uin', 'intern_id', 'app_status', 'app_year'])
    if not good_request:
        abort(400)

    response = patch_intern_application(request.json)
    if response == "success":
        return jsonify({"response": response})
    else:
        abort(401)

@bp.route("/<int:ia_num>", methods=["DELETE"])
@authenticate
def remove_intern_application(ia_num) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    response = delete_intern_application(ia_num=ia_num)
    return jsonify(response)
