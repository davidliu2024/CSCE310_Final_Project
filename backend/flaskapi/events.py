from flask import Blueprint, request, g, abort, Response
import psycopg
from toolkit.user_tools import authenticate, check_if_admin
from toolkit.event_tools import *
from db_interface.users import User

bp = Blueprint("events", __name__, url_prefix="/events")

@bp.route("", methods=["POST"])
@authenticate
@check_if_admin
def create_new_event():
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    assert isinstance(request.json, dict)
    good_request &= all(field in request.json for field in ['uin', 'program_num', 'event_name'])
    if not good_request:
        abort(400)
    
    new_event = create_event(request.json)
    return new_event.getJSON()

@bp.route("", methods=["GET"])
@authenticate
def get_all_events():
    assert isinstance(g.conn, psycopg.Connection)
    return fetch_all_events()

@bp.route("/<int:event_id>", methods=["GET"])
@authenticate
def get_event_by_id(event_id):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(event_id, int):
        abort(400)
    current_event = Event(event_id=event_id)
    if (len(current_event.fetch()) == 0):
        abort(404, f"no event with event_id: {event_id}")
    current_event.auto_fill()
    return current_event.getJSON()

@bp.route("/<int:event_id>", methods=["DELETE"])
@authenticate
@check_if_admin
def delete_event_by_id(event_id):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(event_id, int):
        abort(400)
    current_event = Event(event_id=event_id)
    response = current_event.delete()
    return {"response": response}

@bp.route("", methods=["PUT"])
@authenticate
@check_if_admin
def update_event():
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    assert isinstance(request.json, dict)
    good_request &= all(field in request.json for field in ['uin', 'program_num', 'event_name'])
    response = patch_event(request.json)
    return {"response": response}

@bp.route("<int:event_num>/add-user/<int:uin>", methods=["POST"])
@authenticate
@check_if_admin
def add_to_event(event_num, uin):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(event_num, int):
        abort(400)
    user = User(uin=uin)
    response = user.add_user_to_event(event_id=event_num)
    return { "response": response }

@bp.route("<int:event_num>/remove-user/<int:uin>", methods=["POST"])
@authenticate
@check_if_admin
def remove_from_event(event_num, uin):
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(event_num, int):
        abort(400)
    user = User(uin=uin)
    response = user.remove_user_from_event(event_id=event_num)
    return { "response": response }