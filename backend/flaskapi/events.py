from flask import Blueprint, request, g, abort, Response
import psycopg
import sys
sys.path.insert(1, "/home/david-liu/david_liu/TAMU/FALL2023/CSCE310/final_project/CSCE310_Final_Project/backend")
from db_interface.college_students import CollegeStudent
from toolkit.user_tools import authenticate, check_if_admin
from toolkit.event_tools import *

bp = Blueprint("events", __name__, url_prefix="/events")

@bp.route("", methods=["POST"])
@authenticate
@check_if_admin
def create_new_event() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    good_request &= all(field in request.json for field in ['uin', 'program_num', 'event_name'])
    if not good_request:
        abort(400)
    
    new_event = create_event(request.json)
    return new_event.getJSON()

@bp.route("", methods=["GET"])
@authenticate
def get_all_events() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    return fetch_all_events()

@bp.route("/<int:event_id>", methods=["GET"])
@authenticate
def get_event_by_id(event_id) -> Response:
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
def delete_event_by_id(event_id) -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    if not isinstance(event_id, int):
        abort(400)
    current_event = Event(event_id=event_id)
    response = current_event.delete()
    return {"response": response}

@bp.route("", methods=["PATCH"])
@authenticate
def update_event() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    good_request = request.json is not None
    good_request &= all(field in request.json for field in ['uin', 'program_num', 'event_name'])
    response = patch_event(request.json)
    return {"response": response}
