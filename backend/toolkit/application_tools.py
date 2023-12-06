from flask import Blueprint, request, g, abort, Response, jsonify
import psycopg
from db_interface.applications import Application

application_tools_bp = Blueprint('application_tools', __name__)

@application_tools_bp.before_app_request
def before_request():
    try:
        g.conn = psycopg.connect(
            dbname='your_db_name',
            user='your_db_user',
            password='your_db_password',
            host='your_db_host',
            port='your_db_port'
        )
    except Exception as e:
        abort(Response(f"Error connecting to the database: {e}", status=500))

@application_tools_bp.teardown_app_request
def teardown_request(exception):
    if hasattr(g, 'conn'):
        g.conn.close()

@application_tools_bp.route('/application/set_connection', methods=['POST'])
def set_connection_manually():
    conn = request.get_json().get('conn')
    Application().set_connection_manually(conn)
    return jsonify({"response": "success"})

@application_tools_bp.route('/application/close_connection', methods=['POST'])
def close_connection_manually():
    Application().close_connection_manually()
    return jsonify({"response": "success"})
