from flask import Blueprint, request
from db_interface.documents import Document
from toolkit.user_tools import *
from toolkit.college_student_tools import *
from toolkit.document_tools import *
from toolkit.application_tools import *

bp = Blueprint("applications", __name__, url_prefix="/applications")

@bp.route('/<int:appnum>/document', methods = ['POST'])
@authenticate
def upload_document_by_appnum(appnum):
    uploaded_file=request.files.get("file")
    return upload_document(appnum=appnum, uploaded_file=uploaded_file)

@bp.route('/<int:docnum>/document', methods = ['DELETE'])
@authenticate
def delete_document_by_appnum(docnum):
    doc = Document(doc_num=docnum)
    response = doc.delete()
    return { "response": response }


@bp.route("", methods=["POST"])
def submit_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(request.json, dict):
        abort(400)
    good_request = all(field in request.json for field in ['program_num', 'uncom_cert', 'com_cert', 'purpose_statement'])
    if not good_request:
        abort(400)

    application_response = create_application(g.userobj.uin, request.json)
    return jsonify({"response": application_response})

@bp.route("", methods=["GET"])
@authenticate
def get_user_applications() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    applications = fetch_user_applications(g.userobj.uin)
    return jsonify(applications)

@bp.route("", methods=["PUT"])
def update_user_application() -> Response:
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(request.json, dict):
        abort(400)
    good_request = all(field in request.json for field in ['app_num', 'program_num', 'uncom_cert', 'com_cert', 'purpose_statement'])
    if not good_request:
        abort(400)

    application_response = update_application(request.json)
    return jsonify({"response": application_response})

@bp.route("<int:app_num>", methods=["DELETE"])
@authenticate
def delete_user_application(app_num):
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)

    if not isinstance(app_num, int):
        abort(400)

    application_response = delete_application(app_num)
    return jsonify({"response": application_response})
