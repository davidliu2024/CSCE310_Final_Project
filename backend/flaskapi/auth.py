from flask import Blueprint, g, abort
import psycopg
from db_interface.users import User
from toolkit.user_tools import *

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("", methods=["GET"])
@authenticate
def login() -> dict:
    assert isinstance(g.conn, psycopg.Connection)
    current_user = User(g.useruin)
    if current_user.user_type == "DEACTIVATED":
        abort(401, "This account has been deactivated")
    current_user.autoFill()

    return current_user.getJSON()
