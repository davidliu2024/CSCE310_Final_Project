from flask import Blueprint, request, g, abort, Response, jsonify
import psycopg
from toolkit.user_tools import authenticate, check_if_admin
from toolkit.program_tools import *
from db_interface.users import User

bp = Blueprint("programs", __name__, url_prefix="/programs")

@bp.route("", methods=["POST"])
@authenticate
@check_if_admin
def create_new_program():
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    assert isinstance(request.json, dict)
    good_request &= all(field in request.json for field in ['program_name', 'program_description', 'program_status'])
    if not good_request:
        abort(400)
    
    new_program = create_program(request.json)
    return new_program.get_json()

#gets all programs student is a enrolled in
@bp.route("", methods=["GET"])
@authenticate
def get_all_programs():
    assert isinstance(g.conn, psycopg.Connection)
    return fetch_all_programs()

#gets specific program details
@bp.route("/<int:program_num>", methods=["GET"])
@authenticate
def get_program_by_num(program_num):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(program_num, int):
        abort(400)
    current_program = Program(program_num=program_num)
    if (len(current_program.fetch()) == 0):
        abort(404, f"no program with program_num: {program_num}")
    current_program.auto_fill()
    return current_program.get_json()

@bp.route("/<int:program_num>", methods=["DELETE"])
@authenticate
@check_if_admin
def delete_program_by_num(program_num):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(program_num, int):
        abort(400)
    current_program = Program(program_num=program_num)
    response = current_program.delete()
    return response

#updates whole program (description, name, status, etc.)
@bp.route("/<int:program_num>", methods=["PUT"])
@authenticate
@check_if_admin
def update_program(program_num):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(request.json, dict):
        abort(400)
    assert isinstance(request.json, dict)
    good_request = all(field in request.json for field in ['program_name', 'program_status'])
    if not good_request:
        abort(400)
    response = patch_program(program_num, request.json)
    return response

#activates program and makes it available to students
@bp.route("/<int:program_num>/activate", methods=["PUT"])
@authenticate
@check_if_admin
def activate_program(program_num):
    assert isinstance(g.conn, psycopg.Connection)
    program = Program(program_num=program_num)
    return {"response" : program.activate_program()}

#deactivates program so students can't sign up
@bp.route("/<int:program_num>/deactivate", methods=["PUT"])
@authenticate
@check_if_admin
def deactivate_program(program_num):
    assert isinstance(g.conn, psycopg.Connection)
    program = Program(program_num=program_num)
    return {"response" : program.deactivate_program()}

#student can sign up for programs
@bp.route("/<int:program_num>/sign-up", methods=["PUT"])
@authenticate
def sign_up_program(program_num):
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    if not isinstance(program_num, int):
        abort(400)
    response = g.userobj.add_user_to_program(program_num = program_num)
    return { "response": response }

#removes user from program
@bp.route("/<int:program_num>/remove", methods=["PUT"])
@authenticate
def remove_program(program_num):
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    if not isinstance(program_num, int):
        abort(400)
    response = g.userobj.remove_user_from_program(program_num=program_num)
    return { "response": response }