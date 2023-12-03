from flask import Blueprint, request, g, abort, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Unauthorized
import psycopg

bp = Blueprint("auth", __name__, url_prefix="/auth")


def authenticate(func):
    """
    Requires HTTP Basic Authentication before a request is processed.
    On failure, returns a 401 status code.
    On success, sets `g.userid` to the authenticated user's ID.
    """
    def inner(*args, **kwargs):
        if request.authorization is None or request.authorization.type != "basic":
            abort(401)
        username = request.authorization.parameters["username"].lower()
        password = request.authorization.parameters["password"]

        assert isinstance(g.conn, psycopg.Connection)
        with g.conn.cursor() as cur:
            cur.execute("SELECT passwords, uin FROM users WHERE username = %s;", (username,))
            if cur.rowcount == 0:
                abort(401)
            passwordhash, uin = cur.fetchone()
            if passwordhash != password:
                abort(401)
            g.useruin = uin
        
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner


@bp.route("", methods=["GET"])
@authenticate
def login() -> Response:
    """
    Returns a 200 status code if the given HTTP authorization is valid, or 401 if not.
    Response body is a JSON object with two fields:
    """
    assert isinstance(g.conn, psycopg.Connection)
    with g.conn.cursor() as cur:
        print(g.useruin)
        cur.execute("SELECT first_name FROM users WHERE uin = %s;", (g.useruin,))
        dname, = cur.fetchone()
        return {"uin": g.useruin, "first_name": dname}