from flask import Blueprint, request
from db_interface.documents import Document
from db_interface.applications import Application
from db_interface.users import User
from toolkit.user_tools import *
from toolkit.college_student_tools import *
from toolkit.document_tools import *
from toolkit.application_tools import *

bp = Blueprint("applications", __name__, url_prefix="/applications")

@bp.route('/documents/<int:appnum>', methods = ['POST'])
@authenticate
def upload_document_by_appnum(appnum):
    uploaded_file=request.files.get("file")
    return upload_document(appnum=appnum, uploaded_file=uploaded_file)

@bp.route('/documents/<int:app_num>', methods = ['GET'])
@authenticate
def get_document_by_app(app_num):
    assert isinstance(g.userobj, User)
    app = Application(app_num=app_num)
    app.auto_fill()
    app.uin = g.userobj.uin
    return fetch_documents(app_num=app_num)

@bp.route('/documents/user', methods = ['GET'])
@authenticate
def get_document_by_uin():
    assert isinstance(g.userobj, User)
    return fetch_documents(uin=g.userobj.uin)

@bp.route('/documents/<int:docnum>', methods = ['DELETE'])
@authenticate
def delete_document_by_appnum(docnum)->Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    doc = Document(doc_num=docnum)
    doc.auto_fill()
    appnum = doc.app_num
    app = Application(app_num = appnum)
    app.auto_fill()
    if not (g.userobj.uin == app.uin or g.userobj.isAdmin()):
        abort(401, "user cannot delete this file")

    response = doc.delete()
    return Response(response, 202)


@bp.route("", methods=["POST"])
@authenticate
def submit_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(request.json, dict):
        abort(400)
    good_request = all(field in request.json for field in ['program_num', 'uncom_cert', 'com_cert', 'purpose_statement'])
    if not good_request:
        abort(400)

    return create_application(g.userobj.uin, request.json)

@bp.route("/get-all", methods=["GET"])
@authenticate
@check_if_admin
def get_all_applications():
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    applications = fetch_all_applications()
    return applications

@bp.route("", methods=["GET"])
@authenticate
def get_user_applications() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    applications = fetch_user_applications(g.userobj.uin)
    return jsonify(applications)

@bp.route("", methods=["PUT"])
@authenticate
def update_user_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(request.json, dict):
        abort(400)
    good_request = all(field in request.json for field in ['app_num', 'program_num', 'uncom_cert', 'com_cert', 'purpose_statement'])
    if not good_request:
        abort(400)

    response = update_application(request.json)
    if response == "success":
        return Response(response, 202)
    else:
        abort(400)

@bp.route("<int:app_num>", methods=["DELETE"])
@authenticate
def delete_user_application(app_num):
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(app_num, int):
        abort(400)

    response = delete_application(g.userobj.uin, app_num)
    if response == "success":
        return Response(response, 202)
    else:
        abort(400)
