from flask import Blueprint, request, g, abort, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Unauthorized
import psycopg
import sys
import os
# sys.path.insert(1, os.getcwd())
from db_interface.users import User
from toolkit.user_tools import *

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("", methods=["GET"])
@authenticate
def login() -> dict:
    assert isinstance(g.conn, psycopg.Connection)
    current_user = User(g.useruin)
    current_user.autoFill()

    return current_user.getJSON()
