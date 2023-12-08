from flask import Blueprint, request
from toolkit.user_tools import *
from toolkit.internship_tools import *

bp = Blueprint("internships", __name__, url_prefix="/internships")

@bp.route('', methods = ['POST'])
@authenticate
def create_intern_app():
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    if not isinstance(request.json, dict):
        abort(400)
    good_request = all(field in request.json for field in ['internship_name', 'internship_description', 'is_gov'])
    if not good_request:
        abort(400)
    return Response(create_internship(request.json),202)

@bp.route('', methods = ['GET'])
@authenticate
def get_intern_applications()->Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    response = fetch_all_internships()
    return jsonify(response)

@bp.route("", methods=["PUT"])
@authenticate
def update_internship_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(request.json, dict):
        abort(400)
    good_request = all(field in request.json for field in ['intern_id', 'internship_name', 'internship_description', 'is_gov'])
    if not good_request:
        abort(400)

    response = patch_internship(request.json)
    if response == "success":
        return jsonify({"response": response})
    else:
        abort(401)

@bp.route("/<int:id>", methods=["DELETE"])
@authenticate
def remove_intern_application(id) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    response = remove_internship(id=id)
    return jsonify(response)