from flask import request, g, Blueprint, Response
import psycopg
import psycopg.adapt
import os


bp = Blueprint("db", __name__)

@bp.before_app_request
def connect() -> None:
    """
    Connect to the database and add the handle to the app context's globals.
    """
    filename = os.environ.get("PSQL_CONF")
    if filename is None:
        raise RuntimeError("Environment variable PSQL_CONF is not set.")
    connstr = None
    try:
        file = open(filename)
        connstr = file.read()
    except OSError:
        raise RuntimeError("Could not open PSQL_CONF.")
    finally:
        file.close()
    
    try:
        g.conn = psycopg.connect(connstr, autocommit=True)
    except psycopg.Error as e:
        raise RuntimeError(e.pgconn)

@bp.after_app_request
def disconnect(response: Response) -> Response:
    """
    Close the database connection stored in the app context.
    """
    g.conn.close()
    return response