from flask import Blueprint, request, g, abort, Response
import psycopg
from toolkit.user_tools import authenticate, check_if_admin
from toolkit.certification_tools import *

bp = Blueprint("certifications", __name__, url_prefix="/certifications")

@bp.route("", methods=["POST"])
@authenticate
@check_if_admin
def create_new_certification():
    assert isinstance(g.conn, psycopg.Connection)
    if request.json is None:
        abort(400, "JSON empty")
    assert isinstance(request.json, dict)
    good_request = all(field in request.json for field in ['cert_level', 'cert_name', 'cert_description'])
    if not good_request:
        abort(400)
    
    response = create_certification(request.json)
    if response=="success":
        return Response(response, 202)
    else:
        abort(400,response)

@bp.route("", methods=["GET"])
@authenticate
def get_all_certifications():
    assert isinstance(g.conn, psycopg.Connection)
    return fetch_all_certifications()

@bp.route("/<int:cert_id>", methods=["GET"])
@authenticate
def get_certification_by_id(cert_id):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(cert_id, int):
        abort(400)
    current_certification = Certification(cert_id=cert_id)
    if (len(current_certification.fetch()) == 0):
        abort(404, f"no certification with cert_id: {cert_id}")
    current_certification.auto_fill()
    return current_certification.get_json()

@bp.route("/<int:cert_id>", methods=["DELETE"])
@authenticate
@check_if_admin
def delete_certification_by_id(cert_id):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(cert_id, int):
        abort(400)
    current_certification = Certification(cert_id=cert_id)
    response = current_certification.delete()
    if response=="success":
        return Response(response, 202)
    else:
        abort(400,response)

@bp.route("/<int:cert_id>", methods=["PUT"])
@authenticate
@check_if_admin
def update_certification(cert_id):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(request.json, dict):
        abort(400)
    assert isinstance(request.json, dict)
    good_request = all(field in request.json for field in ['cert_level', 'cert_name', 'cert_description'])
    if not good_request:
        abort(400)
    response = patch_certification(cert_id, request.json)
    if response=="success":
        return Response(response, 202)
    else:
        abort(400,response)

